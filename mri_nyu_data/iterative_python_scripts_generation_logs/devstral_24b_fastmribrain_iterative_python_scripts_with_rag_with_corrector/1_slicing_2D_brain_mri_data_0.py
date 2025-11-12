import h5py
import numpy as np
import matplotlib.pyplot as plt

# Define constants for file paths
FULL_DATA_PATH = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/1_fastMRI_brain_first_10_dcm_to_h5.h5'
FAST_MRI_BRAIN_H5_FILE = FULL_DATA_PATH
FAST_MRI_BRAIN_H5_FILE_DATA_PATH = 'FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'

# Open the HDF5 file in read mode
with h5py.File(FAST_MRI_BRAIN_H5_FILE, 'r') as f:
    # Access the brain volume data at the specified path
    brain_vol = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][:]

# Print information about the brain volume data
print(f"Brain volume shape: {brain_vol.shape}")
print(f"Data type: {brain_vol.dtype}")

# Visualize a slice through different planes of the brain volume data
plt.figure(figsize=(12, 8))

# Plot bone map (slice from 10 to 502)
plt.subplot(1, 3, 1)
plt.imshow(brain_vol[10:502, 10:502], cmap='gray')
plt.title('Bone Map Slice')

# Save the plotted file with the same base name and .png extension
output_path = FULL_DATA_PATH.rsplit('.', 1)[0] + '.png'
plt.savefig(output_path)

print(f"Plot saved to {output_path}")

