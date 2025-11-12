import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
# climate datasets
# simple queries
# both w rag and corrector
w_rag_and_corrector = {'Pass': [], 'Fail': []}
# w/o rag and w only corrector
without_rag_and_with_corrector = {'Pass': [], 'Fail': []}
# w only rag and w/o corrector
with_rag_and_without_corrector = {'Pass': [], 'Fail': []}
#w/o rag and corrector
without_rag_and_corrector = {'Pass': [], 'Fail': []}

csv_base_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag'

all_csv_sub_directory = [
    "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector",
    "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector",
    "_python_scripts_without_rag_with_errors_with_corrector",
    "_python_scripts_without_rag_with_errors_without_corrector",
    # expert queries
    "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector",
    "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector",
    "_python_scripts_without_rag_with_corrector",
    "_python_scripts_without_rag_without_corrector",

]

# Sample data
categories = ['devstral:24b', 'gemma3:27b', 'magicoder', 'deepseek-r1:32b', 'llama3:70b']
for model in categories:
        # w_rag_corrector_file_path = os.path.join(csv_base_dir, f"{model.replace(':', '_').replace('-', '_')}{all_csv_sub_directory[0]}/error_categorization_report.csv")
        w_rag_corrector_file_path = os.path.join(csv_base_dir, f"{model.replace(':', '_').replace('-', '_')}{all_csv_sub_directory[4]}/error_categorization_report.csv")
        w_rag_corrector_df = pd.read_csv(w_rag_corrector_file_path)
        w_rag_corrector_pass_count = w_rag_corrector_df['Pass Count'].sum()
        print(f'CSV pass count: {w_rag_corrector_pass_count}')
        w_rag_corrector_fail_count = w_rag_corrector_df['Fail Count'].sum()
        print(f'CSV fail count: {w_rag_corrector_fail_count}')
        w_rag_and_corrector['Pass'].append(w_rag_corrector_pass_count)
        w_rag_and_corrector['Fail'].append(w_rag_corrector_fail_count)

        # w_rag_wo_corrector_file_path = os.path.join(csv_base_dir, f"{model.replace(':', '_').replace('-', '_')}{all_csv_sub_directory[1]}/error_categorization_report.csv")
        w_rag_wo_corrector_file_path = os.path.join(csv_base_dir, f"{model.replace(':', '_').replace('-', '_')}{all_csv_sub_directory[5]}/error_categorization_report.csv")
        w_rag_wo_corrector_df = pd.read_csv(w_rag_wo_corrector_file_path)
        w_rag_wo_corrector_pass_count = w_rag_wo_corrector_df['Pass Count'].sum()
        print(f'CSV w_rag wo_c pass count: {w_rag_wo_corrector_pass_count}')
        w_rag_wo_corrector_fail_count = w_rag_wo_corrector_df['Fail Count'].sum()
        print(f'CSV fail count: {w_rag_wo_corrector_fail_count}')
        without_rag_and_with_corrector['Pass'].append(w_rag_wo_corrector_pass_count)
        without_rag_and_with_corrector['Fail'].append(w_rag_wo_corrector_fail_count)

        # wo_rag_w_corrector_file_path = os.path.join(csv_base_dir, f"{model.replace(':', '_').replace('-', '_')}{all_csv_sub_directory[2]}/error_categorization_report.csv")
        wo_rag_w_corrector_file_path = os.path.join(csv_base_dir, f"{model.replace(':', '_').replace('-', '_')}{all_csv_sub_directory[6]}/error_categorization_report.csv")
        wo_rag_w_corrector_df = pd.read_csv(wo_rag_w_corrector_file_path)
        wo_rag_w_corrector_pass_count = wo_rag_w_corrector_df['Pass Count'].sum()
        print(f'CSV pass count: {wo_rag_w_corrector_pass_count}')
        wo_rag_w_corrector_fail_count = wo_rag_w_corrector_df['Fail Count'].sum()
        print(f'CSV fail count: {wo_rag_w_corrector_fail_count}')
        with_rag_and_without_corrector['Pass'].append(wo_rag_w_corrector_pass_count)
        with_rag_and_without_corrector['Fail'].append(wo_rag_w_corrector_fail_count)

        # wo_rag_corrector_file_path = os.path.join(csv_base_dir, f"{model.replace(':', '_').replace('-', '_')}{all_csv_sub_directory[3]}/error_categorization_report.csv")
        wo_rag_corrector_file_path = os.path.join(csv_base_dir, f"{model.replace(':', '_').replace('-', '_')}{all_csv_sub_directory[7]}/error_categorization_report.csv")
        wo_rag_corrector_df = pd.read_csv(wo_rag_corrector_file_path)
        wo_rag_corrector_pass_count = wo_rag_corrector_df['Pass Count'].sum()
        print(f'CSV pass count: {wo_rag_corrector_pass_count}')
        wo_rag_corrector_fail_count = wo_rag_corrector_df['Fail Count'].sum()
        print(f'CSV fail count: {wo_rag_corrector_fail_count}')
        without_rag_and_corrector['Pass'].append(wo_rag_corrector_pass_count)
        without_rag_and_corrector['Fail'].append(wo_rag_corrector_fail_count)






