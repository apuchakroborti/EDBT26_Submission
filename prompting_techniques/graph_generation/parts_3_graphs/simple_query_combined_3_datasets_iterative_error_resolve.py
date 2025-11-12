import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
import pandas as pd

def count_high_similarity(csv_path):
    """
    Reads a CSV file and counts how many values in the 'Similarity Raw' column
    are greater than 0.85.

    Parameters:
        csv_path (str): The path to the CSV file.

    Returns:
        int: Count of rows with 'Similarity Raw' > 0.85
    """
    df = pd.read_csv(csv_path)

    if 'Similarity Raw' not in df.columns:
        raise ValueError("'Similarity Raw' column not found in the CSV.")

    # count = (df['Similarity Raw'] > 0.85).sum()
    count = (df['Similarity Raw'] >= 0.85).sum()
    return count

project_base_directory = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data'
climate_csv_dir = f'{project_base_directory}/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag'
list_of_python_scripts_sub_dirs_for_climate = [
             "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_corrector"
            ]

import os
categories = ['']
csv_file_basename = 'error_categorization_report_'
correct_runnable_csv_file_basename = 'similarity_results_'

# models_category_simple_q_in_percentage = []
# models_category_expert_q_in_percentage = []

iterations_category = []
iterations_category_in_percentage = []

for i in range(0, 6):
    print(f'\n\Climate Iteration-------{i}')
    # simple_iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': [], 'Correct': []}
    iteration_pass_fail = {'Pass': [], 'Fail': [], 'Correct': []}
    iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': [], 'Correct': []}
    # category 2
    # file_path = os.path.join(climate_csv_dir, f"{matplotagent_all_csv_files_sub_dir[0]}/{csv_file_basename}{i}.csv")
    file_path = os.path.join(climate_csv_dir, f"{list_of_python_scripts_sub_dirs_for_climate[0]}/{csv_file_basename}{i}.csv")
    if not os.path.exists(file_path):
        print(f"Missing: {file_path}")
        continue
    df = pd.read_csv(file_path)
    pass_count = df['Pass Count'].sum()
    print(f'Climate CSV pass count: {pass_count}')
    
    fail_count = df['Fail Count'].sum()
    print(f'Climate CSV fail count: {fail_count}')

    # read correct and runnable scripts
    correct_runnable_file_path = os.path.join(climate_csv_dir, f"{list_of_python_scripts_sub_dirs_for_climate[0]}/{correct_runnable_csv_file_basename}{i}.csv")
    if not os.path.exists(correct_runnable_file_path):
        print(f"Missing correct_runnable_file_path: {correct_runnable_file_path}")
        continue

    correct_count = count_high_similarity(correct_runnable_file_path)
    print(f'Climate CSV Correct count: {correct_count}')

    # from previous experiment
    cumulative_correct_count = correct_count
    current_correct_count = 0
    if i ==0:
        current_correct_count=correct_count
        iteration_pass_fail['Correct'].append(current_correct_count)
        iteration_pass_fail_in_percentage['Correct'].append((current_correct_count*100)/61)
    else:
        current_correct_count=iterations_category[i-1]['Correct'][0]
        iteration_pass_fail['Correct'].append(current_correct_count+correct_count)
        iteration_pass_fail_in_percentage['Correct'].append(((current_correct_count+correct_count)*100)/61)
        cumulative_correct_count = current_correct_count+correct_count
    
    
    current_pass_count=0
    pass_count = pass_count - correct_count
    cumulative_pass_count = pass_count
    if i ==0:
        current_pass_count=pass_count
        iteration_pass_fail['Pass'].append(current_pass_count)
        iteration_pass_fail_in_percentage['Pass'].append((current_pass_count*100)/61)
        
    else:
        current_pass_count=iterations_category[i-1]['Pass'][0]
        iteration_pass_fail['Pass'].append(current_pass_count+pass_count)
        iteration_pass_fail_in_percentage['Pass'].append(((current_pass_count+pass_count)*100)/61)
        cumulative_pass_count = current_pass_count+pass_count
    # print(f'Current pass count: {current_pass_count}')
    iteration_pass_fail['Fail'].append(fail_count)
    iteration_pass_fail_in_percentage['Fail'].append((fail_count*100)/61)
    
    print(f'Climate Current cumulative pass count: {cumulative_pass_count}')
    print(f'Climate Current cumulative correct count: {cumulative_correct_count}')
    print(f'Climate Current cumulative fail count: {fail_count}')    
    
    iterations_category.append(iteration_pass_fail)
    iterations_category_in_percentage.append(iteration_pass_fail_in_percentage)

