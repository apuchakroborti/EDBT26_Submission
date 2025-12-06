import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
import pandas as pd

def count_high_similarity(csv_path, key):
    df = pd.read_csv(csv_path)

    if 'Similarity Raw' not in df.columns:
        raise ValueError("'Similarity Raw' column not found in the CSV.")

    # count = (df['Similarity Raw'] > 0.85).sum()
    success_count = (df['Similarity Raw'] >= 0.85).sum()
    runnable_count = (df['Similarity Raw'] < 0.85).sum()
    fail_count_climate = 61-(success_count+runnable_count)
    # print(f'Success: {success_count}, Runnable: {runnable_count}, Failed: {fail_count_climate}')
    # return success_count*100/61, runnable_count*100/61, fail_count_climate*100/61
    print(f'Percentage--> {key}:: Success: {success_count/61}, Runnable: {runnable_count/61}, Failed: {fail_count_climate/61}')
    # print(f'Percentage--> {key}:: Success: {success_count*100/61}, Runnable: {runnable_count*100/61}, Failed: {fail_count_climate*100/61}')
    return success_count/61, runnable_count/61, fail_count_climate/61

project_base_directory="/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data"
        
# list_of_python_scripts_sub_dirs = ["_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector"]
sub_dir = "_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector"
model = "devstral:24b"
temperature_list = [0.0, 0.2, 0.4, 0.6, 0.8]
# generated_image_directory_full_path_list = []
similarity_directory_full_path_list_dict ={}

# for iteration in range(1, 6):
for temp in temperature_list:
    # for sub_dir in list_of_python_scripts_sub_dirs:
    for iteration in range(1, 6):
    # for temp in temperature_list:

        model_name = model.replace("-", "_").replace(":", "_")
        temperature_str = str(temp).replace(".", "_")

        similarity_score_dir = f"{model_name}_single_phase_{iteration}/{model_name}_{temperature_str}{sub_dir}"
        similarity_directory_full_path_list_dict[f'Phase {iteration}-{temp}'] = similarity_score_dir


common_path = f"{project_base_directory}/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag/generated_image_from_running_evaluation/similarity_score_files"
file_name="similarity_results.csv"

points = []
score_tuples = {}
point_lables = []
for key in similarity_directory_full_path_list_dict.keys():
    # print(f'Processing key: {key}')
    full_score_csv_path = f'{common_path}/{similarity_directory_full_path_list_dict[key]}/{file_name}'
    score_tuples[key]=count_high_similarity(full_score_csv_path, key)
    points.append(score_tuples[key])
    point_lables.append(key)



import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal, ROUND_HALF_UP

# ----------------------------------------------------
# Generate Example Data
# ----------------------------------------------------
# models = [f"Model_{i+1}" for i in range(5)]

models = ["Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5"]
temperatures = [0.0, 0.2, 0.4, 0.6, 0.8]



# start version 2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ArrowStyle, FancyArrowPatch
import mpltern  # noqa: F401

# ------------------------------------------------------------------
# Create subplot with ternary projection
# ------------------------------------------------------------------
ax = plt.subplot(projection='ternary')

# ------------------------------------------------------------------
# Arrow decorations (kept from your provided code)
# ------------------------------------------------------------------
arrowstyle = ArrowStyle('simple', head_length=10, head_width=5)
kwargs_arrow = {
    'transform': ax.transAxes,      # Used with ``ax.transAxesProjection``
    'arrowstyle': arrowstyle,
    'linewidth': 1,
    'clip_on': False,
    'zorder': -10,
}

# Start and end points for arrows (barycentric coords)
ta = np.array([0.00, -0.20, 1.20])   # moved further out
tb = np.array([1.00, -0.20, 0.20])

la = np.array([1.20, 0.00, -0.20])
lb = np.array([0.20, 1.00, -0.20])

ra = np.array([-0.20, 1.20, 0.00])
rb = np.array([-0.20, 0.20, 1.00])

f = ax.transAxesProjection.transform

tarrow = FancyArrowPatch(f(ta), f(tb), ec='C2', fc='C2', **kwargs_arrow)
larrow = FancyArrowPatch(f(la), f(lb), ec='C0', fc='C0', **kwargs_arrow)
rarrow = FancyArrowPatch(f(ra), f(rb), ec='r', fc='r', **kwargs_arrow)

ax.add_patch(tarrow)
ax.add_patch(larrow)
ax.add_patch(rarrow)

