import h5py
import matplotlib.pyplot as plt
import numpy as np
import time


# file_name = '/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/multicoil_test/file_brain_AXFLAIR_200_6002451.h5'
file_name = '/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/singlecoil_val/file1000000.h5'
hf = h5py.File(file_name)

volume_kspace = hf['kspace'][()]

middle_index = volume_kspace.shape[0] //2
slice_kspace = volume_kspace[middle_index] # Choosing the middle slice of this volume



def show_coils(data, slice_nums, image_title, cmap=None):
    fig = plt.figure()
    for i, num in enumerate(slice_nums):
        plt.subplot(1, len(slice_nums), i + 1)
        plt.imshow(data[num], cmap=cmap)
        output_file_path = file_name.rsplit('.', 1)[0] + image_title+'.png'
        plt.savefig(output_file_path, format='png')

# show_coils(np.log(np.abs(slice_kspace) + 1e-9), [0, 5, 10], 'primary')  # This shows coils 0, 5 and 10
# Note that a small constant is added for numerical stability.


def inverse_fft2_shift(kspace):
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(kspace, axes=(-2,-1)), norm='ortho'),axes=(-2,-1))

show_coils(np.abs(inverse_fft2_shift(slice_kspace)), [0, 5, 10],'_inverse_shift', cmap='gray')  # This shows coils 0, 5 and 10


image_data = inverse_fft2_shift(slice_kspace)

# Extract the magnitude of the image data.
magnitude_data = np.abs(image_data)
show_coils(magnitude_data, [0, 5, 10], '_magnitude_data')  # This shows coils 0, 5 and 10

# Extract the phase of the image data.
phase_data = np.angle(image_data)
show_coils(phase_data, [0, 5, 10], '_phase_data')  # This shows coils 0, 5 and 10

# Separate out the real component of the image data.
real_data = np.real(image_data)
show_coils(real_data, [0, 5, 10], '_real_data')  # This shows coils 0, 5 and 10

# Separate out the imaginary component of the image data.
imaginary_data = np.imag(image_data)
show_coils(imaginary_data, [0, 5, 10], '_imaginary_data')  # This shows coils 0, 5 and 10

# Combine multi-coil data using Root Sum of Squares (RSS) to create magnitude image
# magnitude_slice = np.sqrt(np.sum(np.abs(volume_kspace)**2, axis=0))
# show_coils(magnitude_slice, [0, 5, 10], '_magnitude_slice')  # This shows coils 0, 5 and 10

"""

def center_crop(data, shape):
    
    # Crop to center of the image, so the background is not taken into account
    # with calculating the similarity scores.
    
    if len(shape) != 3:
        raise ValueError("Shape should be a 3-tuple.")

    if not all(0 < s <= d for s, d in zip(shape, data.shape)):
        raise ValueError("Invalid shapes.")

    w_from = (data.shape[-3] - shape[0]) // 2
    h_from = (data.shape[-2] - shape[1]) // 2
    d_from = (data.shape[-1] - shape[2]) // 2

    w_to = w_from + shape[0]
    h_to = h_from + shape[1]
    d_to = d_from + shape[2]

    return data[w_from:w_to, h_from:h_to, d_from:d_to]


# don't work error is: TypeError: Image data of dtype complex64 cannot be converted to float
# center crop
volume_kspace = hf['kspace'][()]
# middle_index = volume_kspace.shape[0] //2
# slice_kspace = volume_kspace[middle_index] # Choosing the middle slice of this volume
print('Shape of kspace: ', volume_kspace.shape)
center_crop_data = center_crop(volume_kspace, volume_kspace.shape)
print('Center cropped data: ', center_crop_data)

show_coils(center_crop_data, [0, 5, 10], '_center_crop_data')  # This shows coils 0, 5 and 10

"""