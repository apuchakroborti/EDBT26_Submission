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
csv_files_base_path = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag'
# with_corrector = read_pass_fail('with_corrector.csv')
# without_corrector = read_pass_fail('without_corrector.csv')
model_list = ["devstral:24b",  "gemma3:27b", "magicoder", "deepseek-r1:32b", "llama3:70b"]

simple_queries_only_without_any_corrector_or_rag = {}
simple_queries_with_corrector_only = {}            
simple_queries_with_only_rag_and_without_corrector = {}
simple_queries_with_both_correct_and_rag = {}
expert_queries_only = {}
expert_queries_with_rag_only_and_without_corrector = {}
expert_queries_with_both_rag_and_corrector = {}

list_of_python_scripts_sub_dirs = [
            # simple queries only without any corrector or rag
            "_python_scripts_without_rag_with_errors_without_corrector", #0            
            # simple queries with corrector only
              "_python_scripts_without_rag_with_errors_with_corrector", # 1            
             # simple queries with only rag and without corrector
            "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector", #2            
            # simple queries with both correct and rag
            "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector", #3
            # expert queries only
            "_python_scripts_without_rag_without_corrector", #4
            # expert queries with rag only and without corrector
            "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector", #5
            # expert queries with both rag and corrector
             "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector" #6      
            # "_python_scripts_without_rag_with_corrector" #7
    ]
"llama3_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector"
# for each model
for index in range(0, 5):
    model = model_list[index]
    model_name = model.replace(':', '_')
    model_name = model_name.replace('-', '_')

    # for each scripts
    for index2 in range(0, 7):
        csv_directory = csv_files_base_path+f'/{model_name}{list_of_python_scripts_sub_dirs[index2]}'
        full_file_path = csv_directory+'/error_categorization_report.csv'
        if index2 == 0:
            simple_queries_only_without_any_corrector_or_rag[f'{model_name}'] = read_pass_fail(full_file_path)
        elif index2 == 1:
            simple_queries_with_corrector_only[f'{model_name}'] = read_pass_fail(full_file_path)            
        elif index2 == 2:
            continue
            # simple_queries_with_only_rag_and_without_corrector[f'{model_name}'] = read_pass_fail(full_file_path)
        elif index2 == 3:
            simple_queries_with_both_correct_and_rag[f'{model_name}'] = read_pass_fail(full_file_path)
        elif index2 == 4:
            expert_queries_only[f'{model_name}'] = read_pass_fail(full_file_path)
        elif index2 == 5:
            expert_queries_with_rag_only_and_without_corrector[f'{model_name}'] = read_pass_fail(full_file_path)
        elif index2 == 6:
            expert_queries_with_both_rag_and_corrector[f'{model_name}'] = read_pass_fail(full_file_path)

# Sample data
# model_list = ["devstral:24b",  "gemma3:27b", "magicoder", "deepseek-r1:32b", "llama3:70b"]
categories = ['Devstral-24B', 'Gemma-3-27B', 'Magicoder','DeepSeek-R1-32B', 'Llama-3-70B']

# with_corrector = {'Pass': [7, 9, 3], 'Fail': [17, 15, 21]}
# without_corrector = {'Pass': [3, 3, 1], 'Fail': [21, 21, 23]}
with_corrector = {'Pass': [
                  simple_queries_only_without_any_corrector_or_rag['devstral_24b']['Pass'],
                  simple_queries_only_without_any_corrector_or_rag['gemma3_27b']['Pass'],
                  simple_queries_only_without_any_corrector_or_rag['magicoder']['Pass'],
                  simple_queries_only_without_any_corrector_or_rag['deepseek_r1_32b']['Pass'],
                  simple_queries_only_without_any_corrector_or_rag['llama3_70b']['Pass']
                  ], 
                  
                  'Fail': [
                        simple_queries_only_without_any_corrector_or_rag['devstral_24b']['Fail'],
                        simple_queries_only_without_any_corrector_or_rag['gemma3_27b']['Fail'],
                        simple_queries_only_without_any_corrector_or_rag['magicoder']['Fail'],
                        simple_queries_only_without_any_corrector_or_rag['deepseek_r1_32b']['Fail'],
                        simple_queries_only_without_any_corrector_or_rag['llama3_70b']['Fail']
                      ]
                  }
without_corrector = {'Pass': [
                  simple_queries_with_corrector_only['devstral_24b']['Pass'],
                  simple_queries_with_corrector_only['gemma3_27b']['Pass'],
                  simple_queries_with_corrector_only['magicoder']['Pass'],
                  simple_queries_with_corrector_only['deepseek_r1_32b']['Pass'],
                  simple_queries_with_corrector_only['llama3_70b']['Pass']
                  ], 
                  
                  'Fail': [
                        simple_queries_with_corrector_only['devstral_24b']['Fail'],
                        simple_queries_with_corrector_only['gemma3_27b']['Fail'],
                        simple_queries_with_corrector_only['magicoder']['Fail'],
                        simple_queries_with_corrector_only['deepseek_r1_32b']['Fail'],
                        simple_queries_with_corrector_only['llama3_70b']['Fail']
                      ]
                  }
print(f'Data with corrector: {with_corrector}')
print(f'Data without corrector: {without_corrector}')

# Number of categories
n_categories = len(categories)
# Bar width and positions
# bar_width = 0.25
bar_width = 0.15
x = np.arange(n_categories)
# Use seaborn style
sns.set(font_scale=1.5,style="whitegrid")
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'
# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 6))
# Plot bars for "Without Corrector"
bars_1 = ax.bar(
    x - bar_width / 2,
    without_corrector['Pass'],
    width=bar_width,
    color='darkseagreen',
    edgecolor='black',
    label='Pass - w/o Corrector'
)
bars_2 = ax.bar(
    x - bar_width / 2,
    without_corrector['Fail'],
    width=bar_width,
    bottom=without_corrector['Pass'],
    color='lightcoral',
    edgecolor='black',
    label='Fail - w/o Corrector'
)
# Plot bars for "With Corrector"
bars_3 = ax.bar(
    x + bar_width / 2,
    with_corrector['Pass'],
    width=bar_width,
    color='darkseagreen',
    hatch='//',
    edgecolor='black',
    label='Pass - w/Corrector'
)
bars_4 = ax.bar(
    x + bar_width / 2,
    with_corrector['Fail'],
    width=bar_width,
    bottom=with_corrector['Pass'],
    color='lightcoral',
    hatch='//',
    edgecolor='black',
    label='Fail - w/Corrector'
)
# Add category labels
ax.set_xticks(x)
ax.set_xticklabels(categories)
# Add labels and title
ax.set_xlabel('LLM Models')
ax.set_ylabel('Number of Evaluated Python Scripts')
ax.set_title('MatPlotBench Datasets')
# Add grid for better visibility
ax.grid(axis='y', linestyle='--', alpha=0.7)
# Add a legend outside to the right of the bar graph
ax.legend(loc='center left', bbox_to_anchor=(0.155, 0.915), title='', handletextpad=0.5, ncol=2)
ax.set_ylim(0, 35)
# Adjust layout to ensure no cropping
plt.tight_layout()
# Save and show the plot
plt.savefig('total_pass_fail_count_different_models_MatPlotBench_single_attempt.pdf', bbox_inches='tight',pad_inches=0.02)
plt.show()