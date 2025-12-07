import imageio as iio
import scipy.ndimage as ndi
import numpy as np
import matplotlib.pyplot as plt

# brain_slice = iio.imread('data/DICOM/IM-0004-0096.dcm', 'DICOM')
# we used prostate data instead of brain data here
# DICOM_DATA_FILE = '/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/DICOMS/001/AX_T2/408.dcm'

# fastMRI brain data 39.5 GB
FASTMRI_BRAIN_DICOM_DATA_FILE = '/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/fastMRI_brain_DICOM/100099070170/279.dcm'
brain_slice = iio.imread(FASTMRI_BRAIN_DICOM_DATA_FILE, 'DICOM')

print('type(brain_slice): ', type(brain_slice))
# imageio.core.util.Array
# iio.core.util.Array

print('brain_slice.meta: ', brain_slice.meta)
print('brain_slice.shape: ', brain_slice.shape)
print('brain_slice.meta[\'sampling\']: ', brain_slice.meta['sampling'])
print('brain_slice[0]: ', brain_slice[0])
print('brain_slice[:, 0]: ', brain_slice[:, 0])

print('# Since the MRI data is a 2D NumPy array of integers, we can plot it using Matplotlib’s plt.imshow():')
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
plt.imshow(brain_slice)
# ax.set_xticks(np.arange(0, 255, 10))
# ax.set_yticks(np.arange(0, 255, 10))
# ax.set_xticks(np.arange(0, 255, 2), minor=True)
# ax.set_yticks(np.arange(0, 255, 2), minor=True)
# ax.grid(which='major', color='grey', linestyle='-', linewidth=1)
# ax.grid(which='minor', color='grey', linestyle='-', linewidth=1)

print('\n\n# Since the MRI data is a 2D NumPy array of integers, we can plot it using Matplotlib’s plt.imshow() with gray map:')
plt.imshow(brain_slice, cmap='gray')
plt.axis('off')
plt.show()

"""
Load a brain volume
Above re loaded a single slice through the head, but in fact this was from a scan that covered the entire head. 
As noted, each slice was 1 mm thick, and it took 184 slices to cover the entire head in the sagittal plane. 
Each slice is saved in a separate DICOM file. 
All of the DICOM images (slices) from this scan are stored in the data/DICOM folder. 
Above we used iio.imread() and specified a specific filename as the first argument, to load a single 2D slice/image. 
To load the entire 3D brain volume, we use imageio’s volread() function, and pass as the first argument the name of the folder, rather than a list of files:

"""
print('\n\n Reading Volume: ')

# brain_vol = iio.volread(DICOM_DATA_FILE, 'DICOM')
brain_vol = iio.volread(FASTMRI_BRAIN_DICOM_DATA_FILE, 'DICOM')


# Reading DICOM (examining files): 
# 1/184 files (0.5%)
# 184/184 files (100.0%)
#   Found 1 correct series.
# 184/184  (100.0%)


# for the file ~/fastMRI_brain_DICOM/100099070170/279.dcm
# Reading DICOM (examining files): 32/32 files (100.0%)
#   Found 2 correct series.
# Reading DICOM (loading data): 16/16  (100.0%)
# brain_vol.shape:  (16, 512, 512)
print('brain_vol.shape: ', brain_vol.shape)

"""
Visualize one slice of the volume
We can plot a slice of the 3D volume using the same plt.imshow() command as before; 
the one difference is we need to specify which slice number to plot. 
Since slices are the first dimension of the array, we only need to supply one index, 
even though it is a 3D array (the other dimensions are treated as if we specified brain_vol[96, :, :]). 
We pick a slice in the middle of the volume, because if we picked one near the edges (e.g., slice 0) we would likely see little or no interesting anatomy. 
THis time we use the bone colormap, which is another monochrome palette but with a slight blueish hue:

"""
# plt.imshow(brain_vol[96], cmap='bone')
# plt.imshow(brain_vol[28], cmap='bone')
plt.imshow(brain_vol[10], cmap='bone')
plt.axis('off')
plt.show()


"""
Visualize a slice through different planes
Since the data are a 3D NumPy array, it is very easy to “reslice” the image and 
visualize the head from one of the other two orientations, axial and coronal. 
Below we pass : to select all sagittal slices, 
and 128 for the second dimension to get the slice midway through the volume, in the axial plane. 
Again, we omit the third dimension and so : is assumed:

"""
plt.imshow(brain_vol[:, 128], cmap='bone')
plt.axis('off')
plt.show()


