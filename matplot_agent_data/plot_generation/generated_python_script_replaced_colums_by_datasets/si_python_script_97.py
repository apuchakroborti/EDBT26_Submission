import h5py
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset from the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/97_h5_data.h5"
f = h5py.File(file_path, 'r')
dataset = f['No.', 'IL (25°C)', 'toluene (25°C)', 'n-heptane (25°C)']

# Extract data from the dataset
no = np.array(dataset['No.'])
il = np.array(dataset['IL (25°C)'])
toluene = np.array(dataset['toluene (25°C)'])
n_heptane = np.array(dataset['n-heptane (25°C)'])

# Function to transform ternary coordinates to Cartesian for equilateral triangle
def ternary_to_cartesian(x, y):
    return x * 100, y * 100 * np.sqrt(3)/2

# Create a figure with two subplots (equilateral and right-angled triangle)
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Plot for equilateral triangle
for group in np.unique(no):
    mask = no == group
    x_vals = [0, toluene[mask]/100, (toluene[mask] + n_heptane[mask])/100]
    y_vals = [il[mask]/100, 0, 0]
    axes[0].plot(x_vals, y_vals, 'o-', label=f'Group {group}')
axes[0].set_title("Liquid-Liquid Phase Diagram (Equilateral Triangle)")
axes[0].set_xlabel('Toluene')
axes[0].set_ylabel('n-Heptane')
axes[0].legend()
axes[0].axhline(0, color='black',linewidth=0.5)
axes[0].axvline(0, color='black',linewidth=0.5)
axes[0].set_aspect('equal', 'box')
axes[0].tick_params(axis='both', which='both', length=0)
axes[0].text(0.5, 0.02, 'IL', ha='center', va='center', transform=axes[0].transAxes)
axes[0].text(-0.02, 0.5, 'Toluene', ha='center', va='center', transform=axes[0].transAxes)
axes[0].text(1.02, -0.02, 'n-Heptane', ha='center', va='center', transform=axes[0].transAxes)

# Plot for right-angled triangle
for group in np.unique(no):
    mask = no == group
    x_vals = toluene[mask]/100
    y_vals = il[mask]/100
    axes[1].plot(x_vals, y_vals, 'o-', label=f'Group {group}')
axes[1].set_title("Liquid-Liquid Phase Diagram (Right-Angled Triangle)")
axes[1].set_xlabel('Toluene')
axes[1].set_ylabel('IL')
axes[1].legend()
axes[1].axhline(0, color='black',linewidth=0.5)
axes[1].axvline(0, color='black',linewidth=0.5)
axes[1].tick_params(axis='both', which='both', length=0)
axes[1].text(-0.02, 1.02, 'n-Heptane', ha='center', va='center', transform=axes[1].transAxes)

plt.tight_layout()
plt.show()
