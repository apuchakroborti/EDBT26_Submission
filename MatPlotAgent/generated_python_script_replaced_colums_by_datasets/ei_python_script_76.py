import h5py
import matplotlib.pyplot as plt
import numpy as np

# Define file path
file_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/76_h5_data.h5'

# Open the HDF5 file
with h5py.File(file_path, 'r') as file:
    # Read data from the dataset "Woman's millions of dollars"
    women_sales = np.array(file['Woman\'s millions of dollars']).flatten()

# Create a figure with two subplots (1 row, 2 columns)
fig, axes = plt.subplots(2, 1, figsize=(8, 10), gridspec_kw={'height_ratios': [1, 4]})

# Plot the box plot on the top axis
axes[0].boxplot(women_sales, vert=False)
axes[0].set_axis_off()  # Turn off axes for the box plot

# Calculate key statistics
stats = np.percentile(women_sales, [25, 50, 75])
min_val = np.min(women_sales)
max_val = np.max(women_sales)

# Add labels for the key statistics just above the box plot
axes[0].text(1, 0.9, f'Min: {min_val:.2f}', verticalalignment='center', ha='right', transform=axes[0].transAxes)
axes[0].text(1, 0.6, f'Q1: {stats[0]:.2f}', verticalalignment='center', ha='right', transform=axes[0].transAxes)
axes[0].text(1, 0.3, f'Median: {stats[1]:.2f}', verticalalignment='center', ha='right', transform=axes[0].transAxes)
axes[0].text(1, 0.0, f'Q3: {stats[2]:.2f}', verticalalignment='center', ha='right', transform=axes[0].transAxes)
axes[0].text(1, -0.3, f'Max: {max_val:.2f}', verticalalignment='center', ha='right', transform=axes[0].transAxes)

# Plot the histogram below the box plot
axes[1].hist(women_sales, bins=np.arange(min_val, max_val + 1), edgecolor='black')
axes[1].set_xlabel('Sales (Millions of dollars)')
axes[1].set_ylabel('Frequency')

# Add red dashed lines for the quartiles
axes[1].axvline(stats[0], color='red', linestyle='--')  # Lower quartile
axes[1].axvline(stats[2], color='red', linestyle='--')  # Upper quartile

# Adjust layout to tightly lay out the plots with no space between them
plt.tight_layout()

# Show the plot
plt.show()
