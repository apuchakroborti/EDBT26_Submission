import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from h5py import File

# Define file path
file_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/83_h5_data.h5'

# Open the HDF5 file
with File(file_path, 'r') as f:
    # Read datasets into pandas DataFrames
    date = pd.DataFrame(f['date'][:], columns=['Date'])
    dow_jones = pd.DataFrame(f['Dow Jones Industrial Average'][:], columns=['Dow Jones'])
    moving_avg = pd.DataFrame(f['1 year moving average'][:], columns=['Moving Avg'])

# Merge DataFrames to have all data in one DataFrame
data = pd.concat([date, dow_jones, moving_avg], axis=1)

# Convert 'Date' column to datetime if not already
data['Date'] = pd.to_datetime(data['Date'])

# Plotting the data
plt.figure(figsize=(14, 7))

# Plot Dow Jones Industrial Average
plt.plot(data['Date'], data['Dow Jones'], label='Dow Jones Industrial Average', color='blue')

# Plot 1 year moving average
plt.plot(data['Date'], data['Moving Avg'], label='1 Year Moving Average', color='red')

# Fill the area between the two lines
plt.fill_between(data['Date'], data['Dow Jones'], data['Moving Avg'], where=data['Dow Jones'] >= data['Moving Avg'], facecolor='green', alpha=0.3)
plt.fill_between(data['Date'], data['Dow Jones'], data['Moving Avg'], where=data['Dow Jones'] <= data['Moving Avg'], facecolor='red', alpha=0.3)

# Adding title and labels
plt.title('Dow Jones Industrial Average from October 2006 to August 2013')
plt.xlabel('Date')
plt.ylabel('Value')

# Formatting date labels for better readability
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

# Adding legend
plt.legend()

# Display the plot
plt.show()
