import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
# climate datasets


climate_csv_file_base_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag'

climate_all_csv_files_sub_dir = [
    # "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_corrector"
    # "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_without_corrector",
    # "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_corrector",
    # "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_without_corrector",

    "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_with_corrector",
    # "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_without_corrector",
    # "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_with_corrector",
    # "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_without_corrector" 
]


matplotagent_csv_base_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/matplot_agent_data/plot_generation/error_categorization_evaluation_result/iterative_error_resolve'
matplotagent_all_csv_files_sub_dir = [
    # "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_corrector"
    # "devstral_24b_matplotagent_iterative_python_scripts_with_rag_without_corrector",
    # "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_corrector",
    # "devstral_24b_matplotagent_iterative_python_scripts_without_rag_without_corrector",
    
    "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_with_corrector",
    # "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_without_corrector",
    # "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_errors_with_corrector",
    # "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_errors_without_corrector",
]


fastmribrain_csv_base_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/mri_nyu_data/error_categorization_evaluation_result/iterative_evaluation_results'
fastmribrain_all_csv_files_sub_dir = [
    # "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_corrector"
    # "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_without_corrector",
    # "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_corrector",
    # "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_without_corrector",
    
    "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_errors_with_corrector",
    # "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_errors_without_corrector",
    # "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_errors_with_corrector",
    # "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_errors_without_corrector",
    
]

