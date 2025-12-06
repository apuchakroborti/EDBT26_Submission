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
# with_corrector = read_pass_fail('with_corrector.csv')
# without_corrector = read_pass_fail('without_corrector.csv')
model_list = ["devstral:24b",  "gemma3:27b", "magicoder", "deepseek-r1:32b", "llama3:70b"]

simple_queries_only_without_any_corrector_or_rag = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}
simple_queries_with_corrector_only = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}            
simple_queries_with_only_rag = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}
simple_queries_with_both_correct_and_rag = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}
expert_queries_only = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}
expert_queries_with_rag_only = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}
expert_queries_with_only_corrector = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}
expert_queries_with_both_rag_and_corrector = {'devstral_24b': {'Pass': 0, 'Fail': 0}, 'gemma3_27b': {'Pass': 0, 'Fail': 0}, 'magicoder': {'Pass': 0, 'Fail': 0}, 'deepseek_r1_32b': {'Pass': 0, 'Fail': 0}, 'llama3_70b': {'Pass': 0, 'Fail': 0}}

list_of_python_scripts_sub_dirs = [
            # simple queries only without any corrector or rag
            "_python_scripts_without_rag_with_errors_without_corrector", #0            
            # simple queries with corrector only
              "_python_scripts_without_rag_with_errors_with_corrector", # 1            
             # simple queries with only rag
            "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector", #2            
            # simple queries with both correct and rag
            "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector", #3
            # expert queries only
            "_python_scripts_without_rag_without_corrector", #4
            # expert queries with rag only
            "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector", #5
            # expert queries with only corrector
            "_python_scripts_without_rag_with_corrector", #6
            # expert queries with both rag and corrector
             "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector", #7      
            
    ]
"llama3_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector"
# for each model
for index in range(0, 5):
    model = model_list[index]
    model_name = model.replace(':', '_')
    model_name = model_name.replace('-', '_')

    # for each scripts
    for index2 in range(0, 8):
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
        elif index2 == 4:
            expert_queries_only[f'{model_name}'] = read_pass_fail(full_file_path)
        elif index2 == 5:
            expert_queries_with_rag_only[f'{model_name}'] = read_pass_fail(full_file_path)
        elif index2 == 6:
            expert_queries_with_only_corrector[f'{model_name}'] = read_pass_fail(full_file_path)
        elif index2 == 7:
            expert_queries_with_both_rag_and_corrector[f'{model_name}'] = read_pass_fail(full_file_path)

# Sample data
# model_list = ["devstral:24b",  "gemma3:27b", "magicoder", "deepseek-r1:32b", "llama3:70b"]
categories = ['Devstral-24B', 'Gemma-3-27B', 'Magicoder','DeepSeek-R1-32B', 'Llama-3-70B']


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Setup
sns.set(font_scale=1.0, style="whitegrid")
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

# categories = ['DeepSeek-R1-32B', 'Llama-3-70B', 'Magicoder']
# metrics = ['P1', 'P2', 'P3', 'F1', 'F2', 'F3', 'F4']
# categories = ['Devstral-24B', 'Gemma-3-27B', 'Magicoder','DeepSeek-R1-32B', 'Llama-3-70B']
categories = ['devstral_24b', 'gemma3_27b', 'magicoder','deepseek_r1_32b', 'llama3_70b']

metrics = [
    "simple queries",
    "simple queries with CORRECTOR only",
    "simple queries with RAG only",
    "simple queries with both CORRECTOR and RAG",
    "expert queries",
    "expert queries with RAG only",
    "expert queries with CORRECTOR only",
    "expert queries with both CORRECTOR and RAG"
]


