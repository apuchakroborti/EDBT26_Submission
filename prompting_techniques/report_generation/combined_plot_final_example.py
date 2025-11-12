import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Patch
from pathlib import Path

# === CONFIGURATION ===
model_names = ["deepseek_r1_70b", "magicoder", "llama3_70b"]
common_path = "/Users/apukumarchakroborti/gsu_research/adm_research_spring_2025/generated_images_from_experiments/similarity_score_files"


full_labels = ['Simple Level Queries(SLQ)', 'Expert Level Queries(ELQ)', 
               'SLQ with Interquartile Range(IQR)', 
               'SLQ with Z-score', 
               'SLQ with Frequency-IQR (F-IQR)']

# full_labels = ['Simple Level Queries', 'Expert Level Queries', 
#                'Simple Level Queries with Interquartile Range(IQR) based Outlier', 
#                'Simple Level Queries with Z-score based Outlier', 
#                'Simple Level Queries with (Our Proposed) Frequency Based IQR as (F-IQR) base Outlier']
short_labels = ['A', 'B', 'C', 'D', 'E']
colors = ['skyblue', 'salmon', 'lightgreen', 'orange', 'violet']
column_name = 'Similarity (%)'

# === CREATE 3 SIDE-BY-SIDE SUBPLOTS ===
fig, axs = plt.subplots(1, 3, figsize=(14, 5.5), sharey=True)
plt.subplots_adjust(wspace=0.15)

for ax, full_model_name in zip(axs, model_names):
    csv_files = [
        f'{common_path}/{full_model_name}_generated_python_scripts_from_simple_queries_final/similarity_results.csv',
        f'{common_path}/{full_model_name}_generated_python_scripts_from_expert_queries_final/similarity_results.csv',
        f'{common_path}/{full_model_name}_IQR_generated_python_scripts_from_simple_user_queries_final/similarity_results.csv',
        f'{common_path}/{full_model_name}_Z_SCORE_generated_python_scripts_from_simple_user_queries_final/similarity_results.csv',
        f'{common_path}/{full_model_name}_F_IQR_generated_python_scripts_from_simple_user_queries_final/similarity_results.csv',
    ]

    similarity_scores = []
    for file in csv_files:
        df = pd.read_csv(file)
        total = df[column_name].sum()
        similarity_scores.append(total)

    bars = ax.bar(short_labels, similarity_scores, color=colors, width=0.5)
    ax.set_title(f'{full_model_name.replace("_", " ").title()}', fontsize=11, pad=10)
    ax.set_ylim(0, 6600)
    ax.axhline(6400, color='gray', linestyle='--', linewidth=1)
    ax.text(len(short_labels) - 0.5, 6370, 'Max Score = 6400', color='gray', ha='right', va='bottom', fontsize=9)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 40, f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    # ax.set_xlabel('Query Type')
    # ax.set_xlabel('Performance of different types of formatted user queries')
    if ax == axs[0]:
        ax.set_ylabel('Total Similarity Score')
    if ax == axs[1]:
        ax.set_xlabel('Performance of different types of formatted user queries')
    ax.set_xticks(range(len(short_labels)))
    ax.set_xticklabels(short_labels)

# === Shared Legend on the Right ===
# === Shared Legend on the Right ===
legend_elements = [Patch(facecolor=color, label=label) for color, label in zip(colors, full_labels)]

# Adjust subplot layout to make room on the right
plt.subplots_adjust(right=0.78)

# Place legend on the right side
# fig.legend(handles=legend_elements, title='Bar Labels', loc='center right', bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=9, title_fontsize=10)
fig.legend(handles=legend_elements, title='Bar Labels', loc='center', bbox_to_anchor=(.87, 0.5), frameon=False, fontsize=9, title_fontsize=10)

# Reduce bar width in this line (from 0.5 to 0.3)
bars = ax.bar(short_labels, similarity_scores, color=colors, width=0.3)

# legend_elements = [Patch(facecolor=color, label=label) for color, label in zip(colors, full_labels)]
# fig.legend(handles=legend_elements, title='Bar Labels', loc='upper left', bbox_to_anchor=(1.05, 1),   ncol=1, frameon=False, fontsize=9, title_fontsize=10)
# plt.tight_layout(rect=[0, 0, 0.9, 1])  # Leave space for legend on the right

target_dir = Path(common_path)
plt.savefig(target_dir / 'all_models_separate_similarity_scores_with_legend_right.pdf', format='pdf', bbox_inches='tight')
plt.show()
