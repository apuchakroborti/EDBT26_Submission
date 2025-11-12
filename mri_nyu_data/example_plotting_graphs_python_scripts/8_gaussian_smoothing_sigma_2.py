import scipy.ndimage as ndi
import numpy as np
import matplotlib.pyplot as plt
import h5py

FAST_MRI_BRAIN_H5_FILE = '/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/fastMRI_brain_dcm_to_h5/fastMRI_brain_first_10_dcm_to_h5.h5'
FAST_MRI_BRAIN_H5_FILE_DATA_PATH = 'FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'


with h5py.File(FAST_MRI_BRAIN_H5_FILE, 'r') as f:
    # reshaping start
    dataset_2d = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][:]
    print("Original shape:", dataset_2d.shape)

    # Reshape to 3D (e.g., group every 512 columns into slices)
    # The total number of elements must match
    dataset_3d = dataset_2d.reshape((16, 32, 512))  # Example: 4 slices, 4 rows, 512 columns
    print("Reshaped to 3D:", dataset_3d.shape)
    
    print('Brain vol is assigned by 3D dataset')
    brain_vol = dataset_3d

    """
    Image smoothing
    One preprocessing operation that can be useful in working with images smoothing. 
    Smoothing is really spatial filtering, and it is commonly applied by averaging together the intensity values of nearby voxels. 
    This averaging is done in a weighted fashion, based on distance between voxels. 
    For example, for each voxel we could average together the intensity of that voxel, with half the intensity of the voxels adjacent to it on all sides, 
    and perhaps 10% of intensities that were 2 voxels away from it. In fact, the most common smoothing kernel 
    (the mathematical function used to perform this weighted averaging) 
    is called a Gaussian kernel, which is shaped like a normal (bell) curve. In 2 dimensions, it looks like this:
    """

    """
    When applied to an image slice, a Gaussian smoothing kernel reduces noise, that is, 
    the amount of voxel-to-voxel variation in intensities. 
    So, adjacent voxels will have more similar intensity values after smoothing, making the image appear more blurred. 
    The image below shows an example of the effects of smoothing. 
    In this image, the intensity at each point in the image slice is shown by the height of the mesh at that location, as well as the color.
    """

    """
    Below we will apply Gaussian smoothing to our MRI volume using ndimage’s gaussian_filter() function. 
    The one argument we need to supply is sigma, which is the width of the smoothing kernel, expressed as units of standard deviation. 
    A larger sigma value will result in a smoother (blurrier) image, because we average over a larger number of voxels.
    """

    # This is suitable for the 3D data

    print('\nGaussian smoothing to our MRI volume using ndimage’s gaussian_filter() function: ')
    sigma = 2
    smoothed = ndi.gaussian_filter(brain_vol, sigma)

    # To plot the image we just re-use the code we used above:

    fig_rows = 4
    fig_cols = 4
    n_subplots = fig_rows * fig_cols
    n_slice = brain_vol.shape[0]
    step_size = n_slice // n_subplots
    plot_range = n_subplots * step_size

    start_stop = int((n_slice - plot_range) / 2)


    # fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[10, 10])
    fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[15, 15])

    for idx, img in enumerate(range(start_stop, plot_range, step_size)):
        axs.flat[idx].imshow(smoothed[img, :, :], cmap='gray')
        axs.flat[idx].axis('off')
            
    plt.tight_layout()
    plt.show()