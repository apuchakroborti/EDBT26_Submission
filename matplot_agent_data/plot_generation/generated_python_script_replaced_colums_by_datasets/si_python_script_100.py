import h5py
import matplotlib.pyplot as plt
import numpy as np

# Open the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/100_h5_data.h5"
f = h5py.File(file_path, 'r')

# Extract data from the datasets
series = f['Series'][:]
wavelengths = f['Wavelength'][:]
l_position = f['l position'][:]
p_position = f['p position'][:]

# Sort data by series
sorted_indices = np.argsort(series)
series = series[sorted_indices]
wavelengths = wavelengths[sorted_indices]
l_position = l_position[sorted_indices]
p_position = p_position[sorted_indices]

# Create a polar plot for electron transitions
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, projection='polar')

# Define the number of energy levels and create concentric regions
n_levels = 6
radius = np.linspace(0, 1, n_levels)

# Plot the semi-circle with energy level labels on the left and corresponding energies on the right
ax.set_thetamin(-90)
ax.set_thetamax(90)
ax.set_rticks([1])  # Only show one radial tick for simplicity

for i in range(n_levels):
    ax.plot([np.deg2rad(0), np.deg2rad(360)], [radius[i], radius[i]], 'k-')
    ax.text(-np.pi/2, radius[i], f'{i+1}n', ha='center', va='center')
ax.set_rlabel_position(270)  # Move radial labels to the right side
for i in range(n_levels):
    ax.text(np.pi/2, radius[i], f'{13.22 - (i * 2.2)} eV', ha='center', va='center')

# Plot arrows for electron transitions
arrow_colors = {'Lyman Series': 'blue', 'Balmer Series': 'green', 'Paschen Series': 'red'}
for i in range(len(series)):
    start_angle = np.arctan2(-l_position[i], -1)  # Angle corresponding to l position
    end_angle = np.arctan2(p_position[i], 1)      # Angle corresponding to p position
    ax.plot([start_angle, end_angle], [radius[int(l_position[i])-1], radius[int(p_position[i])-1]], 'k--', head_width=0.05, head_length=0.1)
    ax.text((start_angle + end_angle)/2, (radius[int(l_position[i])-1] + radius[int(p_position[i])-1])/2, f'{wavelengths[i]} eV', ha='center', va='center')
    ax.fill_between([start_angle, end_angle], [radius[int(l_position[i])-1], radius[int(p_position[i])-1]], color=arrow_colors[series[i]], alpha=0.3)

# Title and display the plot
plt.title("Electron Transitions for an Atom")
plt.show()
