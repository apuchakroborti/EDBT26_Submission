import h5py

# Function to recursively create a dictionary representing the HDF5 structure
def hdf5_to_dict(hdf5_group):
    result = {}
    for key, item in hdf5_group.items():
        if isinstance(item, h5py.Group):
            # If the item is a group, recursively build the dictionary
            result[key] = hdf5_to_dict(item)
        elif isinstance(item, h5py.Dataset):
            # If the item is a dataset, store the dataset's shape and dtype
            result[key] = {'shape': item.shape, 'dtype': item.dtype}
    return result

# Function to check if a child exists in the HDF5 file
def check_child_exists(hdf5_group, child_name):
    return child_name in hdf5_group

# Open the HDF5 file and build the dictionary
# with h5py.File('/Users/apukumarchakroborti/gsu_research/llam_test/ASF/SMAP_L1C_S0_HIRES_02298_A_20150707T160502_R13080_001.h5', 'r') as h5file:
with h5py.File('/Users/apukumarchakroborti/gsu_research/llam_test/LaRC/TES-Aura_L3-CH4_r0000033028_C01_F01_12.he5', 'r') as h5file:

    # Convert the HDF5 structure to a dictionary
    hdf5_structure = hdf5_to_dict(h5file)
    
    # Print the resulting dictionary structure
    print("HDF5 structure:", hdf5_structure)
    
    # Check if a specific child (group or dataset) exists
    group_to_check = h5file['/Spacecraft_Data']  # Specify the group where you want to check
    child_name = 'along_track_mode_flag'  # Replace with the name of the child you want to check
    if check_child_exists(group_to_check, child_name):
        print(f"Child '{child_name}' exists in the group '/Spacecraft_Data'.")
    else:
        print(f"Child '{child_name}' does not exist in the group '/Spacecraft_Data'.")
