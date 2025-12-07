import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Define the path to your HDF5 file
file_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/83_h5_data.h5'

# Read the data from the HDF5 file
df = pd.read_hdf(file_path, key='your_dataset_name')  # Replace 'your_dataset_name' with the actual dataset name if different

# Convert the date column to datetime format for proper plotting
df['date'] = pd.to_datetime(df['date'])

# Set the date column as the index of the DataFrame
df.set_index('date', inplace=True)

# Plotting the data
plt.figure(figsize=(14, 7))

# Plot the daily DJIA values
plt.plot(df.index, df['Dow Jones Industrial Average'], label='DJIA', color='blue')

# Plot the 1-year moving average
plt.plot(df.index, df['1 year moving average'], label='1 Year Moving Avg', color='red')

# Fill the area between the two lines
plt.fill_between(df.index, df['Dow Jones Industrial Average'], df['1 year moving average'], color='lightblue', alpha=0.5)

# Set the title and labels for the plot
plt.title('DJIA and 1-Year Moving Average from Oct 2006 to Aug 2013')
plt.xlabel('Date')
plt.ylabel('Value')

# Format the X-axis to display dates properly
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator())

# Add a legend
plt.legend()

# Show the plot
plt.show()
