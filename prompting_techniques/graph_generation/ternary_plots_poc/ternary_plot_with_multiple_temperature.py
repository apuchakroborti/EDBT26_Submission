import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------
# Generate Example Data
# ----------------------------------------------------
models = [f"Model_{i+1}" for i in range(5)]
temperatures = [0.0, 0.2, 0.4, 0.6, 0.8]

data = []
for model in models:
    for temp in temperatures:
        vals = np.random.rand(3)
        vals = vals / vals.sum()  # normalize to 1
        data.append((model, temp, vals[0], vals[1], vals[2]))


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
for model_idx, model in enumerate(models):
    for temp_idx, temp in enumerate(temperatures):
        s, r, f = data[model_idx*5 + temp_idx][2:5]
        x, y = ternary_to_cartesian(s, r, f)

        ax.scatter(
            x, y,
            color=colors[model_idx],
            marker=markers[temp_idx],
            s=90,
            edgecolor="black",
            linewidth=0.5,
            label=f"{model}, T={temp}"
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

directory = "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/graph_generation/ternary_plots_poc"
output_path = f"{directory}/ternary_plot_with_scales.png"

plt.savefig(output_path, dpi=300, bbox_inches="tight")
print("Saved:", output_path)

plt.show()





# Iteration 1
# import numpy as np
# import matplotlib.pyplot as plt

# # ----------------------------------------------------
# # Generate Example Data
# # ----------------------------------------------------
# models = [f"Model_{i+1}" for i in range(5)]
# temperatures = [0.0, 0.2, 0.4, 0.6, 0.8]

# data = []
# for model in models:
#     for temp in temperatures:
#         vals = np.random.rand(3)
#         vals = vals / vals.sum()  # normalize to sum to 1
#         data.append((model, temp, vals[0], vals[1], vals[2]))  # success, runnable, failed


# # ----------------------------------------------------
# # Ternary Conversion Function
# # ----------------------------------------------------
# def ternary_to_cartesian(success, runnable, failed):
#     """Convert ternary (s, r, f) to Cartesian coordinates."""
#     x = 0.5 * (2 * runnable + failed)
#     y = (np.sqrt(3) / 2) * failed
#     return x, y


# # ----------------------------------------------------
# # Plot Setup
# # ----------------------------------------------------
# fig, ax = plt.subplots(figsize=(9, 9))

# colors = plt.cm.tab10(np.linspace(0, 1, len(models)))
# markers = ["o", "s", "D", "^", "v"]  # 5 temperature markers

# # Plot all points
# for model_idx, model in enumerate(models):
#     for temp_idx, temp in enumerate(temperatures):
#         success, runnable, failed = data[model_idx * 5 + temp_idx][2:5]
#         x, y = ternary_to_cartesian(success, runnable, failed)

#         ax.scatter(
#             x, y,
#             color=colors[model_idx],
#             marker=markers[temp_idx],
#             s=90,
#             edgecolor="black",
#             linewidth=0.5,
#             label=f"{model}, T={temp}"  # now *all* temps appear in legend
#         )


# # ----------------------------------------------------
# # Draw Triangle Outline
# # ----------------------------------------------------
# triangle = np.array([
#     [0, 0],                # Success = 100%
#     [1, 0],                # Runnable = 100%
#     [0.5, np.sqrt(3)/2],   # Failed = 100%
#     [0, 0]
# ])
# ax.plot(triangle[:, 0], triangle[:, 1], color="black", linewidth=2)


# # ----------------------------------------------------
# # Add Axis Labels (Success, Runnable, Failed)
# # ----------------------------------------------------
# ax.text(-0.05, -0.05, "Success (0–100%)", ha="center", va="center", fontsize=12)
# ax.text(1.05, -0.05, "Runnable (0–100%)", ha="center", va="center", fontsize=12)
# ax.text(0.5, np.sqrt(3)/2 + 0.07, "Failed (0–100%)", ha="center", va="center", fontsize=12)

# # ----------------------------------------------------
# # Add Ticks & Grid Lines for Percentages
# # ----------------------------------------------------
# ticks = np.linspace(0, 1, 6)

# for t in ticks:
#     # Success axis ticks (bottom-left → bottom-right)
#     ax.text(t, -0.03, f"{int((1-t)*100)}%", ha="center", fontsize=8)

#     # Runnable axis ticks (bottom-right → top)
#     xr = 1 - t/2
#     yr = (np.sqrt(3)/2) * t
#     ax.text(xr + 0.03, yr, f"{int(t*100)}%", fontsize=8)

#     # Failed axis ticks (top → bottom-left)
#     xf = t/2
#     yf = (np.sqrt(3)/2) * (1 - t)
#     ax.text(xf - 0.03, yf, f"{int(t*100)}%", fontsize=8)


# # ----------------------------------------------------
# # Formatting
# # ----------------------------------------------------
# ax.set_title("Ternary Plot with 0–100% Scales\n5 Models × 5 Temperatures", fontsize=15)
# ax.set_xlim(-0.1, 1.1)
# ax.set_ylim(-0.1, 1.0)
# ax.set_xticks([])
# ax.set_yticks([])

# # Avoid duplicate legend entries
# handles, labels = ax.get_legend_handles_labels()
# unique = dict(zip(labels, handles))
# ax.legend(unique.values(), unique.keys(), fontsize=8, bbox_to_anchor=(1.05, 1))

# # ----------------------------------------------------
# # Save Figure
# # ----------------------------------------------------
# directory = "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/graph_generation/ternary_plots_poc"
# # output_path = f"{directory}/ternary_plot.png"
# output_path = f"{directory}/ternary_plot_with_scales.png"
# plt.savefig(output_path, dpi=300, bbox_inches="tight")
# print("Saved:", output_path)

# plt.show()
