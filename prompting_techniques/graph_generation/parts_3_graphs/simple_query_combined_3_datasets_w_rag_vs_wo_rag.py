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

project_base_directory = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
climate_csv_dir = f'{project_base_directory}/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag'
list_of_python_scripts_sub_dirs_for_climate = [
            "devstral_24b_python_scripts_without_rag_with_errors_with_corrector",
            "devstral_24b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector",

            "magicoder_python_scripts_without_rag_with_errors_with_corrector",
            "magicoder_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector",

            "llama3_70b_python_scripts_without_rag_with_errors_with_corrector",
            "llama3_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector",

            "gemma3_27b_python_scripts_without_rag_with_errors_with_corrector",
            "gemma3_27b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector",
            
            "deepseek_r1_32b_python_scripts_without_rag_with_errors_with_corrector",
            "deepseek_r1_32b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector",
            ]
models = [
            "devstral_24b",
            "devstral_24b",

            "magicoder",
            "magicoder",

            "llama3_70b",
            "llama3_70b",

            "gemma3_27b",
            "gemma3_27b",

            "deepseek_r1_32b",
            "deepseek_r1_32b",
            ]
import os
categories = ['']
csv_file_basename = 'error_categorization_report'
correct_runnable_csv_file_basename = 'similarity_results_'

models_category_simple_q_in_percentage = []
models_category_expert_q_in_percentage = []
for i in range(0, 10, 2):
    print(f'\n\Model-------{models[i]}')
    # iteration_pass_fail = {'Pass': [], 'Fail': [], 'Correct': []}
    simple_iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': [], 'Correct': []}
    # category 2
    # file_path = os.path.join(climate_csv_dir, f"{matplotagent_all_csv_files_sub_dir[0]}/{csv_file_basename}{i}.csv")
    file_path = os.path.join(climate_csv_dir, f"{list_of_python_scripts_sub_dirs_for_climate[i]}/{csv_file_basename}.csv")
    if not os.path.exists(file_path):
        print(f"Missing: {file_path}")
        continue
    df = pd.read_csv(file_path)
    pass_count = df['Pass Count'].sum()
    print(f'Climate CSV pass count: {pass_count}')
    
    fail_count = df['Fail Count'].sum()
    print(f'Climate CSV fail count: {fail_count}')

    # read correct and runnable scripts
    correct_runnable_file_path = os.path.join(climate_csv_dir, f"{list_of_python_scripts_sub_dirs_for_climate[i]}/{correct_runnable_csv_file_basename}.csv")
    if not os.path.exists(correct_runnable_file_path):
        print(f"Missing correct_runnable_file_path: {correct_runnable_file_path}")
        continue
    # correct_runnable_file_path_df = pd.read_csv(correct_runnable_file_path)

    correct_count = count_high_similarity(correct_runnable_file_path)
    print(f'Climate CSV Correct count: {correct_count}')

    simple_iteration_pass_fail_in_percentage['Correct'].append((correct_count*100)/61)

    pass_count = pass_count - correct_count
    print(f'Climate CSV actual pass count: {pass_count}\n\n')
    simple_iteration_pass_fail_in_percentage['Pass'].append((pass_count*100)/61)
    simple_iteration_pass_fail_in_percentage['Fail'].append((fail_count*100)/61)
    
    models_category_simple_q_in_percentage.append(simple_iteration_pass_fail_in_percentage)

    # expert
    expert_iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': [], 'Correct': []}
    # category 2
    # file_path = os.path.join(climate_csv_dir, f"{matplotagent_all_csv_files_sub_dir[0]}/{csv_file_basename}{i}.csv")
    file_path = os.path.join(climate_csv_dir, f"{list_of_python_scripts_sub_dirs_for_climate[i+1]}/{csv_file_basename}.csv")
    if not os.path.exists(file_path):
        print(f"Missing: {file_path}")
        continue
    df = pd.read_csv(file_path)
    pass_count = df['Pass Count'].sum()
    print(f'Climate CSV pass count: {pass_count}')
    
    fail_count = df['Fail Count'].sum()
    print(f'Climate CSV fail count: {fail_count}')

    # read correct and runnable scripts
    correct_runnable_file_path = os.path.join(climate_csv_dir, f"{list_of_python_scripts_sub_dirs_for_climate[i+1]}/{correct_runnable_csv_file_basename}.csv")
    if not os.path.exists(correct_runnable_file_path):
        print(f"Missing correct_runnable_file_path: {correct_runnable_file_path}")
        continue
    correct_runnable_file_path_df = pd.read_csv(correct_runnable_file_path)
    correct_count = count_high_similarity(correct_runnable_file_path)
    print(f'Climate CSV Correct count: {correct_count}')

    expert_iteration_pass_fail_in_percentage['Correct'].append((correct_count*100)/61)

    pass_count = pass_count - correct_count
    print(f'Climate CSV actual pass count: {pass_count}\n\n')
    expert_iteration_pass_fail_in_percentage['Pass'].append((pass_count*100)/61)
    expert_iteration_pass_fail_in_percentage['Fail'].append((fail_count*100)/61)
    
    models_category_expert_q_in_percentage.append(expert_iteration_pass_fail_in_percentage)

