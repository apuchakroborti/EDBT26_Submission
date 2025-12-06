import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os


# csv_file_base_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag'
csv_file_base_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag'
climate_all_csv_files_sub_dir = [
    # "_python_scripts_without_rag_with_corrector",
    # "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector",
    
    "_python_scripts_without_rag_with_errors_with_corrector",                                           
    # "_python_scripts_without_rag_with_errors_without_corrector",                                      
    # "_python_scripts_without_rag_without_corrector",                                                    
                    
    "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector",     
    # "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector",  
    # "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector"

    # "deepseek_r1_32b_python_scripts_without_rag_with_corrector",
    # "deepseek_r1_32b_python_scripts_without_rag_with_errors_with_corrector",                                           
    # "deepseek_r1_32b_python_scripts_without_rag_with_errors_without_corrector",                                      
    # "deepseek_r1_32b_python_scripts_without_rag_without_corrector",                                                    
    # "deepseek_r1_32b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector",                 
    # "deepseek_r1_32b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector",     
    # "deepseek_r1_32b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector",  
    # "deepseek_r1_32b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector"
]

# categories = ['EQ W RAG & C', 'EQ W RAG & W/O C', 'EQ W/O RAG & W C', 'EQ W/O RAG & C', 'SQ W RAG & C', 'SQ W RAG & W/O C', 'SQ W/O RAG & W C', 'SQ W/O RAG & C']
categories = ['devstral:24b', 'gemma3:27b', 'magicoder', 'deepseek-r1:32b', 'llama3:70b']
csv_file_basename = 'error_categorization_report'
# climate datasets
model_wise_pass_fail_result = []
w_corrector_pass_fail_result_wc = {'Pass': [], 'Fail': []}
model_wise_pass_fail_result.append(w_corrector_pass_fail_result_wc)

wo_corrector_pass_fail_result_wc = {'Pass': [], 'Fail': []}
model_wise_pass_fail_result.append(wo_corrector_pass_fail_result_wc)

for inedx in range(0, 5):
    model_name = categories[inedx].replace('-', '_').replace(':', '_')

    # w_o_corrector_pass_fail_result = {'Pass': [], 'Fail': []}
    
    # category 1
    file_path_wc = os.path.join(csv_file_base_dir, f"{model_name}{climate_all_csv_files_sub_dir[0]}/{csv_file_basename}.csv")
    if not os.path.exists(file_path_wc):
        print(f"Missing: {file_path_wc}")
        continue

    df_wc = pd.read_csv(file_path_wc)

    pass_count_wc = df_wc['Pass Count'].sum()
    print(f'CSV pass_count_wc: {pass_count_wc}')
    # w_o_corrector_pass_fail_result['Pass'].append(pass_count)
    model_wise_pass_fail_result[0]['Pass'].append(pass_count_wc)

    fail_count_wc = df_wc['Fail Count'].sum()
    print(f'CSV fail_count_wc: {fail_count_wc}')
    # w_o_corrector_pass_fail_result['Fail'].append(fail_count)
    model_wise_pass_fail_result[0]['Fail'].append(fail_count_wc)

    # category 2
    file_path = os.path.join(csv_file_base_dir, f"{model_name}{climate_all_csv_files_sub_dir[1]}/{csv_file_basename}.csv")
    if not os.path.exists(file_path):
        print(f"Missing: {file_path}")
        continue

    df = pd.read_csv(file_path)

    pass_count = df['Pass Count'].sum()
    print(f'CSV pass count: {pass_count}')
    # w_o_corrector_pass_fail_result['Pass'].append(pass_count)
    model_wise_pass_fail_result[1]['Pass'].append(pass_count)
    
    fail_count = df['Fail Count'].sum()
    print(f'CSV fail count: {fail_count}')
    # w_o_corrector_pass_fail_result['Fail'].append(fail_count)
    model_wise_pass_fail_result[1]['Fail'].append(fail_count)

    # model_wise_pass_fail_result.append(w_o_corrector_pass_fail_result)
    


