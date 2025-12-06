import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import csv

# Define category names
categories = ['DeepSeek-R1-32B', 'Llama-3-70B', 'Magicoder', 'devstral:24b', 'gemma3:27b']

def read_pass_fail(filename):
    # pass_counts = []
    # fail_counts = []
    pass_counts = 0
    fail_counts = 0
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        for row in reader:
            # pass_counts.append(int(row[1]))  # second column: Pass
            # fail_counts.append(int(row[2]))  # third column: Fail
            pass_counts+=(int(row[1]))  # second column: Pass
            fail_counts+=(int(row[2]))  # third column: Fail
    return {'Pass': pass_counts, 'Fail': fail_counts}

# Read from CSVs
csv_files_base_path = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag'
                    #   'devstral_24b_matplotagent_python_scripts_with_rag_with_errors_without_correctorr'
# with_corrector = read_pass_fail('with_corrector.csv')
# without_corrector = read_pass_fail('without_corrector.csv')
model_list = ["devstral:24b",  "gemma3:27b", "magicoder", "deepseek-r1:32b", "llama3:70b"]

simple_queries_only_without_any_corrector_or_rag = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}
simple_queries_with_corrector_only = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}            
simple_queries_with_only_rag = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}
simple_queries_with_both_correct_and_rag = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}
# expert_queries_only = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}
# expert_queries_with_rag_only = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}
# expert_queries_with_only_corrector = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}
# expert_queries_with_both_rag_and_corrector = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}

list_of_python_scripts_sub_dirs = [
             # simple queries only without any corrector or rag
            "_python_scripts_without_rag_with_errors_without_corrector", #0            
            # simple queries with corrector only
              "_python_scripts_without_rag_with_errors_with_corrector", # 1            
             # simple queries with only rag
            "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector", #2            
            # simple queries with both correct and rag
            "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector", #3
            
            # # expert queries only
            # "_matplotagent_python_scripts_without_rag_without_corrector", #4
            # # expert queries with rag only
            # "_matplotagent_python_scripts_with_rag_without_corrector", #5
            # # expert queries with only corrector
            # "_matplotagent_python_scripts_without_rag_with_corrector", #6
            # # expert queries with both rag and corrector
            #  "_matplotagent_python_scripts_with_rag_with_corrector" #7      
            
    ]


# for each model
for index in range(0, 5):
    model = model_list[index]
    model_name = model.replace(':', '_')
    model_name = model_name.replace('-', '_')

    # for each scripts
    for index2 in range(0, 4):
        csv_directory = csv_files_base_path+f'/{model_name}{list_of_python_scripts_sub_dirs[index2]}'
        full_file_path = csv_directory+'/error_categorization_report.csv'
        if index2 == 0:
            simple_queries_only_without_any_corrector_or_rag[f'{model_name}'] = read_pass_fail(full_file_path)
        elif index2 == 1:
            simple_queries_with_corrector_only[f'{model_name}'] = read_pass_fail(full_file_path)            
        elif index2 == 2:
            # continue
            simple_queries_with_only_rag[f'{model_name}'] = read_pass_fail(full_file_path)
        elif index2 == 3:
            simple_queries_with_both_correct_and_rag[f'{model_name}'] = read_pass_fail(full_file_path)
        # elif index2 == 4:
        #     expert_queries_only[f'{model_name}'] = read_pass_fail(full_file_path)
        # elif index2 == 5:
        #     expert_queries_with_rag_only[f'{model_name}'] = read_pass_fail(full_file_path)
        # elif index2 == 6:
        #     expert_queries_with_only_corrector[f'{model_name}'] = read_pass_fail(full_file_path)
        # elif index2 == 7:
        #     expert_queries_with_both_rag_and_corrector[f'{model_name}'] = read_pass_fail(full_file_path)



import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Patch
from pathlib import Path

# === CONFIGURATION ===
# model_names = ["deepseek_r1_70b", "magicoder", "llama3_70b"]
model_names = ["devstral_24b", "gemma3_27b", "deepseek_r1_32b", "magicoder", "llama3_70b"]
common_path = "/Users/apukumarchakroborti/gsu_research/adm_research_spring_2025/generated_images_from_experiments/similarity_score_files"


# full_labels = ['Simple Level Queries(SLQ)', 'Expert Level Queries(ELQ)', 
#                'SLQ with Interquartile Range(IQR)', 
#                'SLQ with Z-score', 
#                'SLQ with Frequency-IQR (F-IQR)']

full_labels = [

    "simple queries",
    "simple queries with CORRECTOR only",
    "simple queries with RAG only",
    "simple queries with both CORRECTOR and RAG",
    # "expert queries",
    # "expert queries with RAG only",
    # "expert queries with CORRECTOR only",
    # "expert queries with both CORRECTOR and RAG"
]


