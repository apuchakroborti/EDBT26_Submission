import pandas as pd
import h5py
import plotly.express as px

# Load data from HDF5 file
file_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/87_h5_data.h5'
data = pd.read_hdf(file_path, key='table')  # Assuming the data is stored in a table format in the HDF5 file

# Calculate average lifespan weighted by population
average_lifeExp = (data['pop'] * data['lifeExp']).sum() / data['pop'].sum()

# Create a hierarchical structure: continents -> countries
sunburst_data = {
    'name': data['continent'],
    'children': []
}
for continent, subset in data.groupby('continent'):
    sunburst_data['children'].append({
        'name': continent,
        'children': [
            {'name': country, 'value': value} for country, value in zip(subset['country'], subset['pop'])
        ],
        'value': subset['pop'].sum()
    })

# Create the sunburst plot
fig = px.sunburst(
    sunburst_data,
    path=['name', 'children'],  # Path in the hierarchy
    values='value',             # Size of each segment
    color=data['lifeExp'],      # Color based on life expectancy
    color_continuous_scale=['red', 'yellow', 'blue'],  # Scale from red to blue
    range_color=(average_lifeExp - (average_lifeExp * 0.5), average_lifeExp + (average_lifeExp * 0.5))  # Range based on average lifespan
)

# Update layout for better readability and aesthetics
fig.update_layout(title='Population and Life Expectancy by Continent and Country', margin=dict(t=50, l=25, r=25, b=25))

# Show the plot
fig.show()