print(model_wise_pass_fail_result)
# Number of categories
n_categories = len(categories)

# Bar width and positions
# bar_width = 0.35
bar_width = 0.15
x = np.arange(n_categories)

# Use seaborn style
sns.set_style('whitegrid')

# N=6
N = 2
positions = [x - bar_width*(N-1)/2 + i*bar_width for i in range(N)]


# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# Plot bars for "Without Corrector"
bars_1 = ax.bar(
    # x - bar_width / 2,
    # x - 3*bar_width, 
    positions[0],
    # model_wise_pass_fail_result[0]['Pass'], 
    model_wise_pass_fail_result[0]['Pass'], 
    width=bar_width, 
    color='green', 
    edgecolor='black', 
    # label='W RAG and Corrector - Pass'
    label=f'W/O RAG - Pass'
)
bars_2 = ax.bar(
    # x - bar_width / 2,
    positions[0], 
    model_wise_pass_fail_result[0]['Fail'], 
    width=bar_width, 
    bottom=model_wise_pass_fail_result[0]['Pass'],  
    color='red', 
    edgecolor='black', 
    # label='W RAG and Corrector - Fail'
    label='W/O RAG - Fail'
)

# Plot bars for "With Corrector"
bars_3 = ax.bar(
    # x + bar_width / 2,
    positions[1], 
    model_wise_pass_fail_result[1]['Pass'], 
    width=bar_width, 
    color='green', 
    hatch='//', 
    edgecolor='black', 
    label='W RAG - Pass'
)
bars_4 = ax.bar(
    # x + bar_width / 2, 
    positions[1],
    model_wise_pass_fail_result[1]['Fail'], 
    width=bar_width, 
    bottom=model_wise_pass_fail_result[1]['Pass'], 
    color='red', 
    hatch='//', 
    edgecolor='black', 
    label='W RAG - Fail'
)

# # Plot bars for "Without Corrector"
# bars_5 = ax.bar(
#     # x - bar_width / 2,
#     positions[2], 
#     model_wise_pass_fail_result[2]['Pass'], 
#     width=bar_width, 
#     color='gray', 
#     edgecolor='black', 
#     label='Iet. 2 - Pass'
# )
# bars_6 = ax.bar(
#     # x - bar_width / 2, 
#     positions[2], 
#     model_wise_pass_fail_result[2]['Fail'], 
#     width=bar_width, 
#     bottom=model_wise_pass_fail_result[2]['Pass'], 
#     color='salmon', 
#     edgecolor='black', 
#     label='Iet. 2 - Fail'
# )

# # Plot bars for "With Corrector"
# bars_7 = ax.bar(
#     # x + bar_width / 2,
#     positions[3],  
#     model_wise_pass_fail_result[3]['Pass'], 
#     width=bar_width, 
#     color='gray', 
#     hatch='//', 
#     edgecolor='black', 
#     label='Iet. 3 - Pass'
# )
# bars_8 = ax.bar(
#     # x + bar_width / 2,
#     positions[3], 
#     model_wise_pass_fail_result[3]['Fail'], 
#     width=bar_width, 
#     bottom=model_wise_pass_fail_result[3]['Pass'], 
#     color='salmon', 
#     hatch='//', 
#     edgecolor='black', 
#     label='Iet. 3 - Fail'
# )

# bars_9 = ax.bar(
#     # x + bar_width / 2,
#     positions[4],  
#     model_wise_pass_fail_result[4]['Pass'], 
#     width=bar_width, 
#     color='purple', 
#     # hatch='//', 
#     edgecolor='black', 
#     label='Iet. 4 - Pass'
# )
# bars_10 = ax.bar(
#     # x + bar_width / 2,
#     positions[4], 
#     model_wise_pass_fail_result[4]['Fail'], 
#     width=bar_width, 
#     bottom=model_wise_pass_fail_result[4]['Pass'], 
#     color='brown', 
#     # hatch='//', 
#     edgecolor='black', 
#     label='Iet. 4 - Fail'
# )

