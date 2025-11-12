import h5py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Load the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/78_h5_data.h5"
f = h5py.File(file_path, 'r')

# Extract datasets
acceleration_time = f["0-60 mph(sec)"][:]
gas_mileage = f["Gas Mileage(mpg)"][:]
power = f["Power(kW)"][:]
weight = f["Weight(kg)"][:]
engine_displacement = f["Engine Displacement(cc)"][:]

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the points with size and color based on engine displacement
scatter = ax.scatter(acceleration_time, gas_mileage, power, c=engine_displacement, s=weight/50, cmap='viridis')

# Add a color bar to show the relationship between color and engine displacement
cbar = plt.colorbar()
cbar.set_label('Engine Displacement (cc)')

# Label each axis
ax.set_xlabel('Acceleration Time (sec)')
ax.set_ylabel('Gas Mileage (mpg)')
ax.set_zlabel('Power (kW)')

# Add flat projections of the points onto the XY, ZX, and YZ planes
ax.view_init(30)  # Adjust view angle for better perspective

# Create additional plots for side, bottom, and front views
def add_flat_projection(plane):
    if plane == 'xy':
        ax2 = fig.add_subplot(1, 3, 1)
        ax2.scatter(acceleration_time, gas_mileage, color='blue')
        ax2.set_xlabel('Acceleration Time (sec)')
        ax2.set_ylabel('Gas Mileage (mpg)')
    elif plane == 'zx':
        ax3 = fig.add_subplot(1, 3, 2)
        ax3.scatter(weight, power, color='red')
        ax3.set_xlabel('Weight (kg)')
        ax3.set_ylabel('Power (kW)')
    elif plane == 'yz':
        ax4 = fig.add_subplot(1, 3, 3)
        ax4.scatter(weight, acceleration_time, color='green')
        ax4.set_xlabel('Weight (kg)')
        ax4.set_ylabel('Acceleration Time (sec)')

# Add flat projections for XY, ZX, and YZ planes
add_flat_projection('xy')
add_flat_projection('zx')
add_flat_projection('yz')

plt.show()
