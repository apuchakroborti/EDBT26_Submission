import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import h5py

# Define file path and dataset name
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/96_h5_data.h5"
dataset_name = ["Quarter", "Samsung", "Nokia/Microsoft", "Apple", "LG", "ZTE", "Huawei"]

# Read the HDF5 file and extract the dataset
with h5py.File(file_path, 'r') as file:
    data = pd.DataFrame(file[dataset_name])
    data.columns = ["Quarter"] + [f"Brand_{i}" for i in range(1, 6)]

# Calculate the mean sales for each brand across all quarters
mean_sales = data[["Samsung", "Nokia/Microsoft", "Apple", "LG", "ZTE", "Huawei"]].mean()

# Prepare colors based on quarters (assuming a cyclic pattern)
quarters = data['Quarter'].unique()
colors = plt.cm.tab10.colors  # Use a colormap to cycle through colors
color_map = {quarter: colors[i % len(colors)] for i, quarter in enumerate(quarters)}

# Plotting the box plots and individual data points
fig, ax = plt.subplots()

boxprops = dict(linestyle='-', linewidth=2, color='black')
whiskerprops = dict(linestyle='--', linewidth=1, color='gray')
medianprops = dict(linewidth=2, color='red')

for i, brand in enumerate(["Samsung", "Nokia/Microsoft", "Apple", "LG", "ZTE", "Huawei"]):
    sales_data = data[brand]
    ax.boxplot(sales_data, positions=[i], boxprops=boxprops, whiskerprops=whiskerprops, medianprops=medianprops)
    ax.scatter(np.random.normal(range(len(sales_data)), 0.1), sales_data, color=color_map[sales_data.name[:-2]], alpha=0.5)

# Plot the mean lines
ax.plot([0, len(dataset_name)-1], [mean_sales['Samsung'], mean_sales['Samsung']], color='black', linestyle='-', label='Mean Samsung')
ax.plot([0, len(dataset_name)-1], [mean_sales['Nokia/Microsoft'], mean_sales['Nokia/Microsoft']], color='blue', linestyle='-', label='Mean Nokia/Microsoft')
ax.plot([0, len(dataset_name)-1], [mean_sales['Apple'], mean_sales['Apple']], color='green', linestyle='-', label='Mean Apple')
ax.plot([0, len(dataset_name)-1], [mean_sales['LG'], mean_sales['LG']], color='purple', linestyle='-', label='Mean LG')
ax.plot([0, len(dataset_name)-1], [mean_sales['ZTE'], mean_sales['ZTE']], color='orange', linestyle='-', label='Mean ZTE')
ax.plot([0, len(dataset_name)-1], [mean_sales['Huawei'], mean_sales['Huawei']], color='cyan', linestyle='-', label='Mean Huawei')

# Add legend and labels
ax.legend()
plt.xticks(range(len(dataset_name)), dataset_name, rotation=45)
plt.ylabel('Sales')
plt.title('Sales Data by Brand and Mean Values')

plt.show()