# models_category_simple_q_in_percentage = []
# models_category_expert_q_in_percentage = []
print(f'Size of models_category_simple_q_in_percentage: {len(models_category_simple_q_in_percentage)}')
print(f'Size of models_category_expert_q_in_percentage: {len(models_category_expert_q_in_percentage)}')


# -----------------------MATPLOTAGENT---------------------

matplotagent_csv_dir = f'{project_base_directory}/matplot_agent_data/plot_generation/error_categorization_evaluation_result/llm_generated_code_with_rag'
list_of_python_scripts_sub_dirs_for_matplotagent = [
            "devstral_24b_matplotagent_python_scripts_without_rag_with_errors_with_corrector",
            "devstral_24b_matplotagent_python_scripts_with_rag_with_errors_with_corrector",

            "magicoder_matplotagent_python_scripts_without_rag_with_errors_with_corrector",
            "magicoder_matplotagent_python_scripts_with_rag_with_errors_with_corrector",
            
            "llama3_70b_matplotagent_python_scripts_without_rag_with_errors_with_corrector",
            "llama3_70b_matplotagent_python_scripts_with_rag_with_errors_with_corrector",
            
            "gemma3_27b_matplotagent_python_scripts_without_rag_with_errors_with_corrector",
            "gemma3_27b_matplotagent_python_scripts_with_rag_with_errors_with_corrector",

            "deepseek_r1_32b_matplotagent_python_scripts_without_rag_with_errors_with_corrector",
            "deepseek_r1_32b_matplotagent_python_scripts_with_rag_with_errors_with_corrector",

            ]

