import h5py
import matplotlib.pyplot as plt
import numpy as np

# Open the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/100_h5_data.h5"
f = h5py.File(file_path, 'r')

# Extract data from the datasets
series = f['Series'][:]
wavelength = f['Wavelength'][:]
l_position = f['l position'][:]
p_position = f['p position'][:]

# Sort data by Series
sorted_indices = np.argsort(series)
series_sorted = series[sorted_indices]
wavelength_sorted = wavelength[sorted_indices]
l_position_sorted = l_position[sorted_indices]
p_position_sorted = p_position[sorted_indices]

# Group transitions by series and get unique series names
unique_series = np.unique(series_sorted)
transitions = {ser: (wavelength_sorted[series_sorted == ser], l_position_sorted[series_sorted == ser], p_position_sorted[series_sorted == ser]) for ser in unique_series}

# Set up the polar plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_theta_zero_location('N')  # North position
ax.set_thetamin(-90)             # Start from -90 degrees (top half of circle)
ax.set_thetamax(90)              # End at 90 degrees

# Define colors for each series
colors = plt.cm.get_cmap('tab10', len(unique_series))

# Plot transitions and fill series areas
for i, ser in enumerate(unique_series):
    ax.scatter(np.deg2rad(np.linspace(-90, 90, 36)), np.full(36, 1), c=colors(i), label=ser)
    for w, l, p in zip(*transitions[ser]):
        ax.plot([np.deg2rad(l), np.deg2rad(p)], [0, 1], 'k-', linewidth=1)
        ax.text(np.mean([np.deg2rad(l), np.deg2rad(p)]), 1.1, f'{w:.2f} eV', ha='center')
    ax.fill_betweenx([0, 1], np.deg2rad(np.linspace(-90, 90, 36)), color=colors(i), alpha=0.3)

# Add labels and title
ax.set_rticks([1])  # Only one radial tick for simplicity
ax.set_rlabel_position('left')
ax.set_title("Electron Transitions for an Atom")
ax.legend()
plt.show()
