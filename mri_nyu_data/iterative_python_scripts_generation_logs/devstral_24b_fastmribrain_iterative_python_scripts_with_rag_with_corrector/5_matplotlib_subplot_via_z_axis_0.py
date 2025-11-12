import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import rotate

# Define file paths
FULL_DATA_PATH = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/5_fastMRI_brain_first_10_dcm_to_h5.h5'
FAST_MRI_BRAIN_H5_FILE = FULL_DATA_PATH
FAST_MRI_BRAIN_H5_FILE_DATA_PATH = 'FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'

# Load the HDF5 file in read mode and extract brain MRI data
with h5py.File(FAST_MRI_BRAIN_H5_FILE, 'r') as f:
    brain_vol = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][:]

# Reshape the 2D dataset into a 3D array (group every 512 columns into slices)
brain_volume_3d = brain_vol.reshape(brain_vol.shape[0], -1, 512)

# Plot the coronal plane of the brain MRI volume
fig_rows, fig_cols = 4, 8
n_slices = brain_volume_3d.shape[0]
n_subplots = fig_rows * fig_cols

step_size = n_slices // n_subplots
plot_range = step_size * n_subplots
start_stop = (n_slices - plot_range) // 2

fig, axs = plt.subplots(fig_rows, fig_cols, figsize=(15, 31))

for i, ax in enumerate(axs.flat):
    z = start_stop + i * step_size
    slice_data = rotate(brain_volume_3d[z], 270)
    im = ax.imshow(slice_data, cmap='gray')
    ax.axis('off')

plt.tight_layout()
output_path = FULL_DATA_PATH.replace('.h5', '.png')
plt.savefig(output_path)

# Display the plot
plt.show()

