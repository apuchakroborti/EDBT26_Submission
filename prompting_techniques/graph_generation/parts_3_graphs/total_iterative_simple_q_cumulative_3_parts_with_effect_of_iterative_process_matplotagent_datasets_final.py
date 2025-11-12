import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os

matplotagent_csv_base_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/error_categorization_evaluation_result/iterative_error_resolve'
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


# categories = ['CLIMATE', 'MATPLOTAGENT', 'FASTMRIBRAIN']
categories = ['']
csv_file_basename = 'error_categorization_report_'
iterations_category = []
iterations_category_in_percentage = []
for i in range(0, 6):
    print(f'\n\nIterations-------{i}')
    iteration_pass_fail = {'Pass': [], 'Fail': [], 'Correct': []}
    iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': [], 'Correct': []}
    # category 2
    file_path = os.path.join(matplotagent_csv_base_dir, f"{matplotagent_all_csv_files_sub_dir[0]}/{csv_file_basename}{i}.csv")
    if not os.path.exists(file_path):
        print(f"Missing: {file_path}")
        continue

    df = pd.read_csv(file_path)

    pass_count = df['Pass Count'].sum()
    print(f'Matplotagent CSV pass count: {pass_count}')
    
    correct_count = df['Correct'].sum()
    print(f'Matplotagent CSV Correct count: {correct_count}')

    fail_count = df['Fail Count'].sum()
    print(f'Matplotagent CSV fail count: {fail_count}\n')

    

    current_fail_count = fail_count
    

    # correct count
    cumulative_correct_count = correct_count
    current_correct_count = 0
    if i ==0:
        current_correct_count=correct_count
        iteration_pass_fail['Correct'].append(current_correct_count)
        iteration_pass_fail_in_percentage['Correct'].append((current_correct_count*100)/12)
    else:
        current_correct_count=iterations_category[i-1]['Correct'][0]
        iteration_pass_fail['Correct'].append(current_correct_count+correct_count)
        iteration_pass_fail_in_percentage['Correct'].append(((current_correct_count+correct_count)*100)/12)
        cumulative_correct_count = current_correct_count+correct_count
    
    
    # iteration_pass_fail['Fail'].append(current_fail_count)
    
    current_pass_count=0
    pass_count = pass_count - correct_count
    cumulative_pass_count = pass_count
    if i ==0:
        current_pass_count=pass_count
        iteration_pass_fail['Pass'].append(current_pass_count)
        iteration_pass_fail_in_percentage['Pass'].append((current_pass_count*100)/12)
        
    else:
        current_pass_count=iterations_category[i-1]['Pass'][0]
        iteration_pass_fail['Pass'].append(current_pass_count+pass_count)
        iteration_pass_fail_in_percentage['Pass'].append(((current_pass_count+pass_count)*100)/12)
        cumulative_pass_count = current_pass_count+pass_count
    # print(f'Current pass count: {current_pass_count}')
    iteration_pass_fail_in_percentage['Fail'].append((current_fail_count*100)/12)
    
    cumulative_fail_count = fail_count
    print(f'Current cumulative pass count: {cumulative_pass_count}')
    print(f'Current cumulative correct count: {cumulative_correct_count}')
    print(f'Current cumulative fail count: {cumulative_fail_count}')

    iteration_pass_fail['Fail'].append(current_fail_count)
    
    iterations_category.append(iteration_pass_fail)
    iterations_category_in_percentage.append(iteration_pass_fail_in_percentage)
    

print(iterations_category_in_percentage)
# Number of categories
n_categories = len(categories)

# Bar width and positions
# bar_width = 0.35
bar_width = 0.10
x = np.arange(n_categories)

# Use seaborn style
# sns.set_style('whitegrid')
sns.set(font_scale=1.5,style="whitegrid")

N=6
spacing_factor = 1.2  # Try values like 1.05 to 1.2 for small gaps
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
# green_shades = [
#     '#009900',  # very light green
#     '#009900',  # light green
#     '#009900',  # medium-light green
#     '#009900',  # medium green
#     '#009900',  # dark green
#     '#009900'   # very dark green
# ]
green_shades = [
    '#e6ffe6',  # very light green
    '#99ff99',  # light green
    '#66ff66',  # medium-light green
    '#33cc33',  # medium green
    '#009900',  # dark green
    '#006600'   # very dark green
]

# Create the figure and axes
# fig, ax = plt.subplots(figsize=(10, 6))
fig, ax = plt.subplots(figsize=(7, 5))

