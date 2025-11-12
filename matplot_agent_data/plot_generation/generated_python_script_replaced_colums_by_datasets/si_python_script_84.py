import h5py
import matplotlib.pyplot as plt
import numpy as np

# Open the HDF5 file
file_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/84_h5_data.h5'
with h5py.File(file_path, 'r') as file:
    # Extract data from datasets 1 and 2 for the gas-liquid line
    temperature_gas_liquid = file['dataset1'][:]
    pressure_gas_liquid = file['dataset2'][:]
    
    # Convert temperatures to Celsius if they are in Kelvin
    temperature_gas_liquid += 273.15
    
    # Extract data from datasets 3 and 4 for the solid-liquid line
    temperature_solid_liquid = file['dataset3'][:]
    pressure_solid_liquid = file['dataset4'][:]
    
    # Convert temperatures to Celsius if they are in Kelvin
    temperature_solid_liquid += 273.15
    
# Create the plot
plt.figure(figsize=(10, 8))
ax = plt.gca()

# Plot the solid-liquid line
ax.plot(temperature_solid_liquid, pressure_solid_liquid, label='Solid-Liquid', color='blue')

# Plot the gas-liquid line
ax.plot(temperature_gas_liquid, pressure_gas_liquid, label='Gas-Liquid', color='green')

# Mark the triple point (273.16 K and 611.657 Pa)
plt.scatter(273.16, 611.657, color='black', marker='o', label='Triple Point')

# Mark the critical point (647.396 K and 22.064 MPa)
critical_pressure = 22.064 * 1e6  # Convert MPa to Pa
plt.scatter(647.396, critical_pressure, color='red', marker='x', label='Critical Point')

# Draw vertical lines for freezing (0°C or 273.15 K) and boiling points of water at normal pressure (100°C or 373.15 K)
plt.axvline(x=273.15, color='red', linestyle='--')
plt.axvline(x=373.15, color='red', linestyle='--')

# Label axes and add title
plt.xlabel('Temperature (°C)')
plt.ylabel('Pressure (Pa)')
plt.title('Phase Diagram of Water')
plt.legend()

# Set pressure scale to logarithmic
ax.set_yscale('log')

# Add grid for better readability
plt.grid(True)

# Show the plot
plt.show()
