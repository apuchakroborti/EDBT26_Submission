import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
import pandas as pd

def count_high_similarity(csv_path):
    df = pd.read_csv(csv_path)

    if 'Similarity Raw' not in df.columns:
        raise ValueError("'Similarity Raw' column not found in the CSV.")

    # count = (df['Similarity Raw'] > 0.85).sum()
    success_count = (df['Similarity Raw'] >= 0.85).sum()
    runnable_count = (df['Similarity Raw'] < 0.85).sum()
    fail_count_climate = 61-(success_count+runnable_count)
    print(f'Success: {success_count}, Runnable: {runnable_count}, Failed: {fail_count_climate}')
    # return success_count*100/61, runnable_count*100/61, fail_count_climate*100/61
    return success_count/61, runnable_count/61, fail_count_climate/61

project_base_directory="/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data"
        
# list_of_python_scripts_sub_dirs = ["_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector"]
sub_dir = "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector"
model = "devstral:24b"
temperature_list = [0.0, 0.2, 0.4, 0.6, 0.8]
# generated_image_directory_full_path_list = []
similarity_directory_full_path_list_dict ={}

for iteration in range(1, 6):
# for temp in temperature_list:
    # for sub_dir in list_of_python_scripts_sub_dirs:
    # for iteration in range(1, 6):
    for temp in temperature_list:

        model_name = model.replace("-", "_").replace(":", "_")
        temperature_str = str(temp).replace(".", "_")

        similarity_score_dir = f"{model_name}_single_phase_{iteration}/{model_name}_{temperature_str}{sub_dir}"
        similarity_directory_full_path_list_dict[f'Phase {iteration}-{temp}'] = similarity_score_dir


common_path = f"{project_base_directory}/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag/generated_image_from_running_evaluation/similarity_score_files"
file_name="similarity_results.csv"


score_tuples = {}
for key in similarity_directory_full_path_list_dict.keys():
    # print(f'Processing key: {key}')
    full_score_csv_path = f'{common_path}/{similarity_directory_full_path_list_dict[key]}/{file_name}'
    score_tuples[key]=count_high_similarity(full_score_csv_path)



import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal, ROUND_HALF_UP

# ----------------------------------------------------
# Generate Example Data
# ----------------------------------------------------
# models = [f"Model_{i+1}" for i in range(5)]

models = ["Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5"]
temperatures = [0.0, 0.2, 0.4, 0.6, 0.8]

data = []
for temp in temperatures:
# for model in models:
    for model in models:
#     for temp in temperatures:
        val1, val2, val3 = score_tuples[f'{model}-{temp}']
        print(f'{model}-{temp}: success: {val1}, runnable: {val2}, failed: {val3}')
        val1=round(val1, 2)
        val2=round(val2, 2)
        val3=round(val3, 2)

        # print(f'{model}-{temp}: Rounded success: {rounded_val1}, runnable: {rounded_val2}, failed: {rounded_val3}')
        print(f'{model}-{temp}: Rounded success: {val1}, runnable: {val2}, failed: {val3}')

        # data.append((model, temp, rounded_val1, rounded_val2, rounded_val3))
        data.append((model, temp, val1, val2, val3))


# ----------------------------------------------------
# Ternary to Cartesian Conversion
# ----------------------------------------------------
def ternary_to_cartesian(s, r, f):
    # Standard ternary to Cartesian formula
    x = r + 0.5 * f
    y = (np.sqrt(3)/2) * f
    return x, y


# ----------------------------------------------------
# Plot Setup
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 9))

colors = plt.cm.tab10(np.linspace(0, 1, len(models)))
markers = ["o", "s", "D", "^", "v"]


# ----------------------------------------------------
# Plot All Points
# ----------------------------------------------------
# for model_idx, model in enumerate(models):
#     for temp_idx, temp in enumerate(temperatures):
#         s, r, f = data[model_idx*5 + temp_idx][2:5]
#         # print(f'data[model_idx*5 + temp_idx][2:5]: {data[model_idx*5 + temp_idx][2:5]}')
#         # print(f'model_idx*5 + temp_idx: {model_idx*5 + temp_idx}')
#         x, y = ternary_to_cartesian(s, r, f)

