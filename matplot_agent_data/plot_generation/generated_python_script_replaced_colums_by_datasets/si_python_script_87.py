import pandas as pd
import h5py
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# Load the HDF5 file
file_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/87_h5_data.h5'
hdf = h5py.File(file_path, 'r')

# Extract the datasets into a DataFrame
data = {
    'country': pd.Series(hdf['country'][:], dtype='U'),  # Unicode string type for country names
    'continent': pd.Series(hdf['continent'][:]),
    'lifeExp': hdf['lifeExp'][:].astype('float32'),
    'pop': hdf['pop'][:].astype('int64')
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Calculate weighted average life expectancy for color scaling
avg_lifeExp = np.average(df['lifeExp'], weights=df['pop'])

# Define the sunburst chart
fig = px.sunburst(
    df, 
    path=['continent', 'country'],  # Hierarchical data structure
    values='pop',                   # Size of segments based on population
    color='lifeExp',                # Color code by life expectancy
    color_continuous_scale=['red', 'blue'],  # Scale from red (lower) to blue (higher)
    range_color=[df['lifeExp'].min(), avg_lifeExp],  # Range of the color scale based on life expectancy
    title='Sunburst Chart of Countries by Continent and Life Expectancy'
)

# Update layout for better readability and aesthetics
fig.update_layout(
    legend=dict(title="Life Expectancy", yanchor="top", y=0.9, xanchor="left", x=0.1),
    margin=dict(t=50, l=25, r=25, b=25)
)

# Show the plot
fig.show()
