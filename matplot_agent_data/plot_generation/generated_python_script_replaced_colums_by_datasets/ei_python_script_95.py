import numpy as np
import matplotlib.pyplot as plt
import h5py

# Load the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/95_h5_data.h5"
f = h5py.File(file_path, 'r')

# Extract the temperature data for the specified date range
years = f['Year'][:]
dates = f['Date'][:]
temperatures = f['Temperature'][:]

# Filter data from January 1, 2004, to August 1, 2015
start_date = np.datetime64('2004-01-01')
end_date = np.datetime64('2015-08-01')
mask = (years >= start_date) & (years <= end_date)
filtered_temperatures = temperatures[mask]
filtered_dates = dates[mask]

# Extract months and years from the filtered dates
months = np.array([dt.month for dt in filtered_dates])
years_filtered = np.array([dt.year for dt in filtered_dates])

# Initialize lists to store temperature data by month
monthly_temperatures = {i: [] for i in range(1, 13)}

# Populate the list with temperatures according to their months
for year, temp in zip(years_filtered, filtered_temperatures):
    monthly_temperatures[year].append(temp)

# Calculate the mean temperature for each month
mean_temperatures = [np.mean(temps) for temps in monthly_temperatures.values()]

# Define the angles for the polar plot (each month is π/6 radians apart)
angles = np.linspace(0, 2 * np.pi, 12, endpoint=False).tolist()

# Shift the angles to avoid overlapping points on a single radial line
shifted_angles = [angle + i * (np.pi / 6) for i, angle in enumerate(angles)]

# Plotting the polar plot
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, projection='polar')

# Plot the mean temperatures with a blue curve
ax.plot(shifted_angles, mean_temperatures, 'bo-', label='Mean Temperature')

# Add month labels
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ax.set_thetagrids(np.degrees(angles), labels=month_labels)

# Set the title and legend
plt.title("Mean Temperature by Month (2004-2015)")
plt.legend(loc='right', bbox_to_anchor=(1.2, 0))

# Show the plot
plt.show()
