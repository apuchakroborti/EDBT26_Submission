import h5py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from matplotlib.patches import Ellipse

# Load the dataset from HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/77_h5_data.h5"
with h5py.File(file_path, 'r') as file:
    data = np.array([file[name][:] for name in ["Country", "Red Meat", "White Meat", "Eggs", "Milk", "Fish", "Cereals", "Starch", "Nuts", "Fruits & Vegetables"]])
    dataset = data.T  # Transpose to have countries as rows and features as columns

# Perform PCA for dimensionality reduction
pca = PCA(n_components=2)
pca_result = pca.fit_transform(dataset[:, 1:])  # Apply PCA excluding the country names

# Apply K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(pca_result)
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

# Plotting
plt.figure(figsize=(10, 8))
colors = ['blue', 'red', 'green']
for i in range(3):
    cluster_points = pca_result[labels == i]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], c=colors[i], label=f'Cluster {i}', alpha=0.6)
    
    # Draw ellipse around the cluster
    cov = np.cov(cluster_points, rowvar=False)
    lambda_, v = np.linalg.eig(cov)
    angle = np.degrees(np.arctan2(v[0, 1], v[0, 0]))
    width, height = 2 * np.sqrt(lambda_)
    ellipse = Ellipse(xy=centroids[i], width=width, height=height, angle=angle, color=colors[i], alpha=0.3)
    plt.gca().add_patch(ellipse)
    
    # Connect each point to the centroid with a thick grey line
    for j in range(len(cluster_points)):
        plt.plot([cluster_points[j, 0], centroids[i, 0]], [cluster_points[j, 1], centroids[i, 1]], 'k-', alpha=0.7)

# Annotate each point with country names
for i, txt in enumerate(dataset[:, 0]):
    plt.annotate(txt, (pca_result[i, 0], pca_result[i, 1]), fontsize=8)

plt.title('K-Means Clustering with PCA-reduced Data and Colored Ellipses')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid(True)
plt.legend()
plt.show()
