import h5py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Load the HDF5 file and dataset
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/77_h5_data.h5"
dataset_name = "protein_consumption"
with h5py.File(file_path, 'r') as file:
    data = pd.DataFrame(file[dataset_name][:], columns=["Country", "Red Meat", "White Meat", "Eggs", "Milk", "Fish", "Cereals", "Starch", "Nuts", "Fruits & Vegetables"])

# Prepare the data for clustering (excluding the 'Country' column)
X = data.iloc[:, 1:].values

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
data['Cluster'] = kmeans.fit_predict(X_scaled)

# Plotting the data points with cluster coloring and centroids
plt.figure(figsize=(12, 8))
colors = ['r', 'g', 'b']
for i in range(3):
    plt.scatter(data[data['Cluster'] == i].iloc[:, 1], data[data['Cluster'] == i].iloc[:, 2], c=colors[i], label='Cluster '+str(i), alpha=0.5)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='yellow', marker='*', label='Centroids')

# Adding ellipses around clusters (not standard in scatter plot but can be added using other methods)
# This requires additional plotting code to draw ellipses based on covariance matrix of each cluster

# Annotate each point with country names
for i, txt in enumerate(data['Country']):
    plt.annotate(txt, (data.iloc[i, 1], data.iloc[i, 2]), fontsize=8)

plt.xlabel("Red Meat")
plt.ylabel("White Meat")
plt.title("K-Means Clustering of Protein Consumption Data")
plt.legend()
plt.show()
