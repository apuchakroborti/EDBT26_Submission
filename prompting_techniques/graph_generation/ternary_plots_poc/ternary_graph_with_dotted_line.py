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
        vals = vals / vals.sum()  # normalize
        data.append((model, temp, vals[0], vals[1], vals[2]))


# ----------------------------------------------------
# Ternary to Cartesian Conversion
# ----------------------------------------------------
def ternary_to_cartesian(s, r, f):
    x = r + 0.5 * f
    y = (np.sqrt(3) / 2) * f
    return x, y


# ----------------------------------------------------
# Projection of point to each axis (Success, Runnable, Failed)
# ----------------------------------------------------
def projection_to_success_axis(s, r, f):
    # Face S varies from 1→0 while R increases
    return ternary_to_cartesian(0, r + s, f)

def projection_to_runnable_axis(s, r, f):
    return ternary_to_cartesian(s + r, 0, f)

def projection_to_failed_axis(s, r, f):
    return ternary_to_cartesian(s, r + f, 0)


# ----------------------------------------------------
# Plot Setup
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 10))

colors = plt.cm.tab10(np.linspace(0, 1, len(models)))
markers = ["o", "s", "D", "^", "v"]


# ----------------------------------------------------
# Plot points + projection lines
# ----------------------------------------------------
for model_idx, model in enumerate(models):
    for temp_idx, temp in enumerate(temperatures):

        s, r, f = data[model_idx * 5 + temp_idx][2:5]
        x, y = ternary_to_cartesian(s, r, f)
        c = colors[model_idx]

        # --- Plot point ---
        ax.scatter(
            x, y, color=c,
            marker=markers[temp_idx],
            s=110,
            edgecolor="black",
            linewidth=0.7,
            label=f"{model}, T={temp}"
        )

        # --- Projection to Success axis ---
        xs, ys = projection_to_success_axis(s, r, f)
        ax.plot([x, xs], [y, ys], linestyle="dotted", color=c, linewidth=1.8)

        # --- Projection to Runnable axis ---
        xr, yr = projection_to_runnable_axis(s, r, f)
        ax.plot([x, xr], [y, yr], linestyle="dotted", color=c, linewidth=1.8)

        # --- Projection to Failed axis ---
        xf, yf = projection_to_failed_axis(s, r, f)
        ax.plot([x, xf], [y, yf], linestyle="dotted", color=c, linewidth=1.8)


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
# Add Tick Marks for all faces (0–100%)
# ----------------------------------------------------
ticks = np.linspace(0, 1, 6)  # 0, .2, .4, .6, .8, 1

for t in ticks:
    pct = int(t * 100)

    # Success axis (bottom)
    xs, ys = ternary_to_cartesian(1 - t, t, 0)
    ax.text(xs, ys - 0.035, f"{pct}%", ha="center", fontsize=8)

    # Runnable axis (right)
    xr, yr = ternary_to_cartesian(0, 1 - t, t)
    ax.text(xr + 0.03, yr, f"{pct}%", ha="left", fontsize=8)

    # Failed axis (left)
    xf, yf = ternary_to_cartesian(t, 0, 1 - t)
    ax.text(xf - 0.03, yf, f"{pct}%", ha="right", fontsize=8)


# ----------------------------------------------------
# Axis Labels
# ----------------------------------------------------
ax.text(0.50, -0.08, "Success (0–100%)", ha="center", fontsize=13)
ax.text(1.10, 0.02, "Runnable (0–100%)", ha="left", fontsize=13)
ax.text(0.50, np.sqrt(3)/2 + 0.07, "Failed (0–100%)", ha="center", fontsize=13)


# ----------------------------------------------------
# Formatting
# ----------------------------------------------------
ax.set_xlim(-0.1, 1.15)
ax.set_ylim(-0.1, 1.0)
ax.set_xticks([])
ax.set_yticks([])

handles, labels = ax.get_legend_handles_labels()
unique = dict(zip(labels, handles))
ax.legend(unique.values(), unique.keys(), fontsize=7, bbox_to_anchor=(1.05, 1))

ax.set_title("Ternary Plot with Projection Lines\nSuccess / Runnable / Failed", fontsize=16)

# ----------------------------------------------------
# Save
# ----------------------------------------------------
directory = "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/graph_generation/ternary_plots_poc"
output_path = f"{directory}/ternary_plot_with_projection_lines.png"

plt.savefig(output_path, dpi=300, bbox_inches="tight")
print("Saved:", output_path)

plt.show()
