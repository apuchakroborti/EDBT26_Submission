import pandas as pd
import plotly.express as px
import numpy as np

# Load the dataset from the HDF5 file
file_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/87_h5_data.h5'
df = pd.read_hdf(file_path, key='dataset')  # Assuming the dataset is stored under this key in the HDF5 file

# Calculate the weighted average life expectancy for color scale midpoint
weights = df['pop'] / df['pop'].sum()
midpoint_lifeExp = np.average(df['lifeExp'], weights=weights)

# Create a sunburst chart
fig = px.sunburst(
    df, 
    path=['continent', 'country'],  # The hierarchy defined by continent and country
    values='pop',                   # Size determined by population
    color='lifeExp',                # Color determined by life expectancy
    color_continuous_scale='RdBu', # Diverging scale from red to blue
    color_midpoint=midpoint_lifeExp # Midpoint of the color scale set to the weighted average life expectancy
)

# Add a color bar as a legend for 'lifeExp'
fig.update_coloraxes(colorbar_title='Life Expectancy (lifeExp)')

# Show the plot
fig.show()