"""
Rotate the image
Typically in showing axial slices, we orient them so that the nose and eyes are at the top of the image. 
The scipy.ndimage package (which we imported with the alias ndi provides a tool to rotate images, 
and we can embed it inside our .imshow() command to apply a rotation. 
The first argument to ndi.rotate() is the image, and the second is the amount of rotation, in degrees. 
The rotation is counter-clockwise, so here we need to use 270 deg rotation:
"""
plt.imshow(ndi.rotate(brain_vol[:, 128], 270), cmap='bone')
plt.axis('off')
plt.show()


"""
Coronal plane
Finally, we can do this in the coronal place as well; again rotation is necessary.
"""
plt.imshow(ndi.rotate(brain_vol[:, :, 128], 270), cmap='bone')
plt.axis('off')
plt.show()

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

fig_rows = 4
fig_cols = 4
n_subplots = fig_rows * fig_cols
n_slice = brain_vol.shape[0]
step_size = n_slice // n_subplots
plot_range = n_subplots * step_size
start_stop = int((n_slice - plot_range) / 2)

fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[10, 10])

for idx, img in enumerate(range(start_stop, plot_range, step_size)):
    axs.flat[idx].imshow(brain_vol[img, :, :], cmap='gray')
    axs.flat[idx].axis('off')
        
plt.tight_layout()
plt.show()

"""
Slice through a different axis
We can use the same approach to plot the data through other image planes. The only things we need to change are:

which dimension of the image to use to derive n_slice

the dimension that we specify the slice number in, inside the .imshow() command

adding rotation for axial and coronal slices, as we did above when plotting a single slice

"""
n_slice = brain_vol.shape[1]
step_size = n_slice // n_subplots
plot_range = n_subplots * step_size
start_stop = int((n_slice - plot_range) / 2)

fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[10, 10])

for idx, img in enumerate(range(start_stop, plot_range, step_size)):
    axs.flat[idx].imshow(ndi.rotate(brain_vol[:, img, :], 270), 
                         cmap='gray')
    axs.flat[idx].axis('off')
        
plt.tight_layout()
plt.show()

# Coronal plane
fig_rows = 4
fig_cols = 4
n_subplots = fig_rows * fig_cols
n_slice = brain_vol.shape[2]
step_size = n_slice // n_subplots
plot_range = n_subplots * step_size

start_stop = int((n_slice - plot_range) / 2)


fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[10, 10])

for idx, img in enumerate(range(start_stop, plot_range, step_size)):
    axs.flat[idx].imshow(ndi.rotate(brain_vol[:, :, img], 270), 
                         cmap='gray')
    axs.flat[idx].axis('off')
        
plt.tight_layout()
plt.show()


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

"""
In the histogram above, there is a large peak close to zero which represents the fact that 
a large number of voxels in the image don’t contain the head at all, 
and therefore have values at or close to zero. 
We can see a peak just above 10 on the x axis 
(note that the numbers on the x axis are bin numbers, not intensity values), 
with a slight decrease and then a second small peak just before 20, followed by a flat area. 
The peaks just above 10 and just below 20 reflect the concentration of similar intensity values corresponding to grey and 
white matter respectively.
"""


"""
Mask an image
We can use an image histogram like this to create a mask that isolates a particular range of intensity values in the image, while setting all other intensity values to zero. This can be useful in certain types of analysis, such as if we want to isolate only grey matter, or only white matter, from the rest of the brain. This is often used in studies that measure the volume of grey and/or white matter separately, as well as in functional MRI analyses where the interest is often only in activation in the cerebral cortex (grey matter).

In the code below, we will attempt to isolate grey matter based on intensity values from the histogram above. Note that this is an overly-simplistic approach to separating grey and white matter in MRIs, compared to more sophisticated, automated, and accurate approaches that would be used in research or clinical care. However, it is an important step in those more sophisticated approaches.

First, we manually define the range of intensity values that we consider grey matter. Based on the histogram above, we will choose a range from bins 10 – 15. Since the x axis of the histogram is bin numbers, not intensity values, we need to determine what intensities those bin numbers correspond to. Since we know the histogram divided the range from 0 to the maximum intensity value in the image, into 50 bins, we can divide the max intensity value by 50 to get the width of each bin, then multiply by the values we observed on the x axis:
"""
gm_min = ((np.max(brain_vol)) / 50) * 10
gm_max = ((np.max(brain_vol)) / 50) * 15

