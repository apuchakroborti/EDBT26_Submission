import h5py
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Load data from HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/95_h5_data.h5"
f = h5py.File(file_path, 'r')
data = f['Temperature'][:]  # Assuming "Temperature" is the dataset name

# Extract year and month from the date column (assuming it's in a format like YYYY-MM)
dates = [datetime.strptime(date, '%Y-%m') for date in f['Date'][:]]
years = np.array([date.year for date in dates])
months = np.array([date.month for date in dates])
temperatures = data

# Filter data for the year 2015 and other years
is_2015 = (years == 2015)
temperatures_2015 = temperatures[is_2015]
months_2015 = months[is_2015]

# Create a polar plot with offset points for each month
plt.figure(figsize=(8, 6))
ax = plt.subplot(111, projection='polar')

# Define the number of sectors (months) and calculate offsets
num_months = 12
month_offsets = np.linspace(0, np.pi/6, num_months)

# Plot each month's data with an offset
for i in range(num_months):
    mask = (months == (i + 1))
    temperatures_per_month = temperatures[mask]
    ax.scatter(np.arange(len(temperatures_per_month)) * np.pi/6 + month_offsets[i], temperatures_per_month, label=datetime(1900, i+1, 1).strftime('%b'), s=50)

# Plot the curve for 2015
ax.plot(np.arange(len(temperatures_2015)) * np.pi/6 + month_offsets[months_2015 - 1], temperatures_2015, label='2015', color='blue')

# Set labels and title
ax.set_thetagrids([i for i in range(0, 361, 30)], labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax.set_rlabel_position(270)
plt.title("Temperature Data by Month (2004-2015)")

# Add legend and adjust layout to avoid overlap
plt.legend(loc='right', bbox_to_anchor=(1.3, 0.5))
plt.tight_layout()
plt.show()
