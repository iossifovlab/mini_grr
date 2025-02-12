from collections import defaultdict

from dae.genomic_resources.gene_models import build_gene_models_from_resource_id

# GM = build_gene_models_from_resource_id("hg38/gene_models/refSeq_v20240129").load()
# GM = build_gene_models_from_resource_id("hg38/gene_models/GENCODE/46/comprehensive/ALL").load()
# GM = build_gene_models_from_resource_id("hg38/gene_models/GENCODE/46/basic/PRI").load()
GM = build_gene_models_from_resource_id("hg38/gene_models/MANE/1.3").load()

genes = [
    "ACTB", "GAPDH", "RPLP0", "RPS18", "EEF1A1", "TUBB", "UBC", "HSPA8", "GUSB", "PGK1",
    "RPL13A", "RPS27A", "HSP90AB1", "B2M", "VIM", "LDHA", "HNRNPA1", "SF3B1", "YWHAG", "NPM1"
]

chroms_to_use = {f'chr{c}' for c in range(1, 23)} 
chroms_to_use.add('chrX')


for gene in genes:

    tsss = defaultdict(list)
    for tr in GM.gene_models_by_gene_name(gene):
        if tr.chrom not in chroms_to_use:
            continue
        tss = tr.tx[0] if tr.strand == '+' else tr.tx[1]
        tsss[tss].append(tr)

    spread = max(tsss.keys()) - min(tsss.keys())
    print(f"\n\n{gene=}, {spread=}")
    for tss, trs in sorted(tsss.items()):
        print(tss, len(trs), end=' ')
        for tr in trs:
            print("\t", tr.tr_id, tr.chrom, tr.strand, tr.tx, end='')
        print() 