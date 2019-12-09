import sys

def getmem(prg, pos):
    if pos < 0:
        raise Exception("Cannot access memory positions below 0.")
    else:
        return prg.get(pos, 0)

def getval(prg, mode, pc, offset, relbase):
    retval = None
    if mode == 0:
        pos = prg.get(pc + offset, 0)
        retval = prg.get(pos, 0)
    elif mode == 1:
        retval = prg.get(pc + offset, 0)
    elif mode == 2:
        relpos = prg.get(pc + offset, 0)
        retval = prg.get(relbase + relpos, 0)
    return retval

def getaddr(prg, mode, pc, offset, relbase):
    if mode == 0:
        return prg.get(pc+offset, 0)
    elif mode == 1:
        raise Exception("Can't do immediate mode for address")
    elif mode == 2:
        relpos = prg.get(pc+offset, 0)
        return relbase + relpos

def compute(prg, instream=sys.stdin, outstream=sys.stdout, debug=False):
    program = prg[:]
    program = dict(enumerate(program))
    output = []
    pc = 0
    relbase = 0
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
        v3 = None

        if inst_code != 99:
            if len(inst_digits) > 2 and inst_code in [1,2,7,8]:
                modes = inst_digits[-3::-1]
                while len(modes) < 3:
                    modes.append(0)
                v1 = getval(program, modes[0], pc, 1, relbase)
                v2 = getval(program, modes[1], pc, 2, relbase)
                v3 = getaddr(program, modes[2], pc, 3, relbase)
            elif len(inst_digits) > 2 and inst_code in [5,6]:
                modes = inst_digits[-3::-1]
                while len(modes) < 2:
                    modes.append(0)
                v1 = getval(program, modes[0], pc, 1, relbase)
                v2 = getval(program, modes[1], pc, 2, relbase)
            elif len(inst_digits) > 2 and inst_code in [4,9]:
                modes = [inst_digits[0]]
                v1 = getval(program, modes[0], pc, 1, relbase)
            elif len(inst_digits) > 2 and inst_code in [3]:
                modes = [inst_digits[0]]
                v1 = getaddr(program, modes[0], pc, 1, relbase)
            elif inst_code in [4,9]:
                v1 = getval(program, 0, pc, 1, relbase)
            elif inst_code in [3]:
                v1 = getaddr(program, 0, pc, 1, relbase)
            else:
                v1 = getval(program, 0, pc, 1, relbase)
                v2 = getval(program, 0, pc, 2, relbase)

        if debug:
            print(inst, "\t", inst_code,
                   "\t|", v1, v2, v3, "\t|", "relbase =", relbase, "pc =", pc)

        if inst_code == 1:
            val = v1 + v2
            program[v3] = val
            pc += 4
        elif inst_code == 2:
            val = v1 * v2
            program[v3] = val
            pc += 4
        elif inst_code == 3:
            val = int(instream.readline().strip())
            program[v1] = val
            pc += 2
        elif inst_code == 4:
            outstream.write("%d\n" % v1)
            output.append(v1)
            pc += 2
        elif inst_code == 5:
            if v1 != 0:
                pc = v2
            else:
                pc += 3
        elif inst_code == 6:
            if v1 == 0:
                pc = v2
            else:
                pc += 3
        elif inst_code == 7:
            program[v3] = int(v1 < v2)
            pc += 4
        elif inst_code == 8:
            program[v3] = int(v1 == v2)
            pc += 4
        elif inst_code == 9:
            relbase += v1
            pc += 2
        elif inst_code == 99:
            break
        else:
            raise Exception("Opcode not supported : %d" % inst_code)
    return (program[0], output)
