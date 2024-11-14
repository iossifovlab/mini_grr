#!/usr/bin/env python

import os
import pylab as plt
import pandas as pd
import numpy as np
import seaborn as sns

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

    sc = NPScore(gr).open()
    
    print(f"#### Resource: {gr.get_id()} #### ")
    all_score_names = sc.get_all_scores()
    # Initialize a list to store rows for the DataFrame
    data = []


    for chi, ch in enumerate(ref.chromosomes):
        # print(f"\t### chr {ch}")
        chrom_len = ref.get_chrom_length(ch)
        for p in range(1, chrom_len + 1):
            rf = ref.get_sequence(ch, p, p)
            for al in ['A', 'T', 'G', 'C']:
                scores = sc.fetch_scores(ch, p, rf, al)
                if scores is not None:
                    print("\t\t", ch, p, rf, al, list(zip(all_score_names, scores)))
                    
                    # Collect the row data as a dictionary
                    row = {
                        "chromosome": ch[3:],
                        "position": p,
                        "reference": rf,
                        "allele": al
                    }
                    # Add the scores to the row dictionary
                    row.update(dict(zip(all_score_names, scores)))
                    # Append the row to the data list
                    data.append(row)

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(data)
    print(df)
    
    
    # Parameters
    chromosomes = df['chromosome'].unique()
    positions = range(1, 11)  # Positions 1-10
    allele_order = ['A', 'T', 'G', 'C']

    # Plot setup for subplots
    fig, axes = plt.subplots(len(chromosomes), len(all_score_names), figsize=(8, 4))

    # Loop over score names and chromosomes
    for idx, chrom in enumerate(chromosomes):
        chrom_data = df[df['chromosome'] == chrom]
        
        for jdx, score_name in enumerate(all_score_names):
            if score_name.endswith('num'):
                # Heatmap for numeric values (np_tsv_0_num)
                heatmap_data = chrom_data.pivot(index='allele', columns='position', values=score_name)
                heatmap_data = heatmap_data.reindex(index=allele_order, columns=positions)
                sns.heatmap(heatmap_data, ax=axes[idx, jdx], cmap="YlGnBu", annot=True, cbar=False,
                            linecolor='black', linewidths=0.5)

                axes[idx, jdx].set_title(f'Chromosome {chrom} - {score_name}')
                axes[idx, jdx].set_ylabel('Allele')

            elif score_name.endswith('cat'):
                # Grid for categorical values (np_tsv_0_cat)
                grid = np.full((len(allele_order), len(positions)), '', dtype=object)
                for _, row in chrom_data.iterrows():
                    grid[allele_order.index(row['allele']), row['position'] - 1] = row[score_name]
                
                ax = axes[idx, jdx]
                cax = ax.imshow(grid == grid, cmap="Blues", aspect="auto", interpolation="nearest")
                ax.set_xticks(np.arange(len(positions)))
                ax.set_yticks(np.arange(len(allele_order)))
                ax.set_xticklabels(positions)
                ax.set_yticklabels(allele_order)
                ax.set_xticks(np.arange(-0.5, len(positions), 1), minor=True)
                ax.set_yticks(np.arange(-0.5, len(allele_order), 1), minor=True)
                ax.grid(which='minor', color='black', linestyle='-', linewidth=0.5)

                for i in range(len(allele_order)):
                    for j in range(len(positions)):
                        if grid[i, j]:
                            ax.text(j, i, grid[i, j], ha='center', va='center', color="black", fontsize=8)

                ax.set_title(f'Chromosome {chrom} - {score_name}')
                ax.set_ylabel('Allele')
                ax.set_xlabel('position')

    # Adjust layout
    plt.tight_layout()
    plt.savefig(f"{gr.get_id()}/scores_graph.png")




