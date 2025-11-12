import h5py
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import os

# Define file paths
FULL_DATA_PATH = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/10_fastMRI_brain_first_10_dcm_to_h5.h5'
DATASET_PATH = 'FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'

# Open the HDF5 file in read mode
with h5py.File(FULL_DATA_PATH, 'r') as f:
    # Access the dataset at the specified path
    brain_vol = f[DATASET_PATH][:]

    # Print the shape of the original 2D dataset
    print(f"Original dataset shape: {brain_vol.shape}")

# Reshape the 2D dataset into a 3D array with dimensions (16, 32, 512)
reshaped_brain_vol = brain_vol.reshape((16, 32, 512))

# Compute histogram of the brain volume data
min_val = reshaped_brain_vol.min()
max_val = reshaped_brain_vol.max()
hist, bin_edges = ndi.histogram(reshaped_brain_vol, min_val, max_val, bins=100)

# Plot the histogram
plt.figure(figsize=(8, 4))
plt.plot(bin_edges[:-1], hist, color='blue')
plt.title("Voxel Intensity Histogram of Brain Volume")
plt.xlabel("Intensity Value")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()

# Save the plotted file with the same base name from FULL_DATA_PATH and .png extension
output_path = os.path.splitext(FULL_DATA_PATH)[0] + '.png'
plt.savefig(output_path)

# Show the plot (optional, if running in an interactive environment)
plt.show()

