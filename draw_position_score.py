#!/usr/bin/env python

from collections import defaultdict
import os
import pylab
from dae.genomic_resources import build_genomic_resource_repository
from dae.genomic_resources.reference_genome import build_reference_genome_from_resource_id
from dae.genomic_resources.genomic_scores import PositionScore


# GRR = build_genomic_resource_repository()
GRR = build_genomic_resource_repository({
    "id": "this", 
    "type": "directory", 
    "directory": os.getcwd() 
})


ref = build_reference_genome_from_resource_id("mini_genome", GRR).open()


for ch in ref.chromosomes:
    print(ch, ref.get_chrom_length(ch))

for gr in GRR.get_all_resources():
    if gr.get_type() != "position_score":
        continue
    if not gr.get_id().startswith('mini'):
        continue
    sc = PositionScore(gr)
    sc.open()
    pylab.figure()
    print(f"##### {gr.get_id()} #####")
    
    for chi, ch in enumerate(ref.chromosomes):
        pylab.subplot(len(ref.chromosomes), 1, chi+1)
        xs = defaultdict(list)
        ys = defaultdict(list)
        chrom_len = ref.get_chrom_length(ch)
        all_score_names = sc.get_all_scores()
        for p in range(1, chrom_len+1):
            scores = sc.fetch_scores(ch, p)
            if scores is not None:
                assert len(scores) == len(all_score_names)
                for score_name, score in zip(all_score_names, scores):
                    if score is not None:
                        xs[score_name].append(p)
                        ys[score_name].append(score)
        for score_name in all_score_names:
            pylab.scatter(xs[score_name], ys[score_name], label=score_name)
        pylab.xlim([1-0.5, chrom_len+0.5])
        pylab.xticks(range(1, chrom_len+1))
        pylab.legend()
    
    pylab.savefig(f"{gr.get_id()}/scores_graph.png")
