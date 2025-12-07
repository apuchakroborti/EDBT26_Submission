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

    # reshaping end
    
    gm_min = ((np.max(brain_vol)) / 50) * 10
    gm_max = ((np.max(brain_vol)) / 50) * 15

    
    brain_mask1 = np.where(brain_vol > gm_min, 1, 0)
    print('Shape of brain_mask1: ', brain_mask1.shape)

    brain_mask2 = np.where(brain_vol < gm_max, 1, 0)
    print('Shape of brain_mask2: ', brain_mask2.shape)


    brain_mask = brain_mask1 + brain_mask2
    print('Shape of brain_mask: ', brain_mask.shape)
    # print('brain_mask = brain_mask1 + brain_mask2: ', brain_mask)

    brain_mask = np.where(brain_mask == 2, 1, 0)
    print('Shape of brain_mask after np.where: ', brain_mask.shape)
    # print('brain_mask = np.where(brain_mask == 2, 1, 0): ', brain_mask)
    print('\n\nMask gray')
    plt.imshow(brain_mask[:, 20, :], cmap='gray')
    plt.axis('off')
    plt.show()
