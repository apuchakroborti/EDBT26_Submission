import h5py
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Define file paths
FULL_DATA_PATH = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/3_fastMRI_brain_first_10_dcm_to_h5.h5'
FAST_MRI_BRAIN_H5_FILE = FULL_DATA_PATH
FAST_MRI_BRAIN_H5_FILE_DATA_PATH = 'FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'

# Load the HDF5 file and access brain MRI data
with h5py.File(FAST_MRI_BRAIN_H5_FILE, 'r') as f:
    # Access the dataset at the specified path
    data = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][:]

# Reshape the data into a 3D array with shape (16, 32, 512)
data_reshaped = np.reshape(data, (16, 32, 512))

# Define plot parameters
fig_rows = 4
fig_cols = 4
n_subplots = fig_rows * fig_cols

n_slice = data_reshaped.shape[0]
step_size = n_slice // n_subplots
plot_range = n_subplots * step_size
start_stop = (n_slice - plot_range) // 2

# Create a figure with multiple subplots
plt.figure(figsize=(15, 15))
for i in range(start_stop, start_stop + plot_range, step_size):
    plt.subplot(fig_rows, fig_cols, (i - start_stop) // step_size + 1)
    plt.imshow(data_reshaped[i, :, :], cmap='gray')
    plt.axis('off')

plt.tight_layout()

# Save the plotted figure
output_path = Path(FULL_DATA_PATH).with_suffix('.png')
plt.savefig(output_path)

# Display the figure
plt.show()

