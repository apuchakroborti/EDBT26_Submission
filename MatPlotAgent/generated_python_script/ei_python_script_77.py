import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import h5py

# Load the data from HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/77_h5_data.h5"
data = pd.read_hdf(file_path, key="dataset")  # Assuming the dataset is named "dataset" in the HDF5 file

# Extract features and scale them if necessary (though not explicitly required here)
X = data[["Red Meat", "White Meat", "Eggs", "Milk", "Fish", "Cereals", "Starch", "Nuts", "Fruits & Vegetables"]]

# Perform PCA for dimensionality reduction to 2D
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# Apply K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
data['Cluster'] = kmeans.fit_predict(X_pca)

# Plotting
plt.figure(figsize=(10, 8))
colors = ['blue', 'red', 'green']
markers = ['o', 's', '^']

for cluster in range(3):
    plt.scatter(X_pca[data['Cluster'] == cluster, 0], X_pca[data['Cluster'] == cluster, 1], c=colors[cluster], label=f'Cluster {cluster}', marker=markers[cluster])
    
# Draw ellipses around clusters
for cluster in range(3):
    plt.scatter([], [], color=colors[cluster], alpha=0.5, edgecolor='k', linewidths=1, label=f'Cluster {cluster}')  # Dummy plot for legend
    cov = np.cov(X_pca[data['Cluster'] == cluster].T)
    lambda_, v = np.linalg.eig(cov)
    lambda_ = np.sqrt(lambda_)
    if any(np.isnan(lambda_).values):  # Check for NaN values in eigenvalues
        continue
    theta = np.degrees(np.arctan2(*v[::-1]))
    width, height = 2 * np.sqrt(5.99 * lambda_)
    ell = plt.Ellipse(kmeans.cluster_centers_[cluster], width, height, theta, color=colors[cluster], alpha=0.3)
    ax = plt.gca()
    ax.add_artist(ell)
    
# Connect each data point to the centroid with a thick grey line
for i in range(len(X_pca)):
    plt.plot([X_pca[i, 0], kmeans.cluster_centers_[data['Cluster'].iloc[i]][0]], [X_pca[i, 1], kmeans.cluster_centers_[data['Cluster'].iloc[i]][1]], 'k-', alpha=0.7)

# Annotate each data point with the country name
for i, txt in enumerate(data['Country']):
    plt.annotate(txt, (X_pca[i, 0], X_pca[i, 1]), fontsize=8)

plt.title('K-Means Clustering with PCA-reduced Data and Colored Ellipses')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.grid(True)
plt.show()
