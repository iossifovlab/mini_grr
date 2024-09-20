#!/usr/bin/env python

import os
from dae.genomic_resources import build_genomic_resource_repository
from dae.genomic_resources.reference_genome import build_reference_genome_from_resource
from dae.genomic_resources.genomic_scores import PositionScore


# GRR = build_genomic_resource_repository()
GRR = build_genomic_resource_repository({
	"id":"this", 
	"type":"directory", 
	"directory":os.getcwd() 
} )

ref_gr = GRR.get_resource("mini_genome")
ref = build_reference_genome_from_resource(ref_gr)
ref.open()

for ch in ref.chromosomes:
	print(ch, ref.get_chrom_length(ch))

for gr in GRR.get_all_resources():
	if gr.get_type() != "position_score":
		continue
	if not gr.get_id().startswith('mini'): 
		continue
	print(gr.get_id())
	sc = PositionScore(gr)
	sc.open()

	print(f"##### {gr.get_id()} #####")
	for ch in ref.chromosomes:
		for p in range(1, ref.get_chrom_length(ch)+1):
			print(ch, p, sc.fetch_scores(ch, p))