print(f'Climate Size of iterations_category: {len(iterations_category)}')
print(f'Climate Size of iterations_category_in_percentage: {len(iterations_category_in_percentage)}')

# -----------------------MATPLOTAGENT---------------------

matplotagent_csv_dir = f'{project_base_directory}/matplot_agent_data/plot_generation/error_categorization_evaluation_result/iterative_error_resolve'
list_of_python_scripts_sub_dirs_for_matplotagent = [
              "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_with_corrector",
            ]


m_iterations_category = []
m_iterations_category_in_percentage = []

for i in range(0, 6):
    print(f'\n\Matplotagent Iteration-------{i}')
    # simple_iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': [], 'Correct': []}
    iteration_pass_fail = {'Pass': [], 'Fail': [], 'Correct': []}
    iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': [], 'Correct': []}
    # category 2
    # file_path = os.path.join(climate_csv_dir, f"{matplotagent_all_csv_files_sub_dir[0]}/{csv_file_basename}{i}.csv")
    file_path = os.path.join(matplotagent_csv_dir, f"{list_of_python_scripts_sub_dirs_for_matplotagent[0]}/{csv_file_basename}{i}.csv")
    if not os.path.exists(file_path):
        print(f"Missing: {file_path}")
        continue
    df = pd.read_csv(file_path)
    pass_count = df['Pass Count'].sum()
    print(f'Matplotagent CSV pass count: {pass_count}')
    
    fail_count = df['Fail Count'].sum()
    print(f'Matplotagent CSV fail count: {fail_count}')

    # read correct and runnable scripts
    correct_runnable_file_path = os.path.join(matplotagent_csv_dir, f"{list_of_python_scripts_sub_dirs_for_matplotagent[0]}/{correct_runnable_csv_file_basename}{i}.csv")
    if not os.path.exists(correct_runnable_file_path):
        print(f"Missing correct_runnable_file_path: {correct_runnable_file_path}")
        continue

    correct_count = count_high_similarity(correct_runnable_file_path)
    print(f'Matplotagent CSV Correct count: {correct_count}')

    # from previous experiment
    cumulative_correct_count = correct_count
    current_correct_count = 0
    if i ==0:
        current_correct_count=correct_count
        iteration_pass_fail['Correct'].append(current_correct_count)
        iteration_pass_fail_in_percentage['Correct'].append((current_correct_count*100)/12)
    else:
        current_correct_count=m_iterations_category[i-1]['Correct'][0]
        iteration_pass_fail['Correct'].append(current_correct_count+correct_count)
        iteration_pass_fail_in_percentage['Correct'].append(((current_correct_count+correct_count)*100)/12)
        cumulative_correct_count = current_correct_count+correct_count
    
    
    current_pass_count=0
    pass_count = pass_count - correct_count
    cumulative_pass_count = pass_count
    if i ==0:
        current_pass_count=pass_count
        iteration_pass_fail['Pass'].append(current_pass_count)
        iteration_pass_fail_in_percentage['Pass'].append((current_pass_count*100)/12)
        
    else:
        current_pass_count=m_iterations_category[i-1]['Pass'][0]
        iteration_pass_fail['Pass'].append(current_pass_count+pass_count)
        iteration_pass_fail_in_percentage['Pass'].append(((current_pass_count+pass_count)*100)/12)
        cumulative_pass_count = current_pass_count+pass_count
    # print(f'Current pass count: {current_pass_count}')
    iteration_pass_fail['Fail'].append(fail_count)
    iteration_pass_fail_in_percentage['Fail'].append((fail_count*100)/12)
    
    print(f'Matplotagent Current cumulative pass count: {cumulative_pass_count}')
    print(f'Matplotagent Current cumulative correct count: {cumulative_correct_count}')
    print(f'Matplotagent Current cumulative fail count: {fail_count}')    
    
    m_iterations_category.append(iteration_pass_fail)
    m_iterations_category_in_percentage.append(iteration_pass_fail_in_percentage)

