import h5py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

# Load data from HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/78_h5_data.h5"
f = h5py.File(file_path, 'r')

# Extract data from the specified columns in the dataset
data = f["0-60 mph(sec)"][:], f["Gas Mileage(mpg)"][:], f["Power(kW)"][:], f["Weight(kg)"][:], f["Engine Displacement(cc)"][:]

# Convert data to numpy arrays for easier manipulation
x = np.array(data[0])
y = np.array(data[1])
z = np.array(data[2])
weight = np.array(data[3])
disp = np.array(data[4])

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the main data points with color mapping to engine displacement
sc = ax.scatter(x, y, z, c=disp, s=weight*0.1, cmap=cm.viridis, alpha=0.7)

# Add a color bar to show the correlation between color and engine displacement
cbar = plt.colorbar(sc)
cbar.set_label('Engine Displacement (cc)')

# Set labels for each axis
ax.set_xlabel("0-60 mph (sec)")
ax.set_ylabel("Gas Mileage (mpg)")
ax.set_zlabel("Power (kW)")

# Create projections on XY, ZX, and YZ planes
ax.scatter(x, y, np.zeros_like(x), c='blue', alpha=0.3)  # XY plane projection
ax.scatter(z, np.zeros_like(z), x, c='red', alpha=0.3)   # ZX plane projection
ax.scatter(np.zeros_like(y), y, z, c='green', alpha=0.3) # YZ plane projection

# Show the plot
plt.show()