# short_labels = ['A', 'B', 'C', 'D', 'E']
# colors = ['skyblue', 'salmon', 'lightgreen', 'orange', 'violet']
# column_name = 'Similarity (%)'

short_labels = ['A', 'B', 'C', 'D']
colors = ['skyblue', 'salmon', 'lightgreen', 'orange']
# column_name = 'Similarity (%)'


# === CREATE 3 SIDE-BY-SIDE SUBPLOTS ===
# fig, axs = plt.subplots(1, 5, figsize=(14, 5.5), sharey=True)
fig, axs = plt.subplots(1, 5, figsize=(10, 6), sharey=True)
plt.subplots_adjust(wspace=0.15)

similarity_scores = []

for ax, full_model_name in zip(axs, model_names):
    # csv_files = [
    #     f'{common_path}/{full_model_name}_generated_python_scripts_from_simple_queries_final/similarity_results.csv',
    #     f'{common_path}/{full_model_name}_generated_python_scripts_from_expert_queries_final/similarity_results.csv',
    #     f'{common_path}/{full_model_name}_IQR_generated_python_scripts_from_simple_user_queries_final/similarity_results.csv',
    #     f'{common_path}/{full_model_name}_Z_SCORE_generated_python_scripts_from_simple_user_queries_final/similarity_results.csv',
    #     f'{common_path}/{full_model_name}_F_IQR_generated_python_scripts_from_simple_user_queries_final/similarity_results.csv',
    # ]
    # dic = [

    # ]

    similarity_scores = [ 
                            (simple_queries_only_without_any_corrector_or_rag[full_model_name]['Pass']/61)*100,
                            (simple_queries_with_corrector_only[full_model_name]['Pass']/61)*100,
                            (simple_queries_with_only_rag[full_model_name]['Pass']/61)*100,
                            (simple_queries_with_both_correct_and_rag[full_model_name]['Pass']/61)*100,
                        ]
    # for file in csv_files:
    #     df = pd.read_csv(file)
    #     total = df[column_name].sum()
    #     similarity_scores.append(total)

    bars = ax.bar(short_labels, similarity_scores, color=colors, width=0.5)
    ax.set_title(f'{full_model_name.replace("_", " ").title()}', fontsize=11, pad=10)
    ax.set_ylim(0, 6*10)
    ax.axhline(6*10, color='gray', linestyle='--', linewidth=1)
    # ax.text(len(short_labels) - 0.5, 7, 'Max Score = 11', color='gray', ha='right', va='bottom', fontsize=9)
    if ax == axs[0]:
        ax.spines['right'].set_visible(False)
        ax.text(len(short_labels)- 0.7, 5*10, 'Max Score = 100', color='gray', ha='right', va='bottom', fontsize=9)
    else:
        if ax == axs[4]:
            ax.spines['left'].set_visible(False)
        else:
            ax.spines['left'].set_visible(False)
            ax.spines['right'].set_visible(False)
        ax.tick_params(axis='y', left=False, labelleft=False)
        ax.text(len(short_labels)- 0.7, 5*10, '', color='gray', ha='right', va='bottom', fontsize=9)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    # ax.set_xlabel('Query Type')
    # ax.set_xlabel('Performance of different types of formatted user queries')
    if ax == axs[0]:
        ax.set_ylabel('Total Pass in Percentage')
    if ax == axs[1]:
        ax.set_xlabel('Performance of simple queries under different conditions')
    ax.set_xticks(range(len(short_labels)))
    ax.set_xticklabels(short_labels)

# === Shared Legend on the Right ===
# === Shared Legend on the Right ===
legend_elements = [Patch(facecolor=color, label=label) for color, label in zip(colors, full_labels)]

# Adjust subplot layout to make room on the right
plt.subplots_adjust(right=0.78)

# Place legend on the right side
# fig.legend(handles=legend_elements, title='Bar Labels', loc='center right', bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=9, title_fontsize=10)
# fig.legend(handles=legend_elements, title='Bar Labels', loc='center', bbox_to_anchor=(.87, 0.5), frameon=False, fontsize=9, title_fontsize=10)
fig.legend(handles=legend_elements, title='Query Type', loc='center', bbox_to_anchor=(.60, 0.8), frameon=False, fontsize=9, title_fontsize=10)

# Reduce bar width in this line (from 0.5 to 0.3)
bars = ax.bar(short_labels, similarity_scores, color=colors, width=0.3)

# legend_elements = [Patch(facecolor=color, label=label) for color, label in zip(colors, full_labels)]
# fig.legend(handles=legend_elements, title='Bar Labels', loc='upper left', bbox_to_anchor=(1.05, 1),   ncol=1, frameon=False, fontsize=9, title_fontsize=10)
# plt.tight_layout(rect=[0, 0, 0.9, 1])  # Leave space for legend on the right

target_dir = Path(common_path)
plt.savefig('climate_all_models_separate_total_pass_count_with_legend_right.pdf', format='pdf', bbox_inches='tight')
plt.show()
