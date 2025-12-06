"""
Here’s the modified code to include a **side mapping** of labels (`A`, `B`, `C`, etc.) for the categories and display the mapping on the right side of the graph. 

### Modified Code:

```python
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# # Sample data
# data = {
#     'Category': ['Total Pass Count', 'Total Fail Count', 'Dataset & Paths Related Errors', 
#                  'Attribute Related Errors', 'Slicing Related Errors', 'Other Errors'],
#     'With Corrector': [14, 55, 10, 17, 9, 19],
#     'Without Corrector': [11, 58, 20, 16, 4, 18]
# }

# # Simplified labels for the categories
# simplified_labels = ['A', 'B', 'C', 'D', 'E', 'F']

# Sample data
data = {
   #  'Category': ['Dataset & Paths Related Errors', 'Attribute Related Errors', 'Slicing Related Errors', 'Other Errors'],
   'Category': ['Dataset & Paths Related Errors', 'Attribute Related Errors', 'Subarray Access Errors', 'Other Errors'],
   'With Corrector': [10, 17, 9, 19],
   'Without Corrector': [20, 16, 4, 18]
}

# Simplified labels for the categories
simplified_labels = ['A', 'B', 'C', 'D']


# Create a mapping of simplified labels to categories
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
# plt.figure(figsize=(12, 6))
plt.figure(figsize=(7, 5))
sns.barplot(data=df_melted, x='Category (Simplified)', y='Value', hue='Parameter')

# Rotate x-axis labels to 45 degrees
# plt.xticks(rotation=45, ha='right')



# Add labels and title
plt.title('Evaluation of Generated Code for the CLIMATE Datasets', fontsize=12)
plt.xlabel('Different types of errors and total pass count for the deepseek-coder-v2 model', fontsize=12, ha='center')
plt.ylabel('Number of Evaluated Python Scripts', fontsize=12)

# Adjust layout to prevent cropping
# plt.tight_layout(pad=2.0)

# Add the mapping text on the right
# mapping_text = "\n".join(f"{simp} = {full}" for simp, full in category_mapping.items())
# plt.text(len(simplified_labels) + 0.5, max(df_melted['Value']) * 0.8, 
#          mapping_text, fontsize=10, va='top', ha='left')

# Add the mapping text on the right, closer to the graph
# mapping_text = "\n".join(f"{simp} = {full}" for simp, full in category_mapping.items())
# mapping_text = " ".join(f"{simp} = {full}" for simp, full in category_mapping.items())
# Prepare the mapping text for two rows with 3 items per row
# Group the labels into two rows of 3 items each
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


# plt.text(len(simplified_labels) - 0.2, max(df_melted['Value']) * 0.8,  # Adjust `x` and `y` positions
         # mapping_text, fontsize=12, va='top', ha='left')



# does not work for getting cropped of xlabel
# plt.tight_layout(pad=5.0)
# plt.subplots_adjust(bottom=0.15)

# # Zoom out by adjusting y-axis limits
# current_ylim = plt.ylim()
# plt.ylim(current_ylim[0], current_ylim[1] * 1.2)

# # Save the plot as a PDF
# plt.savefig('deepseek_coder_v2_climate_datasets_bar_graph_comparison_with_mapping.pdf')

# # Show the plot
# plt.show()

# Adjust layout to fit everything
plt.tight_layout()

# Save the plot as a PDF
plt.savefig('deepseek_coder_v2_climate_datasets_bar_graph_comparison.pdf', bbox_inches='tight')

# Show the plot
plt.show()


"""
```

### Explanation of Changes:
1. **Simplified Labels**:
   - Added `simplified_labels` (`A`, `B`, `C`, etc.) to map each category.

2. **Category Mapping**:
   - Created `category_mapping` to link simplified labels to the full category names.

3. **Text Display**:
   - Used `plt.text()` to display the mapping on the right side of the plot.

4. **Positioning the Mapping**:
   - Adjusted the `x` position to place the text outside the graph and the `y` position for proper alignment.

5. **Zoom Out**:
   - Adjusted the `y-axis` to add more space and ensure a clean layout.

6. **Save and Display**:
   - The final plot is saved as a PDF and displayed with the mapping on the side.

Let me know if you'd like further refinements!
"""