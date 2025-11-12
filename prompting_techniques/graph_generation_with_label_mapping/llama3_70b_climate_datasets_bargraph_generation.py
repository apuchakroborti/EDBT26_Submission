"""
To move the mapping labels closer to the bar graph, you can adjust the `x` and `y` coordinates in the `plt.text()` function. Here's how you can refine the code to position the mapping labels closer to the graph:

### Updated Code with Adjusted Mapping Label Position:

```python
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# # Sample data
# data = {
#     'Category': ['Total Pass Count', 'Total Fail Count', 'Dataset & Paths Related Errors', 
#                  'Attribute Related Errors', 'Slicing Related Errors', 'Other Errors'],
#     'With Corrector': [17, 52, 14, 5, 9, 24],
#     'Without Corrector': [10, 58, 18, 15, 5, 20]
# }

# # Simplified labels
# simplified_labels = ['A', 'B', 'C', 'D', 'E', 'F']

# Sample data
data = {
    # 'Category': ['Dataset & Paths Related Errors', 'Attribute Related Errors', 'Slicing Related Errors', 'Other Errors'],
    'Category': ['Dataset & Paths Related Errors', 'Attribute Related Errors', 'Subarray Access Errors', 'Other Errors'],
    'With Corrector': [14, 5, 9, 24],
    'Without Corrector': [18, 15, 5, 20]
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
plt.title('Evaluation of Generated Code for the CLIMATE Datasets')
plt.xlabel('Different types of errors and total pass count for the llama3:70b model')
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
plt.savefig('llama3_70b_climate_datasets_bar_graph_comparison.pdf')

# Show the plot
plt.show()

"""```

### Key Adjustments:
1. **Adjusted `x` Position**:
   - Changed `x` from `len(simplified_labels) + 0.5` to `len(simplified_labels) - 0.2` to bring the text closer to the bars.

2. **Adjusted `y` Position**:
   - Ensured the mapping text starts closer to the graph by modifying `max(df_melted['Value']) * 0.8`.

### Customizing the Placement:
- **`x` coordinate**:
  - Reduces or increases the distance of the mapping text from the bar graph horizontally.
- **`y` coordinate**:
  - Moves the mapping text vertically closer or farther from the graph.

Let me know if you'd like to adjust the text further!
"""