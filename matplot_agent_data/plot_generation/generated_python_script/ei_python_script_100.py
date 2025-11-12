import pandas as pd
import matplotlib.pyplot as plt
from math import pi

# Load the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/100_h5_data.h5"
df = pd.read_hdf(file_path)

# Sort the data by 'Series' column and group by series
grouped = df.sort_values('Series').groupby('Series')

# Define colors for each series
colors = plt.cm.get_cmap('viridis', len(grouped))

# Create a polar plot
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
ax.set_theta_zero_location("N")
ax.set_thetamin(-90)
ax.set_thetamax(90)

# Define energy levels and labels
energy_levels = range(1, 7)
energy_labels = [f"{i}n" for i in energy_levels]
energy_values = [0, 10.2, 12.09, 12.75, 13.06, 13.22]

# Plot the radial divisions and labels
ax.set_rticks(energy_values)
ax.set_rlabel_text([''] + energy_labels)

# Draw black lines for each energy level
for i in range(len(energy_levels)):
    ax.plot([0, pi], [i+1, i+1], 'k-')

# Plot transitions as arrows
for name, group in grouped:
    color = colors(group['Series'].first())
    for idx, row in group.iterrows():
        start_angle = (row['l position'] - 1) * pi / 3  # Assuming l and p positions range from 1 to 6
        end_angle = (row['p position'] - 1) * pi / 3
        ax.arrow(start_angle, energy_levels[group['Series'].first() % len(energy_levels)] - 0.5, 
                 end_angle - start_angle, 0, color=color, head_width=0.1, length_includes_head=True)
        ax.text(end_angle, energy_levels[group['Series'].first() % len(energy_levels)] - 0.5, 
                f"{row['Wavelength']} eV", ha='center', va='center')

# Set title and axis properties
ax.set_title("Electron Transitions for an Atom")
plt.show()