print(f'Matplotagent Size of m_iterations_category: {len(m_iterations_category)}')
print(f'Matplotagent Size of m_iterations_category_in_percentage: {len(m_iterations_category_in_percentage)}')

# -----------FASTMRIBRAIN------------
fastmribrain_csv_dir = f'{project_base_directory}/mri_nyu_data/error_categorization_evaluation_result/iterative_evaluation_results'
list_of_python_scripts_sub_dirs_for_fastmribrain = [          
            "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_errors_with_corrector",         
            ]

f_iterations_category = []
f_iterations_category_in_percentage = []

for i in range(0, 6):
    print(f'\n\Fastmribrain Iteration-------{i}')
    # simple_iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': [], 'Correct': []}
    iteration_pass_fail = {'Pass': [], 'Fail': [], 'Correct': []}
    iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': [], 'Correct': []}
    # category 2
    # file_path = os.path.join(climate_csv_dir, f"{matplotagent_all_csv_files_sub_dir[0]}/{csv_file_basename}{i}.csv")
    file_path = os.path.join(fastmribrain_csv_dir, f"{list_of_python_scripts_sub_dirs_for_fastmribrain[0]}/{csv_file_basename}{i}.csv")
    if not os.path.exists(file_path):
        print(f"Missing: {file_path}")
        continue
    df = pd.read_csv(file_path)
    pass_count = df['Pass Count'].sum()
    print(f'Fastmribrain CSV pass count: {pass_count}')
    
    fail_count = df['Fail Count'].sum()
    print(f'Fastmribrain CSV fail count: {fail_count}')

    # read correct and runnable scripts
    correct_runnable_file_path = os.path.join(fastmribrain_csv_dir, f"{list_of_python_scripts_sub_dirs_for_fastmribrain[0]}/{correct_runnable_csv_file_basename}{i}.csv")
    if not os.path.exists(correct_runnable_file_path):
        print(f"Missing correct_runnable_file_path: {correct_runnable_file_path}")
        continue

    correct_count = count_high_similarity(correct_runnable_file_path)
    print(f'Climate CSV Correct count: {correct_count}')

    # from previous experiment
    cumulative_correct_count = correct_count
    current_correct_count = 0
    if i ==0:
        current_correct_count=correct_count
        iteration_pass_fail['Correct'].append(current_correct_count)
        iteration_pass_fail_in_percentage['Correct'].append((current_correct_count*100)/11)
    else:
        current_correct_count=f_iterations_category[i-1]['Correct'][0]
        iteration_pass_fail['Correct'].append(current_correct_count+correct_count)
        iteration_pass_fail_in_percentage['Correct'].append(((current_correct_count+correct_count)*100)/11)
        cumulative_correct_count = current_correct_count+correct_count
    
    
    current_pass_count=0
    pass_count = pass_count - correct_count
    cumulative_pass_count = pass_count
    if i ==0:
        current_pass_count=pass_count
        iteration_pass_fail['Pass'].append(current_pass_count)
        iteration_pass_fail_in_percentage['Pass'].append((current_pass_count*100)/11)
        
    else:
        current_pass_count=f_iterations_category[i-1]['Pass'][0]
        iteration_pass_fail['Pass'].append(current_pass_count+pass_count)
        iteration_pass_fail_in_percentage['Pass'].append(((current_pass_count+pass_count)*100)/11)
        cumulative_pass_count = current_pass_count+pass_count
    # print(f'Current pass count: {current_pass_count}')
    iteration_pass_fail['Fail'].append(fail_count)
    iteration_pass_fail_in_percentage['Fail'].append((fail_count*100)/11)
    
    print(f'Fastmribrain Current cumulative pass count: {cumulative_pass_count}')
    print(f'Fastmribrain Current cumulative correct count: {cumulative_correct_count}')
    print(f'Fastmribrain Current cumulative fail count: {fail_count}')    
    
    f_iterations_category.append(iteration_pass_fail)
    f_iterations_category_in_percentage.append(iteration_pass_fail_in_percentage)

