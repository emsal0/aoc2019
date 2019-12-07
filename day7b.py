import sys
from io import StringIO
import itertools
from intcode import compute
import threading
import concurrent.futures
import queue

# phase_settings = [int(i) for i in input().strip().split(',')]
prg = "3,8,1001,8,10,8,105,1,0,0,21,34,43,60,81,94,175,256,337,418,99999,3,9,101,2,9,9,102,4,9,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,102,4,9,9,1001,9,4,9,102,3,9,9,4,9,99,3,9,102,4,9,9,1001,9,2,9,1002,9,3,9,101,4,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,99"
program = [int(i) for i in prg.strip().split(',')]

class QueueIOObj(object):
    def __init__(self, q):
        self.q = q

    def readline(self):
        item = str(self.q.get())
        return item

    def write(self, obj):
        # print(str(obj))
        self.q.put(str(obj))


def worker(name, inqueue, outqueue):
    qin = QueueIOObj(inqueue)
    qout = QueueIOObj(outqueue)
    r, output = compute(program, instream=qin, outstream=qout)
    return output[-1]

def compute_signal(phase):
    msg_queues = []
    threads = []

    for i in range(5):
        msg_queues.append(queue.Queue())
        msg_queues[i].put(phase[i])
    msg_queues[0].put(0)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futureA = executor.submit(worker, "A", msg_queues[0], msg_queues[1])
        futureB = executor.submit(worker, "B", msg_queues[1], msg_queues[2])
        futureC = executor.submit(worker, "C", msg_queues[2], msg_queues[3])
        futureD = executor.submit(worker, "D", msg_queues[3], msg_queues[4])
        futureE = executor.submit(worker, "E", msg_queues[4], msg_queues[0])

        return_val = futureE.result()
        return return_val

combos_results = []

for combo in itertools.permutations([5,6,7,8,9]):
    phase_settings = list(combo)
    result = compute_signal(phase_settings)
    combos_results.append((result, phase_settings))

print(sorted(combos_results, key = lambda x: x[0], reverse = True))
