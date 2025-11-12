import h5py
import numpy as np
import matplotlib.pyplot as plt

# Set the input data file path
FULL_DATA_PATH = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/6_fastMRI_brain_first_10_dcm_to_h5.h5'

# Load the HDF5 file in read-only mode
with h5py.File(FULL_DATA_PATH, 'r') as f:
    # Access the dataset within the HDF5 file using full path
    data = f['FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'][:]

# Reshape the data into 3D (assuming it's a flat array)
data_3d = np.reshape(data, (16, 32, 512))

# Create masks
max_value = np.max(data_3d)
mask1 = data_3d > 0.1 * max_value
mask2 = data_3d < 0.15 * max_value

# Combine the masks using element-wise addition and thresholding
combined_mask = (mask1 + mask2) > 0

# Visualize the mask - select slice of 20th column from 3D array
slice_to_display = combined_mask[:, :, 20]

# Plot the mask using a gray colormap
plt.imshow(slice_to_display, cmap='gray')
plt.colorbar()

# Save the plotted file with the same base name and .png extension in the same directory
output_path = FULL_DATA_PATH.rsplit('.', 1)[0] + '.png'
plt.savefig(output_path)

# Show the plot (optional)
plt.show()

