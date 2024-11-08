#!/usr/bin/env python

from collections import defaultdict
import os
import pylab
import numpy as np

from dae.genomic_resources.gene_models import build_gene_models_from_resource_id

GM = build_gene_models_from_resource_id("hg38/gene_models/refSeq_v20240129").load()

L = [tm.total_len() for tm in GM.transcript_models.values() ] # if tm.is_coding()]

# L = [l for l in L if l < 6000]

mxL = 20000
bs  = 100
nBin  = mxL//bs
D = np.zeros(nBin)
xc = [n+bs/2 for n in range(0,mxL,bs)]
for l in L:
    D[min(nBin-1,l//bs)] += 1
D /= D.sum()
D /= bs 

pylab.figure()
pylab.hist(L,xc, density=True)
pylab.plot(xc, D)
# pylab.xlim([0,6000])
pylab.show(block=False)
pylab.gcf().savefig('b-2.png')
