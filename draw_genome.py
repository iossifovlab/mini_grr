
import pandas as pd
import matplotlib.pyplot as plt


# Define the path to your file
file_path = 'mini_genome/mini.genome.fa'

# Initialize a list to store sequences
sequences = []

# Open the file and parse it
with open(file_path, 'r') as file:
    sequence = ""
    for line in file:
        if line.startswith('>'):
            if sequence:  # Save the previous sequence when a new header is encountered
                sequences.append(sequence)
                sequence = ""
        else:
            sequence += line.strip()  # Append the line to the current sequence
    if sequence:  # Add the last sequence after the loop ends
        sequences.append(sequence)

# Create DataFrame with only sequences
df = pd.DataFrame({'sequence': sequences})

# Display the DataFrame
print(df)


# Create a figure and subplots
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(3, 3), sharex=True)

# Plot each sequence
for i, ax in enumerate(axes):
    sequence = df['sequence'].iloc[i]
    positions = list(range(1, len(sequence) + 1))  # 1-based positions

    # Plot each nucleotide at its position
    for pos, nucleotide in zip(positions, sequence):
        ax.text(pos, 0.5, nucleotide, ha='center', va='center', fontsize=10)
    
    # Set axis labels and title
    ax.set_xlim(1, len(sequence) + 1)
    ax.set_ylim(0, 1)
    ax.set_yticks([])  # Hide y-axis
    ax.set_xticks(positions)
    ax.set_title(f'Chromosome {i+1}')
    ax.set_xlabel('Position')
    ax.set_xlim(0.5, 10.5)
    ax.xaxis.set_tick_params(labeltop=False, labelbottom=True)

# Adjust layout
plt.tight_layout()
plt.savefig('mini_genome/sequence_plot.png', dpi=300, bbox_inches='tight')

plt.show()
import matplotlib.pyplot as plt
import numpy as np

# Input data from the refseq string
refstr = "1	transcriptA	chr1	+	0	10	1	10	1	0,	10,	0	geneA	none	none	-1,"
# Split the refstr to get relevant fields
fields = refstr.split("\t")
strand = fields[3]  # + or -
start_position = int(fields[4])  # Start position (0)
end_position = int(fields[5])  # End position (10)
gene_name = fields[12]  # Gene name (geneA)
transcript_name = fields[1]  # Transcript name (transcriptA)

# Create figure and axis
fig, ax = plt.subplots(figsize=(6, 2))

# Define positions for the strands (from start_position to end_position)
positions = np.arange(start_position + 1, end_position + 1)  # Positions from 1 to 10

# Add lines for the strands
ax.plot(positions, [1] * len(positions), color='black', lw=2)  # + strand
ax.plot(positions, [0] * len(positions), color='black', lw=2)  # - strand

# Add a red line for the gene above the black line
ax.plot(positions, [1.1] * len(positions), color='red', lw=3)  # Gene A as a red line

# Add a dashed red line for the transcript above the gene line
ax.plot(positions, [1.2] * len(positions), color='red', linestyle='--', lw=2)  # Transcript A as a red dashed line

# Add labels inside the plot area, close to the lines
ax.text(positions[0], 1.1, gene_name, verticalalignment='center', horizontalalignment='left', fontsize=10, color='red')
ax.text(positions[0], 1.2, transcript_name, verticalalignment='center', horizontalalignment='left', fontsize=10, color='red', style='italic')

# Add labels on the left for strands
ax.text(-0.1, 1, '+', verticalalignment='center', horizontalalignment='right', fontsize=12)
ax.text(-0.1, 0, '-', verticalalignment='center', horizontalalignment='right', fontsize=12)

# Set axis labels
ax.set_xlabel('Position')

# Set x-ticks and x-tick labels
ax.set_xticks(np.arange(1, 11))
ax.set_xticklabels(np.arange(1, 11))

# Remove y ticks
ax.set_yticks([])

# Set axis limits
ax.set_xlim(0, 11)
ax.set_ylim(-0.3, 1.3)

# Display the plot
plt.show()
