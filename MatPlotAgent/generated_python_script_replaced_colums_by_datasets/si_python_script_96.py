import pandas as pd
import matplotlib.pyplot as plt
import h5py

# Load the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/96_h5_data.h5"
f = h5py.File(file_path, 'r')

# List of dataset names
dataset_names = ["Quarter", "Samsung", "Nokia/Microsoft", "Apple", "LG", "ZTE", "Huawei"]

# Read the datasets into a DataFrame
data = {name: f[name][()] for name in dataset_names}
df = pd.DataFrame(data)

# Set 'Quarter' as index
df.set_index('Quarter', inplace=True)

# Transpose the DataFrame to have brands as columns and quarters as rows
df_transposed = df.T

# Plotting
plt.figure(figsize=(14, 8))
brands = ["Samsung", "Nokia/Microsoft", "Apple", "LG", "ZTE", "Huawei"]
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']

# Create box plots for each brand with individual data points and average line
for i, brand in enumerate(brands):
    plt.boxplot(df_transposed[brand], positions=[i+1], widths=0.5, patch_artist=True)
    plt.scatter(np.repeat(i+1, len(df_transposed[brand])), df_transposed[brand], color='k', alpha=0.5)

# Calculate and plot the average sales for each brand
averages = df_transposed.mean()
plt.plot(range(1, len(brands)+1), averages, marker='o', linestyle='-', color='k')

# Customizing the plot
plt.xticks(range(1, len(brands)+1), brands, rotation=45)
plt.title('Sales Distribution and Average Values by Brand')
plt.xlabel('Brand')
plt.ylabel('Sales')
plt.grid(axis='y')

# Adding a legend for color coding (assuming different shades represent years which are not explicitly defined here)
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=f'Average {brand}', markerfacecolor=colors[i], markersize=8) for i, brand in enumerate(brands)]
plt.legend(handles=legend_elements, title="Legend")

# Show the plot
plt.tight_layout()
plt.show()