# Plot bars for "Without Corrector"
bars_1 = ax.bar(
    # x - bar_width / 2,
    # x - 3*bar_width, 
    positions[0],
    iterations_category_in_percentage[0]['Correct'], 
    width=bar_width, 
    color=f'{green_shades[3]}',
    #hatch='.',  
    edgecolor='black', 
    # label='W RAG and Corrector'
    label=f'1'
)
bars_1_2 = ax.bar(
    positions[0], 
    iterations_category_in_percentage[0]['Pass'], 
    width=bar_width, 
    bottom=iterations_category_in_percentage[0]['Correct'], 
    color='#ADD8E6', 
    edgecolor='black', 
    label='Ite. 0 - Fail'
)
# Add the third segment
bars_1_3 = ax.bar(
    positions[0], 
    iterations_category_in_percentage[0]['Fail'],  # or your third category
    width=bar_width, 
    bottom=[
        iterations_category_in_percentage[0]['Correct'][i] + iterations_category_in_percentage[0]['Pass'][i] 
        for i in range(len(positions[0]))
    ],
    color=red_shades[2],  # or another color you prefer
    edgecolor='black', 
    label='Fail'
)

# add label at the bottom of each bar
for bar in bars_1:
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    ax.text(
        bar_x,
        (bar_height/2)-3,  # small offset above the bar
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
    ax.text(
        bar_x,
        -5,  # small offset above the bar
        f"1",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )

# add label at the bottom of each bar
for i, bar in enumerate(bars_1_2):
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    
    # Get the bottom height for the middle segment
    bottom_height = bars_1[i].get_height()  # assuming bars_6_1 is the bottom bar
    
    ax.text(
        bar_x,
        bottom_height + (bar_height / 2),  # place in middle of the middle segment
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='center',
        fontsize=14,
        rotation=0
    )

# add label at the bottom of each bar
for i, bar in enumerate(bars_1_3):
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    
    # Get the bottom height for the middle segment
    bottom_height = bars_1[i].get_height()+bars_1_2[i].get_height()  # assuming bars_6_1 is the bottom bar
    
    ax.text(
        bar_x,
        bottom_height + (bar_height / 2),  # place in middle of the middle segment
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='center',
        fontsize=14,
        rotation=0
    )
    

# Plot bars for "With Corrector"
bars_2 = ax.bar(
    # x + bar_width / 2,
    positions[1], 
    iterations_category_in_percentage[1]['Correct'], 
    width=bar_width, 
    color=f'{green_shades[3]}', 
    #hatch='..', 
    edgecolor='black', 
    label='Iet. 1'
)
bars_2_2 = ax.bar(
    positions[1], 
    iterations_category_in_percentage[1]['Pass'], 
    width=bar_width, 
    bottom=iterations_category_in_percentage[1]['Correct'], 
    color='#ADD8E6', 
    edgecolor='black', 
    label='Ite. 0 - Fail'
)
# Add the third segment
bars_2_3 = ax.bar(
    positions[1], 
    iterations_category_in_percentage[1]['Fail'],  # or your third category
    width=bar_width, 
    bottom=[
        iterations_category_in_percentage[1]['Correct'][i] + iterations_category_in_percentage[1]['Pass'][i] 
        for i in range(len(positions[1]))
    ],
    color=red_shades[2],  # or another color you prefer
    edgecolor='black', 
    label='Fail'
)


# add label at the bottom of each bar
for bar in bars_2:
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    ax.text(
        bar_x,
        (bar_height/2)-3,  # small offset above the bar
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
    ax.text(
        bar_x,
        -5,  # small offset above the bar
        f"2",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
# add label at the bottom of each bar
for i, bar in enumerate(bars_2_2):
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    
    # Get the bottom height for the middle segment
    bottom_height = bars_2[i].get_height()  # assuming bars_6_1 is the bottom bar
    
    ax.text(
        bar_x,
        bottom_height + (bar_height / 2),  # place in middle of the middle segment
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='center',
        fontsize=14,
        rotation=0
    )

# add label at the bottom of each bar
for i, bar in enumerate(bars_2_3):
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    
    # Get the bottom height for the middle segment
    bottom_height = bars_2[i].get_height()+bars_2_2[i].get_height()  # assuming bars_6_1 is the bottom bar
    
    ax.text(
        bar_x,
        bottom_height + (bar_height / 2),  # place in middle of the middle segment
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='center',
        fontsize=14,
        rotation=0
    )

# Plot bars for "Without Corrector"
bars_3 = ax.bar(
    # x - bar_width / 2,
    positions[2], 
    iterations_category_in_percentage[2]['Correct'], 
    width=bar_width, 
    color=f'{green_shades[3]}',
    #hatch='*',  
    edgecolor='black', 
    label='Iet. 2'
)

bars_3_2 = ax.bar(
    positions[2], 
    iterations_category_in_percentage[2]['Pass'], 
    width=bar_width, 
    bottom=iterations_category_in_percentage[2]['Correct'], 
    color='#ADD8E6', 
    edgecolor='black', 
    label='Ite. 0 - Fail'
)
# Add the third segment
bars_3_3 = ax.bar(
    positions[2], 
    iterations_category_in_percentage[2]['Fail'],  # or your third category
    width=bar_width, 
    bottom=[
        iterations_category_in_percentage[2]['Correct'][i] + iterations_category_in_percentage[2]['Pass'][i] 
        for i in range(len(positions[2]))
    ],
    color=red_shades[2],  # or another color you prefer
    edgecolor='black', 
    label='Fail'
)


# add label at the bottom of each bar
for bar in bars_3:
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    ax.text(
        bar_x,
        (bar_height/2)-3,  # small offset above the bar
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
    ax.text(
        bar_x,
        -5,  # small offset above the bar
        f"3",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )

# add label at the bottom of each bar
for i, bar in enumerate(bars_3_2):
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    
    # Get the bottom height for the middle segment
    bottom_height = bars_3[i].get_height()  # assuming bars_6_1 is the bottom bar
    
    ax.text(
        bar_x,
        bottom_height + (bar_height / 2),  # place in middle of the middle segment
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='center',
        fontsize=14,
        rotation=0
    )

# add label at the bottom of each bar
for i, bar in enumerate(bars_3_3):
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    
    # Get the bottom height for the middle segment
    bottom_height = bars_3[i].get_height()+bars_3_2[i].get_height()  # assuming bars_6_1 is the bottom bar
    
    ax.text(
        bar_x,
        bottom_height + (bar_height / 2),  # place in middle of the middle segment
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='center',
        fontsize=14,
        rotation=0
    )
# Plot bars for "With Corrector"
bars_4 = ax.bar(
    # x + bar_width / 2,
    positions[3],  
    iterations_category_in_percentage[3]['Correct'], 
    width=bar_width, 
    color=f'{green_shades[3]}', 
    #hatch='**', 
    edgecolor='black', 
    label='Iet. 3'
)
bars_4_2 = ax.bar(
    positions[3], 
    iterations_category_in_percentage[3]['Pass'], 
    width=bar_width, 
    bottom=iterations_category_in_percentage[3]['Correct'], 
    color='#ADD8E6', 
    edgecolor='black', 
    label='Ite. 0 - Fail'
)
# Add the third segment
bars_4_3 = ax.bar(
    positions[3], 
    iterations_category_in_percentage[3]['Fail'],  # or your third category
    width=bar_width, 
    bottom=[
        iterations_category_in_percentage[3]['Correct'][i] + iterations_category_in_percentage[3]['Pass'][i] 
        for i in range(len(positions[3]))
    ],
    color=red_shades[2],  # or another color you prefer
    edgecolor='black', 
    label='Fail'
)

# add label at the bottom of each bar
for bar in bars_4:
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    ax.text(
        bar_x,
        (bar_height/2)-3,  # small offset above the bar
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
    ax.text(
        bar_x,
        -5,  # small offset above the bar
        f"4",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )

# add label at the bottom of each bar
for i, bar in enumerate(bars_4_2):
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    
    # Get the bottom height for the middle segment
    bottom_height = bars_4[i].get_height()  # assuming bars_6_1 is the bottom bar
    
    ax.text(
        bar_x,
        bottom_height + (bar_height / 2),  # place in middle of the middle segment
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='center',
        fontsize=14,
        rotation=0
    )

# add label at the bottom of each bar
for i, bar in enumerate(bars_4_3):
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    
    # Get the bottom height for the middle segment
    bottom_height = bars_4[i].get_height()+bars_4_2[i].get_height()  # assuming bars_6_1 is the bottom bar
    
    ax.text(
        bar_x,
        bottom_height + (bar_height / 2),  # place in middle of the middle segment
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='center',
        fontsize=14,
        rotation=0
    )

bars_5 = ax.bar(
    # x + bar_width / 2,
    positions[4],  
    iterations_category_in_percentage[4]['Correct'], 
    width=bar_width, 
    color=f'{green_shades[3]}', 
    #hatch='o', 
    edgecolor='black', 
    label='5'
)

bars_5_2 = ax.bar(
    positions[4], 
    iterations_category_in_percentage[4]['Pass'], 
    width=bar_width, 
    bottom=iterations_category_in_percentage[4]['Correct'], 
    color='#ADD8E6', 
    edgecolor='black', 
    label='Ite. 0 - Fail'
)
# Add the third segment
bars_5_3 = ax.bar(
    positions[4], 
    iterations_category_in_percentage[4]['Fail'],  # or your third category
    width=bar_width, 
    bottom=[
        iterations_category_in_percentage[4]['Correct'][i] + iterations_category_in_percentage[4]['Pass'][i] 
        for i in range(len(positions[4]))
    ],
    color=red_shades[2],  # or another color you prefer
    edgecolor='black', 
    label='Fail'
)

# add label at the bottom of each bar
for bar in bars_5:
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    ax.text(
        bar_x,
        (bar_height/2)-3,  # small offset above the bar
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
    ax.text(
        bar_x,
        -5,  # small offset above the bar
        f"5",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
    
# add label at the bottom of each bar
for i, bar in enumerate(bars_5_2):
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    
    # Get the bottom height for the middle segment
    bottom_height = bars_5[i].get_height()  # assuming bars_6_1 is the bottom bar
    
    ax.text(
        bar_x,
        bottom_height + (bar_height / 2),  # place in middle of the middle segment
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='center',
        fontsize=14,
        rotation=0
    )

# add label at the bottom of each bar
for i, bar in enumerate(bars_5_3):
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    
    # Get the bottom height for the middle segment
    bottom_height = bars_5[i].get_height()+bars_5_2[i].get_height()  # assuming bars_6_1 is the bottom bar
    
    ax.text(
        bar_x,
        bottom_height + (bar_height / 2),  # place in middle of the middle segment
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='center',
        fontsize=14,
        rotation=0
    )


bars_6 = ax.bar(
    # x + bar_width / 2,
    positions[5],  
    iterations_category_in_percentage[5]['Correct'], 
    width=bar_width, 
    color=f'{green_shades[3]}', 
    #hatch='O', 
    edgecolor='black', 
    label='6'
)
bars_6_2 = ax.bar(
    positions[5], 
    iterations_category_in_percentage[5]['Pass'], 
    width=bar_width, 
    bottom=iterations_category_in_percentage[5]['Correct'], 
    color='#ADD8E6', 
    edgecolor='black', 
    label='Ite. 0 - Fail'
)
# Add the third segment
bars_6_3 = ax.bar(
    positions[5], 
    iterations_category_in_percentage[5]['Fail'],  # or your third category
    width=bar_width, 
    bottom=[
        iterations_category_in_percentage[5]['Correct'][i] + iterations_category_in_percentage[5]['Pass'][i] 
        for i in range(len(positions[5]))
    ],
    color=red_shades[2],  # or another color you prefer
    edgecolor='black', 
    label='Fail'
)
# add label at the bottom of each bar
for bar in bars_6:
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    ax.text(
        bar_x,
        (bar_height/2)-3,  # small offset above the bar
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )
    ax.text(
        bar_x,
        -5,  # small offset above the bar
        f"6",  # Customize as needed
        ha='center',
        va='bottom',
        fontsize=14,
        rotation=0
    )

# add label at the bottom of each bar
for i, bar in enumerate(bars_6_2):
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    
    # Get the bottom height for the middle segment
    bottom_height = bars_6[i].get_height()  # assuming bars_6_1 is the bottom bar
    
    ax.text(
        bar_x,
        bottom_height + (bar_height / 2),  # place in middle of the middle segment
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='center',
        fontsize=14,
        rotation=0
    )
# for bar in bars_6_2:


# add label at the bottom of each bar
for i, bar in enumerate(bars_6_3):
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    
    # Get the bottom height for the middle segment
    bottom_height = bars_6[i].get_height()+bars_6_2[i].get_height()  # assuming bars_6_1 is the bottom bar
    
    ax.text(
        bar_x,
        bottom_height + (bar_height / 2),  # place in middle of the middle segment
        f"{bar_height:.1f}%",  # Customize as needed
        ha='center',
        va='center',
        fontsize=14,
        rotation=0
    )


# Add category labels
# bar_labels = ['Iter 0', 'Iter 1', 'Iter 2', 'Iter 3', 'Iter 4', 'Iter 5']
ax.set_xticks(x)
# ax.set_xticks(positions)
ax.set_xticklabels(categories, fontsize=14)

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
plt.savefig('total_iterative_simple_q_cumulative_3_parts_with_effect_of_iterative_process_matplotagent_datasets_final.pdf', bbox_inches='tight')
# plt.savefig('total_iterative_expert_q_cumulative_3_parts_with_effect_of_iterative_process_matplotagent_datasets_final.pdf', bbox_inches='tight')
plt.show()