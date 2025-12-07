import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set a dark style theme for Seaborn
sns.set_context("paper", font_scale=1.5)  # Adjusting the scale for better readability on paper-like context
sns.set_style("dark")

# Load the data from HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/99_h5_data.h5"
data = pd.read_hdf(file_path, key='your_table_name')  # Replace 'your_table_name' with the actual table name in HDF5 file

# Filter data for plotting: only consider 'total_bill' and 'day', distinguishing by 'smoker'
filtered_data = data[['total_bill', 'day', 'smoker']]

# Create the violin plot
plt.figure(figsize=(14, 8))
sns.violinplot(x='day', y='total_bill', hue='smoker', data=filtered_data, split=True, palette={'Yes': 'green', 'No': 'grey'})

# Adding labels and title
plt.xlabel('Day')
plt.ylabel('Total Bill')
plt.title('Violin Plot of Total Bills by Day and Smoker Status')
plt.legend(title='Smoker')

# Show the plot
plt.show()