# ------------------------------------------------------------------
# Axis labels placed consistent with arrows
# ------------------------------------------------------------------
kwargs_label = {
    'transform': ax.transTernaryAxes,
    'backgroundcolor': 'w',
    'ha': 'center',
    'va': 'center',
    'rotation_mode': 'anchor',
    'zorder': -9,
}
tpos = (ta + tb) * 0.5
lpos = (la + lb) * 0.5
rpos = (ra + rb) * 0.5

ax.text(*tpos, 'Correct',  color='C2', fontsize=16, rotation=-60, **kwargs_label)   # top
ax.text(*lpos, 'Runnable', color='C0', fontsize=16, rotation= 60, **kwargs_label)   # left
ax.text(*rpos, 'Failed', color='r', fontsize=16, rotation= 0,  **kwargs_label)  # right

# ------------------------------------------------------------------
# Generate 25 sample ternary points (each row sums to 1)
# ------------------------------------------------------------------
# np.random.seed(42)
# points = np.random.dirichlet(alpha=[1.0, 1.0, 1.0], size=25)  # shape (25,3)

# Column order = [Success, Runnable, Failed]

# ------------------------------------------------------------------
# Colors (non-deprecated)
# ------------------------------------------------------------------
group_colors = plt.get_cmap('Accent')(np.linspace(0, 1, 5))

