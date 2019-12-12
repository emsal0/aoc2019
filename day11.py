import sys
from intcode import compute
import threading
import concurrent.futures
import queue

class QueueIOObj(object):
    def __init__(self, q):
        self.q = q

    def readline(self):
        item = str(self.q.get())
        return item

    def write(self, obj):
        # print("OUTPUT", str(obj))
        self.q.put(str(obj))


def intcode_worker(program, inqueue, outqueue):
    qin = QueueIOObj(inqueue)
    qout = QueueIOObj(outqueue)
    r, output = compute(program, instream=qin, outstream=qout)
    outqueue.put(9)
    outqueue.put(9)
    return output[-1]

def robot_worker(inqueue, outqueue, initial_floor=None):
    floor = {}
    if initial_floor is not None:
        floor = initial_floor

    dirmap = { '^': ('<', '>'), '>': ('^', 'v'), 'v': ('>', '<'), '<': ('v', '^') }

    curpos = (0,0)
    curdir = '^'

    paint_color = None
    dir_inst = None

    while dir_inst != 9:
        # print("ROBOT INPUT QUEUE:", list(inqueue.queue))
        current_color = floor.get(curpos, 0)
        # print("ROBOT INPUTS", current_color)
        outqueue.put(current_color)
        paint_color = int(inqueue.get())
        dir_inst = int(inqueue.get())
        # print("BOT RECEIVED:", paint_color, dir_inst)

        if paint_color == 9 and dir_inst == 9:
            break
        elif paint_color == 9 or dir_inst == 9:
            raise Exception("invalid instruction combo: %d, %d" % (paint_color, dir_inst))

        floor[curpos] = paint_color

        # print("BOT SETTING CURDIR")
        curdir = dirmap[curdir][dir_inst]

        # print("BOT SETTING CURPOS")
        if curdir == 'v':
            curpos = (curpos[0], curpos[1]+1)
        elif curdir == '^':
            curpos = (curpos[0], curpos[1]-1)
        elif curdir == '>':
            curpos = (curpos[0]+1, curpos[1])
        elif curdir == '<':
            curpos = (curpos[0]-1, curpos[1])


    return floor

def run_robot(program, initial_floor=None):
    qin = queue.Queue()
    qout = queue.Queue()
    with concurrent.futures.ThreadPoolExecutor() as exc:
        intcode_F = exc.submit(intcode_worker, program, qin, qout)
        robot_F = exc.submit(robot_worker, qout, qin, initial_floor)

        val = robot_F.result()
        return val

def output_painting(painting):
    x_coords = [c[0] for c in painting.keys()]
    x_strt = min(x_coords)
    max_x = max(x_coords) - min(x_coords)

    y_coords = [c[1] for c in painting.keys()]
    y_strt = min(y_coords)
    max_y = max(y_coords) - min(y_coords)

    for i in range(max_y+1):
        row = '0' * max_x
        for j in x_coords:
            row = row[:j - x_strt] + str(painting.get((j , y_strt + i), 0)) + row[j - x_strt + 1:]

        print(row.replace('0', '\033[40m \033[0m')
                 .replace('1', '\033[107m \033[0m'))

program = [int(i) for i in sys.stdin.read().strip().split(',')]

# 7a
print(len(run_robot(program).keys()))

# 7b
painting = run_robot(program, initial_floor = {(0,0): 1})
output_painting(painting)
