import h5py
import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

# Define file paths and variables
FULL_DATA_PATH = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/7_fastMRI_brain_first_10_dcm_to_h5.h5'
FAST_MRI_BRAIN_H5_FILE = FULL_DATA_PATH
FAST_MRI_BRAIN_H5_FILE_DATA_PATH = 'FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'

# Read the HDF5 file
with h5py.File(FAST_MRI_BRAIN_H5_FILE, 'r') as f:
    # Read brain MRI data from the HDF5 file
    brain_mri_data = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][:]

# Reshape the 2D dataset into a 3D array with shape (16, 32, 512)
brain_volume_3d = np.reshape(brain_mri_data, (16, 32, 512))

# Apply Gaussian filter to reduce noise in the image
smoothed_brain_volume = gaussian_filter(brain_volume_3d, sigma=4)

# Prepare to plot slices of the smoothed brain volume data
fig_rows, fig_cols = 4, 4
n_subplots = fig_rows * fig_cols
n_slices = smoothed_brain_volume.shape[0]
step_size = n_slices // n_subplots
plot_range = n_subplots * step_size
start_stop = (n_slices - plot_range) // 2

# Create a figure with subplots and iterate over the slices, plotting each one as a grayscale image
plt.figure(figsize=(15, 15))
for i in range(start_stop, start_stop + plot_range, step_size):
    plt.subplot(fig_rows, fig_cols, (i - start_stop) // step_size + 1)
    plt.imshow(smoothed_brain_volume[i], cmap='gray')
    plt.axis('off')

# Adjust the layout so that the plots fit nicely in the figure
plt.tight_layout()

# Save the plotted file with the same base name from FULL_DATA_PATH and .png extension to the same directory
output_path = FULL_DATA_PATH.rsplit('.', 1)[0] + '.png'
plt.savefig(output_path)