m_models_category_simple_q_in_percentage = []
m_models_category_expert_q_in_percentage = []
for i in range(0, 10, 2):
    print(f'\n\Model-------{models[i]}')
    # iteration_pass_fail = {'Pass': [], 'Fail': [], 'Correct': []}
    simple_iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': [], 'Correct': []}
    # category 2
    # file_path = os.path.join(climate_csv_dir, f"{matplotagent_all_csv_files_sub_dir[0]}/{csv_file_basename}{i}.csv")
    file_path = os.path.join(matplotagent_csv_dir, f"{list_of_python_scripts_sub_dirs_for_matplotagent[i]}/{csv_file_basename}.csv")
    if not os.path.exists(file_path):
        print(f"Missing: {file_path}")
        continue
    df = pd.read_csv(file_path)
    pass_count = df['Pass Count'].sum()
    print(f'Matplotagent CSV pass count: {pass_count}')
    
    fail_count = df['Fail Count'].sum()
    print(f'Matplotagent CSV fail count: {fail_count}')

    # read correct and runnable scripts
    correct_runnable_file_path = os.path.join(matplotagent_csv_dir, f"{list_of_python_scripts_sub_dirs_for_matplotagent[i]}/{correct_runnable_csv_file_basename}.csv")
    if not os.path.exists(correct_runnable_file_path):
        print(f"Missing correct_runnable_file_path: {correct_runnable_file_path}")
        continue
    # correct_runnable_file_path_df = pd.read_csv(correct_runnable_file_path)

    correct_count = count_high_similarity(correct_runnable_file_path)
    print(f'Matplotagent CSV Correct count: {correct_count}')

    simple_iteration_pass_fail_in_percentage['Correct'].append((correct_count*100)/12)

    pass_count = pass_count - correct_count
    print(f'Matplotagent CSV actual pass count: {pass_count}\n\n')
    simple_iteration_pass_fail_in_percentage['Pass'].append((pass_count*100)/12)
    simple_iteration_pass_fail_in_percentage['Fail'].append((fail_count*100)/12)
    
    m_models_category_simple_q_in_percentage.append(simple_iteration_pass_fail_in_percentage)

    # expert
    expert_iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': [], 'Correct': []}
    # category 2
    # file_path = os.path.join(climate_csv_dir, f"{matplotagent_all_csv_files_sub_dir[0]}/{csv_file_basename}{i}.csv")
    file_path = os.path.join(matplotagent_csv_dir, f"{list_of_python_scripts_sub_dirs_for_matplotagent[i+1]}/{csv_file_basename}.csv")
    if not os.path.exists(file_path):
        print(f"Missing: {file_path}")
        continue
    df = pd.read_csv(file_path)
    pass_count = df['Pass Count'].sum()
    print(f'Matplotagent CSV pass count: {pass_count}')
    
    fail_count = df['Fail Count'].sum()
    print(f'Matplotagent CSV fail count: {fail_count}')

    # read correct and runnable scripts
    correct_runnable_file_path = os.path.join(matplotagent_csv_dir, f"{list_of_python_scripts_sub_dirs_for_matplotagent[i+1]}/{correct_runnable_csv_file_basename}.csv")
    if not os.path.exists(correct_runnable_file_path):
        print(f"Missing correct_runnable_file_path: {correct_runnable_file_path}")
        continue
    correct_runnable_file_path_df = pd.read_csv(correct_runnable_file_path)
    
    correct_count = count_high_similarity(correct_runnable_file_path)
    print(f'Matplotagent CSV Correct count: {correct_count}')
    expert_iteration_pass_fail_in_percentage['Correct'].append((correct_count*100)/12)

    pass_count = pass_count - correct_count
    print(f'Matplotagent CSV actual pass count: {pass_count}\n\n')
    expert_iteration_pass_fail_in_percentage['Pass'].append((pass_count*100)/12)
    expert_iteration_pass_fail_in_percentage['Fail'].append((fail_count*100)/12)
    
    m_models_category_expert_q_in_percentage.append(expert_iteration_pass_fail_in_percentage)



# -----------FASTMRIBRAIN------------
fastmribrain_csv_dir = f'{project_base_directory}/mri_nyu_data/error_categorization_evaluation_result/llm_generated_code_with_rag'
list_of_python_scripts_sub_dirs_for_fastmribrain = [          
           "devstral_24b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector",
            "devstral_24b_fastmribrain_python_scripts_with_rag_with_errors_with_corrector",

            "magicoder_fastmribrain_python_scripts_without_rag_with_errors_with_corrector",
            "magicoder_fastmribrain_python_scripts_with_rag_with_errors_with_corrector",

            "llama3_70b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector",
            "llama3_70b_fastmribrain_python_scripts_with_rag_with_errors_with_corrector",

            "gemma3_27b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector",
            "gemma3_27b_fastmribrain_python_scripts_with_rag_with_errors_with_corrector",

            "deepseek_r1_32b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector",
            "deepseek_r1_32b_fastmribrain_python_scripts_with_rag_with_errors_with_corrector",          
            ]

