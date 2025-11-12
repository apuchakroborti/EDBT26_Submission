import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import rotate

# Define file paths
FULL_DATA_PATH = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/2_fastMRI_brain_first_10_dcm_to_h5.h5'
FAST_MRI_BRAIN_ROOT = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/'
DATA_PATH = '100099070170/279/fastMRI_brain_data'

# Open the HDF5 file
with h5py.File(FULL_DATA_PATH, 'r') as f:
    # Access datasets and attributes
    brain_2D_data = f[f'{FAST_MRI_BRAIN_ROOT}{DATA_PATH}']['brain_2D_data'][:]

    # Print information about the dataset
    print("Dataset: brain_2D_data")
    print(f"Type: {type(brain_2D_data)}")
    print(f"Shape: {brain_2D_data.shape}")

# Rotate and plot the 2D slice of brain data
rotated_image = rotate(brain_2D_data[10:502, 10:502], angle=270, reshape=False)

plt.figure(figsize=(8, 8))
plt.imshow(rotated_image, cmap='bone')
plt.axis('off')  # Turn off axis labels
plt.tight_layout()

# Save the plot with the same base name and .png extension in the same directory as FULL_DATA_PATH
output_path = FULL_DATA_PATH.rsplit('.', 1)[0] + '.png'
plt.savefig(output_path)
plt.close()

