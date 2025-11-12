import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# Set the input data file path
FULL_DATA_PATH = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/9_fastMRI_brain_first_10_dcm_to_h5.h5'

# Load the HDF5 file in read-only mode
with h5py.File(FULL_DATA_PATH, 'r') as f:
    # Access the specific dataset within the HDF5 file
    brain_vol = f['FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'][:]

# Reshape the 2D dataset into a 3D array with dimensions (16, 32, 512)
brain_vol = brain_vol.reshape((16, 32, 512))

# Apply Gaussian filter to reduce noise
smoothed_brain_vol = gaussian_filter(brain_vol, sigma=1)

# Plot a subset of smoothed images from the 3D volume (every 4th slice starting from the middle)
mid_index = smoothed_brain_vol.shape[0] // 2
plt.figure(figsize=(15, 10))
for i in range(mid_index, smoothed_brain_vol.shape[0], 4):
    plt.subplot(4, 4, (i - mid_index) // 4 + 1)
    plt.imshow(smoothed_brain_vol[i], cmap='gray')
    plt.axis('off')

# Save the plot with the same base name and .png extension
output_path = FULL_DATA_PATH.rsplit('.', 1)[0] + '.png'
plt.savefig(output_path)

# Segmenting smoothed images by applying another Gaussian filter
segmented_brain_vol = gaussian_filter(smoothed_brain_vol, sigma=2)

# Plot histogram of filtered values to select range for grey matter (16-25)
histogram_data = segmented_brain_vol.flatten()
plt.figure(figsize=(8, 6))
plt.hist(histogram_data, bins=50)
plt.title('Histogram of Filtered Values')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

# Create a mask for the brain region based on selected range
brain_mask = (segmented_brain_vol >= 16) & (segmented_brain_vol <= 25)

# Plot the brain mask
plt.figure(figsize=(8, 6))
plt.imshow(brain_mask[mid_index], cmap='gray')
plt.axis('off')

# Save the brain mask plot with the same base name and .png extension
mask_output_path = FULL_DATA_PATH.rsplit('.', 1)[0] + '_brain_mask.png'
plt.savefig(mask_output_path)

