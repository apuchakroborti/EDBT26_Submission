import h5py
import matplotlib.pyplot as plt
import numpy as np

# Open the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/84_h5_data.h5"
f = h5py.File(file_path, 'r')

# Extract data from datasets 1 and 2 for solid-liquid-gas boundary and critical point
temperature_solid_liquid_gas, pressure_solid_liquid_gas = f['dataset1'][:], f['dataset2'][:]

# Convert Kelvin to Celsius for the top X-axis
temperature_celsius = temperature_solid_liquid_gas - 273.15

# Extract data from datasets 3 and 4 for solid-liquid boundary
temperature_solid_liquid, pressure_solid_liquid = f['dataset3'][:], f['dataset4'][:]

# Convert pressures to bars for better visualization on the right Y-axis
pressure_bars = pressure_solid_liquid / 100000
pressure_log = np.log10(pressure_bars)

# Extract critical point data
critical_temperature, critical_pressure = f['dataset5'][:], f['dataset6'][:]

# Plotting setup
fig, ax = plt.subplots()

# Plot solid-liquid-gas boundary
ax.plot(temperature_celsius, pressure_solid_liquid_gas, label='Solid-Liquid-Gas Boundary')

# Plot solid-liquid boundary
ax.plot(temperature_solid_liquid - 273.15, pressure_solid_liquid / 100000, label='Solid-Liquid Boundary', color='gray')

# Mark special points
triple_point = (273.16 - 273.15, 611.657)
critical_point = (critical_temperature - 273.15, critical_pressure / 100000)
ax.scatter(*triple_point, color='black', label='Triple Point')
ax.scatter(*critical_point, color='red', label='Critical Point')

# Add red lines for freezing and boiling points
freezing_line = ax.axvline(x=0, color='red', linestyle='--')
boiling_line = ax.axvline(x=100, color='red', linestyle='--')

# Axis labels and title
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Pressure (bars)')
plt.title('Phase Diagram of Water')

# Legend
plt.legend()

# Grid and scaling
ax.grid(True)
ax.set_yscale('log')

# Annotate special points
ax.annotate('Triple Point', xy=triple_point, textcoords='offset points', xytext=(0,10), ha='center')
ax.annotate('Critical Point', xy=critical_point, textcoords='offset points', xytext=(0,10), ha='center')

# Show plot
plt.show()
