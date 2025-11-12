import pandas as pd
import plotly.express as px
import h5py

# Define the path to your HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/78_h5_data.h5"

# Open the HDF5 file
with h5py.File(file_path, 'r') as file:
    # Load data into a pandas DataFrame
    df = pd.DataFrame()
    for column in ["0-60 mph(sec)", "Gas Mileage(mpg)", "Power(kW)", "Weight(kg)", "Engine Displacement(cc)"]:
        df[column] = file[column][:]

# Create a 3D scatter plot
fig = px.scatter_3d(df, x="0-60 mph(sec)", y="Gas Mileage(mpg)", z="Power(kW)",
                     size="Engine Displacement(cc)", color="Engine Displacement(cc)",
                     size_max=50, range_color=[min(df["Engine Displacement(cc)"]), max(df["Engine Displacement(cc)")])

# Update layout for clarity and aesthetics
fig.update_layout(scene=dict(xaxis_title='Acceleration Time (sec)', yaxis_title='Gas Mileage (mpg)', zaxis_title='Power (kW)'),
                  title="Car Specifications in 3D Space", showlegend=True, legend_title="Engine Displacement (cc)")

# Add flat projections
fig.add_scatter3d(x=df["0-60 mph(sec)"], y=df["Gas Mileage(mpg)"], z=[0]*len(df), mode='markers', marker=dict(size=8, color='blue'), name="XY Plane Projection")
fig.add_scatter3d(x=[0]*len(df), y=df["Gas Mileage(mpg)"], z=df["Power(kW)"], mode='markers', marker=dict(size=8, color='red'), name="ZX Plane Projection")
fig.add_scatter3d(x=df["0-60 mph(sec)"], y=[0]*len(df), z=df["Power(kW)"], mode='markers', marker=dict(size=8, color='green'), name="YZ Plane Projection")

# Show the plot
fig.show()
