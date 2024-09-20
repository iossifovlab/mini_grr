filename="mini_positionscore_interval_bedgraph_0.bedgraph"
bgzip -c "$filename" > ${filename}.gz
tabix -p bed ${filename}.gz