f_models_category_simple_q_in_percentage = []
f_models_category_expert_q_in_percentage = []
for i in range(0, 10, 2):
    print(f'\n\Model-------{models[i]}')
    # iteration_pass_fail = {'Pass': [], 'Fail': [], 'Correct': []}
    simple_iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': [], 'Correct': []}
    # category 2
    # file_path = os.path.join(climate_csv_dir, f"{matplotagent_all_csv_files_sub_dir[0]}/{csv_file_basename}{i}.csv")
    file_path = os.path.join(fastmribrain_csv_dir, f"{list_of_python_scripts_sub_dirs_for_fastmribrain[i]}/{csv_file_basename}.csv")
    if not os.path.exists(file_path):
        print(f"Missing: {file_path}")
        continue
    df = pd.read_csv(file_path)
    pass_count = df['Pass Count'].sum()
    print(f'Fastmribrain CSV pass count: {pass_count}')
    
    fail_count = df['Fail Count'].sum()
    print(f'Fastmribrain CSV fail count: {fail_count}')

    # read correct and runnable scripts
    correct_runnable_file_path = os.path.join(fastmribrain_csv_dir, f"{list_of_python_scripts_sub_dirs_for_fastmribrain[i]}/{correct_runnable_csv_file_basename}.csv")
    if not os.path.exists(correct_runnable_file_path):
        print(f"Missing correct_runnable_file_path: {correct_runnable_file_path}")
        continue
    # correct_runnable_file_path_df = pd.read_csv(correct_runnable_file_path)

    correct_count = count_high_similarity(correct_runnable_file_path)
    print(f'Fastmribrain CSV Correct count: {correct_count}')

    simple_iteration_pass_fail_in_percentage['Correct'].append((correct_count*100)/11)

    pass_count = pass_count - correct_count
    print(f'Fastmribrain CSV actual pass count: {pass_count}\n\n')
    simple_iteration_pass_fail_in_percentage['Pass'].append((pass_count*100)/11)
    simple_iteration_pass_fail_in_percentage['Fail'].append((fail_count*100)/11)
    
    f_models_category_simple_q_in_percentage.append(simple_iteration_pass_fail_in_percentage)

    # expert
    expert_iteration_pass_fail_in_percentage = {'Pass': [], 'Fail': [], 'Correct': []}
    # category 2
    # file_path = os.path.join(climate_csv_dir, f"{matplotagent_all_csv_files_sub_dir[0]}/{csv_file_basename}{i}.csv")
    file_path = os.path.join(fastmribrain_csv_dir, f"{list_of_python_scripts_sub_dirs_for_fastmribrain[i+1]}/{csv_file_basename}.csv")
    if not os.path.exists(file_path):
        print(f"Missing: {file_path}")
        continue
    df = pd.read_csv(file_path)
    pass_count = df['Pass Count'].sum()
    print(f'Fastmribrain CSV pass count: {pass_count}')
    
    fail_count = df['Fail Count'].sum()
    print(f'Fastmribrain CSV fail count: {fail_count}')

    # read correct and runnable scripts
    correct_runnable_file_path = os.path.join(fastmribrain_csv_dir, f"{list_of_python_scripts_sub_dirs_for_fastmribrain[i+1]}/{correct_runnable_csv_file_basename}.csv")
    if not os.path.exists(correct_runnable_file_path):
        print(f"Missing correct_runnable_file_path: {correct_runnable_file_path}")
        continue
    correct_runnable_file_path_df = pd.read_csv(correct_runnable_file_path)
    correct_count = count_high_similarity(correct_runnable_file_path)
    print(f'Fastmribrain CSV Correct count: {correct_count}')

    expert_iteration_pass_fail_in_percentage['Correct'].append((correct_count*100)/11)

    pass_count = pass_count - correct_count
    print(f'Fastmribrain CSV actual pass count: {pass_count}\n\n')
    expert_iteration_pass_fail_in_percentage['Pass'].append((pass_count*100)/11)
    expert_iteration_pass_fail_in_percentage['Fail'].append((fail_count*100)/11)
    
    f_models_category_expert_q_in_percentage.append(expert_iteration_pass_fail_in_percentage)


# Set style
sns.set(style="whitegrid")

def make_df(category, green1, blue1, red1, green2, blue2, red2):
    methods = ['M1', 'M2', 'M3', 'M4', 'M5']
    data = []
    for i, method in enumerate(methods):
        data.append({
            'Method': method,
            'Run': 'W/O RAG',
            'Correct': green1[i],
            'Runnable': blue1[i],
            'Failed': red1[i],
            'Dataset': category
        })
        data.append({
            'Method': method,
            'Run': 'W RAG',
            'Correct': green2[i],
            'Runnable': blue2[i],
            'Failed': red2[i],
            'Dataset': category
        })
    return pd.DataFrame(data)

# climate
s_correct = [
    models_category_simple_q_in_percentage[0]['Correct'][0],
    models_category_simple_q_in_percentage[1]['Correct'][0],
    models_category_simple_q_in_percentage[2]['Correct'][0],
    models_category_simple_q_in_percentage[3]['Correct'][0],
    models_category_simple_q_in_percentage[4]['Correct'][0],
             ]
