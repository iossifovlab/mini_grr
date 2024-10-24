filename="mini_positionscore_bedgraph_0.bedgraph"
bgzip -c "$filename" > ${filename}.gz
tabix -p bed ${filename}.gz
