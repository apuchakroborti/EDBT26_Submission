import os
import pandas as pd
import h5py

"""
# Define the base directory where folders 76 to 100 are located
base_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data'

# Initialize a list to store file paths and their data
file_paths = []
data_frames = []

# Loop through folders 76 to 100
for folder_number in range(76, 101):
    h5_file_path = os.path.join(base_directory, f"{folder_number}_h5_data.h5")
    
    # Check if the HDF5 file exists, then add path and read data
    if os.path.isfile(h5_file_path):
        file_paths.append(h5_file_path)  # Store file path
        df = pd.read_hdf(h5_file_path, key='data')  # Read data
        data_frames.append(df)  # Store DataFrame
        print(f"\nRead data from: {h5_file_path}")
    else:
        print(f"HDF5 file {h5_file_path} does not exist.")

# Display the paths and optionally the data
for path in file_paths:
    print("HDF5 file paths:", path)
# Uncomment the following line to print data if needed
# print("Data:", data_frames)

"""



# Define the base directory where folders 76 to 100 are located
# base_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data'
base_directory = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/csv_to_h5_data'

# Initialize a list to store file paths and their datasets
file_paths = []
dataset_contents = {}
dataset_paths = []

# Loop through folders 76 to 100
for folder_number in range(76, 101):
    # h5_file_path = os.path.join(base_directory, str(folder_number), f"{folder_number}_h5_data.h5")
    h5_file_path = os.path.join(base_directory, f"{folder_number}_h5_data.h5")
    print(f'\n\nh5 file data path: {h5_file_path}')
    
    # Check if the HDF5 file exists, then add path and read datasets
    if os.path.isfile(h5_file_path):
        # print("File")
        file_paths.append(h5_file_path)  # Store file path
        try:
            with h5py.File(h5_file_path, 'r') as f:
                def collect_structure(name, obj):
                    """Callback function to collect file structure"""
                    if isinstance(obj, h5py.Dataset):
                        print(f'\nFile Name: {h5_file_path}, Dataset name: {name}')
                        dataset_paths.append(f'File Name: {h5_file_path}, Dataset name: {name}')
                        print(obj[0:10])
                        """
                        datasets_attributes['description'][name] = {
                            'shape': obj.shape,
                            'dtype': str(obj.dtype),
                            # 'first_5_elements': obj[0:5] if obj.size > 0 else None
                        }
                        """
                        if obj.attrs:
                            keys = []
                            for key, value in obj.attrs.items():
                                keys.append(key)
                            # datasets_attributes['attributes'][name]=keys
                        
                    # elif isinstance(obj, h5py.Group):
                    #     summary['groups'].append(name)
                        
                # Traverse the file and collect its structure
                f.visititems(collect_structure)
            
        except Exception as e:
            print(f"Error reading HDF5 file: {e}")


        """
        with h5py.File(h5_file_path, 'r') as h5_file:
            print('Read successfull')
            # Iterate through all datasets within the HDF5 file
            for dataset_name in h5_file.keys():
                print('Dataset name: ', dataset_name)
                print()
                # dataset_contents[(h5_file_path, dataset_name)] = h5_file[dataset_name][:]
                print(f"Read dataset '{dataset_name}' from {h5_file_path}")
        """
    else:
        print(f"HDF5 file {h5_file_path} does not exist.")
    
    # break

# Display the paths and optionally the data
# print("HDF5 file paths:", file_paths)
# Uncomment the following line to print data if needed
# print("Dataset contents:", dataset_contents)


# for path in dataset_paths:
#     print(path)