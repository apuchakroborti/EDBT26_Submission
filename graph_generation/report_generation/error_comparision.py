import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv("./prompting_techniques/report_generation/error_type_count_single_attempt.csv")
print(df)
sns.set(font_scale=1.5,style="whitegrid")
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'
# Set up FacetGrid
g = sns.FacetGrid(df, row="dataset", col="model", margin_titles=True, height=4, aspect=1.2, sharey='row')
# Plot grouped bar charts
g.map_dataframe(sns.barplot, x="error type", y="count", hue="config", dodge=True, palette="muted")
# Adjusting legend and titles
g.add_legend(title="")
sns.move_legend(g, "center left", bbox_to_anchor=(0.4, 0.6))
g.set_titles(row_template="{row_name}", col_template="{col_name}")
# Remove redundant axis labels
for ax in g.axes.flat:
    ax.set_xlabel("")
    ax.set_ylabel("")
# Set one x-label and one y-label
g.figure.text(0.452, 0.025, "Error Type", ha="center")  # X-axis label at the bottom
g.figure.text(0.035, 0.5, "Count", va="center", rotation=90)  # Y-axis label on the left
dataset_1_axes = g.axes[0, :]  # Access all columns for Dataset 1
for ax in dataset_1_axes:
    ax.set_yticks([0, 4, 8, 12, 16])  # Custom y-ticks for Dataset 1
#plt.tight_layout()
# Save and show the plot
plt.savefig('error_type_count_single_attempt.pdf', bbox_inches='tight', pad_inches=0.02)
plt.show()