import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Sample data
categories = ['magicoder', 'deepseek-coder-v2', 'llama3:70b']
with_corrector = {'Pass': [3, 4, 8], 'Fail': [21, 20, 16]}
without_corrector = {'Pass': [2, 2, 6], 'Fail': [22, 22, 18]}

# Number of categories
n_categories = len(categories)

# Bar width and positions
bar_width = 0.35
x = np.arange(n_categories)

# Use seaborn style
sns.set_style('whitegrid')

# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# Plot bars for "Without Corrector"
bars_1 = ax.bar(
    x - bar_width / 2, 
    without_corrector['Pass'], 
    width=bar_width, 
    color='green', 
    edgecolor='black', 
    label='Without Corrector - Pass'
)
bars_2 = ax.bar(
    x - bar_width / 2, 
    without_corrector['Fail'], 
    width=bar_width, 
    bottom=without_corrector['Pass'], 
    color='red', 
    edgecolor='black', 
    label='Without Corrector - Fail'
)

# Plot bars for "With Corrector"
bars_3 = ax.bar(
    x + bar_width / 2, 
    with_corrector['Pass'], 
    width=bar_width, 
    color='green', 
    hatch='//', 
    edgecolor='black', 
    label='With Corrector - Pass'
)
bars_4 = ax.bar(
    x + bar_width / 2, 
    with_corrector['Fail'], 
    width=bar_width, 
    bottom=with_corrector['Pass'], 
    color='red', 
    hatch='//', 
    edgecolor='black', 
    label='With Corrector - Fail'
)

# Add category labels
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12)

# Add labels and title
ax.set_xlabel('LLM Models', fontsize=14)
ax.set_ylabel('Number of Evaluated Python Scripts', fontsize=14)
ax.set_title('Evaluation of Generated Code for the MATPLOT_AGENT Datasets', fontsize=16)

# Add grid for better visibility
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Add a legend outside to the right of the bar graph
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10, title='Parameters')

# Adjust layout to ensure no cropping
plt.tight_layout()

# Save and show the plot
plt.savefig('total_pass_fail_count_different_models_matplot_agent_datasets.pdf', bbox_inches='tight')
plt.show()