#         ax.scatter(
#             x, y,
#             color=colors[model_idx],
#             marker=markers[temp_idx],
#             s=90,
#             edgecolor="black",
#             linewidth=0.5,
#             label=f"{model}, T={temp}"
#         )

# for giving the same color to the same temperature
for temp_idx, temp in enumerate(temperatures):
# for model_idx, model in enumerate(models):
    # for temp_idx, temp in enumerate(temperatures):
    for model_idx, model in enumerate(models):
        s, r, f = data[model_idx*5 + temp_idx][2:5]
        # print(f'data[model_idx*5 + temp_idx][2:5]: {data[model_idx*5 + temp_idx][2:5]}')
        # print(f'model_idx*5 + temp_idx: {model_idx*5 + temp_idx}')
        x, y = ternary_to_cartesian(s, r, f)

        ax.scatter(
            x, y,
            color=colors[model_idx],
            marker=markers[temp_idx],
            s=90,
            edgecolor="black",
            linewidth=0.5,
            # label=f"{model}, T={temp}"
            label=f"T={temp}, {model}"
        )


# ----------------------------------------------------
# Draw Triangle Outline
# ----------------------------------------------------
triangle = np.array([
    ternary_to_cartesian(1, 0, 0),   # Success
    ternary_to_cartesian(0, 1, 0),   # Runnable
    ternary_to_cartesian(0, 0, 1),   # Failed
    ternary_to_cartesian(1, 0, 0)
])
ax.plot(triangle[:, 0], triangle[:, 1], color="black", linewidth=2)


# ----------------------------------------------------
# Draw perfectly aligned ticks for all 3 faces
# ----------------------------------------------------
ticks = np.linspace(0, 1, 6)  # 0, .2, .4, .6, .8, 1

for t in ticks:
    pct = int(t * 100)

    # --- Success axis (bottom edge: S=1→0, R=t, F=0)
    xs, ys = ternary_to_cartesian(1-t, t, 0)
    ax.text(xs, ys - 0.035, f"{pct}%", ha="center", va="center", fontsize=8)

    # --- Runnable axis (right edge: R=1→0, F=t, S=0)
    xr, yr = ternary_to_cartesian(0, 1-t, t)
    ax.text(xr + 0.03, yr, f"{pct}%", ha="left", va="center", fontsize=8)

    # --- Failed axis (left edge: F=1→0, S=t, R=0)
    xf, yf = ternary_to_cartesian(t, 0, 1-t)
    ax.text(xf - 0.03, yf, f"{pct}%", ha="right", va="center", fontsize=8)


# ----------------------------------------------------
# Axis Labels
# ----------------------------------------------------
ax.text(0.5, -0.08, "Success (0–100%)", ha="center", fontsize=12)
ax.text(1.08, 0.0, "Runnable (0–100%)", ha="left", fontsize=12)
ax.text(0.5, np.sqrt(3)/2 + 0.06, "Failed (0–100%)", ha="center", fontsize=12)


# ----------------------------------------------------
# Formatting
# ----------------------------------------------------
ax.set_xlim(-0.1, 1.15)
ax.set_ylim(-0.1, 1.0)
ax.set_xticks([])
ax.set_yticks([])

# Remove duplicate legend entries
handles, labels = ax.get_legend_handles_labels()
unique = dict(zip(labels, handles))
ax.legend(unique.values(), unique.keys(), fontsize=7, bbox_to_anchor=(1.05, 1))

ax.set_title("Corrected Ternary Plot with Perfectly Aligned Tick Scales", fontsize=15)

# ----------------------------------------------------
# Save Figure
# ----------------------------------------------------

directory = "/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/graph_generation/ternary_plots_poc"
output_path = f"{directory}/edbt_simple_query_with_rag_corrector_with_different_temps.png"

plt.savefig(output_path, dpi=300, bbox_inches="tight")
print("Saved:", output_path)

plt.show()
