import h5py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset from the HDF5 file
file_path = "/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/97_h5_data.h5"
f = h5py.File(file_path, 'r')
dataset = f['/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/97_h5_data.h5']  # Corrected this line to properly reference the dataset
df = pd.DataFrame(dataset)

# Function to convert ternary coordinates to Cartesian for equilateral triangle
def ternary_to_cartesian(x, y):
    return x * np.sqrt(3), y * 2

# Function to plot equilateral triangle diagram
def plot_equilateral_triangle(df):
    fig, ax = plt.subplots()
    unique_groups = df['No.'].unique()
    colors = plt.cm.get_cmap('viridis', len(unique_groups))
    
    for i, group in enumerate(unique_groups):
        subset = df[df['No.'] == group]
        x, y = ternary_to_cartesian(subset['toluene (25°C)'], subset['n-heptane (25°C)'])
        ax.scatter(x, y, color=colors(i), label=f'No.{group}')
        if i > 0:
            for j in range(len(subset)):
                ax.plot([x[j], x[(j+1)%len(subset)]], [y[j], y[(j+1)%len(subset)]], '--', color=colors(i))
    
    ax.set_title("Liquid-Liquid Phase Diagram (Equilateral Triangle)")
    ax.set_xlabel('Toline Cartesian Coordinates')
    ax.set_ylabel('n-Heptane Cartesian Coordinates')
    ax.legend()
    plt.show()

# Function to plot right-angled triangle diagram
def plot_right_angled_triangle(df):
    fig, ax = plt.subplots()
    unique_groups = df['No.'].unique()
    colors = plt.cm.get_cmap('viridis', len(unique_groups))
    
    for i, group in enumerate(unique_groups):
        subset = df[df['No.'] == group]
        x, y = ternary_to_cartesian(subset['toluene (25°C)'], subset['IL (25°C)'])
        ax.scatter(x, y, color=colors(i), label=f'No.{group}')
        if i > 0:
            for j in range(len(subset)):
                ax.plot([x[j], x[(j+1)%len(subset)]], [y[j], y[(j+1)%len(subset)]], '--', color=colors(i))
    
    ax.set_title("Liquid-Liquid Phase Diagram (Right-Angled Triangle)")
    ax.set_xlabel('Toluene Cartesian Coordinates')
    ax.set_ylabel('IL Cartesian Coordinates')
    ax.legend()
    plt.show()

# Plotting the diagrams
plot_equilateral_triangle(df)
plot_right_angled_triangle(df)
