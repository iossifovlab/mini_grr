#!/bin/bash

# Input file
input_file="mini_vcf.vcf"

# Output file for header
output_file="mini_vcf.header.vcf"

# Extract lines starting with '#' and save them into the output file
grep '^#' "$input_file" > "$output_file"

# Compress both the original VCF and the header file with bgzip while keeping the originals
bgzip -c "$input_file" > "${input_file}.gz"
bgzip -c "$output_file" > "${output_file}.gz"

# Index the compressed VCF and header files using tabix
tabix -p vcf "${input_file}.gz"
tabix -p vcf "${output_file}.gz"

# Confirmation message
echo "Both files have been bgzipped and indexed with tabix: ${input_file}.gz and ${output_file}.gz"
