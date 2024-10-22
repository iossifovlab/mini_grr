filename="mini_positionscore_bedgraph_0.bedgraph"
bgzip -c "$filename" > ${filename}.gz
# tabix -p bed -S 0 ${filename}.gz
tabix -b 2 -e 3 -s 1 -0 -S 0 ${filename}.gz