d_correct = [
    models_category_expert_q_in_percentage[0]['Correct'][0],
    models_category_expert_q_in_percentage[1]['Correct'][0],
    models_category_expert_q_in_percentage[2]['Correct'][0],
    models_category_expert_q_in_percentage[3]['Correct'][0],
    models_category_expert_q_in_percentage[4]['Correct'][0],
]

s_runnable = [
    models_category_simple_q_in_percentage[0]['Pass'][0],
    models_category_simple_q_in_percentage[1]['Pass'][0],
    models_category_simple_q_in_percentage[2]['Pass'][0],
    models_category_simple_q_in_percentage[3]['Pass'][0],
    models_category_simple_q_in_percentage[4]['Pass'][0],
]
d_runnable = [
    models_category_expert_q_in_percentage[0]['Pass'][0],
    models_category_expert_q_in_percentage[1]['Pass'][0],
    models_category_expert_q_in_percentage[2]['Pass'][0],
    models_category_expert_q_in_percentage[3]['Pass'][0],
    models_category_expert_q_in_percentage[4]['Pass'][0],
]

s_failed = [
    models_category_simple_q_in_percentage[0]['Fail'][0],
    models_category_simple_q_in_percentage[1]['Fail'][0],
    models_category_simple_q_in_percentage[2]['Fail'][0],
    models_category_simple_q_in_percentage[3]['Fail'][0],
    models_category_simple_q_in_percentage[4]['Fail'][0],
]
d_failed = [
    models_category_expert_q_in_percentage[0]['Fail'][0],
    models_category_expert_q_in_percentage[1]['Fail'][0],
    models_category_expert_q_in_percentage[2]['Fail'][0],
    models_category_expert_q_in_percentage[3]['Fail'][0],
    models_category_expert_q_in_percentage[4]['Fail'][0],
]

# matplotagent
m_s_correct = [m_models_category_simple_q_in_percentage[0]['Correct'][0],
    m_models_category_simple_q_in_percentage[1]['Correct'][0],
    m_models_category_simple_q_in_percentage[2]['Correct'][0],
    m_models_category_simple_q_in_percentage[3]['Correct'][0],
    m_models_category_simple_q_in_percentage[4]['Correct'][0],]
m_d_correct = [m_models_category_expert_q_in_percentage[0]['Correct'][0],
    m_models_category_expert_q_in_percentage[1]['Correct'][0],
    m_models_category_expert_q_in_percentage[2]['Correct'][0],
    m_models_category_expert_q_in_percentage[3]['Correct'][0],
    m_models_category_expert_q_in_percentage[4]['Correct'][0],]

m_s_runnable = [m_models_category_simple_q_in_percentage[0]['Pass'][0],
    m_models_category_simple_q_in_percentage[1]['Pass'][0],
    m_models_category_simple_q_in_percentage[2]['Pass'][0],
    m_models_category_simple_q_in_percentage[3]['Pass'][0],
    m_models_category_simple_q_in_percentage[4]['Pass'][0],]
m_d_runnable = [m_models_category_expert_q_in_percentage[0]['Pass'][0],
    m_models_category_expert_q_in_percentage[1]['Pass'][0],
    m_models_category_expert_q_in_percentage[2]['Pass'][0],
    m_models_category_expert_q_in_percentage[3]['Pass'][0],
    m_models_category_expert_q_in_percentage[4]['Pass'][0],]

m_s_failed = [ m_models_category_simple_q_in_percentage[0]['Fail'][0],
    m_models_category_simple_q_in_percentage[1]['Fail'][0],
    m_models_category_simple_q_in_percentage[2]['Fail'][0],
    m_models_category_simple_q_in_percentage[3]['Fail'][0],
    m_models_category_simple_q_in_percentage[4]['Fail'][0],]
m_d_failed = [m_models_category_expert_q_in_percentage[0]['Fail'][0],
    m_models_category_expert_q_in_percentage[1]['Fail'][0],
    m_models_category_expert_q_in_percentage[2]['Fail'][0],
    m_models_category_expert_q_in_percentage[3]['Fail'][0],
    m_models_category_expert_q_in_percentage[4]['Fail'][0],]

