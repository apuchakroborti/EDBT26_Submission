"""
Plotting a series of slices through a volume
We can use our skills with Matplotlib subplots to plot a series of slices through the brain, 
which is a more comprehensive way of visualizing the data. 
The biggest trick with this is deciding on the number of subplots (slices) we want, 
and then doing the necessary math to select the appropriate slices from the 3D volume 
such that the slices are evenly-spaced through the volume, and centered in the middle of the volume. 
For instance, below we will generate a 4 x 4 array of 16 subplots. 
Our number of slices — 184 — does not divide evenly by 16 (184 / 16 = 11.5). 
For this reason, we can’t simply run a for loop over a range of slice numbers that starts at 0 
and goes up to the number of slices, in steps of n_slices / n_subplots. 
Instead, we use floor division (//) to generate the integer result of dividing the number of slices by subplots (11) 
so that we get a step size that ensures we have 16 evenly-spaced slices through the volume. 
Then, we determine the number of slices that will be covered by 16 subplots, 
spaced 11 slices apart from each other (which will be < 184). 
Finally, we compute a start_stop value which tells us which slice to start from (i.e., the first slice to plot), 
such that the set of slices we generate will be centered on the volume. 
This is determined by computing how many slices in the volume are not covered by our 16 subplots 
(i.e., the slices at either edge of the volume), and dividing this by 2, 
since half of those slices should be at one edge of the volume, at the other at the other end of the volume.
"""

import scipy.ndimage as ndi
import numpy as np
import matplotlib.pyplot as plt
import h5py

FAST_MRI_BRAIN_H5_FILE = '/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/fastMRI_brain_dcm_to_h5/fastMRI_brain_first_10_dcm_to_h5.h5'
FAST_MRI_BRAIN_H5_FILE_DATA_PATH = 'FAST_MRI_BRAIN_ROOT/100099070170/279/fastMRI_brain_data'


with h5py.File(FAST_MRI_BRAIN_H5_FILE, 'r') as f:
   
    dataset_2d = f[FAST_MRI_BRAIN_H5_FILE_DATA_PATH][:]
    print("Original shape:", dataset_2d.shape)

    # Reshape to 3D (e.g., group every 512 columns into slices)
    # The total number of elements must match
    # Example: 16 slices, 32 rows, 512 columns
    dataset_3d = dataset_2d.reshape((16, 32, 512))  
    print("Reshaped to 3D:", dataset_3d.shape)
    
    print('Brain vol is assigned by 3D dataset')
    brain_vol = dataset_3d

    # reshaping end
    
    fig_rows = 4
    fig_cols = 4
    n_subplots = fig_rows * fig_cols
    n_slice = brain_vol.shape[0]
    print('n_slice: ', n_slice)
    step_size = n_slice // n_subplots
    plot_range = n_subplots * step_size
    start_stop = int((n_slice - plot_range) / 2)

    fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[15, 31])

    for idx, img in enumerate(range(start_stop, plot_range, step_size)):
        axs.flat[idx].imshow(brain_vol[img, :, :], cmap='gray')
        axs.flat[idx].axis('off')
            
    plt.tight_layout()
    plt.show()
