import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Define the path to your HDF5 file
file_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/83_h5_data.h5'

# Read the data from the HDF5 file
df = pd.read_hdf(file_path, key='your_dataset_name')  # Replace 'your_dataset_name' with actual dataset name if different

# Convert the date column to datetime format for proper plotting
df['date'] = pd.to_datetime(df['date'])

# Plotting the data
plt.figure(figsize=(14, 7))

# Plotting the daily DJIA values
plt.plot(df['date'], df['Dow Jones Industrial Average'], label='Daily DJIA', color='blue')

# Plotting the 1-year moving average
plt.plot(df['date'], df['1 year moving average'], label='1 Year Moving Average', color='red')

# Filling the area between the two lines
plt.fill_between(df['date'], df['Dow Jones Industrial Average'], df['1 year moving average'], color='lightblue', alpha=0.5)

# Setting the title and labels
plt.title('DJIA from October 2006 to August 2013')
plt.xlabel('Date')
plt.ylabel('Value')

# Adjusting the X-axis to display dates properly
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator())

# Adding a legend
plt.legend()

# Displaying the plot
plt.show()