# bars_11 = ax.bar(
#     # x + bar_width / 2,
#     positions[5],  
#     model_wise_pass_fail_result[5]['Pass'], 
#     width=bar_width, 
#     color='purple', 
#     hatch='//', 
#     edgecolor='black', 
#     label='Iet. 5 - Pass'
# )
# bars_12 = ax.bar(
#     # x + bar_width / 2,
#     positions[5], 
#     model_wise_pass_fail_result[5]['Fail'], 
#     width=bar_width, 
#     bottom=model_wise_pass_fail_result[5]['Pass'], 
#     color='brown', 
#     hatch='//', 
#     edgecolor='black', 
#     label='Iet. 5 - Fail'
# )

# Add category labels
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12)

# Add labels and title
ax.set_xlabel('Expert Queries with and without RAG where CORRECTOR is present', fontsize=14)
ax.set_ylabel('Number of Evaluated Python Scripts', fontsize=14)
ax.set_title('Evaluation of Generated Code for the Climate Datasets', fontsize=16)

# Add grid for better visibility
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Add a legend outside to the right of the bar graph
# this legend on the right
# ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10, title='Parameters')

# this legend at the bottom
ax.legend(
    loc='lower center',         # Place legend at the bottom center
    # bbox_to_anchor=(0.5, -0.25),# Fine-tune vertical position (adjust if cropped)
    bbox_to_anchor=(0.5, -0.35),# Fine-tune vertical position (adjust if cropped)
    ncol=6,                     # 4 columns = 2 rows for 8 items
    fontsize=10,
    title='Parameters'
)



# Adjust layout to ensure no cropping
plt.tight_layout()

# Save and show the plot
# plt.savefig('total_pass_fail_count_simple_queries_different_models_climate_datasets.pdf', bbox_inches='tight')
plt.savefig('total_single_iteration_simple_q_w_corrector_w_o_rag_pass_fail_count_climate_dataset_final.pdf', bbox_inches='tight')

plt.show()



"""
In matplotlib (used in your example via `ax.bar()`), you can use a wide variety of color options for bars, including:
### ✅ **Basic Named Colors**
These are predefined names you can pass as strings (like `'green'`):

* `'blue'`
* `'green'`
* `'red'`
* `'cyan'`
* `'magenta'`
* `'yellow'`
* `'black'`
* `'white'`
* `'gray'`, `'lightgray'`, `'darkgray'`
* `'orange'`
* `'purple'`
* `'brown'`
* `'pink'`
* `'lime'`
* `'navy'`
* `'teal'`
* `'gold'`
* `'skyblue'`
* `'salmon'`

You can use them as `color='skyblue'` or `color='salmon'`.
### ✅ **Hexadecimal Codes**
You can specify any RGB color as a hex string, e.g.:
```python
color='#1f77b4'  # A shade of blue
color='#ff7f0e'  # A shade of orange
```
### ✅ **Grayscale**
You can use a string of a number between `0.0` (black) and `1.0` (white):
```python
color='0.75'  # Light gray
```
### ✅ **RGBA Tuples**
A tuple of (Red, Green, Blue, Alpha), each in the range \[0, 1]:
```python
color=(0.1, 0.2, 0.5, 0.8)  # semi-transparent blue
```
### ✅ **Tableau and CSS Colors**
Matplotlib also supports:
```python
color='tab:blue'
color='tab:orange'
color='tab:green'
color='tab:red'
color='tab:purple'
color='tab:brown'
color='tab:pink'
color='tab:gray'
color='tab:olive'
color='tab:cyan'
```
These are good for creating consistent plots across multiple categories.
### 🔍 To Get All Available Named Colors
You can programmatically list them:
```python
import matplotlib.colors as mcolors
named_colors = list(mcolors.CSS4_COLORS.keys())
print(named_colors)
```
Would you like a recommended palette (with distinct colors) for use with 4-6 bar groups per category?
"""
