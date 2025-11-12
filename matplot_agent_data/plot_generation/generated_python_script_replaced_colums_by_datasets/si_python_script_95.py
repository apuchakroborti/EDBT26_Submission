import numpy as np
import matplotlib.pyplot as plt
import h5py
from datetime import datetime

# Load the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/95_h5_data.h5"
f = h5py.File(file_path, 'r')

# Extract the datasets
years = f['Year'][:]
dates = f['Date'][:]
temperatures = f['Temperature'][:]

# Convert dates to datetime objects for easier month extraction
date_strings = [datetime.strptime(str(year) + '-' + str(d), '%Y-%m-%d') for year, d in zip(years, dates)]
months = np.array([dt.month for dt in date_strings])

# Find the highest temperature for each month
monthly_max_temps = {}
for month in range(1, 13):
    mask = (months == month) & (years >= 2004) & (years <= 2015)
    if np.any(mask):
        monthly_max_temps[datetime(year=2004, month=month, day=1).strftime('%b')] = max(temperatures[mask])

# Prepare data for plotting
theta = list(monthly_max_temps.keys())
r = list(monthly_max_temps.values())

# Plotting
fig, ax = plt.subplots(nrows=1, ncol=1, subplot_kw={'projection': 'polar'})
ax.scatter(np.deg2rad(theta2num(theta)), r, c='blue', s=50)

# Connect the data points from 2015 if available
if 2015 in years:
    mask = (years == 2015)
    ax.plot(np.deg2rad(theta2num(list(monthly_max_temps.keys()))), temperatures[mask], c='blue')

# Customize the plot
ax.set_thetagrids(np.deg2rad([30*i for i in range(12)]), list(monthly_max_temps.keys()))
ax.set_title("Monthly Highest Temperature in Amherst (2004-2015)")
ax.legend(['Temperature Data'])
plt.show()
