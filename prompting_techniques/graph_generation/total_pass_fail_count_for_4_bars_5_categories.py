import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os

# Dummy placeholders (populate from actual reading logic above)
# These should already be filled based on your CSV parsing code
categories = ['devstral:24b', 'gemma3:27b', 'magicoder', 'deepseek-r1:32b', 'llama3:70b']

w_rag_and_corrector = {'Pass': [35, 40, 45, 50, 42], 'Fail': [26, 21, 16, 11, 19]}
with_rag_and_without_corrector = {'Pass': [28, 34, 38, 43, 37], 'Fail': [33, 27, 23, 18, 24]}
without_rag_and_with_corrector = {'Pass': [30, 32, 36, 44, 38], 'Fail': [31, 29, 25, 17, 23]}
without_rag_and_corrector = {'Pass': [25, 30, 33, 39, 34], 'Fail': [36, 31, 28, 22, 27]}

# Bar width and position
n = len(categories)
bar_width = 0.2
x = np.arange(n)

sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(12, 6))

# Shifted bar positions
positions = [
    x - 1.5 * bar_width,
    x - 0.5 * bar_width,
    x + 0.5 * bar_width,
    x + 1.5 * bar_width
]

# Plot 4 sets of stacked bars
bars1_pass = ax.bar(positions[0], w_rag_and_corrector['Pass'], width=bar_width, color='green', label='W RAG + Corrector - Pass')
bars1_fail = ax.bar(positions[0], w_rag_and_corrector['Fail'], width=bar_width, bottom=w_rag_and_corrector['Pass'], color='red', label='W RAG + Corrector - Fail')

bars2_pass = ax.bar(positions[1], with_rag_and_without_corrector['Pass'], width=bar_width, color='limegreen', label='W RAG + No Corrector - Pass')
bars2_fail = ax.bar(positions[1], with_rag_and_without_corrector['Fail'], width=bar_width, bottom=with_rag_and_without_corrector['Pass'], color='indianred', label='W RAG + No Corrector - Fail')

bars3_pass = ax.bar(positions[2], without_rag_and_with_corrector['Pass'], width=bar_width, color='mediumseagreen', label='No RAG + Corrector - Pass')
bars3_fail = ax.bar(positions[2], without_rag_and_with_corrector['Fail'], width=bar_width, bottom=without_rag_and_with_corrector['Pass'], color='salmon', label='No RAG + Corrector - Fail')

bars4_pass = ax.bar(positions[3], without_rag_and_corrector['Pass'], width=bar_width, color='palegreen', label='No RAG + No Corrector - Pass')
bars4_fail = ax.bar(positions[3], without_rag_and_corrector['Fail'], width=bar_width, bottom=without_rag_and_corrector['Pass'], color='lightcoral', label='No RAG + No Corrector - Fail')

# Labels
ax.set_xticks(x)
ax.set_xticklabels(categories, rotation=15, fontsize=11)

ax.set_xlabel('LLM Models', fontsize=13)
ax.set_ylabel('Number of Evaluated Python Scripts', fontsize=13)
ax.set_title('Evaluation Results on Climate Dataset (Pass/Fail Counts)', fontsize=14)

# Legend
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=9, title='Condition Breakdown')

# Grid and layout
ax.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('climate_model_bar_chart_grouped_stacked.pdf', bbox_inches='tight')
plt.show()
