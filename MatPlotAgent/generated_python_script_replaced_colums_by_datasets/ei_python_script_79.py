import h5py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import multivariate_normal
from matplotlib.patches import Ellipse

# Load the HDF5 file and dataset
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/79_h5_data.h5"
dataset_name = "Petal Length(cm)"  # This should be the full path to your dataset in HDF5

# Open the HDF5 file
with h5py.File(file_path, 'r') as file:
    data = file[dataset_name][:]

species = np.unique(data["Species"])
colors = ['red', 'green', 'blue']  # Corresponding colors for each species

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i, specie in enumerate(species):
    data_specie = data[data["Species"] == specie]
    
    # Plot the scatter points for each species with distinct colors
    ax.scatter(data_specie['Petal Length(cm)'], 
                data_specie['Petal Width(cm)'], 
                data_specie['Sepal Length(cm)'], 
                c=colors[i], label=specie, s=20)
    
    # Calculate mean for each species
    mean = np.mean(data_specie[['Petal Length(cm)', 'Petal Width(cm)', 'Sepal Length(cm)']], axis=0)
    
    # Compute the covariance matrix
    cov = np.cov(data_specie[['Petal Length(cm)', 'Petal Width(cm)', 'Sepal Length(cm)']].T)
    
    # Generate points on the ellipsoid surface
    x, y, z = np.random.multivariate_normal(mean, cov, 100).T
    
    # Plot the ellipsoid for each species
    plot_ellipsoid(ax, mean[0], mean[1], mean[2], cov, color=colors[i])

# Add axis labels and legend
ax.set_xlabel('Petal Length (cm)')
ax.set_ylabel('Petal Width (cm)')
ax.set_zlabel('Sepal Length (cm)')
plt.legend()
plt.show()

def plot_ellipsoid(ax, mean, cov, color='red'):
    # Generate points on the ellipsoid surface using a multivariate normal distribution
    u, s, v = np.linalg.svd(cov)
    radii = 2 * np.sqrt(np.diag(s))  # Radii corresponding to the eigenvalues of cov
    
    # Create an ellipsoid mesh
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]
    x = radii[0] * np.cos(u) * np.sin(v) + mean[0]
    y = radii[1] * np.sin(u) * np.sin(v) + mean[1]
    z = radii[2] * np.cos(v) + mean[2]
    
    # Plot the ellipsoid with specified color and opacity
    ax.plot_surface(x, y, z, rstride=4, cstride=4, color=color, alpha=.7)
