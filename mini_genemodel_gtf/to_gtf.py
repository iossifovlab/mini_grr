#!/usr/bin/env python

from dae.genomic_resources.gene_models import build_gene_models_from_file
from dae.genomic_resources.gene_models.serialization import gene_models_to_gtf

# gene_models = build_gene_models_from_file("mini_gtf.gtf", "gtf").load()
gene_models = build_gene_models_from_file("mini_genemodel_gtf/mini_refseq.txt", "refseq").load()
aaa = gene_models_to_gtf(gene_models)


# with open("mini_gtf.gtf", "wt", encoding="utf-8") as F:
#     F.write(aaa)
