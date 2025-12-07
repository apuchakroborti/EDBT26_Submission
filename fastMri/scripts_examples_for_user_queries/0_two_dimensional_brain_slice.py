import scipy.ndimage as ndi
import numpy as np
import matplotlib.pyplot as plt
import h5py

# FAST_MRI_BRAIN_H5_FILE = '/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/fastMRI_brain_dcm_to_h5/fastMRI_brain_first_10_dcm_to_h5.h5'
FAST_MRI_BRAIN_H5_FILE = '/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/fastMRI_brain_first_10_dcm_to_h5.h5'
FAST_MRI_BRAIN_H5_FILE_DATA_PATH = 'FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'

with h5py.File(FAST_MRI_BRAIN_H5_FILE, 'r') as f:
    brain_slice = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][:]
    
    print('brain_slice data: \n', brain_slice)
    print('type(brain_slice): ', type(brain_slice))
    print('brain_slice.shape: ', brain_slice.shape)
    

    plt.imshow(brain_slice)
    plt.show()
    
    plt.imshow(brain_slice, cmap='gray')
    plt.show()

