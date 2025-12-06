"""
Here's a Python code snippet that uses Seaborn and Matplotlib to create a side-by-side bar graph based on multiple parameters, and then saves the plot as a PDF:

```python
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# matplot agent csv to h5 datasets and magicoder model
# Sample data
# data = {
#     # 'Category': ['Pass Count', 'Fail Count', 'Dataset Paths Related Error Count', 
#                 #  'Attribute Related Error Count', 'Slicing Related Error Count', 'Other Errors count'],
#     'Category': ['Total Pass Count', 'Total Fail Count', 'Dataset & Paths Related Errors', 
#                  'Attribute Related Errors', 'Slicing Related Errors', 'Other Errors'],
#     'With Corrector': [3, 8, 3, 1, 0, 4],
#     'Without Corrector': [1, 10, 8, 0, 0, 2]
    
#     # 'Parameter3': [6, 9, 7, 8]
# }

# # Simplified labels
# simplified_labels = ['A', 'B', 'C', 'D', 'E', 'F']

data = {
    'Category': ['Dataset & Paths Related Errors', 'Attribute Related Errors', 'Subarray Access Errors', 'Other Errors'],
    'With Corrector': [3, 1, 0, 4],
    'Without Corrector': [8, 0, 0, 2]
}

# Simplified labels
simplified_labels = ['A', 'B', 'C', 'D']


# Create mapping of simplified labels to categories
category_mapping = dict(zip(simplified_labels, data['Category']))

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Replace the 'Category' column with simplified labels for plotting
df['Category (Simplified)'] = simplified_labels

# Melt the DataFrame for seaborn
df_melted = pd.melt(
    df,
    id_vars='Category (Simplified)',
    value_vars=['With Corrector', 'Without Corrector'],
    var_name='Parameter',
    value_name='Value',
)

# Set the Seaborn style
sns.set_style('whitegrid')

# Create the bar plot
plt.figure(figsize=(7, 5))
sns.barplot(data=df_melted, x='Category (Simplified)', y='Value', hue='Parameter')

# Rotate x-axis labels to 45 degrees
# plt.xticks(rotation=45, ha='right')

# Add labels and title
plt.title('Evaluation of Generated Code for the FAST_MRI_BRAIN Datasets')
plt.xlabel('Different types of errors and total pass count for the magicoder model')
plt.ylabel('Number of Evaluated Python Scripts')

# Add the mapping text on the right, closer to the graph
# mapping_text = "\n".join(f"{simp} = {full}" for simp, full in category_mapping.items())
# plt.text(len(simplified_labels) - 0.2, max(df_melted['Value']) * 0.8,  # Adjust `x` and `y` positions
#          mapping_text, fontsize=10, va='top', ha='left')

# rows = [
#     " ".join(f"{simplified_labels[i]}={category_mapping[simplified_labels[i]]}" for i in range(3)),
#     " ".join(f"{simplified_labels[i]}={category_mapping[simplified_labels[i]]}" for i in range(3, 6))
# ]

rows = [
    " ".join(f"{simplified_labels[i]}={category_mapping[simplified_labels[i]]}" for i in range(len(simplified_labels)//2)),
    " ".join(f"{simplified_labels[i]}={category_mapping[simplified_labels[i]]}" for i in range(len(simplified_labels)//2, len(simplified_labels)))
]

# Join the rows with a line break to place the labels in two rows
mapping_text = "\n".join(rows)
plt.text(0.5, -0.2, mapping_text, ha='center', va='top', fontsize=12, transform=plt.gca().transAxes)


# Adjust layout to fit everything
plt.tight_layout()

# Save the plot as a PDF
plt.savefig('magicoder_fast_mri_brain_datasets_bar_graph_comparison.pdf')

# Show the plot
plt.show()

"""
```

### How it works:
1. **Data Preparation**: The sample data is created in a dictionary, then converted to a Pandas DataFrame.
2. **Data Transformation**: The DataFrame is melted to reshape it for Seaborn.
3. **Plotting**: A Seaborn `barplot` is created with categories on the x-axis and values on the y-axis, using `hue` to differentiate parameters.
4. **Customization**: Labels and a title are added for clarity.
5. **Saving**: The plot is saved as a PDF using `plt.savefig()`.

You can replace the sample data with your own dataset and adjust the figure size and styling as needed.
"""