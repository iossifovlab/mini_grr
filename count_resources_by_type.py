#!/usr/bin/env python

from collections import defaultdict
from dae.genomic_resources.repository_factory import build_genomic_resource_repository


grr = build_genomic_resource_repository()

cnts = defaultdict(int)

for gr in grr.get_all_resources():
    grtp = gr.get_type()
    grid = gr.get_id()

    prefix = grid.split("/")[0]
    # if prefix not in ["hg19", "hg38", "t2t"]:
    #     prefix = "other"
    
    cnts[prefix, grtp] += 1

    # print(f"{gr_type}: {gr.get_id()}")

for k, v in sorted(cnts.items()):
    print(f"{k}: {v}")