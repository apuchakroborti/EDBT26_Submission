import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data from the CSV file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/100_h5_data.h5"
data = pd.read_csv(file_path)  # Assuming the data is in CSV format, adjust if it's HDF5 or HE5

# Sort the data by 'Series' column
data = data.sort_values(by='Series')

# Create a polar plot
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, projection='polar')

# Define energy levels and their labels
energy_levels = np.arange(1, 7)
energy_labels = [f'{i}n' for i in energy_levels]
energy_values = np.linspace(0, 13.22, len(energy_levels))

# Plot the semi-circle with concentric regions and labels
ax.set_thetamin(-90)  # Start from the top of the circle (180 degrees in polar coordinates)
ax.set_thetamax(90)   # End at the bottom of the circle
ax.set_theta_zero_location('N')  # North is at the top

# Plot concentric circles and labels for energy levels
for i, value in enumerate(energy_values):
    ax.plot([0, np.deg2rad(180)], [value, value], 'k-', lw=1)  # Vertical lines from center to edge
    plt.text(np.deg2rad(-9), value + 0.5, f'{energy_labels[i]}', ha='right', va='center')

# Set labels for the right side of the circle
plt.thetagrids([-90], minor=False)
for i in range(len(energy_values)):
    plt.text(np.deg2rad(-9), energy_values[i] - 0.5, f'{round(energy_values[i], 2)} eV', ha='right', va='center')

# Plot transitions as arrows
for index, row in data.iterrows():
    ax.arrow(np.deg2rad(-9), (row['l position'] + row['p position']) / 2, np.deg2rad(180 - ((row['l position'] + row['p position']) / 2)), 0, head_width=0.5, head_length=0.1, fc='k', ec=row['Series'])
    plt.text(np.deg2rad(-9), (row['l position'] + row['p position']) / 2 + 0.6, str(int(round(row['Wavelength']))), ha='left', va='center')

# Color-code transitions based on series
colors = {'Lyman Series': 'blue', 'Balmer Series': 'green', 'Paschen Series': 'red'}
for i, row in data.iterrows():
    plt.plot([np.deg2rad(180)], [row['l position']], 'o', color=colors[row['Series']])
    plt.plot([np.deg2rad(-90)], [row['p position']], '^', color=colors[row['Series']])
    ax.fill_betweenx([row['l position'], row['p position']], np.deg2rad(180), np.deg2rad(-90), alpha=0.3, color=colors[row['Series']])

# Title and display the plot
plt.title("Electron Transitions for an Atom")
plt.show()
