import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import h5py

# Load the HDF5 dataset
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/96_h5_data.h5"
dataset_name = "sales_data"  # Assuming the dataset name in HDF5 is 'sales_data'

# Open the HDF5 file and load the dataset into a pandas DataFrame
with h5py.File(file_path, 'r') as file:
    data = pd.DataFrame(file[dataset_name])

# Rename columns for better understanding
data.columns = ["Quarter", "Samsung", "Nokia/Microsoft", "Apple", "LG", "ZTE", "Huawei"]

# Set the style of the seaborn plot
sns.set(style="whitegrid")

# Create a figure with subplots for each brand's boxplot
plt.figure(figsize=(14, 8))

# List to store average values for lines
average_sales = []

# Plotting the box plots and collecting average sales
brands = ["Samsung", "Nokia/Microsoft", "Apple", "LG", "ZTE", "Huawei"]
colors = sns.color_palette("husl", len(data["Quarter"].unique()))  # Generate distinct colors for each quarter

for i, brand in enumerate(brands):
    plt.subplot(2, 3, i + 1)
    sns.boxplot(x="Quarter", y=brand, data=data, palette=colors)
    sns.stripplot(x="Quarter", y=brand, data=data, color=".3")  # Add individual data points
    
    # Calculate the average sales for this brand and store it
    avg_sales = data[[brand]].mean()
    average_sales.append(avg_sales)

# Convert list of Series to DataFrame for plotting lines
average_df = pd.DataFrame(average_sales, index=brands).T

# Plot the average sales line across all box plots
for i in range(len(average_df.columns)):
    plt.plot(average_df.index, average_df[i], label=f"Average {average_df.columns[i]}", color=colors[i])

# Add legend and labels
plt.legend()
plt.xlabel("Quarter")
plt.ylabel("Sales")
plt.title("Box Plots of Mobile Phone Sales by Brand, with Average Lines")
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()
