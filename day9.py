import sys
from intcode import compute

program = [int(i) for i in input().strip().split(',')]
print(compute(program))
