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

    """
    Plotting an image histogram
    As we saw above, the image is stored as a NumPy array, in which each voxel in the image is represented as a number, 
    which is mapped to an intensity value in the colormap when plotting. 
    Larger values appear as brighter (whiter), and lower values appear as darker.

    Histograms of the anatomical images show the number of voxels of a given intensity value. 
    These can be informative because the distribution of intensity values in an anatomical image is not uniform. 
    Instead, as we can see above, there are many very dark voxels (outside of the head, 
    and in some of the fluid-filled spaces inside the head), 
    and then clusters of voxels that are darker grey (the grey matter, 
    largely in the cerebral cortex that forms the outer layer of the brain), 
    lighter grey (the white matter that comprises much of the inside of the brain), 
    and also some very bright areas that are primarily due to areas of fat concentration.

    We can use ndimage’s .histogram() function to plot a histogram of our brain volume. 
    We use this rather than the NumPy histogram function, because ndimage’s function is designed to work with 3D images. 
    This function requires several arguments, including the minimum and maximum intensity values that 
    define the range of the x axis of the histogram, and the number of bins:

    """

    plt.plot(ndi.histogram(brain_vol, min=0, max=np.max(brain_vol), bins=50))
    plt.show()
