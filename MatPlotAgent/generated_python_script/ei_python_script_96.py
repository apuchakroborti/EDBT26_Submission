import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset from HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/96_h5_data.h5"
dataset_name = "sales_data"  # Assuming the dataset name in HDF5 is named as "sales_data"
df = pd.read_hdf(file_path, key=dataset_name)

# Ensure the DataFrame has the correct columns and are of numeric type for plotting
df['Quarter'] = pd.to_datetime(df['Quarter'], format='Q%y')  # Convert Quarter to datetime if not already
for brand in ['Samsung', 'Nokia/Microsoft', 'Apple', 'LG', 'ZTE', 'Huawei']:
    df[brand] = pd.to_numeric(df[brand], errors='coerce')

# Calculate the mean sales per quarter for each brand
mean_sales = df.groupby('Quarter').mean()

# Plotting setup
plt.figure(figsize=(14, 8))
sns.set(style="whitegrid")

# Plot box plots
boxplots = sns.boxplot(data=df[['Samsung', 'Nokia/Microsoft', 'Apple', 'LG', 'ZTE', 'Huawei']], orient='v', palette='Set2')

# Overlay individual data points on top of the box plots
sns.stripplot(x='Quarter', y='value', hue='variable', data=pd.melt(df, id_vars=['Quarter'], value_vars=['Samsung', 'Nokia/Microsoft', 'Apple', 'LG', 'ZTE', 'Huawei']), jitter=True, color='black', alpha=0.7)

# Plot the mean sales line
mean_line = plt.plot(mean_sales.index, mean_sales['Samsung'], label='Mean Samsung', marker='o', linestyle='-', color='blue')
for i in range(1, len(df['Quarter'].unique())):
    for brand in ['Samsung', 'Nokia/Microsoft', 'Apple', 'LG', 'ZTE', 'Huawei']:
        plt.plot([mean_sales.index[i]], [mean_sales[brand].iloc[i]], marker='o', color=mean_line[0].get_color())

# Adding labels and title
plt.xlabel('Quarter')
plt.ylabel('Sales')
plt.title('Sales Distribution by Brand Across Quarters')
plt.legend(title='Brand')

# Show the plot
plt.show()