# fastmribrain
f_s_correct = [f_models_category_simple_q_in_percentage[0]['Correct'][0],
    f_models_category_simple_q_in_percentage[1]['Correct'][0],
    f_models_category_simple_q_in_percentage[2]['Correct'][0],
    f_models_category_simple_q_in_percentage[3]['Correct'][0],
    f_models_category_simple_q_in_percentage[4]['Correct'][0],]
f_d_correct = [f_models_category_expert_q_in_percentage[0]['Correct'][0],
    f_models_category_expert_q_in_percentage[1]['Correct'][0],
    f_models_category_expert_q_in_percentage[2]['Correct'][0],
    f_models_category_expert_q_in_percentage[3]['Correct'][0],
    f_models_category_expert_q_in_percentage[4]['Correct'][0],]

f_s_runnable = [f_models_category_simple_q_in_percentage[0]['Pass'][0],
    f_models_category_simple_q_in_percentage[1]['Pass'][0],
    f_models_category_simple_q_in_percentage[2]['Pass'][0],
    f_models_category_simple_q_in_percentage[3]['Pass'][0],
    f_models_category_simple_q_in_percentage[4]['Pass'][0],]

f_d_runnable = [f_models_category_expert_q_in_percentage[0]['Pass'][0],
    f_models_category_expert_q_in_percentage[1]['Pass'][0],
    f_models_category_expert_q_in_percentage[2]['Pass'][0],
    f_models_category_expert_q_in_percentage[3]['Pass'][0],
    f_models_category_expert_q_in_percentage[4]['Pass'][0],]

f_s_failed = [ f_models_category_simple_q_in_percentage[0]['Fail'][0],
    f_models_category_simple_q_in_percentage[1]['Fail'][0],
    f_models_category_simple_q_in_percentage[2]['Fail'][0],
    f_models_category_simple_q_in_percentage[3]['Fail'][0],
    f_models_category_simple_q_in_percentage[4]['Fail'][0],]

f_d_failed = [f_models_category_expert_q_in_percentage[0]['Fail'][0],
    f_models_category_expert_q_in_percentage[1]['Fail'][0],
    f_models_category_expert_q_in_percentage[2]['Fail'][0],
    f_models_category_expert_q_in_percentage[3]['Fail'][0],
    f_models_category_expert_q_in_percentage[4]['Fail'][0],]
# # NASA's EOS", "MatPlotBench", "fastMRI
df_A = make_df(
    'NASA\'s EOS',
    green1=s_correct, blue1=s_runnable, red1=s_failed,
    green2=d_correct, blue2=d_runnable, red2=d_failed
)

df_B = make_df(
    'MatPlotBench',
    green1=m_s_correct, blue1=m_s_runnable, red1=m_s_failed,
    green2=m_d_correct, blue2=m_d_runnable, red2=m_d_failed
)

df_C = make_df(
    'fastMRI',
    green1=f_s_correct, blue1=f_s_runnable, red1=f_s_failed,
    green2=f_d_correct, blue2=f_d_runnable, red2=f_d_failed
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
    'Correct': ['#58D68D', '#A9DFBF', ],     # , bright sea green, light mint green
    'Runnable': ['#5DADE2', '#AED6F1', ],    # , moderate blue, light sky blue
    'Failed': ['#EC7063', '#F5B7B1', ]       # , strong coral red, light salmon pink
}

hatch_style = '/'  # hatch for second bar

# Create figure and axes manually for better layout control
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
# fig, axes = plt.subplots(1, 3, figsize=(10, 6), sharey=True)
FONTSIZE = 26
# Plotting function
def plot_grouped_stacked(ax, data):
    methods = ['M1', 'M2', 'M3', 'M4', 'M5']
    # methods = ['devstral:24b', 'magicoder', 'llama3:70b', 'gemma3:27b', 'deepseek-r1:70b']
    # bar_width = 0.35
    bar_width = 0.45
    gap = 0.2

    for i, method in enumerate(methods):
        for j, run in enumerate(['W/O RAG', 'W RAG']):
            subset = data[(data['Method'] == method) & (data['Run'] == run)]
            if subset.empty:
                continue
            x = i * (2 * bar_width + gap) + j * bar_width
            bottom = 0
            for seg in segment_order:
                value = subset[seg].values[0]
                if value == 0:
                    continue
                hatch = hatch_style if run == 'W RAG' else None
                bar_color = colors[seg][1] if run == 'W RAG' else colors[seg][0]
                # ax.bar(x, value, width=bar_width, bottom=bottom, color=colors[seg],
                #        edgecolor='black', hatch=hatch)
                ax.bar(x, value, width=bar_width, bottom=bottom, color=bar_color,
                       edgecolor='black', hatch=hatch)
                # ax.text(x, bottom + value / 2, f"{value:.2f}%", ha='center', va='center', fontsize=8, rotation=45)
                bottom += value

    tick_positions = [(i * (2 * bar_width + gap) + bar_width / 2) for i in range(len(methods))]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(methods, fontsize=FONTSIZE)
    # ax.set_xticklabels(methods, fontsize=14, rotation=45)
    ax.set_ylim(0, 100)
    ax.tick_params(axis='y', labelsize=FONTSIZE)
    # ax.set_ylim(0, 80)
    ax.set_ylabel("Percentage",  fontsize=FONTSIZE)
