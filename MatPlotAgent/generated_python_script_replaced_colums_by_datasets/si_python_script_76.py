import h5py
import matplotlib.pyplot as plt
import numpy as np

# Load the HDF5 file
file_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/76_h5_data.h5'
data = h5py.File(file_path, 'r')

# Extract the "Women's millions of dollars" dataset
women_data = data['Women\'s millions of dollars'][:]

# Plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Box plot
bp = ax1.boxplot(women_data, vert=False, patch_artist=True)
for box in bp['boxes']:
    box.set(facecolor='lightblue')
ax1.set_title('Axis-Free Box Plot of Women\'s Millions Data')
ax1.set_xlabel('Values')
ax1.set_yticklabels([])  # Remove y-axis labels for a cleaner look

# Highlight quartiles with continuous red dashed lines
for whisker in bp['whiskers']:
    whisker.set(linestyle='--', color='red')
for median in bp['medians']:
    median.set(color='red')

# Histogram
ax2.hist(women_data, bins=10, edgecolor='black', linewidth=1.2)
ax2.set_title('Histogram of Women\'s Millions Data')
ax2.set_xlabel('Values')
ax2.set_ylabel('Frequency')

# Highlight quartiles in the histogram
quartiles = np.percentile(women_data, [25, 50, 75])
for q in quartiles:
    ax2.axvline(q, color='red', linestyle='--')

plt.tight_layout()
plt.show()
