import h5py
import seaborn as sns
import matplotlib.pyplot as plt

# Define the path to your HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/99_h5_data.h5"

# Open the HDF5 file
with h5py.File(file_path, 'r') as file:
    # Load the datasets into variables
    total_bill = file['total_bill'][:]
    day = file['day'][:]
    smoker = file['smoker'][:]

# Create a DataFrame for Seaborn to use
import pandas as pd
data = {'total_bill': total_bill, 'day': day.astype(str), 'smoker': smoker.astype(str)}
df = pd.DataFrame(data)

# Set the style of the plot
sns.set_style("dark")

# Create the violin plot
plt.figure(figsize=(10, 6))
sns.violinplot(x='day', y='total_bill', hue='smoker', data=df, split=True, inner='quartile', palette={'yes': 'green', 'no': 'grey'})

# Add title and labels
plt.title('Distribution of Total Bills by Day and Smoker Status')
plt.xlabel('Day of the Week')
plt.ylabel('Total Bill Amount')

# Show the plot
plt.show()
