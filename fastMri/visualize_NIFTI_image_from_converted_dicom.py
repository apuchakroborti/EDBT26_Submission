"""
Working with NIfTI images
NIfTI stands for Neuroimaging Informatics Technology Initiative, which is jointly sponsored by the US National Institute of Mental Health and the National Institute of Neurological Disorders and Stroke. NIfTI defines a file format for neuroimaging data that is meant to meet the needs of the fMRI research community. In particular, NIfTI was developed to support inter-operability of tools and software through a common file format. Prior to NIfTI there were a few major fMRI analysis software packages, and each used a different file format. NIfTI was designed to serve as a common file format for all of these (and future) neuroimaging software packages.

NIfTI was derived from an existing medical image format, called ANALYZE. ANALYZE was originally developed by the Mayo Clinic in the US, and was adopted by several neuroimaging analysis software packages in the 1990s. The ANALYZE header (where meta-data are stored) had extra fields that were not used, and NIfTI format basically expands on ANALYZE by using some of those empty fields to store information relevant to neuroimaging data. In particular the header stores information about the position and orientation of the images. This was a huge issue prior to NIfTI. In particular, there were different standards for how to store the order of the image data. For example, some software packages stored the data in an array that started from the most right, posterior, and inferior voxel, with the three spatial dimensions ordered right-to-left, posterior-to-anterior, and then inferior-to-superior. This is referred to as RPI orientation. Other packages that also used ANALYZE data stored the voxels in RAI format (with the second dimension going anterior-to-posterior) or LPI format (reversing left and right). This caused a lot of problems for researchers, especially if they wanted to try different analysis software, or use a pipeline that involved tools from different software packages. In some cases, this was just annoying (e.g., having to reverse the anterior-posterior dimension of an image). In other cases, it was confounding and potentially created erroneous results. This was especially true of the right-left (x) dimension. While it is immediately obvious when viewing an image which the front and back, and top and bottom, of the brain are, the left and right hemispheres are typically indistinguishable from eahc other, so a left-right swap could easily go undetected, potentially leading researchers to make completely incorrect conclusions about which side of the brain activation occurred on! The NIfTI format was designed to help prevent this by more explicitly storing orientation information in the header.

Another improvement with the NIfTI format was to allow a single file. ANALYZE format requires two files, a header (with a .hdr extension) and the image data itself (.img). These files had to have the same name prior to the extension (e.g., brain_image.hdr and brain_image.img), and doubled the number of files in a directory of images, which created more clutter. NIfTI defines a single image file ending in a .nii extension. As well, NIfTI images can be compressed using a standard, open-source algorithm known as Gzip, which can significantly reduce file sizes and thus the amount of storage required for imaging data. Since neuroimaging data files tend to be large, this compression was an important feature.

Although other file formats are still used by some software, NIfTI has become the most widely used standard for fMRI and other MRI research data file storage. Here we will learn how to convert a DICOM file to NIfTI format, which is typically the first step in an MRI research analysis pipeline, since most MRI scanners produce DICOM files, but the software researchers use to process their data reads NIFTI and not DICOM format.

"""

"""
Import packages
Here we load in three new Python packages designed to work with NIfTI data:

dicom2nifti converst DICOM images to NIfTI format

NiBabel reads and converts between NIfTI and several other common neuroimaging file formats, including ANALYZE

NiLearn is primarily designed to provide statistical analysis and machine learning tools for neuroimaging data. However, it also provides a number of utilities for reading and writing NIfTI images, and working with and visualizing data

As well we’ll load SciPy’s ndimage package, and Matplotlib
"""


import dicom2nifti
import nibabel as nib
import nilearn as nil
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
import os


"""
We will use dicom2nifti’s convert_directory() function to convert the structural MRI images we worked with in the previous lesson from DICOM to NIfTI. We pass it the name of the folder in which the DICOM images are saved, and also instruct it to compress the resulting NIfTI file (to save space). We also use the reorient=True kwarg to force the image to be written in LAI orientation (i.e., starting with the most left, anterior, and inferior voxel), which ensures there is no ambiguity about the resulting NIfTI image.

convert_directory does not take an argument for the output file name. Instead, it uses the name of the scan that was used when it was acquired on the MRI scanner. This might seem like a frustrating lack of control, however it does ensure that there are no user errors in the conversion process, that could result in mis-identified files. Here we will first list the contents of the data folder, then run convert_directory, then list the contents again to see the new NIfTI file and what it is named:

"""

os.listdir('data')
dicom2nifti.convert_directory('data/DICOM', 'data', compression=True, reorient=True)
os.listdir('data')


