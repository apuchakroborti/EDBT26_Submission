import h5py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

# Load data from HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/78_h5_data.h5"
f = h5py.File(file_path, 'r')

# Extract dataset columns
x = f['0-60 mph(sec)'][:]
y = f['Gas Mileage(mpg)'][:]
z = f['Power(kW)'][:]
size = f['Engine Displacement(cc)'][:]

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(x, y, z, c=size, s=50*np.sqrt(size), cmap='viridis', alpha=0.6)

# Set labels for axes
ax.set_xlabel('0-60 mph (sec)')
ax.set_ylabel('Gas Mileage (mpg)')
ax.set_zlabel('Power (kW)')

# Add color bar to show the relationship between size and engine displacement
cbar = plt.colorbar(scatter)
cbar.set_label('Engine Displacement (cc)')

# Create projections on XY, ZX, and YZ planes
ax2 = fig.add_subplot(131)
ax2.scatter(x, y, c='blue')
ax2.set_title('XY Plane Projection')
ax2.set_xlabel('0-60 mph (sec)')
ax2.set_ylabel('Gas Mileage (mpg)')

ax3 = fig.add_subplot(132)
ax3.scatter(z, x, c='red')
ax3.set_title('ZX Plane Projection')
ax3.set_xlabel('Power (kW)')
ax3.set_ylabel('0-60 mph (sec)')

ax4 = fig.add_subplot(133)
ax4.scatter(y, z, c='green')
ax4.set_title('YZ Plane Projection')
ax4.set_xlabel('Gas Mileage (mpg)')
ax4.set_ylabel('Power (kW)')

plt.show()
