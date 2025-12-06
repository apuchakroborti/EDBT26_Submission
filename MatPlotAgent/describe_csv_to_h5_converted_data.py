import os
import pandas as pd
import h5py


# Define the base directory where folders 76 to 100 are located
# base_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data'
base_directory = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/matplot_agent_data/plot_generation/csv_to_h5_data'

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

    else:
        print(f"HDF5 file {h5_file_path} does not exist.")
    