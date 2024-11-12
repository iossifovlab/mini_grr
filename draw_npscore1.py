#!/usr/bin/env python

from collections import defaultdict
import os
import pylab
import pandas as pd
import numpy as np
from dae.genomic_resources import build_genomic_resource_repository
from dae.genomic_resources.reference_genome import build_reference_genome_from_resource
from dae.genomic_resources.genomic_scores import PositionScore
from dae.genomic_resources.genomic_scores import NPScore

# Build the genomic resource repository (GRR) from the current directory
GRR = build_genomic_resource_repository({
    "id": "this",
    "type": "directory",
    "directory": os.getcwd()
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
    "mini_npscore_tabix_0"

]

for resource_id in resources:
    gr = GRR.get_resource(resource_id)
    
    # Check if the resource is of type 'position_score'
    if gr.get_type() == "np_score":
        
        sc = NPScore(gr)
        sc.open()
        
        # Get all chromosomes and scores
        num_chromosomes = len(ref.chromosomes)
        all_score_names = sc.get_all_scores()
        num_scores = len(all_score_names)

        print(all_score_names)
        # # Create a grid of subplots with rows for chromosomes and columns for scores
        # fig, axes = pylab.subplots(num_chromosomes, num_scores, figsize=(5 * num_scores, 4 * num_chromosomes), squeeze=False)


        # scores = sc.fetch_scores('chr1', 1, 'T', 'A')
        # print(scores)
        # Loop through each chromosome
        for chi, ch in enumerate(ref.chromosomes):
            chrom_len = ref.get_chrom_length(ch)
        #     data = {'position': []}  # Initialize dictionary with 'position' column
            
            # Initialize empty lists for each score name
            for score_name in all_score_names:
                # data[score_name] = []
            
            # Iterate through each position in the chromosome
                for p in range(1, chrom_len + 1):
                    for ref in ['A', 'T', 'G', 'C']:
                        for alt in ['A', 'T', 'G', 'C']:
                            scores = sc.fetch_scores(ch, p, ref, alt)
                            # print(ch + ' ' + str(p) + ' ' + scores)
                            if scores:
                                print(ch)
                                print(p)
                                print(scores)
            #     if scores:
            #         assert len(scores) == len(all_score_names)
            #         data['position'].append(p)
            #         for score_name, score in zip(all_score_names, scores):
            #             data[score_name].append(score if score is not None else np.nan)
            #     else:
            #         # If no scores, append position but set NaN for each score
            #         data['position'].append(p)
            #         for score_name in all_score_names:
            #             data[score_name].append(np.nan)
            
            # # Create and print DataFrame from data dictionary
            # df = pd.DataFrame(data)
            # print(f"\nData for Chromosome {ch}:\n", df)
            
    #         # Plot each score in its respective subplot
    #         for score_idx, score_name in enumerate(all_score_names):
    #             ax = axes[chi, score_idx]
                
    #             # Check if the score is numerical or string
    #             if pd.api.types.is_numeric_dtype(df[score_name]):
    #                 # Plot numerical data as scatter
    #                 valid_data = df[['position', score_name]].dropna()
    #                 ax.scatter(valid_data['position'], valid_data[score_name], label=score_name, alpha=0.6, c='m')
    #             else:
    #                 # Plot string data as text at each position
    #                 for _, row in df[['position', score_name]].dropna().iterrows():
    #                     ax.text(row['position'], 0.5, row[score_name], ha='center', va='center', rotation=45)
    #                     # Remove yticks and yticklabels for string plots
    #                 ax.set_yticks([])  # Remove y-ticks
    #                 ax.set_yticklabels([])  # Remove y-tick labels
    #             ax.set_xlim([1 - 0.5, chrom_len + 0.5])
    #             ax.set_xticks(range(1, chrom_len + 1))
                
    #             # Set titles for the first row and first column
    #             ax.set_ylabel(f"{score_name}")
    #             ax.set_title(f"Chromosome {ch.replace('chr', '')}")
                
    #             # ax.legend()

    #     pylab.tight_layout()
    #     pylab.savefig(f"{gr.get_id()}/scores_graph.png")
    
    # else:
    #     print(f"The resource {resource_id} is not of type 'position_score'")
