import h5py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd

# Load the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/77_h5_data.h5"
f = h5py.File(file_path, 'r')
dataset = f['data']  # Assuming the dataset is named "data" in the HDF5 file

# Extract data from the dataset
data = pd.DataFrame(dataset[:], columns=["Country", "Red Meat", "White Meat", "Eggs", "Milk", "Fish", "Cereals", "Starch", "Nuts", "Fruits & Vegetables"])

# Convert DataFrame to numpy array for clustering
X = data[["Red Meat", "White Meat", "Eggs", "Milk", "Fish", "Cereals", "Starch", "Nuts", "Fruits & Vegetables"]].values

# Perform K-Means clustering with 3 clusters
kmeans = KMeans(n_clusters=3, random_state=0)
data['Cluster'] = kmeans.fit_predict(X)

# Plotting the data points and centroids
plt.figure(figsize=(12, 8))
colors = ['blue', 'green', 'red']
markers = ['o', 's', '^']

for cluster in range(3):
    plt.scatter(data[data['Cluster'] == cluster]["Red Meat"], data[data['Cluster'] == cluster]["White Meat"], 
                c=colors[cluster], label='Cluster '+str(cluster), marker=markers[cluster])

# Plot centroids and connect them to the points
centroids = kmeans.cluster_centers_
for i, centroid in enumerate(centroids):
    plt.scatter(centroid[0], centroid[1], c='black', s=100, alpha=0.75)  # Centroid point
    for j in range(len(data[data['Cluster'] == i])):
        plt.plot([data.iloc[i]['Red Meat'], centroid[0]], [data.iloc[i]['White Meat'], centroid[1]], 'k--', alpha=0.5)

# Annotate each point with country names
for i, txt in enumerate(data['Country']):
    plt.annotate(txt, (data.iloc[i]["Red Meat"], data.iloc[i]["White Meat"]), fontsize=8)

plt.xlabel("Red Meat")
plt.ylabel("White Meat")
plt.title("K-Means Clustering of Protein Consumption Data")
plt.legend()
plt.show()