"""
Next we use np.where() to create two binary masks of the image. A binary mask is an image (in this case, a NumPY array) in which each voxel’s value is either 1 or 0. For the first mask, any voxel whose intensity is greater than gm_min is set to 1, and the others (lower values) are set to 0. In the second mask, any voxel less than gm_max is set to 1, and larger values are set to zero.
"""

brain_mask1 = np.where(brain_vol > gm_min, 1, 0)
brain_mask2 = np.where(brain_vol < gm_max, 1, 0)

"""
Having done this, we combine the two masks by adding them. Now, any voxel that is in the range between gm_min and gm_max will have a value of 2. Finally, we use np.where() again to create a final mask in which any voxel from the combined mask with a value of 2 (grey matter) is set to 1, and all other voxels (those both above and below our grey matter range) are set to zero.
"""
brain_mask = brain_mask1 + brain_mask2
brain_mask = np.where(brain_mask == 2, 1, 0)

"""
When we plot this final mask, we can see that it does a pretty good job of isolating the grey matter of the cortex. There is also grey matter around the ventricles (those dark areas in the centre of the brain in the images we plotted above) which shows up here. Unfortunately, a lot of the tissue in the scalp is also in the same intensity range as grey matter, so we are not able to separate these based on intensity values. Often prior to performing this type of image segmentation, a preprocessing step called skull stripping is applied, which (as it sounds) isolates and removes the skull and other non-brain tissues from the image. Skull stripping is more advanced than we will cover here.
"""

plt.imshow(brain_mask[:, 96, :], cmap='gray')
plt.axis('off')
plt.show()


"""
Image smoothing
One preprocessing operation that can be useful in working with images smoothing. Smoothing is really spatial filtering, and it is commonly applied by averaging together the intensity values of nearby voxels. This averaging is done in a weighted fashion, based on distance between voxels. For example, for each voxel we could average together the intensity of that voxel, with half the intensity of the voxels adjacent to it on all sides, and perhaps 10% of intensities that were 2 voxels away from it. In fact, the most common smoothing kernel (the mathematical function used to perform this weighted averaging) is called a Gaussian kernel, which is shaped like a normal (bell) curve. In 2 dimensions, it looks like this:
"""

"""
When applied to an image slice, a Gaussian smoothing kernel reduces noise, that is, the amount of voxel-to-voxel variation in intensities. So, adjacent voxels will have more similar intensity values after smoothing, making the image appear more blurred. The image below shows an example of the effects of smoothing. In this image, the intensity at each point in the image slice is shown by the height of the mesh at that location, as well as the color.
"""

"""
Below we will apply Gaussian smoothing to our MRI volume using ndimage’s gaussian_filter() function. The one argument we need to supply is sigma, which is the width of the smoothing kernel, expressed as units of standard deviation. A larger sigma value will result in a smoother (blurrier) image, because we average over a larger number of voxels.
"""

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


fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[10, 10])

for idx, img in enumerate(range(start_stop, plot_range, step_size)):
    axs.flat[idx].imshow(smoothed[img, :, :], cmap='gray')
    axs.flat[idx].axis('off')
        
plt.tight_layout()
plt.show()


# Below we increase sigma to 4, resulting in a more smoothed image:

sigma = 4
smoothed = ndi.gaussian_filter(brain_vol, sigma)

fig_rows = 4
fig_cols = 4
n_subplots = fig_rows * fig_cols
n_slice = brain_vol.shape[0]
step_size = n_slice // n_subplots
plot_range = n_subplots * step_size

start_stop = int((n_slice - plot_range) / 2)


fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[10, 10])

for idx, img in enumerate(range(start_stop, plot_range, step_size)):
    axs.flat[idx].imshow(smoothed[img, :, :], cmap='gray')
    axs.flat[idx].axis('off')
        
plt.tight_layout()
plt.show()

"""
Segmenting smoothed images
One benefit of smoothing, and the corresponding reduction in noise in the image, is that it can make segmentation a bit cleaner, because adjacent voxels will have more similar values — so they are less extreme overall, and less variable from voxel to voxel. Below we plot the histogram of the smoothed image, and use it (as we did earlier) to determine cutoffs for grey matter and then segment the image. Note that the histogram is different, and more smoothing, due to the smoothing applied to the intensity values.
"""
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

plt.imshow(brain_mask[:, 96, :], cmap='gray')
plt.axis('off')
plt.show()