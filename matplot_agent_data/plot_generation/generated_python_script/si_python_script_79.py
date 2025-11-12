import h5py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Open the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/79_h5_data.h5"
with h5py.File(file_path, 'r') as file:
    # Load the dataset
    data = file['dataset']  # Assuming the dataset is directly in the root level
    
    # Extract columns for plotting
    petal_length = data['Petal Length(cm)'][:]
    petal_width = data['Petal Width(cm)'][:]
    sepal_length = data['Sepal Length(cm)'][:]
    species = data['Species'][:]
    
# Separate the data by species
species_set = np.unique(species)
colors = {
    'setosa': 'red',
    'versicolor': 'green',
    'virginica': 'blue'
}

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot each species with distinct colors and confidence ellipses
for specie in species_set:
    indices = np.where(species == specie)
    x = petal_length[indices]
    y = petal_width[indices]
    z = sepal_length[indices]
    
    ax.scatter(x, y, z, c=colors[specie], label=specie)
    
    # Calculate covariance matrix for confidence ellipses
    mean_vector = np.mean([x, y, z], axis=1)
    cov_matrix = np.cov(np.transpose([x, y, z]))
    
    # Plot the ellipse
    from scipy.stats import chi2
    alpha = 0.95  # 95% confidence level
    df = len(mean_vector)
    critval = chi2.ppf((1-alpha), df)
    
    eigvals, eigvecs = np.linalg.eig(cov_matrix)
    order = eigvals.argsort()[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]
    
    # Ellipse scaling factor based on the critical value of chi-square distribution
    scale_factor = np.sqrt(critval * eigvals)
    
    angle = np.linspace(0, 2*np.pi, 100)
    ellipse_x = mean_vector[0] + scale_factor[0]*np.cos(angle) @ eigvecs[:, 0]
    ellipse_y = mean_vector[1] + scale_factor[1]*np.sin(angle) @ eigvecs[:, 1]
    ellipse_z = mean_vector[2] + np.zeros(len(angle)) * scale_factor[2]
    
    ax.plot(ellipse_x, ellipse_y, ellipse_z, color=colors[specie], alpha=0.5)

# Set labels and legend
ax.set_xlabel('Petal Length (cm)')
ax.set_ylabel('Petal Width (cm)')
ax.set_zlabel('Sepal Length (cm)')
plt.legend()

# Show the plot
plt.show()
