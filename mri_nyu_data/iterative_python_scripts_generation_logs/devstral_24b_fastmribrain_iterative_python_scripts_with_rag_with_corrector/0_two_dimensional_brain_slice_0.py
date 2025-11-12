import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# Define file paths
FULL_DATA_PATH = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/0_fastMRI_brain_first_10_dcm_to_h5.h5'
FAST_MRI_BRAIN_H5_FILE = FULL_DATA_PATH
FAST_MRI_BRAIN_H5_FILE_DATA_PATH = 'FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'

# Open the HDF5 file in read-only mode
with h5py.File(FAST_MRI_BRAIN_H5_FILE, 'r') as f:
    # Access the dataset at the specified path and read its contents into a NumPy array
    brain_slice = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][:]

# Print information about the data
print("Type of brain_slice:", type(brain_slice))
print("Shape of brain_slice:", brain_slice.shape)

# Plot the data using Matplotlib
plt.figure()
plt.imshow(brain_slice, cmap='gray')
plt.title('MRI Brain Slice Visualization')
plt.axis('off')  # Hide axis for better image display

# Save the plotted file with the same base name and .png extension in the same directory
output_path = os.path.splitext(FULL_DATA_PATH)[0] + '.png'
plt.savefig(output_path)
print(f"Plot saved to {output_path}")

