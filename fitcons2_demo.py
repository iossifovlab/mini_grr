#!/usr/bin/env python


import pylab
from dae.genomic_resources import build_genomic_resource_repository
from dae.genomic_resources.genomic_scores import PositionScore

ch = '17'
bg = 1000000
en = 1010000

GRR = build_genomic_resource_repository()
D = {}
for gr in GRR.get_all_resources():
    if gr.get_type() != "position_score":
        continue
    if 'fitCons2' not in gr.get_id():
        continue
    print(f"Working on {gr.get_id()}")
    sc = PositionScore(gr).open()


    vs = []
    for p in range(bg, en):
        va = sc.fetch_scores(ch, p)
        vs.append(None if va is None else va[0])
    D[gr.get_id()] = vs

pylab.figure()
for ii, (r_id, vs) in enumerate(D.items()):
    ss = 1 + ii // 20 
    pylab.subplot(4, 2, ss)
    pylab.plot([-0.1 if v is None else v for v in vs], label=r_id)
# pylab.legend()
pylab.gcf().set_size_inches(10, 10)
pylab.savefig('aaa.png')
