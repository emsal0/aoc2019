from operator import add

path1 = input().split(",")
path2 = input().split(",")

def addlists(l1, l2):
   return list(map(add, l1, l2))

def build_structure(path):
    ret = []

    ret.append([[0,0], None, 0])
    i = 1
    for inst in path:
        dxn = inst[0]
        hop = int(inst[1:])
        dst = None
        if dxn == 'U':
            dst = addlists(ret[i-1][0], [0, hop])
        elif dxn == 'D':
            dst = addlists(ret[i-1][0], [0, -hop])
        elif dxn == 'L':
            dst = addlists(ret[i-1][0], [-hop, 0])
        elif dxn == 'R':
            dst = addlists(ret[i-1][0], [hop, 0])
        ret.append([dst, None, ret[i-1][2]+abs(hop)])
        ret[i-1][1] = dst

        i += 1

    return ret

def inrange(q, v1, v2):
    lo = min(v1, v2)
    hi = max(v1, v2)
    return q >= lo and (q - lo) <= (hi - lo) and q <= hi

def minsame(l1, r1, l2, r2):
    lo1 = min(l1, r1)
    hi1 = max(l1, r1)
    lo2 = min(l2, r2)
    hi2 = max(l2, r2)

    return max(lo1, lo2)


def compare_structs(struct1, struct2):
    hits = []
    for pt1, dst1, h1 in struct1:
        if dst1 is None:
            continue
        x11 = pt1[0]
        x12 = pt1[1]
        x21 = dst1[0]
        x22 = dst1[1]

        for pt2, dst2, h2 in struct2:
            if dst2 is None:
                continue
            y11 = pt2[0]
            y12 = pt2[1]
            y21 = dst2[0]
            y22 = dst2[1]

            if x11 == x21: # up or down
                if y11 == y21: # also up/down
                    if y11 != x11:
                        continue
                    if inrange(x12, y12, y22) or inrange(x22, y11, y21) or inrange(y12, x12, x22) or inrange(y22, x12, x22):
                        print("UU",pt1,dst1,pt2,dst2)
                        hits.append([x11, minsame(x12, x22, y12, y22), h1 + h2])
                elif y12 == y22: # left/right
                    if inrange(x11, y11, y21) and inrange(y12, x12, x22):
                        print("UL",pt1,dst1,pt2,dst2)
                        hits.append([x11, y12, h1 + h2 + abs(x11-y11) + abs(y12-x12)])
            elif x12 == x22: # left/right
                if y11 == y21: # up/down
                    if inrange(x12, y12, y22) and inrange(y11, x11, x21):
                        print("LU",pt1,dst1,pt2,dst2)
                        hits.append([y11,x12, h1 + h2 + abs(y11-x11) + abs(x12 - y12)])
                elif y12 == y22: # also left/right
                    if y12 != x12:
                        continue
                    if inrange(x11, y11, y21) or inrange(x21, y11, y21) or inrange(y11, x11, x21) or inrange(y21, x11, x21):
                        print("LL",pt1,dst1,pt2,dst2)
                        hits.append([minsame(x11, x21, y11, y21), x12, h1 + h2])
    return hits


st1 = build_structure(path1)
st2 = build_structure(path2)

ixns = compare_structs(st1, st2)
# ixns = [(abs(i) + abs(j), i, j, k) for i,j,k in ixns]
print(sorted(ixns, key = lambda f: f[2]))