data = {
                "devstral_24b" : [simple_queries_only_without_any_corrector_or_rag['devstral_24b']['Pass'],
                                  simple_queries_with_corrector_only['devstral_24b']['Pass'],
                                  simple_queries_with_only_rag['devstral_24b']['Pass'],
                                  simple_queries_with_both_correct_and_rag['devstral_24b']['Pass'],
                                  expert_queries_only['devstral_24b']['Pass'],
                                  expert_queries_with_rag_only['devstral_24b']['Pass'],
                                  expert_queries_with_only_corrector['devstral_24b']['Pass'],
                                  expert_queries_with_both_rag_and_corrector['devstral_24b']['Pass']
                                
                                ],
                  
                "gemma3_27b" : [simple_queries_only_without_any_corrector_or_rag['gemma3_27b']['Pass'],
                                simple_queries_with_corrector_only['gemma3_27b']['Pass'],
                                simple_queries_with_only_rag['gemma3_27b']['Pass'],
                                simple_queries_with_both_correct_and_rag['gemma3_27b']['Pass'],
                                expert_queries_only['gemma3_27b']['Pass'],
                                expert_queries_with_rag_only['gemma3_27b']['Pass'],
                                expert_queries_with_only_corrector['gemma3_27b']['Pass'],
                                expert_queries_with_both_rag_and_corrector['gemma3_27b']['Pass']
                
                            ],
                
                "magicoder" : [simple_queries_only_without_any_corrector_or_rag['magicoder']['Pass'],
                               simple_queries_with_corrector_only['magicoder']['Pass'],
                               simple_queries_with_only_rag['magicoder']['Pass'],
                               simple_queries_with_both_correct_and_rag['magicoder']['Pass'],
                               expert_queries_only['magicoder']['Pass'],
                               expert_queries_with_rag_only['magicoder']['Pass'],
                               expert_queries_with_only_corrector['magicoder']['Pass'],
                               expert_queries_with_both_rag_and_corrector['magicoder']['Pass']
                                ],
                
                "deepseek_r1_32b" : [simple_queries_only_without_any_corrector_or_rag['deepseek_r1_32b']['Pass'],
                                     simple_queries_with_corrector_only['deepseek_r1_32b']['Pass'],
                                     simple_queries_with_only_rag['deepseek_r1_32b']['Pass'],
                                     simple_queries_with_both_correct_and_rag['deepseek_r1_32b']['Pass'],
                                     expert_queries_only['deepseek_r1_32b']['Pass'],
                                     expert_queries_with_rag_only['deepseek_r1_32b']['Pass'],
                                     expert_queries_with_only_corrector['deepseek_r1_32b']['Pass'],
                                     expert_queries_with_both_rag_and_corrector['deepseek_r1_32b']['Pass']
                                        
                                        ],
                
                "llama3_70b" : [simple_queries_only_without_any_corrector_or_rag['llama3_70b']['Pass'],
                                simple_queries_with_corrector_only['llama3_70b']['Pass'],
                                simple_queries_with_only_rag['llama3_70b']['Pass'],
                                simple_queries_with_both_correct_and_rag['llama3_70b']['Pass'],
                                expert_queries_only['llama3_70b']['Pass'],
                                expert_queries_with_rag_only['llama3_70b']['Pass'],
                                expert_queries_with_only_corrector['llama3_70b']['Pass'],
                                expert_queries_with_both_rag_and_corrector['llama3_70b']['Pass']
                
                ]

}

bar_width = 0.1
x = np.arange(len(categories))
offsets = np.linspace(-3*bar_width, 3*bar_width, len(metrics))

colors = sns.color_palette("husl", len(metrics))

# Create plot
fig, ax = plt.subplots(figsize=(12, 6))
for i, metric in enumerate(metrics):
    values = [data[cat][i] for cat in categories]
    ax.bar(x + offsets[i], values, width=bar_width, label=metric, color=colors[i], edgecolor='black')

# Labeling
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.set_xlabel('LLM Models')
ax.set_ylabel('Counts')
ax.set_title('Model Evaluation Breakdown for NASA\'s EOS Datasets')
ax.grid(axis='y', linestyle='--', alpha=0.7)
# ax.legend(title='Metric', ncol=4, bbox_to_anchor=(1.05, 1), loc='upper left')
# Add a single-column legend outside the plot (right side)
ax.legend(title='Metric', ncol=1, bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig('climate_dataset_simple_and_expert_query_comparision_with_8_different_criteria.pdf', bbox_inches='tight', pad_inches=0.02)

plt.show()
