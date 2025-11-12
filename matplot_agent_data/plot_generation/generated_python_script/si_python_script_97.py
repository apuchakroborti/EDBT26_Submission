import h5py
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset from the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/97_h5_data.h5"
f = h5py.File(file_path, 'r')
dataset = f['No.', 'IL (25°C)', 'toluene (25°C)', 'n-heptane (25°C)']

# Extract data from the dataset
data = np.array(dataset)
no_values = data[:, 0]
il_values = data[:, 1]
toluene_values = data[:, 2]
n_heptane_values = data[:, 3]

# Function to transform ternary coordinates to Cartesian for equilateral triangle
def ternary_to_cartesian(x, y):
    return x * np.sqrt(3)/2, (1 - x - y) * np.sqrt(3)/2

# Create a figure with two subplots side by side
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# Plot for equilateral triangle diagram
for no in np.unique(no_values):
    mask = no_values == no
    x = toluene_values[mask]
    y = n_heptane_values[mask]
    tx, ty = ternary_to_cartesian(x, y)
    axes[0].plot(tx, ty, 'o-', label=f'No. {int(no)}')
axes[0].set_title("Liquid-Liquid Phase Diagram (Equilateral Triangle)")
axes[0].set_xlabel('Toluene Cartesian Coordinate')
axes[0].set_ylabel('n-Heptane Cartesian Coordinate')
axes[0].legend()
axes[0].axhline(0, color='black',linewidth=0.5)
axes[0].axvline(0, color='black',linewidth=0.5)
axes[0].set_aspect('equal', 'box')

# Plot for right-angled triangle diagram
for no in np.unique(no_values):
    mask = no_values == no
    x = toluene_values[mask]
    y = il_values[mask]
    axes[1].plot(x, y, 'o-', label=f'No. {int(no)}')
axes[1].set_title("Liquid-Liquid Phase Diagram (Right-Angled Triangle)")
axes[1].set_xlabel('Toluene')
axes[1].set_ylabel('IL')
axes[1].legend()
axes[1].axhline(0, color='black',linewidth=0.5)
axes[1].axvline(0, color='black',linewidth=0.5)
axes[1].set_aspect('equal', 'box')

plt.tight_layout()
plt.show()