# with_corrector = {'Pass': [3, 4, 8], 'Fail': [21, 20, 16]}
# without_corrector = {'Pass': [2, 2, 6], 'Fail': [22, 22, 18]}

# Number of categories
n_categories = len(categories)

# Bar width and positions
# bar_width = 0.35
bar_width = 0.2
x = np.arange(n_categories)

# Use seaborn style
sns.set_style('whitegrid')

# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# Plot bars for "Without Corrector"
bars_1 = ax.bar(
    # x - bar_width / 2,
    x - 1.5*bar_width, 
    w_rag_and_corrector['Pass'], 
    width=bar_width, 
    color='green', 
    edgecolor='black', 
    label='W RAG and Corrector - Pass'
)
bars_2 = ax.bar(
    # x - bar_width / 2,
    x - 1.5*bar_width, 
    w_rag_and_corrector['Fail'], 
    width=bar_width, 
    bottom=w_rag_and_corrector['Pass'], 
    color='red', 
    edgecolor='black', 
    label='W RAG and Corrector - Fail'
)

# Plot bars for "With Corrector"
bars_3 = ax.bar(
    # x + bar_width / 2,
    x - 0.5*bar_width, 
    without_rag_and_with_corrector['Pass'], 
    width=bar_width, 
    color='green', 
    hatch='//', 
    edgecolor='black', 
    label='W/O RAG and W Corrector - Pass'
)
bars_4 = ax.bar(
    # x + bar_width / 2, 
    x - 0.5*bar_width,
    without_rag_and_with_corrector['Fail'], 
    width=bar_width, 
    bottom=without_rag_and_with_corrector['Pass'], 
    color='red', 
    hatch='//', 
    edgecolor='black', 
    label='W/O RAG and W corrector - Fail'
)

# Plot bars for "Without Corrector"
bars_5 = ax.bar(
    # x - bar_width / 2,
    x + 0.5* bar_width , 
    with_rag_and_without_corrector['Pass'], 
    width=bar_width, 
    color='yellow', 
    edgecolor='black', 
    label='W RAG and W/O Corrector - Pass'
)
bars_6 = ax.bar(
    # x - bar_width / 2, 
    x + 0.5* bar_width , 
    with_rag_and_without_corrector['Fail'], 
    width=bar_width, 
    bottom=with_rag_and_without_corrector['Pass'], 
    color='orange', 
    edgecolor='black', 
    label='W RAG and W/O Corrector - Fail'
)

# Plot bars for "With Corrector"
bars_7 = ax.bar(
    # x + bar_width / 2,
    x + 1.5*bar_width,  
    without_rag_and_corrector['Pass'], 
    width=bar_width, 
    color='yellow', 
    hatch='//', 
    edgecolor='black', 
    label='W/O RAG and Corrector - Pass'
)
bars_8 = ax.bar(
    # x + bar_width / 2,
    x + 1.5*bar_width, 
    without_rag_and_corrector['Fail'], 
    width=bar_width, 
    bottom=without_rag_and_corrector['Pass'], 
    color='orange', 
    hatch='//', 
    edgecolor='black', 
    label='W/O RAG and Corrector - Fail'
)


# Add category labels
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12)

# Add labels and title
ax.set_xlabel('LLM Models', fontsize=14)
ax.set_ylabel('Number of Evaluated Python Scripts', fontsize=14)
ax.set_title('Evaluation of Generated Code for the Climate Datasets', fontsize=16)

# Add grid for better visibility
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Add a legend outside to the right of the bar graph
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10, title='Parameters')

# Adjust layout to ensure no cropping
plt.tight_layout()

# Save and show the plot
# plt.savefig('total_pass_fail_count_simple_queries_different_models_climate_datasets.pdf', bbox_inches='tight')
plt.savefig('total_pass_fail_count_expert_queries_different_models_climate_datasets.pdf', bbox_inches='tight')

plt.show()
