#!/usr/bin/env python

from collections import defaultdict
import os
import pylab
from dae.genomic_resources import build_genomic_resource_repository
from dae.genomic_resources.reference_genome import build_reference_genome_from_resource
from dae.genomic_resources.genomic_scores import PositionScore

# Build the genomic resource repository (GRR) from the current directory
GRR = build_genomic_resource_repository({
	"id":"this", 
	"type":"directory", 
	"directory":os.getcwd() 
})

# Reference genome setup

ref_gr = GRR.get_resource("mini_genome")
ref = build_reference_genome_from_resource(ref_gr)
ref.open()

# Print chromosome information
for ch in ref.chromosomes:
    print(ch, ref.get_chrom_length(ch))

# Work with the specific resource 'mini_positionscore_tabix_1'

resources = [
    "mini_positionscore_bedgraph_tabix_0"
    ,"mini_positionscore_bedgraph_tabix_interval_0"
    ,"mini_positionscore_bw"
    ,"mini_positionscore_tabix_0"
    ,"mini_positionscore_tabix_1"
    ,"mini_positionscore_tabix_interval_0"
    ,"mini_positionscore_tabix_interval_1"
    ,"mini_positionscore_tsv_0"
    ,"mini_positionscore_tsv_1"
    # ,"mini_positionscore_tsv_1_twoscores"
    ,"mini_positionscore_tsv_interval_0"
    ,"mini_positionscore_tsv_interval_1"
]

for resource_id in resources:
    gr = GRR.get_resource(resource_id)
    
    # Check if the resource is of type 'position_score'
    if gr.get_type() == "position_score":
        # print(f"Working with resource: {gr.get_id()}")
        
        sc = PositionScore(gr)
        sc.open()
        pylab.figure()
        print(f"##### {gr.get_id()} #####")
        
        # Loop through each chromosome
        for chi, ch in enumerate(ref.chromosomes):
            pylab.subplot(len(ref.chromosomes), 1, chi+1)
            pylab.title(f"Chromosome {ch.replace('chr', '')}")

            xs = defaultdict(list)
            ys = defaultdict(list)
            chrom_len = ref.get_chrom_length(ch)
            all_score_names = sc.get_all_scores()
            
            # Iterate through each position in the chromosome
            for p in range(1, chrom_len+1):
                scores = sc.fetch_scores(ch, p)
                
#                # Debugging: Check if position 1 has data
#                if p == 1:
#                    print(f"Position 1: {scores}")
            
                if scores:
                    assert len(scores) == len(all_score_names)
                    for score_name, score in zip(all_score_names, scores):
                        if score is not None:
                            xs[score_name].append(p)
                            ys[score_name].append(score)
            
            # Plot the scores
            for score_name in all_score_names:
                pylab.scatter(xs[score_name], ys[score_name], label=score_name, c='g')
            
            pylab.xlim([1-0.5, chrom_len+0.5])
            pylab.xticks(range(1, chrom_len+1))
            pylab.legend()
            print(xs, ys)
        pylab.tight_layout()
        # Save the figure
        pylab.savefig(f"{gr.get_id()}/scores_graph.png")
    
    else:
        print(f"The resource {resource_id} is not of type 'position_score'")
