import h5py

# Function to recursively search for a dataset by name
def find_dataset_by_name(hdf5_group, dataset_name):
    result = None
    for key, item in hdf5_group.items():
        if isinstance(item, h5py.Group):
            # Recursively search within the group
            result = find_dataset_by_name(item, dataset_name)
            if result:
                break
        elif isinstance(item, h5py.Dataset) and key == dataset_name:
            # Dataset found, return its path
            result = item
            break
    return result

# Open the HDF5 file and search for the dataset
with h5py.File('/Users/apukumarchakroborti/gsu_research/llam_test/ASF/SMAP_L1C_S0_HIRES_02298_A_20150707T160502_R13080_001.h5', 'r') as h5file:
    dataset_name = 'antenna_look_angle'  # Replace with the dataset name you are looking for
    dataset = find_dataset_by_name(h5file, dataset_name)
    
    if dataset:
        print(f"Dataset '{dataset_name}' found! Shape: {dataset.shape}, Data type: {dataset.dtype}")
    else:
        print(f"Dataset '{dataset_name}' not found.")
