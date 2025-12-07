import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import h5py

# Define the path to your HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/99_h5_data.h5"

# Open the HDF5 file
with h5py.File(file_path, 'r') as file:
    # Load the dataset into a pandas DataFrame
    data = pd.DataFrame(file['your_dataset_name'])  # Replace 'your_dataset_name' with the actual name of your dataset in HDF5

# Rename columns if necessary to match the input description
data.rename(columns={'total_bill': 'total_bill', 'tip': 'tip', 'sex': 'sex', 'smoker': 'smoker', 'day': 'day', 'time': 'time', 'size': 'size'}, inplace=True)

# Create a dark-themed plot
sns.set(style="whitegrid")  # Set the style to whitegrid for better contrast with dark theme
plt.figure(figsize=(12, 8))
sns.violinplot(x='day', y='total_bill', hue='smoker', data=data, split=True, palette={'Yes': 'green', 'No': 'grey'}, inner="quartile")

# Add title and labels
plt.title('Total Bill Amounts by Day of the Week (Smokers vs Non-Smokers)')
plt.xlabel('Day of the Week')
plt.ylabel('Total Bill Amount')

# Show legend
plt.legend(title='Smoker', loc='upper right')

# Adjust layout for better readability
plt.tight_layout()

# Save or show the plot
plt.show()  # Use plt.savefig('path_to_save_plot') to save the plot if needed
