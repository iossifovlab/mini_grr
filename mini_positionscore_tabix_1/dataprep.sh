#!/bin/bash

# Input file
input_file="mini_positionscore_tabix_1.tsv"

# Compress the input file with bgzip while keeping the original
bgzip -c "$input_file" > "${input_file}.gz"

# Index the compressed file using tabix with the specified parameters
tabix -s 1 -b 2 -e 2 "${input_file}.gz"

# Confirmation message
echo "${input_file}.gz has been compressed and indexed with tabix."
