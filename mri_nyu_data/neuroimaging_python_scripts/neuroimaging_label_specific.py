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

# print(f"Plotting layer Layer {i}, Channel: {channel} of Image")

output_path = f"{base_path}/mri_nyu_data/neuroimaging_python_scripts/outputs"

# plt.imshow(image_data[:, :, i, channel], cmap="gray")
# plt.axis('off')
# plt.savefig(output_path+'/BRATS_001.png', bbox_inches='tight', pad_inches=0)

def explore_3d_image(layer):
    plt.figure(figsize=(10, 15))
    channel = 3
    plt.imshow(image_data[:, :, layer, channel])
    plt.title('Explore Layers of Brain MRI', family='Arial', fontsize=20)
    plt.axis('off')
    plt.savefig(output_path+f'/BRATS_001_3d_{layer}.png', bbox_inches='tight', pad_inches=0)

    return layer

# Level first 1 to 9, no values 
# for layer_val in range(10, 15):
#     explore_3d_image(layer_val)
# explore_3d_image(layer=(0, image_data[2] - 1))
# interact(explore_3d_image, layer=(0, image_data[2] - 1))


# Define the data path and load the data
label_path = f'{base_path}/mri_nyu_data/neuroimaging_python_scripts/data/Task01_BrainTumour/labelsTr/BRATS_001.nii.gz'
label_obj = nib.load(label_path)
print(f'Type of the label_obj {type(label_obj)}')

label_array = label_obj.get_fdata()

height, width, depth = label_obj.shape
print(f'Dimension of label data:\nheight: {height}, width: {width}, depth: {depth}')

print(f'With the unique values: {np.unique(label_array)}')


print(f'''\nCorresponding to the following label categories:
      0: for normal,
      1: for enema,
      2: for non-enhancing tumor,
      3: for enhancing tumor
''')

print(f'Type of the label_obj {type(label_obj)}')
print(f'Type of the label_array {type(label_array)}')

# Define a single layer for plotting
layer = 50

# Defne a dictionary of class labels
classes_dict = {
    'Normal': 0.0,
    'Edema': 1.0,
    'Non-enhancing tumor': 2.0,
    'Enhancing tumor': 3.0
}

# Set up for plotting
fix, ax = plt.subplots(nrows=1, ncols=4, figsize=(40, 25))

for i in range(4):
    img_label_str = list(classes_dict.keys())[i]
    img = label_array[:, :, layer]
    mask = np.where(img == classes_dict[img_label_str], 255, 0)
    ax[i].imshow(mask)
    ax[i].set_title(f'Layer {layer} for {img_label_str}', fontsize=45, family='Arial')
    ax[i].axis('off')

plt.tight_layout()
plt.savefig(output_path+f'/BRATS_001_layer_{layer}.png', bbox_inches='tight', pad_inches=0)