print(f'Fastmribrain Size of f_iterations_category: {len(f_iterations_category)}')
print(f'Fastmribrain Size of f_iterations_category_in_percentage: {len(f_iterations_category_in_percentage)}')


# Set style
sns.set(style="whitegrid")

def make_df(category, green1, blue1, red1):
    methods = ['1', '2', '3', '4', '5', '6']
    data = []
    for i, method in enumerate(methods):
        data.append({
            'Method': method,
            'Run': 'W RAG & Disambiguation',
            'Correct': green1[i],
            'Runnable': blue1[i],
            'Failed': red1[i],
            'Dataset': category
        })
        # data.append({
        #     'Method': method,
        #     'Run': 'W RAG',
        #     'Correct': green2[i],
        #     'Runnable': blue2[i],
        #     'Failed': red2[i],
        #     'Dataset': category
        # })
    return pd.DataFrame(data)

# climate
s_correct = [
    iterations_category_in_percentage[0]['Correct'][0],
    iterations_category_in_percentage[1]['Correct'][0],
    iterations_category_in_percentage[2]['Correct'][0],
    iterations_category_in_percentage[3]['Correct'][0],
    iterations_category_in_percentage[4]['Correct'][0],
    iterations_category_in_percentage[5]['Correct'][0],
             ]

s_runnable = [
    iterations_category_in_percentage[0]['Pass'][0],
    iterations_category_in_percentage[1]['Pass'][0],
    iterations_category_in_percentage[2]['Pass'][0],
    iterations_category_in_percentage[3]['Pass'][0],
    iterations_category_in_percentage[4]['Pass'][0],
    iterations_category_in_percentage[5]['Pass'][0],
]

s_failed = [
    iterations_category_in_percentage[0]['Fail'][0],
    iterations_category_in_percentage[1]['Fail'][0],
    iterations_category_in_percentage[2]['Fail'][0],
    iterations_category_in_percentage[3]['Fail'][0],
    iterations_category_in_percentage[4]['Fail'][0],
    iterations_category_in_percentage[5]['Fail'][0],
]


# matplotagent
m_s_correct = [
    m_iterations_category_in_percentage[0]['Correct'][0],
    m_iterations_category_in_percentage[1]['Correct'][0],
    m_iterations_category_in_percentage[2]['Correct'][0],
    m_iterations_category_in_percentage[3]['Correct'][0],
    m_iterations_category_in_percentage[4]['Correct'][0],
    m_iterations_category_in_percentage[5]['Correct'][0],
    
    ]

m_s_runnable = [
    m_iterations_category_in_percentage[0]['Pass'][0],
    m_iterations_category_in_percentage[1]['Pass'][0],
    m_iterations_category_in_percentage[2]['Pass'][0],
    m_iterations_category_in_percentage[3]['Pass'][0],
    m_iterations_category_in_percentage[4]['Pass'][0],
    m_iterations_category_in_percentage[5]['Pass'][0],
    
    ]

m_s_failed = [ 
    m_iterations_category_in_percentage[0]['Fail'][0],
    m_iterations_category_in_percentage[1]['Fail'][0],
    m_iterations_category_in_percentage[2]['Fail'][0],
    m_iterations_category_in_percentage[3]['Fail'][0],
    m_iterations_category_in_percentage[4]['Fail'][0],
    m_iterations_category_in_percentage[5]['Fail'][0],
    ]

