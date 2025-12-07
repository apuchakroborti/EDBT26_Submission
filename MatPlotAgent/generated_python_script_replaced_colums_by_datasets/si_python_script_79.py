import h5py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Open the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/79_h5_data.h5"
with h5py.File(file_path, 'r') as file:
    # Load the datasets
    petal_length = file["Petal Length(cm)"][:]
    petal_width = file["Petal Width(cm)"][:]
    sepal_length = file["Sepal Length(cm)"][:]
    species = file["Species"][:].astype('U')  # Assuming 'Species' is categorical and stored as strings

# Separate data by species
species_set = np.unique(species)
colors = plt.cm.get_cmap('viridis', len(species_set))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i, species_name in enumerate(species_set):
    mask = species == species_name
    x = petal_length[mask]
    y = petal_width[mask]
    z = sepal_length[mask]
    
    # Plot the 3D scatter points
    ax.scatter(x, y, z, c=[colors(i) for _ in range(np.sum(mask))], label=species_name)
    
    # Calculate and plot confidence ellipses
    cov = np.cov(x, y)  # Covariance matrix
    mean = [np.mean(x), np.mean(y)]
    eigval, eigvec = np.linalg.eig(cov)
    angle = np.degrees(np.arctan2(eigvec[1, 0], eigvec[0, 0]))
    
    # Ellipse parameters
    width, height = 2 * np.sqrt(eigval)
    ellip = plt.matplotlib.patches.Ellipse(mean, width, height, angle, color=colors(i), alpha=0.6)
    ax.add_artist(ellip)

# Set labels and legend
ax.set_xlabel('Petal Length (cm)')
ax.set_ylabel('Petal Width (cm)')
ax.set_zlabel('Sepal Length (cm)')
plt.legend()

# Show the plot
plt.show()
