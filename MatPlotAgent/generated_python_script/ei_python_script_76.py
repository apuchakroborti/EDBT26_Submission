import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the path to your HDF5 file
file_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/76_h5_data.h5'

# Read data from the specified column in the HDF5 file
data = pd.read_hdf(file_path, key='Women')  # Assuming 'Women' is the dataset name for women's retail sales

# Create a figure with two subplots (1 row, 2 columns)
fig, axes = plt.subplots(2, 1, figsize=(8, 10), gridspec_kw={'height_ratios': [1, 4]})

# Plot the box plot on the top axis
sns.boxplot(data=data, orient='v', ax=axes[0])
axes[0].set_title('Box Plot of Women\'s Retail Sales')
axes[0].set_ylabel('Millions of Dollars')

# Add numerical labels for key statistics
stats = data.describe()
min_val = stats['min'][0]
q1_val = stats['25%'][0]
median_val = stats['50%'][0]
q3_val = stats['75%'][0]
max_val = stats['max'][0]
axes[0].text(0.05, 0.9, f'Min: {min_val:.2f}', transform=axes[0].transAxes)
axes[0].text(0.05, 0.8, f'Q1: {q1_val:.2f}', transform=axes[0].transAxes)
axes[0].text(0.05, 0.7, f'Median: {median_val:.2f}', transform=axes[0].transAxes)
axes[0].text(0.05, 0.6, f'Q3: {q3_val:.2f}', transform=axes[0].transAxes)
axes[0].text(0.05, 0.5, f'Max: {max_val:.2f}', transform=axes[0].transAxes)

# Plot the histogram on the bottom axis
sns.histplot(data, kde=True, ax=axes[1])
axes[1].set_title('Histogram of Women\'s Retail Sales')
axes[1].set_xlabel('Millions of Dollars')
axes[1].set_ylabel('Frequency')

# Add continuous red dashed lines at the lower and upper quartiles
axes[0].axvline(q1_val, color='red', linestyle='--')
axes[0].axvline(q3_val, color='red', linestyle='--')

# Adjust layout to tightly lay out the plots without space between them
plt.tight_layout()

# Show the plot
plt.show()
