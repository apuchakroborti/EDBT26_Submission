import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch

# Define file path and dataset names
file_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/83_h5_data.h5'
dataset_names = {
    'date': 'date',
    'Dow Jones Industrial Average': 'Dow Jones Industrial Average',
    '1 year moving average': '1 year moving average'
}

# Read the data from HDF5 file
df = pd.read_hdf(file_path, key=list(dataset_names.values())[0])
for name in dataset_names:
    df[name] = pd.read_hdf(file_path, key=dataset_names[name])

# Convert 'date' column to datetime if not already
df['date'] = pd.to_datetime(df['date'])

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['Dow Jones Industrial Average'], label='Dow Jones Industrial Average', color='blue')
plt.plot(df['date'], df['1 year moving average'], label='1 Year Moving Average', color='red')

# Coloring the area between the two lines
ax = plt.gca()
ax.fill_between(df['date'], df['Dow Jones Industrial Average'], df['1 year moving average'], where=(df['Dow Jones Industrial Average'] >= df['1 year moving average']), color='green', alpha=0.3)
ax.fill_between(df['date'], df['Dow Jones Industrial Average'], df['1 year moving average'], where=(df['Dow Jones Industrial Average'] < df['1 year moving average']), color='red', alpha=0.3)

# Formatting the date axis for better readability
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gcf().autofmt_xdate()

# Adding title and labels
plt.title('Dow Jones Industrial Average from October 2006 to August 2013')
plt.xlabel('Date')
plt.ylabel('Values')

# Adding legend
legend_elements = [Patch(facecolor='green', edgecolor='black', alpha=0.3, label='Above or Equal Moving Average'),
                    Patch(facecolor='red', edgecolor='black', alpha=0.3, label='Below Moving Average')]
plt.legend(handles=legend_elements)

# Display the plot
plt.show()