# # NASA's EOS", "MatPlotBench", "fastMRI
# Apply to each subplot
for ax, category in zip(axes, ['NASA\'s EOS', 'MatPlotBench', 'fastMRI']):
    data_subset = df_all[df_all['Dataset'] == category]
    plot_grouped_stacked(ax, data_subset)
    ax.set_title(f"{category}", fontsize=FONTSIZE)

# Create custom legend
legend_elements = []
for seg in segment_order:
    # legend_elements.append(Patch(facecolor=colors[seg], edgecolor='black', label=f'{seg} (Simple)'))
    legend_elements.append(Patch(facecolor=colors[seg][0], edgecolor='black', label=f'W/O RAG {seg}'))
for seg in segment_order:
    # legend_elements.append(Patch(facecolor=colors[seg], edgecolor='black', hatch=hatch_style, label=f'{seg} (Detailed)'))
    legend_elements.append(Patch(facecolor=colors[seg][1], edgecolor='black', hatch=hatch_style, label=f'W RAG {seg}'))

# legend_elements.append(Patch(facecolor=colors['Correct'][0], edgecolor='black', label=f'W/O RAG Correct'))
# legend_elements.append(Patch(facecolor=colors['Runnable'][0], edgecolor='black', label=f'W/O RAG Runnable'))
# legend_elements.append(Patch(facecolor=colors['Failed'][0], edgecolor='black', label=f'W/O RAG Failed'))

# legend_elements.append(Patch(facecolor=colors['Correct'][1], edgecolor='black', hatch=hatch_style, label=f'W RAG Correct'))
# legend_elements.append(Patch(facecolor=colors['Runnable'][1], edgecolor='black', hatch=hatch_style, label=f'W RAG Runnable'))
# legend_elements.append(Patch(facecolor=colors['Failed'][1], edgecolor='black', hatch=hatch_style, label=f'W RAG Failed'))



# Adjust spacing
# plt.subplots_adjust(wspace=0.15, hspace=0.3, bottom=0.25)
plt.subplots_adjust(wspace=0.15, hspace=0.3, bottom=0.45)

# Add legend below all plots
# fig.legend(handles=legend_elements,
#            loc='lower center',
#            ncol=3,
#         #    bbox_to_anchor=(0.5, 0.02),
#            bbox_to_anchor=(0.5, -0.12),#(-) down, (+) up
#            frameon=False,
#            fontsize=FONTSIZE)
# Define your desired label order
desired_order = [
    'W/O RAG Correct', 'W RAG Correct', 'W/O RAG Runnable',  'W RAG Runnable', 'W/O RAG Failed',  'W RAG Failed',
]
# Map from label to the original legend element (e.g., Patch)
label_to_element = {le.get_label(): le for le in legend_elements}

# Sort or reorder
sorted_legend_elements = [label_to_element[label] for label in desired_order]

# Apply fig.legend with sorted elements
fig.legend(
    handles=sorted_legend_elements,
    loc='lower center',
    ncol=3,
    bbox_to_anchor=(0.5, -0.12),  # Adjust this as needed
    frameon=False,
    fontsize=FONTSIZE
)


plt.tight_layout(rect=[0, 0.1, 1, 1])
path = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/graph_generation/parts_3_graphs'
plt.savefig(f'{path}/simple_query_combined_3_datasets_w_rag_vs_wo_rag.pdf', bbox_inches='tight')
plt.show()