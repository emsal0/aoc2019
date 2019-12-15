import sys
import re
from copy import deepcopy

TIMESTEP = 1000

inp = """<x=14, y=4, z=5>
<x=12, y=10, z=8>
<x=1, y=7, z=-10>
<x=16, y=-5, z=3>"""

planet_strs = re.findall("<(.*)>", inp)
print(planet_strs)
coords = []
for s in planet_strs:
    coords.append({
            'pos': dict([(i, int(j)) for i, j in re.findall("(\w+)=((?:-|\d)+)", s)]),
            'vel': {'x': 0, 'y': 0, 'z': 0}
        })


states = {}
for t in range(TIMESTEP):
    input()
    kin = [sum([abs(v) for v in c['vel'].values()]) for c in coords]
    pot = [sum([abs(v) for v in c['pos'].values()]) for c in coords]
    print(kin)
    print(pot)
    tot = [k * p for k, p in zip(kin,pot)]
    print(tot, sum(tot))

    # print(coords)
    work = deepcopy(coords)
    n = len(coords)
    for i in range(n):
        for j in range(n):
            xdiff = work[j]['pos']['x'] - work[i]['pos']['x']
            ydiff = work[j]['pos']['y'] - work[i]['pos']['y']
            zdiff = work[j]['pos']['z'] - work[i]['pos']['z']

            xsign = 0 if xdiff == 0 else xdiff // abs(xdiff)
            ysign = 0 if ydiff == 0 else ydiff // abs(ydiff)
            zsign = 0 if zdiff == 0 else zdiff // abs(zdiff)

            coords[i]['vel']['x'] += xsign
            coords[i]['vel']['y'] += ysign
            coords[i]['vel']['z'] += zsign

        for d in ['x', 'y', 'z']:
            coords[i]['pos'][d] += coords[i]['vel'][d]

for c in coords:
    print("pos=<x={},y={},z={}> vel=<x={},y={},z={}>".format(
        c['pos']['x'], c['pos']['y'], c['pos']['z'],
        c['vel']['x'], c['vel']['y'], c['vel']['z'],
    ))

print(sum([ sum([abs(v) for v in c['pos'].values()]) * sum([abs(v) for v in c['vel'].values()]) for c in coords ]))
