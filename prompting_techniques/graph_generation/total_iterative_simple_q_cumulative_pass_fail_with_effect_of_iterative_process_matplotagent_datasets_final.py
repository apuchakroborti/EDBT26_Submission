import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os

matplotagent_csv_base_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/error_categorization_evaluation_result/iterative_error_resolve'
matplotagent_all_csv_files_sub_dir = [
    "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_corrector"
    # "devstral_24b_matplotagent_iterative_python_scripts_with_rag_without_corrector",
    # "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_corrector",
    # "devstral_24b_matplotagent_iterative_python_scripts_without_rag_without_corrector",
    
    # "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_with_corrector",
    
    # "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_without_corrector",
    # "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_errors_with_corrector",
    # "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_errors_without_corrector",
]


# categories = ['CLIMATE', 'MATPLOTAGENT', 'FASTMRIBRAIN']
categories = ['']
csv_file_basename = 'error_categorization_report_'
iterations_category = []
iterations_category_in_percentage = []
for i in range(0, 6):
    print(f'\n\nIterations-------{i}')
    iteration_pass_fail = {'Pass': [], 'Fail': []}
    iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': []}
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

    # iteration_pass_fail['Fail'].append(current_fail_count)
    if i ==0:
        current_pass_count=pass_count
        iteration_pass_fail['Pass'].append(current_pass_count)
        iteration_pass_fail_in_percentage['Pass'].append((current_pass_count*100)/12)
    else:
        current_pass_count=iterations_category[i-1]['Pass'][0]
        iteration_pass_fail['Pass'].append(current_pass_count+pass_count)
        iteration_pass_fail_in_percentage['Pass'].append(((current_pass_count+pass_count)*100)/12)
    print(f'Current pass count: {current_pass_count}')
    iteration_pass_fail_in_percentage['Fail'].append((current_fail_count*100)/12)

    iteration_pass_fail['Fail'].append(current_fail_count)
    
    iterations_category.append(iteration_pass_fail)
    iterations_category_in_percentage.append(iteration_pass_fail_in_percentage)
    

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
spacing_factor = 1.1  # Try values like 1.05 to 1.2 for small gaps
positions = [x - bar_width*(N-1)/2 + i*bar_width*spacing_factor for i in range(N)]

# positions = [x - bar_width*(N-1)/2 + i*bar_width for i in range(N)]
red_shades = [
    '#ffe6e6',  # very light red
    '#ff9999',  # light red
    '#ff6666',  # medium-light red
    '#ff3333',  # medium red
    '#cc0000',  # dark red
    '#990000'   # very dark red
]
green_shades = [
    '#009900',  # very light green
    '#009900',  # light green
    '#009900',  # medium-light green
    '#009900',  # medium green
    '#009900',  # dark green
    '#009900'   # very dark green
]
# green_shades = [
#     '#e6ffe6',  # very light green
#     '#99ff99',  # light green
#     '#66ff66',  # medium-light green
#     '#33cc33',  # medium green
#     '#009900',  # dark green
#     '#006600'   # very dark green
# ]

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
    #hatch='.',  
    edgecolor='black', 
    # label='W RAG and Corrector'
    label=f'0'
)

# add label at the bottom of each bar
for bar in bars_1:
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    ax.text(
        bar_x,
        bar_height + 1,  # small offset above the bar
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
    ax.text(
        bar_x,
        -3,  # small offset above the bar
        f"1",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )

# Plot bars for "With Corrector"
bars_3 = ax.bar(
    # x + bar_width / 2,
    positions[1], 
    iterations_category_in_percentage[1]['Pass'], 
    width=bar_width, 
    color=f'{green_shades[1]}', 
    #hatch='..', 
    edgecolor='black', 
    label='Iet. 1'
)

# add label at the bottom of each bar
for bar in bars_3:
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    ax.text(
        bar_x,
        bar_height + 1,  # small offset above the bar
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
    ax.text(
        bar_x,
        -3,  # small offset above the bar
        f"2",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )


# Plot bars for "Without Corrector"
bars_5 = ax.bar(
    # x - bar_width / 2,
    positions[2], 
    iterations_category_in_percentage[2]['Pass'], 
    width=bar_width, 
    color=f'{green_shades[2]}',
    #hatch='*',  
    edgecolor='black', 
    label='Iet. 2'
)

# add label at the bottom of each bar
for bar in bars_5:
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    ax.text(
        bar_x,
        bar_height + 1,  # small offset above the bar
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
    ax.text(
        bar_x,
        -3,  # small offset above the bar
        f"3",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )


# Plot bars for "With Corrector"
bars_7 = ax.bar(
    # x + bar_width / 2,
    positions[3],  
    iterations_category_in_percentage[3]['Pass'], 
    width=bar_width, 
    color=f'{green_shades[3]}', 
    #hatch='**', 
    edgecolor='black', 
    label='Iet. 3'
)
# add label at the bottom of each bar
for bar in bars_7:
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    ax.text(
        bar_x,
        bar_height + 1,  # small offset above the bar
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
    ax.text(
        bar_x,
        -3,  # small offset above the bar
        f"4",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )


bars_9 = ax.bar(
    # x + bar_width / 2,
    positions[4],  
    iterations_category_in_percentage[4]['Pass'], 
    width=bar_width, 
    color=f'{green_shades[4]}', 
    #hatch='o', 
    edgecolor='black', 
    label='5'
)

# add label at the bottom of each bar
for bar in bars_9:
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    ax.text(
        bar_x,
        bar_height + 1,  # small offset above the bar
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
    ax.text(
        bar_x,
        -3,  # small offset above the bar
        f"5",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
    
bars_11 = ax.bar(
    # x + bar_width / 2,
    positions[5],  
    iterations_category_in_percentage[5]['Pass'], 
    width=bar_width, 
    color=f'{green_shades[5]}', 
    #hatch='O', 
    edgecolor='black', 
    label='6'
)

# add label at the bottom of each bar
for bar in bars_11:
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    ax.text(
        bar_x,
        bar_height + 1,  # small offset above the bar
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
    ax.text(
        bar_x,
        -3,  # small offset above the bar
        f"6",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )



# Add category labels
bar_labels = ['Iter 0', 'Iter 1', 'Iter 2', 'Iter 3', 'Iter 4', 'Iter 5']
ax.set_xticks(x)
# ax.set_xticks(positions)
ax.set_xticklabels(categories, fontsize=12)

# Add labels and title
# ax.set_xlabel('Simple Queries with RAG and CORRECTOR', fontsize=14)
ax.set_xlabel('Iteration', fontsize=14)
# not being used
# ax.set_ylabel('Number of Evaluated Python Scripts', fontsize=14)
ax.set_ylabel('Success rate of evaluated Python Scripts', fontsize=14)
# ax.set_title('Evaluation of Generated Code', fontsize=16)

# Add grid for better visibility
ax.grid(axis='y', linestyle='--', alpha=0.7)


# Adjust layout to ensure no cropping
plt.tight_layout()

# Save and show the plot
# plt.savefig('total_pass_fail_count_simple_queries_different_models_climate_datasets.pdf', bbox_inches='tight')
# plt.savefig('total_iterative_simple_q_cumulative_pass_fail_with_effect_of_iterative_process_matplotagent_datasets_final.pdf', bbox_inches='tight')
plt.savefig('total_iterative_expert_q_cumulative_pass_fail_with_effect_of_iterative_process_matplotagent_datasets_final.pdf', bbox_inches='tight')

plt.show()