# ------------------------------------------------------------------
# Scatter the points on the ternary axes
# ------------------------------------------------------------------
for i, (s, r, f_val) in enumerate(points, start=1):
    color = group_colors[(i - 1) // 5]
    ax.scatter(s, r, f_val,
            #    s=120 → big circles, s=50 → medium, s=20 → small,  s=8 → very small
               s=10,
            #    color=colors[i-1],
               color=color,
               edgecolor='k',
            linewidth=0.6,
               zorder=10

               )

    # Optional: label each point (index). Replace with percentages if you prefer.
    # ax.text(s, r, f_val, str(i),
    #         fontsize=7,
    #         ha='center', va='center',
    #         color='white',
    #         zorder=11,
    #         weight='bold')

# ------------------------------------------------------------------
# Grid, title and axis labels
# ------------------------------------------------------------------
ax.grid(True, linestyle='--', alpha=0.3)
# ax.set_title('Ternary Plot — Success / Runnable / Failed (25 points)', fontsize=14)
# ax.set_title('Ternary Plot — Success / Runnable / Failed', fontsize=20)

# ax.set_tlabel('Failed (%)')
# ax.set_llabel('Success (%)')
# ax.set_rlabel('Runnable (%)')

# ------------------------------------------------------------------
# Correct tick handling using axis objects (taxis, laxis, raxis)
# ------------------------------------------------------------------
ticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
ticklabels = [f"{int(t*100)}%" for t in ticks]

# set ticks
ax.taxis.set_ticks(ticks)
ax.laxis.set_ticks(ticks)
ax.raxis.set_ticks(ticks)

# set labels for ticks (optional)
ax.taxis.set_ticklabels(ticklabels)
ax.laxis.set_ticklabels(ticklabels)
ax.raxis.set_ticklabels(ticklabels)

# style tick labels a bit (optional)
for axis in (ax.taxis, ax.laxis, ax.raxis):
    for lbl in axis.get_ticklabels():
        # lbl.set_fontsize(8)
        lbl.set_fontsize(14)


# ------------------------------------------------------------------
# Create right-side index labels (same color as scatter)
# ------------------------------------------------------------------
from matplotlib import transforms

fig = plt.gcf()

# for the legend
# Create a new axis on the right side for labels
# label_ax = fig.add_axes([0.82, 0.1, 0.15, 0.8])  # (left, bottom, width, height)

# label_ax = fig.add_axes([0.90, 0.1, 0.15, 0.8])  # (left, bottom, width, height)
# label_ax.axis("off")


# label_ax.set_title("Point Index", fontsize=12, pad=10)

# version 2 code for the legend
# Line 1: Temp-1, Temp-2, Temp-3
# We will draw a colored dot and then the label next to it.
legend_ax = fig.add_axes([0.1, 0.95, 0.8, 0.04]) # Positioned high above the main plot
legend_ax.axis('off') # Hide the axes box
marker_size = 10
col_x = [0.05, 0.35, 0.65, 0.95, 1.25]
for i in range(1, 6):
    group_idx = (i - 1)
    color = group_colors[group_idx]
    label = f"Temp-{temperature_list[i-1]}"
    
    # x = [col1_x, col2_x, col3_x][i]
    # y = 0.7 # High Y position for Line 1
    x = col_x[i-1]
    y = 0.7 # High Y position for Line 1
    
    # Draw colored marker
    legend_ax.scatter(x - 0.02, y, c=color, s=marker_size*4, clip_on=False, transform=legend_ax.transAxes)
    
    # Draw label text
    legend_ax.text(x, y,
                  label,
                  color='k', # Label text color
                  fontsize=16,
                  ha='left', va='center', transform=legend_ax.transAxes)
    

# for the zoom in start
import matplotlib.ticker as ticker # Import for advanced tick formatting

# version 2
# ---- ZOOM REGION TRIANGLE ON MAIN PLOT ----

# # left top out of main triangle
# A_zoom = [0.327868852, 0.655737706, 0.016393442]
# B_zoom = [0.147540984, 0.770491803, 0.081967213]
# C_zoom = [0.262295081, 0.590163934, 0.147540983]

# right top out of main triangle
# A_zoom = [0.655737706, 0.016393442, 0.327868852]
# B_zoom = [0.770491803, 0.081967213, 0.147540984]
# C_zoom = [0.590163934, 0.147540983, 0.262295081]

# A_zoom = (0.50, 0.15, 0.35)
# B_zoom = (0.45, 0.20, 0.35)
# C_zoom = (0.45, 0.10, 0.45)
# moving closer
# A_zoom = (0.30, 0.15, 0.55)
# B_zoom = (0.25, 0.20, 0.55)
# C_zoom = (0.25, 0.10, 0.65)

# this is right vertex
A_zoom = (0.14, 0.00, 0.80)
# this is the left vertex
B_zoom = (0.140, 0.25, 0.55)
# this is the top vertex
C_zoom = (0.40, 0.02, 0.60)


ax.fill(
    [A_zoom[0], B_zoom[0], C_zoom[0]],
    [A_zoom[1], B_zoom[1], C_zoom[1]],
    [A_zoom[2], B_zoom[2], C_zoom[2]],
    fc="none", ec="k", lw=1.2
)


# ax.fill(A_zoom, B_zoom, C_zoom, fc="none", ec="k", lw=2)

# ---- INSET AXES ----
# 0.62, 0.72, 0.30, 0.70--> left position, bottom position, width, height
# axins = fig.add_axes([0.62, 0.52, 0.30, 0.30], projection="ternary")
# axins = fig.add_axes([0.62, 0.72, 0.30, 0.75], projection="ternary")

# axins = fig.add_axes([0.62, 0.72, 0.30, 0.70], projection="ternary")
axins = fig.add_axes([0.82, 0.42, 0.30, 0.30], projection="ternary")

# ---- ZOOM LIMITS ----
# axins.set_ternary_min(0.147540984, 0.016393442, 0.590163934)
# axins.set_ternary_min(0.18, 0.02, 0.55)
# axins.set_ternary_min(0.14, 0.01, 0.60)
axins.set_ternary_min(0.14, 0.01, 0.55)

# label and tick
axins.tick_params(axis='both', labelsize=16) # Set a visible font size (e.g., 10 or 12)

# 2. Define and apply percentage formatter
# Formatter multiplies the value by 100 and appends a '%' sign.
formatter = ticker.FuncFormatter(lambda x, pos: f'{x * 100:.0f}%')

axins.taxis.set_major_formatter(formatter)
axins.laxis.set_major_formatter(formatter)
axins.raxis.set_major_formatter(formatter)
# label and tick


for idx, point in enumerate(points):
    group_idx=0
    if idx >= 0 and idx<=4:
        group_idx = 0
    elif idx >= 5 and idx<=9:
        group_idx = 1
    elif idx >= 10 and idx<=14:
        group_idx = 2
    elif idx >= 15 and idx<=19:
        group_idx = 3
    elif idx >= 20 and idx<=24:
        group_idx = 4
    
    color = group_colors[group_idx]

    axins.scatter(point[0], point[1], point[2], c=color, alpha=0.9)
    # axins.scatter(t1, l1, r1, alpha=0.5)

plt.tight_layout()
plt.show()

directory = "/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/graph_generation/ternary_plots_poc"
output_path = f"{directory}/edbt_simple_query_with_rag_corrector_with_different_temps_side_arrow.png"

plt.savefig(output_path, dpi=300, bbox_inches="tight")
print("Saved:", output_path)