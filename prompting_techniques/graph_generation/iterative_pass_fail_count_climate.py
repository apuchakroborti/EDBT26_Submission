import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_pass_fail_cumulative(csv_dir, target_dir, title, report_name, base_filename="file_", iterations=7, total_scripts=61):
    cumulative_pass = []
    cumulative_fail = []

    current_pass_count = 0
    current_fail_count = 0
    for i in range(iterations):
        file_path = os.path.join(csv_dir, f"{base_filename}{i}.csv")
        if not os.path.exists(file_path):
            print(f"Missing: {file_path}")
            continue

        df = pd.read_csv(file_path)

        pass_count = df['Pass Count'].sum()
        print(f'CSV pass count: {pass_count}')
        current_pass_count+=pass_count
        print(f'Current pass count: {current_pass_count}')

        fail_count = df['Fail Count'].sum()
        print(f'CSV fail count: {fail_count}')

        current_fail_count = fail_count
        print(f'Current fail count: {current_fail_count}')

        cumulative_pass.append(current_pass_count)
        cumulative_fail.append(current_fail_count)

    x_labels = [f"Step {i}" for i in range(len(cumulative_pass))]

    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(cumulative_pass))
    width = 0.35

    # Bar plots
    bars_pass = ax.bar([xi - width/2 for xi in x], cumulative_pass, width, label='Pass Count', color='green')
    bars_fail = ax.bar([xi + width/2 for xi in x], cumulative_fail, width, label='Fail Count', color='red')

    # Add text labels on top of bars
    for bar in bars_pass:
        height = bar.get_height()
        ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=9)

    for bar in bars_fail:
        height = bar.get_height()
        ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=9)

    # Labels and legend
    ax.set_ylabel("Count")
    ax.set_xlabel("Iteration Steps")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.savefig(target_dir+f'/{report_name}.pdf')
    # plt.show()

if __name__ == '__main__':
    csv_file_base_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag'

    climate_all_csv_files_sub_dir = [
        "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_corrector",
        "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_with_corrector",
        "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_without_corrector",
        "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_without_corrector",
        "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_corrector",
        "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_with_corrector",
        "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_without_corrector",
        "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_without_corrector"
    ]
    
    target_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/graph_generation'
    base_file_name ='error_categorization_report_'
    # climate
    for csv_sub_path in climate_all_csv_files_sub_dir:
        print(f'\n\n-----------------{csv_sub_path}----------------------')
        csv_dir = f'{csv_file_base_dir}/{csv_sub_path}'

        conditions = csv_sub_path.replace('devstral_24b_climate_iterative_error_resolve_python_scripts_', '').replace('_', ' ')
        
        title = f"CLIMATE datasets' Cumulative Pass/Fail Count over Iterations for devstral:24b {conditions}"
        report_name = title.replace(' ', '_').replace('/', '_').replace(':', '_').replace('\'', '' )    
        # 🔧 Example usage:
        plot_pass_fail_cumulative(csv_dir, target_dir, title, report_name, base_file_name)
    
    
    matplotagent_csv_base_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/error_categorization_evaluation_result/iterative_error_resolve'
    matplotagent_all_csv_files_sub_dir = [
       
        "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_corrector",
        "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_with_corrector",
        "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_without_corrector",
        "devstral_24b_matplotagent_iterative_python_scripts_with_rag_without_corrector",
        "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_corrector",
        "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_errors_with_corrector",
        "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_errors_without_corrector",
        "devstral_24b_matplotagent_iterative_python_scripts_without_rag_without_corrector"
    ]

    # matplotagent
    for csv_sub_path in matplotagent_all_csv_files_sub_dir:
        print(f'\n\n-----------------{csv_sub_path}----------------------')
        csv_dir = f'{matplotagent_csv_base_dir}/{csv_sub_path}'

        conditions = csv_sub_path.replace('devstral_24b_matplotagent_iterative_python_scripts_', '').replace('_', ' ')
        
        title = f"MATPLOTAGENT datasets' Cumulative Pass/Fail Count over Iterations for devstral:24b {conditions}"
        report_name = title.replace(' ', '_').replace('/', '_').replace(':', '_').replace('\'', '' )    
        # 🔧 Example usage:
        plot_pass_fail_cumulative(csv_dir, target_dir, title, report_name, base_file_name)


    fastmribrain_csv_base_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/error_categorization_evaluation_result/iterative_evaluation_results'
    fastmribrain_all_csv_files_sub_dir = [
        "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_corrector",
        "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_errors_with_corrector",
        "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_errors_without_corrector",
        "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_without_corrector",
        "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_corrector",
        "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_errors_with_corrector",
        "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_errors_without_corrector",
        "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_without_corrector"
    ]

    # # fastmribrain
    for csv_sub_path in fastmribrain_all_csv_files_sub_dir:
        print(f'\n\n-----------------{csv_sub_path}----------------------')
        csv_dir = f'{fastmribrain_csv_base_dir}/{csv_sub_path}'

        conditions = csv_sub_path.replace('devstral_24b_fastmribrain_iterative_python_scripts_', '').replace('_', ' ')
        
        title = f"FASTMRIBRAIN datasets' Cumulative Pass/Fail Count over Iterations for devstral:24b {conditions}"
        report_name = title.replace(' ', '_').replace('/', '_').replace(':', '_').replace('\'', '' )    
        # 🔧 Example usage:
        plot_pass_fail_cumulative(csv_dir, target_dir, title, report_name, base_file_name)
