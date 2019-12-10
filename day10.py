import sys
import collections
import math

def genqueue(i, j, M, N):
    queue = []
    dist = max(j, N-j, i, M-i)
    for k in range(1,dist+1):
        for kp in [-k, k]:
            for l in range(-k, k+1):
                queue.append((l,kp))
                queue.append((kp,l))
    return queue

def get_num_asteroids(queue, rows, i, j, M, N):
    queue = queue[:]
    gcd_hash = {}
    while len(queue) > 0:
        cur_i, cur_j = queue.pop(0)
        if (cur_i, cur_j) == (i,j) or i+cur_i < 0 or j+cur_j < 0 \
            or i+cur_i > M-1 or j+cur_j > N-1:
            continue

        if cur_i == 0 and cur_j == 0:
            continue
        else:
            numer = cur_j // math.gcd(cur_i, cur_j)
            denom = cur_i // math.gcd(cur_i, cur_j)
        if (numer, denom) in gcd_hash:
            continue
        elif rows[i+cur_i][j+cur_j] == '#':
            # print("HIT",j+cur_j,i+cur_i)
            gcd_hash[(numer, denom)] = True
    return len(gcd_hash.keys())

def get_lines_of_sight(queue, rows, i, j, M, N):
    queue = queue[:]
    gcd_hash = collections.defaultdict(lambda: [])
    seen_before = {}
    while len(queue) > 0:
        cur_i, cur_j = queue.pop(0)
        if (cur_i, cur_j) in seen_before:
            continue
        else:
            seen_before[(cur_i, cur_j)] = True
        if (cur_i, cur_j) == (i,j) or i+cur_i < 0 or j+cur_j < 0 \
            or i+cur_i > M-1 or j+cur_j > N-1:
            continue
        if cur_i == 0 and cur_j == 0:
            continue
        else:
            numer = cur_j // math.gcd(cur_i, cur_j)
            denom = cur_i // math.gcd(cur_i, cur_j)

        if rows[i+cur_i][j+cur_j] == '#':
            gcd_hash[(numer, denom)].append((j+cur_j, i+cur_i))
    return gcd_hash

def getstats(rows):
    rows = rows[:]
    M = len(rows)
    N = len(rows[0])
    stats = []
    for i in range(M):
        for j in range(N):
            if rows[i][j] == '#':
                q = genqueue(i, j, M, N)
                # print(j,i,q)
                dat = get_num_asteroids(q, rows, i, j, M, N)
                stats.append((dat, (j,i)))
    return stats


def get_destruction_order(rows, i, j, truncate=None):
    rows = rows[:]
    M = len(rows)
    N = len(rows[0])
    q = genqueue(i, j, M, N)
    los = get_lines_of_sight(queue, rows, i, j, M, N)

    destroyed = []

    pm_ratios = [r for r in los.keys() if r[0] >= 0 and r[1] < 0]
    pm_ratios = sorted(pm_ratios, key = lambda r: abs(r[0] / r[1]))

    pp_ratios = [r for r in los.keys() if r[0] > 0 and r[1] >= 0]
    pp_ratios = sorted(pp_ratios, key = lambda r: abs(r[1] / r[0]))

    mp_ratios = [r for r in los.keys() if r[0] <= 0 and r[1] > 0]
    mp_ratios = sorted(mp_ratios, key = lambda r: abs(r[0] / r[1]))

    mm_ratios = [r for r in los.keys() if r[0] < 0 and r[1] <= 0]
    mm_ratios = sorted(mm_ratios, key = lambda r: abs(r[1] / r[0]))
    print("mm:", mm_ratios)

    ratio_order = pm_ratios + pp_ratios + mp_ratios + mm_ratios
    rot_hits = 1
    while rot_hits > 0:
        rot_hits = 0
        for r in ratio_order:
            if len(los[r]) > 0:
                destroyed.append(los[r].pop(0))
                if len(destroyed) == truncate:
                    return destroyed
                rot_hits = 1

    return destroyed

# Order is REVERSED
#for i in range(len(rows)):
#    for j in range(len(rows[i])):
#        if rows[i][j] != '#':
#            continue
#

if len(sys.argv) < 2:
    print("must supply a or b as argument")
if sys.argv[1] == 'a':
    rows = [l.strip() for l in sys.stdin.readlines()]

    sorted_stats = sorted(getstats(rows), key = lambda x: x[0], reverse = True)
    print(sorted_stats)
elif sys.argv[1] == 'b':
    rows = """##.###.#.......#.#....#....#..........#.
....#..#..#.....#.##.............#......
...#.#..###..#..#.....#........#......#.
#......#.....#.##.#.##.##...#...#......#
.............#....#.....#.#......#.#....
..##.....#..#..#.#.#....##.......#.....#
.#........#...#...#.#.....#.....#.#..#.#
...#...........#....#..#.#..#...##.#.#..
#.##.#.#...#..#...........#..........#..
........#.#..#..##.#.##......##.........
................#.##.#....##.......#....
#............#.........###...#...#.....#
#....#..#....##.#....#...#.....#......#.
.........#...#.#....#.#.....#...#...#...
.............###.....#.#...##...........
...#...#.......#....#.#...#....#...#....
.....#..#...#.#.........##....#...#.....
....##.........#......#...#...#....#..#.
#...#..#..#.#...##.#..#.............#.##
.....#...##..#....#.#.##..##.....#....#.
..#....#..#........#.#.......#.##..###..
...#....#..#.#.#........##..#..#..##....
.......#.##.....#.#.....#...#...........
........#.......#.#...........#..###..##
...#.....#..#.#.......##.###.###...#....
...............#..#....#.#....#....#.#..
#......#...#.....#.#........##.##.#.....
###.......#............#....#..#.#......
..###.#.#....##..#.......#.............#
##.#.#...#.#..........##.#..#...##......
..#......#..........#.#..#....##........
......##.##.#....#....#..........#...#..
#.#..#..#.#...........#..#.......#..#.#.
#.....#.#.........#............#.#..##.#
.....##....#.##....#.....#..##....#..#..
.#.......#......#.......#....#....#..#..
...#........#.#.##..#.#..#..#........#..
#........#.#......#..###....##..#......#
...#....#...#.....#.....#.##.#..#...#...
#.#.....##....#...........#.....#...#...""".split('\n')

    i = 20
    j = 31
    M = len(rows)

    #M = int(input())
    #rows = []
    #j = int(input())
    #i = int(input())
    #for l in range(M):
    #    rows.append(input())
    N = len(rows[0])

    queue = genqueue(i,j,M,N)
    #print(queue)
    #print(get_lines_of_sight(queue, rows, i, j, M,N))
    order = get_destruction_order(rows, i, j)
    print('\n'.join(rows))
    print(order)
    print(order[199])
