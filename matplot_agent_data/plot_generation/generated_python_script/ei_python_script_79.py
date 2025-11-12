import h5py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import multivariate_normal
from matplotlib.patches import Ellipse

# Load the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/79_h5_data.h5"
f = h5py.File(file_path, 'r')

# Extract the data from the specified columns in the dataset
data = f["Petal Length(cm)"][:], f["Petal Width(cm)"][:], f["Sepal Length(cm)"][:]
species = f["Species"][:]

# List of unique species for plotting colors and legend
unique_species = np.unique(species)
colors = plt.cm.tab10.colors  # Use a colormap to assign distinct colors to each species

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i, sp in enumerate(unique_species):
    # Select data points for the current species
    selected_data = np.vstack([data[0][species == sp], data[1][species == sp], data[2][species == sp]]).T
    
    # Calculate mean and covariance matrix
    mean_vec = selected_data.mean(axis=0)
    cov_mat = np.cov(selected_data, rowvar=False)
    
    # Generate points on the ellipsoid surface
    def plot_ellipsoid(ax, mean, cov, color, alpha=0.3):
        v, w = np.linalg.eigh(cov)
        u = np.linspace(0, 2 * np.pi, 100)
        vv, ww = np.meshgrid(u, u)
        x = mean[0] + np.sqrt(v[0]) * (np.cos(vv) * np.sin(ww))
        y = mean[1] + np.sqrt(v[1]) * (np.sin(vv) * np.sin(ww))
        z = mean[2] + np.sqrt(v[2]) * np.cos(ww)
        
        ax.plot_surface(x, y, z, color=color, alpha=alpha)
    
    # Plot the ellipsoid for each species
    plot_ellipsoid(ax, mean_vec, cov_mat, colors[i % len(colors)])
    
    # Plot the data points for each species
    ax.scatter(selected_data[:, 0], selected_data[:, 1], selected_data[:, 2], color=colors[i % len(colors)], label=sp)

# Set axis labels and legend
ax.set_xlabel('Petal Length (cm)')
ax.set_ylabel('Petal Width (cm)')
ax.set_zlabel('Sepal Length (cm)')
plt.legend()

plt.show()
