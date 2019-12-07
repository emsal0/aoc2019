import sys
def compute(prg, instream=sys.stdin, outstream=sys.stdout):
    program = prg[:]
    output = []
    pc = 0
    while True:
        inst = program[pc]
        # print("inst", inst, "pc", pc)
        inst_digits = [int(i) for i in str(program[pc])]
        if inst != 99:
            inst_code = inst_digits[-1]
        else:
            inst_code = 99

        v1 = None
        v2 = None

        if inst_code != 99:
            if len(inst_digits) > 2 and inst_code in [1,2,5,6,7,8]:
                modes = inst_digits[-3::-1]
                while len(modes) < 2:
                    modes.append(0)
                v1 = program[program[pc+1]] if modes[0] == 0 else program[pc+1]
                v2 = program[program[pc+2]] if modes[1] == 0 else program[pc+2]
            elif inst_code in [4]:
                modes = [0] if len(inst_digits) == 1 else [inst_digits[0]]
                v1 = program[program[pc+1]] if modes[0] == 0 else program[pc+1]
            elif inst_code in [3]:
                v1 = program[program[pc+1]]
            else:
                v1 = program[program[pc+1]]
                v2 = program[program[pc+2]]

        if inst_code == 1:
            val = v1 + v2
            program[program[pc+3]] = val
            pc += 4
        if inst_code == 2:
            val = v1 * v2
            program[program[pc+3]] = val
            pc += 4
        if inst_code == 3:
            val = int(instream.readline().strip())
            program[program[pc+1]] = val
            pc += 2
        if inst_code == 4:
            outstream.write("%d\n" % v1)
            output.append(v1)
            pc += 2
        if inst_code == 5:
            if v1 != 0:
                pc = v2
            else:
                pc += 3
        if inst_code == 6:
            if v1 == 0:
                pc = v2
            else:
                pc += 3
        if inst_code == 7:
            program[program[pc+3]] = int(v1 < v2)
            pc += 4
        if inst_code == 8:
            program[program[pc+3]] = int(v1 == v2)
            pc += 4
        if inst_code == 99:
            break
    return (program[0], output)
