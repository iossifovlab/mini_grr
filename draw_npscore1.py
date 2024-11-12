#!/usr/bin/env python

from collections import defaultdict
import os
import pylab
import pandas as pd
import numpy as np
from dae.genomic_resources import build_genomic_resource_repository
from dae.genomic_resources.reference_genome import build_reference_genome_from_resource_id
from dae.genomic_resources.genomic_scores import NPScore

# Build the genomic resource repository (GRR) from the current directory
GRR = build_genomic_resource_repository({
    "id": "this",
    "type": "directory",
    "directory": os.getcwd()
})

ref = build_reference_genome_from_resource_id("mini_genome", GRR).open()

# Print chromosome information
for ch in ref.chromosomes:
    print(ch, ref.get_chrom_length(ch))

for gr in GRR.get_all_resources():
    
    if gr.get_type() != "np_score":
        continue

    # if gr.get_id() != "mini_npscore_tabix_0": continue

    sc = NPScore(gr).open()
    
    print(f"#### Resource: {gr.get_id()} #### ")
    all_score_names = sc.get_all_scores()

    for chi, ch in enumerate(ref.chromosomes):
        print(f"\t### chr {ch}")
        chrom_len = ref.get_chrom_length(ch)
        for p in range(1, chrom_len + 1):
            rf = ref.get_sequence(ch, p, p)
            for al in ['A', 'T', 'G', 'C']:
                scores = sc.fetch_scores(ch, p, rf, al)
                if scores is not None:
                    print("\t\t", ch, p, rf, al, list(zip(all_score_names, scores)))

