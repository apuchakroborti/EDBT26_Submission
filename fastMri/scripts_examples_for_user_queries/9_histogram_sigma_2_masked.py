# import imageio as iio
import scipy.ndimage as ndi
import numpy as np
import matplotlib.pyplot as plt
import h5py


FAST_MRI_BRAIN_H5_FILE = '/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/fastMRI_brain_dcm_to_h5/fastMRI_brain_first_10_dcm_to_h5.h5'
FAST_MRI_BRAIN_H5_FILE_DATA_PATH = 'FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'


with h5py.File(FAST_MRI_BRAIN_H5_FILE, 'r') as f:
    # reshaping start
    # dataset_2d = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][()]
    dataset_2d = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][:]
    print("Original shape:", dataset_2d.shape)

    # Reshape to 3D (e.g., group every 512 columns into slices)
    # The total number of elements must match
    dataset_3d = dataset_2d.reshape((16, 32, 512))
    print("Reshaped to 3D:", dataset_3d.shape)
    
    print('Brain vol is assigned by 3D dataset')
    brain_vol = dataset_3d

    # reshaping end


    """
    Segmenting smoothed images
    One benefit of smoothing, and the corresponding reduction in noise in the image, 
    is that it can make segmentation a bit cleaner, because adjacent voxels will have more similar values — so they are less extreme overall, 
    and less variable from voxel to voxel. Below we plot the histogram of the smoothed image, 
    and use it (as we did earlier) to determine cutoffs for grey matter and then segment the image. 
    Note that the histogram is different, and more smoothing, due to the smoothing applied to the intensity values.
    """

    # this is suitable for the 3D data
    filt = ndi.gaussian_filter(brain_vol, sigma=2)
    plt.plot(ndi.histogram(filt, min=0, max=np.max(filt), bins=50))
    plt.show()

     # Based on the above histogram we select 16 – 25 as our range of bins for grey matter.

    gm_min = ((np.max(filt)) / 50) * 16
    gm_max = ((np.max(filt)) / 50) * 25

    brain_mask1 = np.where(filt > gm_min, 1, 0)
    brain_mask2 = np.where(filt < gm_max, 1, 0)

    brain_mask = brain_mask1 + brain_mask2
    brain_mask = np.where(brain_mask == 2, 1, 0)

    # plt.imshow(brain_mask[:, 96, :], cmap='gray')
    # for the shape 16, 32, 512
    plt.imshow(brain_mask[:, 31, :], cmap='gray')
    plt.axis('off')
    plt.show()
