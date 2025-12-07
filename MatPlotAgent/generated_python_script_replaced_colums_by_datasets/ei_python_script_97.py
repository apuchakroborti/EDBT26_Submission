import h5py
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset from the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/97_h5_data.h5"
f = h5py.File(file_path, 'r')
dataset = f['No.']  # Assuming the main dataset is named "No."

# Extract data from the dataset
no_groups = list(dataset.keys())
data = {group: np.array(dataset[group]) for group in no_groups}

# Function to convert ternary coordinates to Cartesian for equilateral triangle
def coords_equilateral(x, y, z):
    return (x + y * 0.5), (y * np.sqrt(3) / 2)

# Function to convert ternary coordinates to Cartesian for right-angled triangle
def coords_right_angled(x, y, z):
    return x, y

# Plotting function
def plot_ternary(ax, data, color_scheme, legend_labels):
    for group, values in data.items():
        xs = [coords[0] for coords in values]
        ys = [coords[1] for coords in values]
        ax.plot(xs, ys, 'o-', label=legend_labels[group], color=color_scheme[group])
    ax.set_aspect('equal')
    ax.axis('off')  # Remove axes and ticks
    ax.legend()

# Create a figure with two subplots (equilateral and right-angled triangle)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Plotting equilateral triangle diagram
ax1.set_title("Liquid-Liquid Phase Diagram - Equilateral Triangle")
for group in no_groups:
    values = [coords_equilateral(row[1], row[2], row[3]) for row in data[group]]
    plot_ternary(ax1, dict(zip(no_groups, [values])), {group: plt.cm.get_cmap('tab10', len(no_groups))(i) for i, group in enumerate(no_groups)}, no_groups)

# Plotting right-angled triangle diagram
ax2.set_title("Liquid-Liquid Phase Diagram - Right-Angled Triangle")
for group in no_groups:
    values = [coords_right_angled(row[1], row[2]) for row in data[group]]
    plot_ternary(ax2, dict(zip(no_groups, [values])), {group: plt.cm.get_cmap('tab10', len(no_groups))(i) for i, group in enumerate(no_groups)}, no_groups)

plt.tight_layout()
plt.show()
