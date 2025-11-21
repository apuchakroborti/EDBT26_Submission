import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------
# Generate Example Data
# ------------------------------------
models = [f"Model_{i+1}" for i in range(5)]
temperatures = [0.0, 0.2, 0.4, 0.6, 0.8]

data = []
for model in models:
    for temp in temperatures:
        vals = np.random.rand(3)
        vals = vals / vals.sum()  # normalize to sum to 1
        data.append((model, temp, vals[0], vals[1], vals[2]))  # success, runnable, failed


# ------------------------------------
# Ternary Conversion
# ------------------------------------
def ternary_to_cartesian(success, runnable, failed):
    """
    Convert ternary coordinates (s, r, f) to Cartesian (x, y)
    for an equilateral triangle.
    """
    x = 0.5 * (2 * runnable + failed)
    y = (np.sqrt(3) / 2) * failed
    return x, y


# ------------------------------------
# Plot
# ------------------------------------
fig, ax = plt.subplots(figsize=(8, 8))

colors = plt.cm.tab10(np.linspace(0, 1, len(models)))
markers = ["o", "s", "D", "^", "v"]  # markers per temperature

for model_idx, model in enumerate(models):
    for temp_idx, temp in enumerate(temperatures):
        success, runnable, failed = data[model_idx * 5 + temp_idx][2:5]
        x, y = ternary_to_cartesian(success, runnable, failed)

        ax.scatter(
            x, y,
            color=colors[model_idx],
            marker=markers[temp_idx],
            s=80,
            label=f"{model}, T={temp}" if temp_idx == 0 else None
        )


# ------------------------------------
# Draw Triangle Outline
# ------------------------------------
triangle = np.array([
    [0, 0],                # Success
    [1, 0],                # Runnable
    [0.5, np.sqrt(3)/2],   # Failed
    [0, 0]
])
ax.plot(triangle[:, 0], triangle[:, 1], color="black", linewidth=1.5)


# ------------------------------------
# Formatting
# ------------------------------------
ax.set_title("Ternary Plot: Success / Runnable / Failed\n5 Models × 5 Temperatures")
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.0)
ax.set_xticks([])
ax.set_yticks([])

# Legend
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

# ------------------------------------
# Save Figure
# ------------------------------------
directory = "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/graph_generation/ternary_plots_poc"
output_path = f"{directory}/ternary_plot.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"Saved figure to: {output_path}")

plt.show()



# import numpy as np
# import plotly.express as px
# import pandas as pd

# # ------------------------------------
# # Generate Example Data
# # ------------------------------------
# models = [f"Model_{i+1}" for i in range(5)]
# temperatures = [0.0, 0.2, 0.4, 0.6, 0.8]

# data = []

# for model in models:
#     for temp in temperatures:
#         # Generate 3 random numbers and normalize to sum to 1
#         vals = np.random.rand(3)
#         vals = vals / vals.sum()

#         success, runnable, failed = vals

#         data.append({
#             "Model": model,
#             "Temperature": temp,
#             "Success": success,
#             "Runnable": runnable,
#             "Failed": failed
#         })

# df = pd.DataFrame(data)

# # ------------------------------------
# # Create Ternary Plot
# # ------------------------------------
# fig = px.scatter_ternary(
#     df,
#     a="Success",
#     b="Runnable",
#     c="Failed",
#     color="Model",
#     symbol="Temperature",
#     size_max=12,
#     title="Ternary Plot of 5 Models × 5 Temperatures",
# )

# fig.update_traces(marker=dict(size=10))
# # fig.show()

