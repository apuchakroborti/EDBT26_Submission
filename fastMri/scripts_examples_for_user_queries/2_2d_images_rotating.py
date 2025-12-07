# import imageio as iio
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
import h5py

# FAST_MRI_BRAIN_H5_FILE = '/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/fastMRI_brain_dcm_to_h5/fastMRI_brain_first_10_dcm_to_h5.h5'
FAST_MRI_BRAIN_H5_FILE = '/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/fastMRI_brain_first_10_dcm_to_h5.h5'

FAST_MRI_BRAIN_H5_FILE_DATA_PATH = 'FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'
with h5py.File(FAST_MRI_BRAIN_H5_FILE, 'r') as f:
    brain_2D_data = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][:]
    
    print('brain_slice data: \n', brain_2D_data)
    print('type(brain_slice): ', type(brain_2D_data))
    print('brain_slice.shape: ', brain_2D_data.shape)

    """
    Rotate the image
    Typically in showing axial slices, we orient them so that the nose and eyes are at the top of the image. 
    The scipy.ndimage package (which we imported with the alias ndi provides a tool to rotate images, 
    and we can embed it inside our .imshow() command to apply a rotation. 
    The first argument to ndi.rotate() is the image, and the second is the amount of rotation, in degrees. 
    The rotation is counter-clockwise, so here we need to use 270 deg rotation:
    """

    print('\nRotate the image: ')
    plt.imshow(ndi.rotate(brain_2D_data[10 : 502], 270), cmap='bone')
    plt.axis('off')
    plt.show()