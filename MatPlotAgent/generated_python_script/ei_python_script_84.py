import h5py
import matplotlib.pyplot as plt
import numpy as np

# Open the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/84_h5_data.h5"
f = h5py.File(file_path, 'r')

# Extract data from the dataset (assuming columns are named appropriately)
temperature_K = f['temperature'][:]  # in Kelvin
pressure_Pa = f['pressure'][:]      # in Pascals
phase = f['phase'][:]                # phase information (e.g., solid, liquid, gas)

# Convert temperature to Celsius for plotting on the top X-axis
temperature_C = temperature_K - 273.15

# Convert pressure from Pa to bars for the right Y-axis
pressure_bars = pressure_Pa / 100000

# Create a figure and axes
fig, ax = plt.subplots()

# Plotting phase boundaries
for i in range(len(temperature_K)):
    if phase[i] == 1:  # Solid phase
        ax.plot(temperature_C[i], pressure_bars[i], 'bo')
    elif phase[i] == 2:  # Liquid phase
        ax.plot(temperature_C[i], pressure_bars[i], 'go')
    elif phase[i] == 3:  # Gas phase
        ax.plot(temperature_C[i], pressure_bars[i], 'yo')

# Plotting special points
triple_point = np.where((temperature_K == 273.16) & (pressure_Pa == 611.657))
critical_point = np.where((temperature_K == 647.396) & (pressure_Pa == 22064000))
if len(triple_point[0]) > 0:
    ax.plot(temperature_C[triple_point], pressure_bars[triple_point], 'ko', label='Triple Point')
if len(critical_point[0]) > 0:
    ax.plot(temperature_C[critical_point], pressure_bars[critical_point], 'ro', label='Critical Point')

# Adding red lines
ax.axvline(x=0, color='r', linestyle='--')  # Freezing point at 0°C and 1 atm
ax.axvline(x=100, color='r', linestyle='--')  # Boiling point at 100°C and 1 atm

# Labeling axes and adding legend
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Pressure (bars)')
plt.gca().invert_yaxis()  # Invert y-axis for better visualization of pressure
plt.legend()

# Adding grid and logarithmic scale for pressure if necessary
plt.grid(True)
if np.min(pressure_bars) < 10**(-2):  # Check if pressures are in the millibar range
    ax.set_yscale('log')

# Show plot
plt.show()