# categories = ['EQ W RAG & C', 'EQ W RAG & W/O C', 'EQ W/O RAG & W C', 'EQ W/O RAG & C', 'SQ W RAG & C', 'SQ W RAG & W/O C', 'SQ W/O RAG & W C', 'SQ W/O RAG & C']
# categories = ['EQ W R & C', 'EQ W R & W/O C', 'EQ W/O R & W C', 'EQ W/O R & C', 'SQ W R & C', 'SQ W R & W/O C', 'SQ W/O R & W C', 'SQ W/O R & C']
# categories = ['EQ W RAG & C', 'EQ W RAG & W/O C', 'EQ W/O RAG & W C', 'EQ W/O RAG & C']
categories = ['CLIMATE', 'MATPLOTAGENT', 'FASTMRIBRAIN']
csv_file_basename = 'error_categorization_report_'
iterations_category = []
iterations_category_in_percentage = []
for i in range(0, 6):
    print(f'\n\nIterations-------{i}')
    iteration_pass_fail = {'Pass': [], 'Fail': []}
    iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': []}
    # category 1
    file_path = os.path.join(climate_csv_file_base_dir, f"{climate_all_csv_files_sub_dir[0]}/{csv_file_basename}{i}.csv")
    if not os.path.exists(file_path):
        print(f"Missing: {file_path}")
        continue

    df = pd.read_csv(file_path)

    pass_count = df['Pass Count'].sum()
    print(f'Climate CSV pass count: {pass_count}')
    fail_count = df['Fail Count'].sum()
    print(f'CSV fail count: {fail_count}')

    current_fail_count = fail_count
    print(f'Current fail count: {current_fail_count}')

    if i ==0:
        current_pass_count=pass_count
        iteration_pass_fail['Pass'].append(current_pass_count)
        iteration_pass_fail_in_percentage['Pass'].append((current_pass_count*100)/61)
    else:
        current_pass_count=iterations_category[i-1]['Pass'][0]
        iteration_pass_fail['Pass'].append(current_pass_count+pass_count)
        iteration_pass_fail_in_percentage['Pass'].append(((current_pass_count+pass_count)*100)/61)
    print(f'Current pass count: {current_pass_count}')
    iteration_pass_fail_in_percentage['Fail'].append((current_fail_count*100)/61)
    

    iteration_pass_fail['Fail'].append(current_fail_count)

    # category 2
    file_path = os.path.join(matplotagent_csv_base_dir, f"{matplotagent_all_csv_files_sub_dir[0]}/{csv_file_basename}{i}.csv")
    if not os.path.exists(file_path):
        print(f"Missing: {file_path}")
        continue

    df = pd.read_csv(file_path)

    pass_count = df['Pass Count'].sum()
    print(f'Matplotagent CSV pass count: {pass_count}')
    fail_count = df['Fail Count'].sum()
    print(f'CSV fail count: {fail_count}')

    current_fail_count = fail_count
    print(f'Current fail count: {current_fail_count}')

    iteration_pass_fail['Fail'].append(current_fail_count)
    if i ==0:
        current_pass_count=pass_count
        iteration_pass_fail['Pass'].append(current_pass_count)
        iteration_pass_fail_in_percentage['Pass'].append((current_pass_count*100)/12)
    else:
        current_pass_count=iterations_category[i-1]['Pass'][1]
        iteration_pass_fail['Pass'].append(current_pass_count+pass_count)
        iteration_pass_fail_in_percentage['Pass'].append(((current_pass_count+pass_count)*100)/12)
    print(f'Current pass count: {current_pass_count}')
    iteration_pass_fail_in_percentage['Fail'].append((current_fail_count*100)/12)
    

    # category 3
    file_path = os.path.join(fastmribrain_csv_base_dir, f"{fastmribrain_all_csv_files_sub_dir[0]}/{csv_file_basename}{i}.csv")
    if not os.path.exists(file_path):
        print(f"Missing: {file_path}")
        continue

    df = pd.read_csv(file_path)

    pass_count = df['Pass Count'].sum()
    print(f'Fastmribrain CSV pass count: {pass_count}')
    fail_count = df['Fail Count'].sum()
    print(f'CSV fail count: {fail_count}')

    current_fail_count = fail_count
    print(f'Current fail count: {current_fail_count}')

    iteration_pass_fail['Fail'].append(current_fail_count)
    if i ==0:
        current_pass_count=pass_count
        iteration_pass_fail['Pass'].append(current_pass_count)
        iteration_pass_fail_in_percentage['Pass'].append((current_pass_count*100)/11)
    else:
        current_pass_count=iterations_category[i-1]['Pass'][2]
        iteration_pass_fail['Pass'].append(current_pass_count+pass_count)
        iteration_pass_fail_in_percentage['Pass'].append(((current_pass_count+pass_count)*100)/11)
    print(f'Current pass count: {current_pass_count}')
    iteration_pass_fail_in_percentage['Fail'].append((current_fail_count*100)/11)


    iterations_category.append(iteration_pass_fail)
    iterations_category_in_percentage.append(iteration_pass_fail_in_percentage)
    # # category 4
    # file_path = os.path.join(climate_csv_file_base_dir, f"{climate_all_csv_files_sub_dir[3]}/{csv_file_basename}{i}.csv")
    # if not os.path.exists(file_path):
    #     print(f"Missing: {file_path}")
    #     continue

    # df = pd.read_csv(file_path)

    # pass_count = df['Pass Count'].sum()
    # print(f'CSV pass count: {pass_count}')
    # if i ==0:
    #     current_pass_count=pass_count
    #     iteration_pass_fail['Pass'].append(current_pass_count)
    # else:
    #     current_pass_count=iterations_category[i-1]['Pass'][3]
    #     iteration_pass_fail['Pass'].append(current_pass_count+pass_count)
    # print(f'Current pass count: {current_pass_count}')

    # fail_count = df['Fail Count'].sum()
    # print(f'CSV fail count: {fail_count}')

    # current_fail_count = fail_count
    # print(f'Current fail count: {current_fail_count}')

    # iteration_pass_fail['Fail'].append(current_fail_count)

    # iterations_category.append(iteration_pass_fail)

print(iterations_category_in_percentage)
# Number of categories
n_categories = len(categories)

# Bar width and positions
# bar_width = 0.35
bar_width = 0.15
x = np.arange(n_categories)

# Use seaborn style
sns.set_style('whitegrid')

N=6
positions = [x - bar_width*(N-1)/2 + i*bar_width for i in range(N)]
red_shades = [
    '#ffe6e6',  # very light red
    '#ff9999',  # light red
    '#ff6666',  # medium-light red
    '#ff3333',  # medium red
    '#cc0000',  # dark red
    '#990000'   # very dark red
]
green_shades = [
    '#e6ffe6',  # very light green
    '#99ff99',  # light green
    '#66ff66',  # medium-light green
    '#33cc33',  # medium green
    '#009900',  # dark green
    '#006600'   # very dark green
]

# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# Plot bars for "Without Corrector"
bars_1 = ax.bar(
    # x - bar_width / 2,
    # x - 3*bar_width, 
    positions[0],
    iterations_category_in_percentage[0]['Pass'], 
    width=bar_width, 
    color=f'{green_shades[0]}', 
    edgecolor='black', 
    # label='W RAG and Corrector - Pass'
    label=f'Ite. 0 - Pass'
)
bars_2 = ax.bar(
    # x - bar_width / 2,
    positions[0], 
    iterations_category_in_percentage[0]['Fail'], 
    width=bar_width, 
    bottom=iterations_category_in_percentage[0]['Pass'], 
    color=f'{red_shades[5]}', 
    edgecolor='black', 
    # label='W RAG and Corrector - Fail'
    label='Ite. 0 - Fail'
)

