import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import rotate

# File paths and variables
FULL_DATA_PATH = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/4_fastMRI_brain_first_10_dcm_to_h5.h5'
FAST_MRI_BRAIN_H5_FILE = FULL_DATA_PATH
FAST_MRI_BRAIN_H5_FILE_DATA_PATH = 'FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'

# Reading data from HDF5 file
with h5py.File(FAST_MRI_BRAIN_H5_FILE, 'r') as f:
    brain_vol = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][:]

# Reshaping data
brain_vol_3d = brain_vol.reshape((16, 32, 512))

# Plotting data
fig_rows, fig_cols = 4, 4
n_subplots = fig_rows * fig_cols

n_slices = brain_vol_3d.shape[0]
step_size = n_slices // n_subplots
plot_range = n_subplots * step_size
start_stop = (n_slices - plot_range) // 2

plt.figure(figsize=(15, 15))
for i in range(start_stop, start_stop + plot_range, step_size):
    plt.subplot(fig_rows, fig_cols, (i - start_stop) // step_size + 1)
    slice_data = rotate(brain_vol_3d[i, :, :], 270)
    plt.imshow(slice_data, cmap='gray')
    plt.axis('off')

plt.tight_layout()
output_path = FULL_DATA_PATH.replace('.h5', '.png')
plt.savefig(output_path)
plt.close()

print(f"Plotted image saved to {output_path}")