# fastmribrain
f_s_correct = [
    f_iterations_category_in_percentage[0]['Correct'][0],
    f_iterations_category_in_percentage[1]['Correct'][0],
    f_iterations_category_in_percentage[2]['Correct'][0],
    f_iterations_category_in_percentage[3]['Correct'][0],
    f_iterations_category_in_percentage[4]['Correct'][0],
    f_iterations_category_in_percentage[5]['Correct'][0],
    ]

f_s_runnable = [
    f_iterations_category_in_percentage[0]['Pass'][0],
    f_iterations_category_in_percentage[1]['Pass'][0],
    f_iterations_category_in_percentage[2]['Pass'][0],
    f_iterations_category_in_percentage[3]['Pass'][0],
    f_iterations_category_in_percentage[4]['Pass'][0],
    f_iterations_category_in_percentage[5]['Pass'][0],
]

f_s_failed = [ 
    f_iterations_category_in_percentage[0]['Fail'][0],
    f_iterations_category_in_percentage[1]['Fail'][0],
    f_iterations_category_in_percentage[2]['Fail'][0],
    f_iterations_category_in_percentage[3]['Fail'][0],
    f_iterations_category_in_percentage[4]['Fail'][0],
    f_iterations_category_in_percentage[5]['Fail'][0],
]



df_A = make_df(
    'NASA\'s EOS',
    green1=s_correct, blue1=s_runnable, red1=s_failed,
    # green2=d_correct, blue2=d_runnable, red2=d_failed
)

df_B = make_df(
    'MatPlotBench',
    green1=m_s_correct, blue1=m_s_runnable, red1=m_s_failed,
    # green2=m_d_correct, blue2=m_d_runnable, red2=m_d_failed
)

df_C = make_df(
    'fastMRI',
    green1=f_s_correct, blue1=f_s_runnable, red1=f_s_failed,
    # green2=f_d_correct, blue2=f_d_runnable, red2=f_d_failed
)


# Combine all
df_all = pd.concat([df_A, df_B, df_C], ignore_index=True)

# Define bar colors
# segment_order = ['Green', 'Blue', 'Red']
segment_order = ['Correct', 'Runnable', 'Failed']

# colors = {'Green': 'lightgreen', 'Blue': 'lightblue', 'Red': 'lightcoral'}
# colors = {'Correct': 'lightgreen', 'Runnable': 'lightblue', 'Failed': 'lightcoral'}
# colors = {'Correct': ['lightgreen', 'mediumseagreen'],
#     'Runnable': ['lightblue', 'skyblue'],
#     'Failed': ['lightcoral', 'indianred']}
# colors = {
#     'Correct': ['#2ECC71', '#1D8348'],      # Bright green, dark green
#     'Runnable': ['#3498DB', '#1B4F72'],     # Bright blue, navy blue
#     'Failed': ['#E74C3C', '#78281F']        # Bright red, dark maroon
# }
# colors = {
#     'Correct': ['#A9DFBF', '#58D68D'],     # light mint green, bright sea green
#     'Runnable': ['#AED6F1', '#5DADE2'],    # light sky blue, moderate blue
#     'Failed': ['#F5B7B1', '#EC7063']       # light salmon pink, strong coral red
# }

colors = {
    'Correct': '#58D68D',     # light mint green, bright sea green
    'Runnable': '#5DADE2',    # light sky blue, moderate blue
    'Failed': '#EC7063'       # light salmon pink, strong coral red
}

hatch_style = ''  # hatch for second bar
FONTSIZE = 24
# Create figure and axes manually for better layout control
# fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
# fig, axes = plt.subplots(1, 3, figsize=(12, 5), sharey=True)
fig, axes = plt.subplots(1, 3, figsize=(8, 5), sharey=True)