# Plot bars for "With Corrector"
bars_3 = ax.bar(
    # x + bar_width / 2,
    positions[1], 
    iterations_category_in_percentage[1]['Pass'], 
    width=bar_width, 
    color=f'{green_shades[1]}', 
    hatch='//', 
    edgecolor='black', 
    label='Iet. 1 - Pass'
)
bars_4 = ax.bar(
    # x + bar_width / 2, 
    positions[1],
    iterations_category_in_percentage[1]['Fail'], 
    width=bar_width, 
    bottom=iterations_category_in_percentage[1]['Pass'], 
    color=f'{red_shades[4]}',  
    hatch='//', 
    edgecolor='black', 
    label='Iet. 1 - Fail'
)

# Plot bars for "Without Corrector"
bars_5 = ax.bar(
    # x - bar_width / 2,
    positions[2], 
    iterations_category_in_percentage[2]['Pass'], 
    width=bar_width, 
    color=f'{green_shades[2]}', 
    edgecolor='black', 
    label='Iet. 2 - Pass'
)
bars_6 = ax.bar(
    # x - bar_width / 2, 
    positions[2], 
    iterations_category_in_percentage[2]['Fail'], 
    width=bar_width, 
    bottom=iterations_category_in_percentage[2]['Pass'], 
    color=f'{red_shades[3]}',  
    edgecolor='black', 
    label='Iet. 2 - Fail'
)

# Plot bars for "With Corrector"
bars_7 = ax.bar(
    # x + bar_width / 2,
    positions[3],  
    iterations_category_in_percentage[3]['Pass'], 
    width=bar_width, 
    color=f'{green_shades[3]}', 
    hatch='//', 
    edgecolor='black', 
    label='Iet. 3 - Pass'
)
bars_8 = ax.bar(
    # x + bar_width / 2,
    positions[3], 
    iterations_category_in_percentage[3]['Fail'], 
    width=bar_width, 
    bottom=iterations_category_in_percentage[3]['Pass'], 
    color=f'{red_shades[2]}',  
    hatch='//', 
    edgecolor='black', 
    label='Iet. 3 - Fail'
)

bars_9 = ax.bar(
    # x + bar_width / 2,
    positions[4],  
    iterations_category_in_percentage[4]['Pass'], 
    width=bar_width, 
    color=f'{green_shades[4]}', 
    # hatch='//', 
    edgecolor='black', 
    label='Iet. 4 - Pass'
)
bars_10 = ax.bar(
    # x + bar_width / 2,
    positions[4], 
    iterations_category_in_percentage[4]['Fail'], 
    width=bar_width, 
    bottom=iterations_category_in_percentage[4]['Pass'], 
    color=f'{red_shades[1]}',  
    # hatch='//', 
    edgecolor='black', 
    label='Iet. 4 - Fail'
)

bars_11 = ax.bar(
    # x + bar_width / 2,
    positions[5],  
    iterations_category_in_percentage[5]['Pass'], 
    width=bar_width, 
    color=f'{green_shades[5]}', 
    hatch='//', 
    edgecolor='black', 
    label='Iet. 5 - Pass'
)
bars_12 = ax.bar(
    # x + bar_width / 2,
    positions[5], 
    iterations_category_in_percentage[5]['Fail'], 
    width=bar_width, 
    bottom=iterations_category_in_percentage[5]['Pass'], 
    color=f'{red_shades[0]}',  
    hatch='//', 
    edgecolor='black', 
    label='Iet. 5 - Fail'
)



# Add category labels
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12)

# Add labels and title
ax.set_xlabel('Simple Queries with RAG and CORRECTOR', fontsize=14)
# ax.set_ylabel('Number of Evaluated Python Scripts', fontsize=14)
ax.set_ylabel('Percentage of Evaluated Python Scripts', fontsize=14)
ax.set_title('Evaluation of Generated Code', fontsize=16)

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
plt.savefig('total_iterative_simple_q_cumulative_pass_fail_with_effect_of_iterative_process_3_datasets_final.pdf', bbox_inches='tight')
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
