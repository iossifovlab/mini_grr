sort -k1,1 -k2,2n mini_positionscore_bw_0.bedgraph > sorted_mini_positionscore_bw_0.bedgraph
./bedGraphToBigWig sorted_mini_positionscore_bw_0.bedgraph chrom.sizes mini_positionscore_bw_0.bw