# Plotting function
def plot_grouped_stacked(ax, data):
    methods = ['1', '2', '3', '4', '5', '6']
    # methods = ['devstral:24b', 'magicoder', 'llama3:70b', 'gemma3:27b', 'deepseek-r1:70b']
    # bar_width = 0.35
    bar_width = 0.50
    # gap = 0.2
    gap = 0.005

    for i, method in enumerate(methods):
        for j, run in enumerate(['W RAG & Disambiguation']):
            subset = data[(data['Method'] == method) & (data['Run'] == run)]
            if subset.empty:
                continue
            # x = i * (2 * bar_width + gap) + j * bar_width
            group_gap = 0.2
            x = i * ((1 * bar_width) + group_gap) + j * bar_width
            bottom = 0
            for seg in segment_order:
                value = subset[seg].values[0]
                if value == 0:
                    continue
                hatch = hatch_style if run == 'W RAG' else None
                bar_color = colors[seg][1] if run == 'W RAG' else colors[seg]
                # ax.bar(x, value, width=bar_width, bottom=bottom, color=colors[seg],
                #        edgecolor='black', hatch=hatch)
                ax.bar(x, value, width=bar_width, bottom=bottom, color=bar_color, edgecolor='black', hatch=hatch)
                # ax.text(x, bottom + value / 2, f"{value:.2f}%", ha='center', va='center', fontsize=8, rotation=45)
                bottom += value

    # tick_positions = [(i * (2 * bar_width + gap) + bar_width / 2) for i in range(len(methods))]
    
    # total_group_width = 1 * bar_width + group_gap
    # tick_positions = [(i * total_group_width) + bar_width / 2 for i in range(len(methods))]
    
    total_bar_width = 1 * bar_width
    tick_positions = [(i * (total_bar_width + group_gap)) + ((total_bar_width / 2)-0.3) for i in range(len(methods))]
   
    
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(methods, fontsize=FONTSIZE)
    # ax.set_xticklabels(methods, fontsize=14, rotation=45)
    ax.set_ylim(0, 100)
    ax.tick_params(axis='y', labelsize=FONTSIZE)
    # ax.set_ylim(0, 80)
    # ax.set_ylabel("Percentage")
    ax.set_ylabel("Percentage", fontsize=FONTSIZE)
# # NASA's EOS", "MatPlotBench", "fastMRI
# Apply to each subplot
for ax, category in zip(axes, ['NASA\'s EOS', 'MatPlotBench', 'fastMRI']):
    data_subset = df_all[df_all['Dataset'] == category]
    plot_grouped_stacked(ax, data_subset)
    # ax.set_title(f"Dataset {category}")
    ax.set_title(f"{category}", fontsize=FONTSIZE)

# Create custom legend
legend_elements = []
for seg in segment_order:
    # legend_elements.append(Patch(facecolor=colors[seg], edgecolor='black', label=f'{seg} (Simple)'))
    legend_elements.append(Patch(facecolor=colors[seg], edgecolor='black', label=f'{seg}'))
# for seg in segment_order:
#     # legend_elements.append(Patch(facecolor=colors[seg], edgecolor='black', hatch=hatch_style, label=f'{seg} (Detailed)'))
#     legend_elements.append(Patch(facecolor=colors[seg][1], edgecolor='black', hatch=hatch_style, label=f'W RAG {seg}'))

# Adjust spacing
# plt.subplots_adjust(wspace=0.15, hspace=0.3, bottom=0.25)
plt.subplots_adjust(wspace=0.15, hspace=0.3, bottom=0.45)

# fig.text(0.5, 0.02, 'Iteration', ha='center', va='center', fontsize=FONTSIZE)
fig.text(0.5, 0.12, 'Iteration', ha='center', va='center', fontsize=FONTSIZE)

# Add legend below all plots
fig.legend(handles=legend_elements,
           loc='lower center',
           ncol=6,
           bbox_to_anchor=(0.5, -0.03), # (-) down, (+) up
           frameon=False,
           fontsize=FONTSIZE)

plt.tight_layout(rect=[0, 0.1, 1, 1])
path = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/graph_generation/parts_3_graphs'
plt.savefig(f'{path}/simple_query_combined_3_datasets_iterative_error_resolve.pdf', bbox_inches='tight')
plt.show()