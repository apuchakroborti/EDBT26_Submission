import scipy.ndimage as ndi
import numpy as np
import matplotlib.pyplot as plt
import h5py

FAST_MRI_BRAIN_H5_FILE = '/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/fastMRI_brain_dcm_to_h5/fastMRI_brain_first_10_dcm_to_h5.h5'
FAST_MRI_BRAIN_H5_FILE_DATA_PATH = 'FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'


with h5py.File(FAST_MRI_BRAIN_H5_FILE, 'r') as f:
    # brain_slice = f[CONVERTED_H5_FILE_DATA_PATH][:]
    brain_vol = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][::]  

    # reshaping start
    # dataset_2d = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][()]
    dataset_2d = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][::]
    print("Original shape:", dataset_2d.shape)

    # Reshape to 3D (e.g., group every 512 columns into slices)
    # The total number of elements must match
    dataset_3d = dataset_2d.reshape((16, 32, 512))  # Example: 4 slices, 4 rows, 512 columns
    print("Reshaped to 3D:", dataset_3d.shape)
    
    print('Brain vol is assigned by 3D dataset')
    brain_vol = dataset_3d

    # reshaping end


    fig_rows = 4
    fig_cols = 4
    n_subplots = fig_rows * fig_cols
    
    """
    Slice through a different axis
    We can use the same approach to plot the data through other image planes. The only things we need to change are:

    which dimension of the image to use to derive n_slice

    the dimension that we specify the slice number in, inside the .imshow() command

    adding rotation for axial and coronal slices, as we did above when plotting a single slice

    """

    # this is for the 3D data
    n_slice = brain_vol.shape[1]
    step_size = n_slice // n_subplots
    plot_range = n_subplots * step_size
    start_stop = int((n_slice - plot_range) / 2)

    # fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[10, 10])
    fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[15, 31])

    for idx, img in enumerate(range(start_stop, plot_range, step_size)):
        axs.flat[idx].imshow(ndi.rotate(brain_vol[:, img, :], 270), cmap='gray')
        axs.flat[idx].axis('off')
            
    plt.tight_layout()
    plt.show()

