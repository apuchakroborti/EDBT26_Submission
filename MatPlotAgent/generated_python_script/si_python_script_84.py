import h5py
import matplotlib.pyplot as plt
import numpy as np

# Open the HDF5 file
file_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/84_h5_data.h5'
with h5py.File(file_path, 'r') as file:
    # Assuming the data is in a dataset named "data" and has at least 4 columns for temperature, pressure, etc.
    data = file["data"][:]

# Extract temperatures and pressures from the dataset
temperatures = data[:, 0]  # First column should be temperature
pressures = data[:, 1]    # Second column should be pressure

# Create a new figure
plt.figure(figsize=(10, 8))

# Plotting the phase diagram
plt.scatter(temperatures, pressures, label='Data Points', color='blue')

# Marking the triple point and critical point
triple_point = [273.16, 611.657]
critical_point = [647.396, 22.064e6]
plt.scatter(triple_point[0], triple_point[1], color='black', label='Triple Point')
plt.scatter(critical_point[0], critical_point[1], color='red', label='Critical Point')

# Adding vertical lines for freezing and boiling points at normal pressure (0°C and 100°C)
freezing_point = [0, 611.657]
boiling_point = [100, 22.064e6]
plt.axvline(x=0, color='green', linestyle='--', label='Freezing Point (0°C)')
plt.axvline(x=100, ymin=0.05, ymax=0.95, color='orange', linestyle='--', label='Boiling Point (100°C)')

# Setting axis labels and title
plt.xlabel('Temperature (°C or K)')
plt.ylabel('Pressure (Pa or bar)')
plt.title('Phase Diagram of Water')
plt.legend()

# Converting pressure to bars for better readability in the diagram
pressure_bars = pressures / 1e5
plt.yscale('log')

# Adding a grid
plt.grid(True)

# Show the plot
plt.show()
