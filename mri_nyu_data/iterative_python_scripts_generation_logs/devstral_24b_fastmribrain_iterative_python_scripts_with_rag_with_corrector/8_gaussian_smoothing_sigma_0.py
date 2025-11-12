import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# Set the input data file path
FULL_DATA_PATH = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/8_fastMRI_brain_first_10_dcm_to_h5.h5'

# Open the HDF5 file in read-only mode
with h5py.File(FULL_DATA_PATH, 'r') as f:
    # Access the dataset named fastMRI_brain_data
    data = f['FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'][:]

# Reshape the data to 3D (16 slices, 32 rows, 512 columns)
data_reshaped = data.reshape((16, 32, 512))

# Apply Gaussian smoothing with sigma=2
smoothed_data = gaussian_filter(data_reshaped, sigma=2)

# Set the number of rows and columns for subplots
fig_rows, fig_cols = 4, 4

# Calculate the number of subplots
n_subplots = fig_rows * fig_cols

# Calculate step size between slices to display
step_size = data_reshaped.shape[0] // n_subplots

# Calculate plot range and start/stop indices for slicing
plot_range = n_subplots * step_size
start_stop = (data_reshaped.shape[0] - plot_range) // 2

# Create a figure with subplots
fig, axes = plt.subplots(fig_rows, fig_cols, figsize=(15, 15))

for i, ax in enumerate(axes.flat):
    # Calculate the slice index to display
    slice_idx = start_stop + i * step_size

    # Display the slice using imshow
    ax.imshow(smoothed_data[slice_idx], cmap='gray')
    ax.axis('off')

plt.tight_layout()
plt.savefig(FULL_DATA_PATH.replace('.h5', '.png'))
plt.show()

