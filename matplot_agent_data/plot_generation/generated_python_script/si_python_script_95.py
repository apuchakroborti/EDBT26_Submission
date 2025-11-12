import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from h5py import File

# Define the path to your HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/95_h5_data.h5"

# Open the HDF5 file
with File(file_path, 'r') as file:
    # Load the data from a dataset in the HDF5 file
    data = pd.DataFrame(file['your_dataset_name'][:])  # Replace 'your_dataset_name' with the actual dataset name

# Convert Date column to datetime if not already done
data['Date'] = pd.to_datetime(data['Date'])

# Filter data for the specified period and extract the highest temperature on the first of each month
filtered_data = data[(data['Year'] >= 2004) & (data['Year'] <= 2015)]
monthly_max_temps = filtered_data.groupby([filtered_data['Date'].dt.month, filtered_data['Date'].dt.day]).max()
monthly_max_temps = monthly_max_temps.reset_index(drop=True)  # Reset index to have a clean DataFrame

# Prepare data for plotting
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
temperatures = monthly_max_temps['Temperature'].values

# Create a polar plot
fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'projection': 'polar'})

# Plot the temperatures with slight offset for each month
ax.scatter(np.deg2rad(np.arange(0, 360, 30)), temperatures, c=temperatures, cmap='viridis')

# Add a blue curve connecting data points from 2015
for year in range(2004, 2016):
    month_indices = np.where(monthly_max_temps['Year'] == year)[0]
    if len(month_indices) > 0:
        ax.plot([np.deg2rad(30 * (i + 1)) for i in range(len(month_indices))], temperatures[month_indices], 'b-')

# Set the labels and title
ax.set_thetagrids(np.arange(0, 360, 30), labels=months)
ax.set_title("Monthly Highest Temperature in Amherst (2004-2015)")
plt.legend(['2015'])

# Show the plot
plt.show()