"""
Load NIfTI file
We use NiBabel to read in the NIfTI file we just created:
"""

brain_vol = nib.load('data/4_sag_3d_t1_spgr.nii.gz')

# What is the type of this object?
type(brain_vol)

"""
Access data in the NIfTI object
NiBabel’s handling of the NIfTI format data is not quite as elegant as what we saw in the previous lesson. Rather than being able to access the data directly by referencing the name of the object (in this case, brain_vol), we need to use the method get_fdata() to do this (the “f” in this method name stands for “floating point”, as this is the type of data it returns). We will assign the result of this to a new variable so that it’s easy to work with.
"""

brain_vol_data = brain_vol.get_fdata()
type(brain_vol_data)
"""
We see that the data is a familiar NumPy array, and below we see the dimensions are identical to what we saw for this image in the previous lesson:
"""

"""
Visualize a slice
We can use .plt.imshow() as in the previous lesson:
"""

plt.imshow(brain_vol_data[96], cmap='bone')
plt.axis('off')
plt.show()

"""
Note that our image is rotated, so use can use ndi.rotate to fix this:
"""
plt.imshow(ndi.rotate(brain_vol_data[96], 90), cmap='bone')
plt.axis('off')
plt.show()

# Plot a series of slices
fig_rows = 4
fig_cols = 4
n_subplots = fig_rows * fig_cols
n_slice = brain_vol_data.shape[0]
step_size = n_slice // n_subplots
plot_range = n_subplots * step_size
start_stop = int((n_slice - plot_range) / 2)

fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[10, 10])

for idx, img in enumerate(range(start_stop, plot_range, step_size)):
    axs.flat[idx].imshow(ndi.rotate(brain_vol_data[img, :, :], 90), cmap='gray')
    axs.flat[idx].axis('off')
        
plt.tight_layout()
plt.show()

"""
Plot with NiLearn
While SciPy’s ndimage module was designed for working with a wide variety of image types, NiLearn was designed to work with neuroimaging data specifically. As such, it’s tools are a bit easier to use and more purpose-built for tasks that neuroimaging data scientists might want to perform. For example, we can plot the NiBabel NIfTI image object directly without first having to extract the data, using the plot_img() function from NiLearn’s plotting module:
"""

from nilearn import plotting

plotting.plot_img(brain_vol)
plt.show()

"""
One nice thing that we see is that since NiLearn is neuroimaging-aware, it explicitly adds labels to our plot showing us clearly which the left and right hemispheres are.

NiLearn’s plotting library uses Matplotlib, so we can use familiar tricks to do things like adjust the image size and colormap:
"""

from nilearn import plotting

fig, ax = plt.subplots(figsize=[10, 5])
plotting.plot_img(brain_vol, cmap='gray', axes=ax)
plt.show()


"""
The plot_img() function also provides a variety of ways to display the brain, with much less code than we had to use when working with raw NumPy arrays and Matplotlib functions:
"""
plotting.plot_img(brain_vol, display_mode='tiled', cmap='gray')
plt.show()


"""
We can use the cut_coords kwarg to specify there to centre the crosshairs and “cuts” through the image that we visualize. In this image, the coordinates are relative to the *isocenter of the MRI scanner — the centre of the magnetic field inside the scanner. The position of a person’s head relative to this isocenter will vary from individual to individual, and scan to scan, due to variations in head size and the optimizations used by the MRI technician and scanner. But we can use the coordinates printed in the above image (which defaulted to the centre of the image volume) and some trial-and-error to get a different view through the brain:
"""

plotting.plot_img(brain_vol, cmap='gray', cut_coords=(-45, 40, 0))
plt.show()

# plot_img() also has a few other ways to see multiple slices at once:
plotting.plot_img(brain_vol, display_mode='x', cmap='gray')
plt.show()

plotting.plot_img(brain_vol, display_mode='mosaic', cmap='gray')
plt.show()


"""
Smoothing
NiLearn has its own function for applying Gaussian spatial smoothing to images as well. The only real difference from scipy.ndimage’s gaussian_filter() function is that instead of specifying the smoothing kernel in standard deviations, we specify it in units of full width half-maximum (FWHM). This is the standard way that most neuroimaging analysis packages specify smoothing kernel size, so it is preferable to SciPy’s approach. As the term implies, FWHM is the width of the smoothing kernel, in millimetres, at the point in the kernel where it is half of its maximum height. Thus a larger FWHM value applies more smoothing.
"""

from nilearn import image

fwhm = 4

brain_vol_smth = image.smooth_img(brain_vol, fwhm)
plotting.plot_img(brain_vol_smth, cmap='gray', cut_coords=(-45, 40, 0))
plt.show()




