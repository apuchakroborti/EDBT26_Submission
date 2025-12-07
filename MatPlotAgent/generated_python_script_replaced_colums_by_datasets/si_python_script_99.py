import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import h5py

# Load the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/99_h5_data.h5"
with h5py.File(file_path, 'r') as file:
    # Read the datasets into a DataFrame
    data = {
        "total_bill": file['total_bill'][:],
        "tip": file['tip'][:],
        "sex": file['sex'][:].astype('category'),
        "smoker": file['smoker'][:].astype('category'),
        "day": file['day'][:].astype('category'),
        "time": file['time'][:].astype('category'),
        "size": file['size'][:]
    }
    df = pd.DataFrame(data)

# Convert the 'smoker' column to a categorical variable for plotting
df['smoker_cat'] = df['smoker'].cat.codes

# Set the dark theme using seaborn
sns.set_context("paper", font_scale=1.5)
sns.set_style("dark")

# Create the violin plot
plt.figure(figsize=(14, 8))
sns.violinplot(x='day', y='total_bill', hue='smoker', data=df, split=True, palette={'yes': 'green', 'no': 'grey'})

# Add labels and title
plt.xlabel('Day of the Week')
plt.ylabel('Total Bill Amount')
plt.title('Total Bill Amounts by Day of the Week (Smokers vs Non-Smokers)')
plt.legend(title='Smoker', labels=['Yes', 'No'])

# Show the plot
plt.show()
