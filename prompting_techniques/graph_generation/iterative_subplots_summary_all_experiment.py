import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_pass_fail_subplot(ax, csv_dir, title, base_filename="error_categorization_report_", iterations=7, total_scripts=61):
    cumulative_pass = []
    cumulative_fail = []
    current_pass_count = 0

    for i in range(iterations):
        file_path = os.path.join(csv_dir, f"{base_filename}{i}.csv")
        if not os.path.exists(file_path):
            print(f"Missing: {file_path}")
            continue

        df = pd.read_csv(file_path)
        pass_count = df['Pass Count'].sum()
        current_pass_count += pass_count
        fail_count = total_scripts - current_pass_count

        cumulative_pass.append(current_pass_count)
        cumulative_fail.append(fail_count)

    x = range(len(cumulative_pass))
    width = 0.35

    # Plot pass/fail bars
    bars_pass = ax.bar([xi - width/2 for xi in x], cumulative_pass, width, label='Pass', color='green')
    bars_fail = ax.bar([xi + width/2 for xi in x], cumulative_fail, width, label='Fail', color='red')

    for bar in bars_pass + bars_fail:
        height = bar.get_height()
        ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=8)

    ax.set_title(title, fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels([f"S{i}" for i in x], fontsize=7)
    ax.tick_params(axis='y', labelsize=7)
    ax.grid(True, linestyle="--", alpha=0.3)

def climate_main():
    target_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/graph_generation'
    csv_file_base_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag'


    climate_all_csv_files_sub_dir = [
        "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_corrector",        
        "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_without_corrector",
        "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_corrector",        
        "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_without_corrector",
        "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_with_corrector",
        "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_without_corrector",
        "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_with_corrector",
        "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_without_corrector"
    ]

    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(18, 8))
    fig.suptitle("CLIMATE: Cumulative Pass/Fail Trends Across 8 Experimental Setups", fontsize=14)

    for idx, sub_dir in enumerate(climate_all_csv_files_sub_dir[:8]):  # take only first 8
        row = idx // 4
        col = idx % 4
        ax = axes[row][col]

        csv_dir = os.path.join(csv_file_base_dir, sub_dir)
        short_name = sub_dir.replace("devstral_24b_climate_iterative_error_resolve_python_scripts_", "").replace('_', ' ')
        title = f"{idx+1}) {short_name[:45]}…" if len(short_name) > 45 else f"{idx+1}) {short_name}"

        plot_pass_fail_subplot(ax, csv_dir, title, "error_categorization_report_", 7, 61)

    # Add shared legend
    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=2)

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig(f"{target_dir}/all_climate_experiments_summary.pdf")
    plt.show()

def matplotagent_main():
    target_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/graph_generation'
    matplotagent_csv_base_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/error_categorization_evaluation_result/iterative_error_resolve'


    matplotagent_all_csv_files_sub_dir = [
        "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_corrector",
        "devstral_24b_matplotagent_iterative_python_scripts_with_rag_without_corrector",
        "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_corrector",
        "devstral_24b_matplotagent_iterative_python_scripts_without_rag_without_corrector",
        "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_with_corrector",
        "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_without_corrector",
        "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_errors_with_corrector",
        "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_errors_without_corrector",
        
    ]

    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(18, 8))
    fig.suptitle("MATPLOTAGENT: Cumulative Pass/Fail Trends Across 8 Experimental Setups", fontsize=14)

    for idx, sub_dir in enumerate(matplotagent_all_csv_files_sub_dir[:8]):  # take only first 8
        row = idx // 4
        col = idx % 4
        ax = axes[row][col]

        csv_dir = os.path.join(matplotagent_csv_base_dir, sub_dir)
        short_name = sub_dir.replace("devstral_24b_matplotagent_iterative_python_scripts_", "").replace('_', ' ')
        title = f"{idx+1}) {short_name[:45]}…" if len(short_name) > 45 else f"{idx+1}) {short_name}"

        plot_pass_fail_subplot(ax, csv_dir, title, "error_categorization_report_", 7, 12)

    # Add shared legend
    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=2)

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig(f"{target_dir}/matplotagent_all_climate_experiments_summary.pdf")
    plt.show()


def fastmribrain_main():
    target_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/graph_generation'
    fastmribrain_csv_base_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/error_categorization_evaluation_result/iterative_evaluation_results'


    fastmribrain_all_csv_files_sub_dir = [
        "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_corrector",
        "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_without_corrector",
        "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_corrector",
        "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_without_corrector",
        "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_errors_with_corrector",
        "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_errors_without_corrector",
        "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_errors_with_corrector",
        "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_errors_without_corrector",
        
    ]

    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(18, 8))
    fig.suptitle("FASTMRIBRAIN: Cumulative Pass/Fail Trends Across 8 Experimental Setups", fontsize=14)

    for idx, sub_dir in enumerate(fastmribrain_all_csv_files_sub_dir[:8]):  # take only first 8
        row = idx // 4
        col = idx % 4
        ax = axes[row][col]

        csv_dir = os.path.join(fastmribrain_csv_base_dir, sub_dir)
        short_name = sub_dir.replace("devstral_24b_fastmribrain_iterative_python_scripts_", "").replace('_', ' ')
        title = f"{idx+1}) {short_name[:45]}…" if len(short_name) > 45 else f"{idx+1}) {short_name}"

        plot_pass_fail_subplot(ax, csv_dir, title, "error_categorization_report_", 7, 11)

    # Add shared legend
    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=2)

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig(f"{target_dir}/fastmribrain_all_climate_experiments_summary.pdf")
    plt.show()


if __name__ == '__main__':
    # climate_main()
    matplotagent_main()
    fastmribrain_main()
