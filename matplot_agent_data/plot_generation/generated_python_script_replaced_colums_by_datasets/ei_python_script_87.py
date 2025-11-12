import h5py
import pandas as pd
import plotly.express as px
import numpy as np

# Load the HDF5 file
file_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/87_h5_data.h5'
with h5py.File(file_path, 'r') as file:
    # Extract datasets
    continent = pd.DataFrame(file['continent'][:], columns=['continent'])
    country = pd.DataFrame(file['country'][:], columns=['country'])
    pop = pd.DataFrame(file['pop'][:], columns=['pop'])
    lifeExp = pd.DataFrame(file['lifeExp'][:], columns=['lifeExp'])
    
# Combine the datasets into a single DataFrame
data = pd.concat([continent, country, pop, lifeExp], axis=1)

# Calculate weighted average for life expectancy color scale midpoint
weights = data['pop'].values
mid_lifeExp = np.average(data['lifeExp'], weights=weights)

# Create the sunburst chart
fig = px.sunburst(
    data,  # The dataframe containing the hierarchy and size/color data
    path=['continent', 'country'],  # The hierarchical structure
    values='pop',  # Size of each segment
    color='lifeExp',  # Color based on life expectancy
    color_continuous_scale='RdBu',  # Diverging scale from red to blue
    color_midpoint=mid_lifeExp,  # Midpoint for the color scale
)

# Add a color bar as a legend
fig.update_coloraxes(colorbar_title='Life Expectancy')

# Show the plot
fig.show()
