import numpy as np
import nibabel as nib
import itk
import itkwidgets
from ipywidgets import interact, interactive, IntSlider, ToggleButtons
import matplotlib.pyplot as plt

import seaborn as sns
sns.set_style('darkgrid')


base_path = "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data"

image_path = f'{base_path}/mri_nyu_data/neuroimaging_python_scripts/data/Task01_BrainTumour/imagesTr/BRATS_001.nii.gz'
image_obj = nib.load(image_path)
print(f'Type of the image_obj {type(image_obj)}')

image_data = image_obj.get_fdata()
print(f'Type of the image_data {type(image_data)}')

height, width, depth, channels = image_data.shape
print(f'The image object has the following dimensions:\nheight: {height}, width: {width}, depth: {depth}, channels: {channels}')

maxval = 154
# select random layer number
i = np.random.randint(0, maxval)

#Define a channel to look at
channel = 0

print(f"Plotting layer Layer {i}, Channel: {channel} of Image")

output_path = f"{base_path}/mri_nyu_data/neuroimaging_python_scripts/outputs"

plt.imshow(image_data[:, :, i, channel], cmap="gray")
plt.axis('off')
plt.savefig(output_path+'/BRATS_001.png', bbox_inches='tight', pad_inches=0)

