import h5py
import json
from . import Utils as utils

import difflib  # For finding close matches

# created on Jan 29, 2025
def describe_dynamic_shape(shape):
    num_dims = len(shape)
    description = f"The dataset has {num_dims} dimensions.\n"

    for i, dim in enumerate(shape):
        description += f"\tDimension {i+1}: {dim} elements\n"

    return description.strip()


# created on Jan 29, 2025
# to get the list of all datasets and attributes list
def collect_all_paths_to_store_memory(file_path):
    print('Inside collect_all_paths_to_store_memory...')
    dataset_attribute_list=""

    # Open the HDF5 file in read mode
    with h5py.File(file_path, 'r') as f:
        
        # Recursive function to traverse groups and datasets
        def collect_structure(name, node):
            nonlocal dataset_attribute_list
            # For datasets, extract attributes
            if isinstance(node, h5py.Dataset):
                dataset_attribute_list+=name
                dataset_attribute_list+="\nThe shape of the above dataset is: "+describe_dynamic_shape(node.shape)

                attributes = ''
                if node.attrs:
                    attributes = ", ".join(node.attrs)
                    dataset_attribute_list+="\n\tAttributes: "+attributes
                dataset_attribute_list+='\n'

        # Start traversal from the root group
        f.visititems(collect_structure)

    return dataset_attribute_list



# created on Nov 29, 2024
def list_all_dataset_and_attribute_name_based_on_conditions(file_path, attribute_name, condition, condition_value):
    print(f'Inside list_all_dataset_and_attribute_name_based_on_conditions: attribute_name: {attribute_name}, condition: {condition}, condition_value: {condition_value}')
    dataset_attribute_list = set()

    # Open the HDF5 file in read mode
    with h5py.File(file_path, 'r') as file:
        dataset_list = []
        
        # Recursive function to traverse groups and datasets
        def collect_structure(name, node):
            
            # For datasets, extract attributes
            # if isinstance(node, h5py.Dataset):
                # print('Name: ', name)
                # datasets = name.split('/')
                # dataset_attribute_list.add(datasets[len(datasets)-1])

                # for attr_name in node.attrs:
                    # dataset_attribute_list.add(attr_name)
            
            # elif isinstance(node, h5py.Group):
            if isinstance(node, h5py.Group):
                # datasets = name.split('/')
                # dataset_attribute_list.add(datasets[len(datasets)-1])
                if node.attrs:
                    # print('Group: ', name)
                    for attr_name in node.attrs:
                        # dataset_attribute_list.add(attr_name)
                        # print('file[name].attrs[\'attr_name\']: ', file[name].attrs[attr_name])
                        if attr_name == attribute_name and file[name].attrs[attr_name]==condition_value:
                            data_name = name.replace('metadata', 'fastMRI_brain_data')
                            # print('Attribute Name: ', attr_name)
                            # print('Object: ', node)
                            # dataset_list.append(file[data_name][()])
                            # dataset_list.append(data_name)
                            dataset_attribute_list.add(data_name)

        # Start traversal from the root group
        file.visititems(collect_structure)
        # if len(dataset_list)>0:
        #     print('Dataset result: ', dataset_list)
        #     return dataset_list[0]
        # else:
        #     return 'NotFound'
    print(list(dataset_attribute_list))
    # return list(dataset_attribute_list)
    dataset_attribute_list = list(dataset_attribute_list)
    if len(dataset_attribute_list)>0:
        return dataset_attribute_list[0]




# created on 03 Nov 2024
#  to get the list of all datasets and attributes list
def list_all_dataset_and_attribute_name(file_path):
    dataset_attribute_list = set()

    # Open the HDF5 file in read mode
    with h5py.File(file_path, 'r') as f:
        
        # Recursive function to traverse groups and datasets
        def collect_structure(name, node):
            
            # For datasets, extract attributes
            if isinstance(node, h5py.Dataset):
                datasets = name.split('/')
                dataset_attribute_list.add(datasets[len(datasets)-1])

                for attr_name in node.attrs:
                    dataset_attribute_list.add(attr_name)
            

        # Start traversal from the root group
        f.visititems(collect_structure)

    return list(dataset_attribute_list)


def summarize_hdf5_print_dataset_paths_attribute(file_path):
    """
    This function reads an HDF5, HE5, or H5 file and returns a summary of its content as a dictionary.
    Args:
        file_path (str): The path to the HDF5 file.
    Returns:
        dict: A dictionary summarizing the file structure and datasets.
    """
    # summary = {'groups': [], 'datasets': {}}
    datasets_attributes = {'attributes': {}, 'description': {}}
    
    try:
        with h5py.File(file_path, 'r') as f:
            def collect_structure(name, obj):
                """Callback function to collect file structure"""
                if isinstance(obj, h5py.Dataset):
                    datasets_attributes['description'][name] = {
                        'shape': obj.shape,
                        'dtype': str(obj.dtype),
                        # 'first_5_elements': obj[0:5] if obj.size > 0 else None
                    }
                    if obj.attrs:
                        keys = []
                        for key, value in obj.attrs.items():
                            keys.append(key)
                        datasets_attributes['attributes'][name]=keys
                    
                # elif isinstance(obj, h5py.Group):
                #     summary['groups'].append(name)
                    
            # Traverse the file and collect its structure
            f.visititems(collect_structure)
        print(datasets_attributes)
        return datasets_attributes
    except Exception as e:
        print(f"Error reading HDF5 file: {e}")
    



def summarize_hdf5(file_path):
    """
    This function reads an HDF5, HE5, or H5 file and returns a summary of its content as a dictionary.
    Args:
        file_path (str): The path to the HDF5 file.
    Returns:
        dict: A dictionary summarizing the file structure and datasets.
    """
    summary = {'groups': [], 'datasets': {}}
    
    try:
        with h5py.File(file_path, 'r') as f:
            def collect_structure(name, obj):
                """Callback function to collect file structure"""
                if isinstance(obj, h5py.Dataset):
                    summary['datasets'][name] = {
                        'shape': obj.shape,
                        'dtype': str(obj.dtype),
                        # 'first_5_elements': obj[0:5] if obj.size > 0 else None
                    }
                elif isinstance(obj, h5py.Group):
                    summary['groups'].append(name)
                    
            # Traverse the file and collect its structure
            f.visititems(collect_structure)
    
    except Exception as e:
        print(f"Error reading HDF5 file: {e}")
    return summary


def extract_filtered_datasets_and_attributes(file_path, dataset_filter_list):
    dataset_info = []

    # Convert the dataset_filter_list to lowercase for case-insensitive matching
    dataset_filter_list_lower = [d.lower() for d in dataset_filter_list]
    try: 
        # Open the HDF5 file in read mode
        with h5py.File(file_path, 'r') as f:
            
            # Function to recursively traverse groups and datasets
            def traverse_hdf5(name, node):
                # Check if the node is a dataset
                if isinstance(node, h5py.Dataset):
                    dataset_path = name  # Full path of the dataset
                    
                    # Check if the dataset path matches any filter in the list (case-insensitive)
                    if any(dataset_path.lower().endswith(d) for d in dataset_filter_list_lower):
                        attributes = dict(node.attrs.items())  # Get all attributes as a dictionary
                        dataset_info.append({
                            'dataset_path': dataset_path,
                            'attributes': attributes
                        })

            # Traverse the HDF5 file and process all datasets
            f.visititems(traverse_hdf5)

        # Convert the dataset_info to JSON format
        dataset_info_json = json.dumps(dataset_info, indent=4)
        return dataset_info_json
    except Exception as e:
        print("Exception occurred, ", e)
        return ""




def list_all_attribute_paths(file_path):
    attribute_paths = []

    # Open the HDF5 file in read mode
    with h5py.File(file_path, 'r') as f:
        
        # Recursive function to traverse groups and datasets
        def traverse_hdf5(name, node):
            
            # Check if the node is a group or a dataset
            if isinstance(node, (h5py.Group, h5py.Dataset)):
                # For datasets, extract attributes
                if isinstance(node, h5py.Dataset):
                    for attr_name in node.attrs:
                        # Create the full path for each attribute
                        full_path = f"{name}/attributes/{attr_name}"
                        attribute_paths.append(full_path)
                
                # For groups, continue traversing
                if isinstance(node, h5py.Group):
                    for key, item in node.items():
                        traverse_hdf5(f"{name}/{key}", item)

        # Start traversal from the root group
        traverse_hdf5('/', f)

    return attribute_paths



def list_filtered_attribute_paths(file_path, dataset_names):
    attribute_paths = []
    
    # Normalize dataset names list to lowercase for case-insensitive comparison
    dataset_names = [name.lower() for name in dataset_names]

    # Open the HDF5 file in read mode
    with h5py.File(file_path, 'r') as f:
        
        # Recursive function to traverse groups and datasets
        def traverse_hdf5(name, node):
            # Check if the node is a dataset and matches the filter condition
            if isinstance(node, h5py.Dataset):
                # Extract only if the dataset name matches case-insensitively
                dataset_name = name.split('/')[-1].lower()
                if dataset_name in dataset_names:
                    for attr_name in node.attrs:
                        # Create the full path for each attribute
                        # full_path = f"{name}/attributes/{attr_name}"
                        full_path = f"{name}/{attr_name}"
                        attribute_paths.append(full_path)
            
            # If it's a group, continue traversing
            if isinstance(node, h5py.Group):
                for key, item in node.items():
                    traverse_hdf5(f"{name}/{key}", item)

        # Start traversal from the root group
        traverse_hdf5('/', f)

    return attribute_paths


def verify_and_correct_paths(hdf5_file_path, paths_to_check):
    # Open the HDF5 file in read mode
    with h5py.File(hdf5_file_path, 'r') as hdf_file:
        # Get all existing paths in the HDF5 file
        all_paths = []

        def add_paths(name, obj):
            all_paths.append(name)

        hdf_file.visititems(add_paths)

        verified_paths = {}
        
        # Loop through the paths to check
        for path in paths_to_check:
            if path in all_paths:
                # Path exists, mark it as valid
                verified_paths[path] = 'Valid'
            else:
                # Path does not exist, try to find closest matches
                close_matches = difflib.get_close_matches(path, all_paths, n=1, cutoff=0.6)
                if close_matches:
                    # Use the closest match if one is found
                    verified_paths[path] = f'Corrected to: {close_matches[0]}'
                else:
                    # No close match found, mark as invalid
                    verified_paths[path] = 'Invalid, no close match found'
        
        return verified_paths

def verify_and_correct_paths_v2(hdf5_file_path, paths_to_check):
    with h5py.File(hdf5_file_path, 'r') as hdf_file:
        all_paths = []           # Store all valid dataset paths
        attribute_paths = []     # Store paths that have attributes
        attribute_names = {}     # Dictionary to store attributes for each path

        def add_paths(name, obj):
            all_paths.append(name)
            if isinstance(obj, h5py.Group) or isinstance(obj, h5py.Dataset):
                # If this object has attributes, store the path and its attributes
                if obj.attrs:
                    attribute_paths.append(name)
                    attribute_names[name] = list(obj.attrs.keys())

        # Traverse the HDF5 file and store paths and attributes
        hdf_file.visititems(add_paths)

        verified_paths = {}

        # Loop through the paths to check
        for path in paths_to_check:
            if path in all_paths:
                # Path exists, mark it as valid
                verified_paths[path] = 'Valid'
            else:
                # Path does not exist, try to find closest matches in datasets
                close_matches = difflib.get_close_matches(path, all_paths, n=1, cutoff=0.6)

                # Also search for attribute matches if no dataset match is found
                found_match = False
                for attr_path in attribute_paths:
                    if path.lower() in [attr.lower() for attr in attribute_names[attr_path]]:
                        verified_paths[path] = f'Matched attribute at: {attr_path}'
                        found_match = True
                        break

                if not found_match:
                    if close_matches:
                        # Use the closest dataset match if found
                        verified_paths[path] = f'Corrected to: {close_matches[0]}'
                    else:
                        # No match found at all
                        verified_paths[path] = 'Invalid, no match found'

        return verified_paths




def match_rightmost_paths(hdf5_file_path, paths_to_check):
    try:
        with h5py.File(hdf5_file_path, 'r') as hdf_file:
            all_paths = []           # Store all valid dataset paths
            attribute_paths = []     # Store paths that have attributes
            attribute_names = {}     # Dictionary to store attributes for each path

            # Traverse and collect all dataset paths and attribute names
            def collect_paths(name, obj):
                all_paths.append(name)
                if isinstance(obj, h5py.Group) or isinstance(obj, h5py.Dataset):
                    if obj.attrs:
                        attribute_paths.append(name)
                        attribute_names[name] = list(obj.attrs.keys())

            hdf_file.visititems(collect_paths)

            corrected_paths = []

            def match_rightmost(path, paths_list):
                """Function to match the rightmost parts of a path with the dataset/attribute paths."""
                components = path.split('/')
                for i in range(len(components)):
                    partial_path = '/'.join(components[i:])
                    matches = [p for p in paths_list if p.endswith(partial_path)]
                    if matches:
                        return matches[0]
                return None

            # Loop through the paths to check
            for path in paths_to_check:
                # First, check if the exact path is valid
                if path in all_paths:
                    corrected_paths.append(path)  # Valid dataset path
                else:
                    # Try to match dataset names by rightmost components
                    dataset_match = match_rightmost(path, all_paths)

                    if dataset_match:
                        corrected_paths.append(dataset_match)
                    else:
                        # Now, try to match attributes in a similar way
                        attribute_match = None
                        for attr_path in attribute_paths:
                            for attr in attribute_names[attr_path]:
                                if attr.lower() == path.split('/')[-1].lower():
                                    attribute_match = f'{attr_path}/{attr}'
                                    break
                            if attribute_match:
                                break

                        if attribute_match:
                            corrected_paths.append(attribute_match)
                        else:
                            # No match found, append the original path
                            print('No match found')
                            # corrected_paths.append(path)

            return corrected_paths
    except Exception as e:
        print("\nException occurred while matching right most, error message: ", e)
        # return paths_to_check
        return []

def match_rightmost_paths_only_dataset_match(hdf5_file_path, paths_to_check):
    try:
        with h5py.File(hdf5_file_path, 'r') as hdf_file:
            all_paths = []           # Store all valid dataset paths
            attribute_paths = []     # Store paths that have attributes
            attribute_names = {}     # Dictionary to store attributes for each path

            # Traverse and collect all dataset paths and attribute names
            def collect_paths(name, obj):
                all_paths.append(name)
                # commenting it off
                if isinstance(obj, h5py.Dataset):
                
                #checking by taking attributes 
                # if isinstance(obj, h5py.AttributeManager):
                    if obj.attrs:
                        attribute_paths.append(name)
                        attribute_names[name] = list(obj.attrs.keys())

            hdf_file.visititems(collect_paths)

            corrected_paths = []

            def match_rightmost(path, paths_list):
                # print("\n\nPath: \n", path)
                # print("\n\nPath List: \n", paths_list)

                """Function to match the rightmost parts of a path with the dataset/attribute paths."""
                components = path.split('/')
                for i in range(len(components)):
                    partial_path = '/'.join(components[i:])
                    # matches = [p for p in paths_list if p.endswith(partial_path)]
                    matches = [p for p in paths_list if (partial_path in p and len(path)>0)]
                    # print("\n\n:Matches \n", matches)

                    if matches:
                        # return matches[0]
                        return matches
                    
                return None

            # Loop through the paths to check
            for path in paths_to_check:
                # First, check if the exact path is valid
                if path in all_paths:
                    corrected_paths.append(path)  # Valid dataset path
                else:
                    # Try to match dataset names by rightmost components
                    dataset_match = match_rightmost(path, all_paths)

                    if dataset_match:
                        # corrected_paths.append(dataset_match)
                        # corrected_paths = corrected_paths + dataset_match
                        if isinstance(corrected_paths, str):
                            corrected_paths.append(dataset_match)  # Append if it's a string
                        elif isinstance(corrected_paths, list):
                                corrected_paths.extend(dataset_match)
                    else:
                        # Now, try to match attributes in a similar way
                        attribute_match = None
                        for attr_path in attribute_paths:
                            for attr in attribute_names[attr_path]:
                                if attr.lower() == path.split('/')[-1].lower():
                                    attribute_match = f'{attr_path}/{attr}'
                                    break
                            if attribute_match:
                                break

                        if attribute_match:
                            # corrected_paths.append(attribute_match)
                            # corrected_paths = corrected_paths + attribute_match
                            if isinstance(attribute_match, str):
                                corrected_paths.append(attribute_match)  # Append if it's a string
                            elif isinstance(attribute_match, list):
                                corrected_paths.extend(attribute_match)
                        else:
                            # No match found, append the original path
                            print('No match found')
                            # corrected_paths.append(path)

            return corrected_paths
    except Exception as e:
        print("\nException occurred while matching right most, error message: ", e)
        # return paths_to_check
        return []
    

# created on 29 Sep 2024 at 10:23 pm
def match_dataset_and_get_full_path_with_attribute(hdf5_file_path, dataset_paths_to_check, attribute_list_to_check):
    try:
        attribute_list_to_check_nor = [utils.normalize(path) for path in attribute_list_to_check]
        print(f"\n\nattribute_list_to_check_nor, size: {len(attribute_list_to_check_nor)} \n", attribute_list_to_check_nor)
        with h5py.File(hdf5_file_path, 'r') as hdf_file:
            # all_paths = []           # Store all valid dataset paths
            # attribute_paths = []     # Store paths that have attributes
            # attribute_names = {}     # Dictionary to store attributes for each path
            matching_dataset_paths = []
            matching_dataset_path_attributes_dic = {}

            # Traverse and collect all dataset paths and attribute names
            def collect_paths(name, obj):
                # all_paths.append(name)
                # commenting it off
                if isinstance(obj, h5py.Dataset):
                    # print("\nname: ", name)
                    # matches = [item for item in paths_to_check if (item in name and len(item)>0)]
                    # print("\nmatches: ", matches)
                    names = name.split('/')
                    # print("\nnames: ", names)
                    if len(names)>0 and names[-1] in dataset_paths_to_check:
                        matching_dataset_paths.append(name)

                        if obj.attrs:
                            if attribute_list_to_check is not None and len(attribute_list_to_check)>0:
                                # print("\n Attribute list present for checking")
                                matches_attribute = [arrtibute for arrtibute in obj.attrs.keys() if (utils.normalize(arrtibute) in attribute_list_to_check_nor and len(arrtibute)>0)]
                                # matching_dataset_path_attributes[name] = list(obj.attrs.keys())
                                matching_dataset_path_attributes_dic[name] = matches_attribute
                            else:
                                # print("\nTaking all attributes")
                                matching_dataset_path_attributes_dic[name] = list(obj.attrs.keys())

            hdf_file.visititems(collect_paths)
            
            print(f"\n\nmatching_dataset_paths, size: {len(matching_dataset_paths)}: \n", matching_dataset_paths)
            print(f"\n\nmatching_dataset_path_attributes, size: {len(matching_dataset_path_attributes_dic)}: \n", matching_dataset_path_attributes_dic)
            
            return matching_dataset_paths, matching_dataset_path_attributes_dic
            # return corrected_paths
    except Exception as e:
        print("\nException occurred while matching right most, error message: ", e)
        # return paths_to_check
        return []


def extract_real_groups_and_attributes(h5file_path, paths_to_check):
    groups = set()
    attributes = set()

    # Open the HDF5 file in read mode
    with h5py.File(h5file_path, 'r') as hdf_file:
        # Function to recursively check paths inside the HDF5 file
        def check_path(name, obj):
            # If it's a group, we add the full path to the groups set
            if isinstance(obj, h5py.Group):
                groups.add(name)
            # If it's a dataset, we add the full path to the attributes set
            elif isinstance(obj, h5py.Dataset):
                attributes.add(name)
            # If it has attributes, we should add them too
            for attr_name in obj.attrs:
                # attributes.add(f"{name}/{attr_name}")
                attributes.add(attr_name)

        # Visit each object in the HDF5 file
        hdf_file.visititems(check_path)
    
    print(f"\n\n groups, size: {len(groups)}: \n", groups)
    print(f"\n\n attributes, size: {len(attributes)}: \n", attributes)

    # Filter provided paths against real groups and attributes
    # real_groups = [path for path in paths_to_check if path in groups]
    # real_attributes = [path for path in paths_to_check if path in attributes]
    real_groups = set()
    for path in paths_to_check:
        for group in groups:
            if path in group and len(path)>0:
                real_groups.add(group)
    
    real_attributes = set()
    for path in paths_to_check:
        for attribute in attributes:
            if path in attribute and len(path)>0:
                real_attributes.add(path)
    
    print(f"\n\n real_attributes, size: {len(real_attributes)}: \n", real_attributes)
    real_attributes= real_attributes.difference(real_groups)
    print(f"\n\n after diiference real_attributes, size: {len(real_attributes)}: \n", real_attributes)

    return list(real_groups), list(real_attributes)

def collect_datasets_with_attributes(hdf5_file):
    try:
        datasets_with_attributes = {}

        def collect_attrs(name, obj):
            # Check if the object is a dataset and has attributes
            if isinstance(obj, h5py.Dataset):
                attributes = {key: obj.attrs[key] for key in obj.attrs.keys()}
                datasets_with_attributes[name] = attributes

        with h5py.File(hdf5_file, 'r') as file:
            file.visititems(collect_attrs)
        
        return datasets_with_attributes
    except Exception as e:
        print(f"Exception occurred while reading file path {hdf5_file}")


def print_datasets_with_attributes(datasets_with_attributes):
    for dataset, attributes in datasets_with_attributes.items():
        print(f"Dataset: {dataset}")
        if attributes:
            print("Attributes:")
            for attr_name, attr_value in attributes.items():
                print(f"  - {attr_name}: {attr_value}")
        else:
            print("No attributes")
        print()  # Blank line for separation


# paths_to_check = single_word_group_dataset_attribute_list
def extract_real_datasets_and_attributes(h5file_path, paths_to_check):
    groups_with_path = set()
    datasets = []
    attributes = []
    attributes_without_parent_path=[]

    # Open the HDF5 file in read mode
    with h5py.File(h5file_path, 'r') as hdf_file:
        # Function to recursively check paths inside the HDF5 file
        def check_path(name, obj):
            # If it's a dataset, we add the full path to the datasets list
            
            if isinstance(obj, h5py.Group):
                group_paths = name.split('/')
                # groups.extend(group_paths)
                for path in group_paths:
                    if len(path)>0 and path in paths_to_check:
                        groups_with_path.add(name)

            elif isinstance(obj, h5py.Dataset):
                datasets.append(name)
                # If it has attributes, we add them to the attributes list
                for attr_name in obj.attrs:
                    attributes.append(f"{name}/{attr_name}")
                    attributes_without_parent_path.append(attr_name)

        # Visit each object in the HDF5 file
        hdf_file.visititems(check_path)
    
    # print(f"\n\n Datasets, size: {len(datasets)}: \n", datasets)
    # print(f"\n\n Attributes, size: {len(attributes)}: \n", attributes)

    # Filter provided paths against real datasets and attributes
    # need to split the paths by / and need to check the end if match then it is the dataset
    # real_groups = [path for path in paths_to_check if any(path in group for group in groups)]
    real_groups = list(groups_with_path)

    # real_datasets = [path for path in paths_to_check if any(utils.normalize(path) in utils.normalize(dataset) for dataset in datasets)] 
    # real_attributes = [path for path in paths_to_check if any(utils.normalize(path) in utils.normalize(attribute) for attribute in attributes)]

    real_dataset_set = set()
    real_attribute_set = set()
    
    for path in paths_to_check:
        for dataset in datasets:
            if utils.normalize(path) in utils.normalize(dataset):
                real_dataset_set.add(dataset)

        for index in range(0, len(attributes)-1):
            if utils.normalize(path) in utils.normalize(attributes_without_parent_path[index]):
                # real_attribute_set.add(attribute)
                real_attribute_set.add(attributes_without_parent_path[index])

    real_attributes = list(set(real_attribute_set).difference(real_dataset_set))
    # print(f"\n\n After filtering Real Attributes, size: {len(real_attributes)}: \n", real_attributes)

    return real_groups, list(real_dataset_set), real_attributes


# created on 30 Sep 2024 at 3:26 AM
def extract_exact_datasets_from_input_generated_by_llm(h5file_path, paths_to_check):
    # groups_with_path = set()
    dataset_exact_paths = set()
    # attributes = []

    # Open the HDF5 file in read mode
    with h5py.File(h5file_path, 'r') as hdf_file:
        # Function to recursively check paths inside the HDF5 file
        def check_path(name, obj):
            # If it's a dataset, we add the full path to the datasets list
            
            if isinstance(obj, h5py.Dataset):
                # print(name)
                if name in paths_to_check or '/'+name in paths_to_check:
                    dataset_exact_paths.add(name)

        # Visit each object in the HDF5 file
        hdf_file.visititems(check_path)
    # print(f"\nExact dataset paths, size: {len(dataset_exact_paths)} \n", dataset_exact_paths)

    return list(dataset_exact_paths)



def format_datasets_and_attributes(data_dict):
    text = ""
    for dataset, attributes in data_dict.items():
        # Add the dataset to the string
        text += f"Dataset: {dataset}\n"
        
        # Add each attribute on the next line with a tab before 'Attributes'
        if attributes:
            text += "\tAttributes: " + ", ".join(attributes) + "\n"
        else:
            text += "\tAttributes: None\n"
    
    return text


def format_datasets_and_attributes_and_add_example_prompt_if_latitude_longtitude_not_present(data_dict):
    text = ""
    attribute_latitude_present = False
    attribute_longditude_present = False
    text_containing_latitude_longtitude="\n The latitude and longtitude should read from the below information: \n"
    
    for dataset, attributes in data_dict.items():
        # Add the dataset to the string
        text += f"Dataset: {dataset}\n"
        
        # Add each attribute on the next line with a tab before 'Attributes'
        if attributes is not None and len(attributes)>0:
            text += "\tAttributes: " + ", ".join(attributes) + "\n"
            
            # check the latitude and longtitude present in the attributes or not
            for attribute in attributes:
                if len(attribute)>0 and 'lat' in utils.normalize(attribute):
                    attribute_latitude_present=True
                if len(attribute)>0 and 'lon' in utils.normalize(attribute):
                    attribute_longditude_present=True
            
        # else:
            # text += "\tAttributes: None\n"
    if attribute_latitude_present==False and attribute_longditude_present==False:
        text+="\n"+text_containing_latitude_longtitude
        text+='\n'+'The projection is GEO, so we can construct the lat/lon arrays ourselves.\n'
        text+='scaleX = 360.0 / data.shape[1]\n'
        text+='scaleY = 180.0 / data.shape[0]\n'
        text+='longitude = np.arange(data.shape[1]) * scaleX - 180 + scaleX/2\n'
        text+='latitude = np.arange(data.shape[0]) * scaleY - 90 + scaleY/2'
          
    return text



def summarize_hdf5_and_print(file_path):
    print(f"Path: {file_path}")
    datasets_attributes = {'attributes': {}, 'description': {}}
    
    try:
        with h5py.File(file_path, 'r') as f:
            def collect_structure(name, obj):
               
                """Callback function to collect file structure"""
                if isinstance(obj, h5py.Dataset):
                    datasets_attributes['description'][name] = {
                        'shape': obj.shape,
                        'dtype': str(obj.dtype),
                        # 'first_5_elements': obj[0:5] if obj.size > 0 else None
                    }
                    if obj.attrs:
                        keys = []
                        for key, value in obj.attrs.items():
                            keys.append(key)
                        datasets_attributes['attributes'][name]=keys
                    
                # elif isinstance(obj, h5py.Group):
                #     summary['groups'].append(name)
                    
            # Traverse the file and collect its structure
            # f.visititems(collect_structure)
            root_element = []
            for key in f.keys():
                if isinstance(f[key], h5py.Dataset):
                    print(f"Dataset Name: {key}")
                else:
                    root_element.append(key)
                    print(f"Name: {key}")
            
            print("\n\n1 Level elements:\n")
            for root in root_element:
                print(f"\nFor the group or dataset name: {root}\n")
                for key in f[root].keys():
                    print(f"sub group: {key}")

        return datasets_attributes
    except Exception as e:
        print(f"Error reading HDF5 file: {e}")


# get all paths
def get_all_paths_from_data_file(file_path):
    summary = []
    try:
        with h5py.File(file_path, 'r') as f:
            def collect_structure(name, obj):
                """Callback function to collect file structure"""
                if isinstance(obj, h5py.Dataset):
                    summary.append(f'{name}')
                # elif isinstance(obj, h5py.Group):
                    # summary['groups'].append(name)
                    
            # Traverse the file and collect its structure
            f.visititems(collect_structure)

    except Exception as e:
        print(f"Error reading HDF5 file: {e}")
    return summary



# by following some cases
# case 1:
# exact full path or dataset names are given but the dataset are unique

# case 1 solution:
# make a list and add the exact matching paths and datasets


# case 2:
# Dataset names are non-unique but exact subgroup given and unique

#case 2 solution:
# get the exact subgroup and filter the matching datasets if multiple 


# case 3:
# Paths contains spaces but while tokenizatio it got splited

def check_exact_or_starts_with_dataset_match_by_whole_path(datasetpath, paths_to_check):
    # print("Datasetpath: ", datasetpath)

    for path in paths_to_check:
        # if datasetpath==path or '/'+datasetpath==path or path.startswith(datasetpath) or ('/'+path).startswith(datasetpath):
        if utils.normalize(datasetpath) == utils.normalize(path) or '/'+utils.normalize(datasetpath)==utils.normalize(path):
            return True
    else:
        return False
    
def check_exact_root_group_match_by_exact_word(datasetpath, paths_to_check):
    # print("Datasetpath: ", datasetpath)

    for path in paths_to_check:
        # if utils.normalize(datasetpath)==utils.normalize(path) or '/'+utils.normalize(datasetpath)==utils.normalize(path) or utils.normalize(path).startswith(utils.normalize(datasetpath)) or ('/'+utils.normalize(path)).startswith(utils.normalize(datasetpath)):
        if utils.normalize(datasetpath) == utils.normalize(path) or '/'+utils.normalize(datasetpath)==utils.normalize(path):
            return True
    else:
        return False
    
def check_exact_dataset_name_only_or_ends_with_match(datasetpath, paths_to_check):
    # print("Datasetpath: ", datasetpath)
    datasetname = datasetpath.split('/')
    datasetname = datasetname[len(datasetname)-1]
    # print("Datasetname: ", datasetname)
    
    for path in paths_to_check:
        # if len(path)>2 and (datasetname==path or '/'+datasetpath==path or datasetpath.endswith(path)):
        if utils.normalize(datasetname)==utils.normalize(path) or '/'+utils.normalize(datasetpath)==utils.normalize(path):
            # print("\nDatasetpath: ", datasetpath)
            # print("Datasetname: ", datasetname, end="\n\n")
            return True
    else:
        return False
    

def check_exact_group_subgroup_path_match_by_whole_path(group_path, paths_to_check):
    # print("Grouppath: ", group_path)
    for path in paths_to_check:
        if utils.normalize(group_path)==utils.normalize(path) or '/'+utils.normalize(group_path)==utils.normalize(path):
            return True
    else:
        return False

def check_exact_immediate_group_subgroup_name_match_by_name_only(group_path, paths_to_check):
    # print("Grouppath: ", group_path)
    for path in paths_to_check:
        if utils.normalize(group_path)==utils.normalize(path):
            return True
    else:
        return False
    

def check_exact_group_subgroup_name_match(group_path, paths_to_check):
    # print("Grouppath: ", group_path)
    group_names = group_path.split('/')
    # datasetname = datasetname[len(datasetname)-1]
    
    for path in paths_to_check:
        for group in group_names:
            if utils.normalize(group)==utils.normalize(path) or '/'+utils.normalize(group)==utils.normalize(path):
                return True
            elif utils.normalize(path).startswith(utils.normalize(group)) or utils.normalize(path).startswith('/'+utils.normalize(group)):
                return True 
    else:
        return False

# date 02 Nov 2024
# current token matching with paths based on upto bigrams
def match_exact_dataset_full_partial_match_upto_bigram(hdf5_file_path, monogram_paths_to_check, bigram_paths_to_check, single_word_tokenization_from_user_input_paths):
    try:
        with h5py.File(hdf5_file_path, 'r') as hdf_file:
            all_paths = []
            root_groups = set()
            exact_datasets_matched_by_whole_path = set()
            exact_datasets_matched_by_name_only = set()
            exact_immediate_group_subgroup_match_by_name_only = set()
            exact_matched_group_subgroups_by_whole_path = set()
            exact_matched_group_subgroups_by_name_only = set()
             # Traverse and collect all dataset paths and attribute names
            def collect_paths(name, obj):
                
                if isinstance(obj, h5py.Dataset):
                    all_paths.append(name)

                    if check_exact_or_starts_with_dataset_match_by_whole_path(name, bigram_paths_to_check) and len(name)>0:
                        exact_datasets_matched_by_whole_path.add(name)
                    elif check_exact_dataset_name_only_or_ends_with_match(name, bigram_paths_to_check) and len(name)>0:
                        exact_datasets_matched_by_name_only.add(name)
                    elif check_exact_or_starts_with_dataset_match_by_whole_path(name, monogram_paths_to_check) and len(name)>0:
                        exact_datasets_matched_by_whole_path.add(name)
                    elif check_exact_dataset_name_only_or_ends_with_match(name, monogram_paths_to_check) and len(name)>0:
                        exact_datasets_matched_by_name_only.add(name)

                    # removing the dataset and taking only the path containign group and sub-group name
                    group_name=name.split('/')
                    group_name.pop()
                   

                    # making list of immediate group sub-groups
                    if len(group_name)>0 and len(group_name[len(group_name)-1])>0 and check_exact_immediate_group_subgroup_name_match_by_name_only(group_name[len(group_name)-1], bigram_paths_to_check):
                        exact_immediate_group_subgroup_match_by_name_only.add(group_name[len(group_name)-1])
                    elif len(group_name)>0 and len(group_name[len(group_name)-1])>0 and check_exact_immediate_group_subgroup_name_match_by_name_only(group_name[len(group_name)-1], monogram_paths_to_check):
                        exact_immediate_group_subgroup_match_by_name_only.add(group_name[len(group_name)-1])

                    # making path without the dataset name
                    group_name = ('/').join(group_name)

                    # this is for the exact match and starts with of the paths
                    if len(group_name)>0 and check_exact_group_subgroup_path_match_by_whole_path(name, bigram_paths_to_check):
                        exact_matched_group_subgroups_by_whole_path.add(group_name)
                    elif len(group_name)>0 and check_exact_group_subgroup_name_match(name, bigram_paths_to_check):
                        exact_matched_group_subgroups_by_name_only.add(group_name)
                    elif len(group_name)>0 and check_exact_group_subgroup_path_match_by_whole_path(name, monogram_paths_to_check):
                        exact_matched_group_subgroups_by_whole_path.add(group_name)
                    elif len(group_name)>0 and check_exact_group_subgroup_name_match(name, monogram_paths_to_check):
                        exact_matched_group_subgroups_by_name_only.add(group_name)
                
                elif isinstance(obj, h5py.Group):
                    group_name=name.split('/')
                    if len(group_name[0])>0 and check_exact_root_group_match_by_exact_word(group_name[0], bigram_paths_to_check):
                        root_groups.add(group_name[0])
                    elif len(group_name[0])>0 and check_exact_root_group_match_by_exact_word(group_name[0], monogram_paths_to_check):
                        root_groups.add(group_name[0])
                    elif len(group_name[0])>0 and check_exact_root_group_match_by_exact_word(group_name[0], single_word_tokenization_from_user_input_paths):
                         root_groups.add(group_name[0])



            hdf_file.visititems(collect_paths)

            print(f"\n\nroot_groups: {len(root_groups)}:\n", root_groups)

            print(f"\nexact_datasets_matched_by_whole_path: {len(exact_datasets_matched_by_whole_path)}:\n", exact_datasets_matched_by_whole_path)
            print(f"\nexact_datasets_matched_by_name_only: {len( exact_datasets_matched_by_name_only)}:\n",  exact_datasets_matched_by_name_only)

            print(f"\nexact_immediate_group_subgroup_match_by_name_only: {len( exact_immediate_group_subgroup_match_by_name_only)}:\n",  exact_immediate_group_subgroup_match_by_name_only)
            
            print(f"\nexact_matched_group_subgroups_by_whole_path: {len(exact_matched_group_subgroups_by_whole_path)}:\n", exact_matched_group_subgroups_by_whole_path)
            print(f"\nexact_matched_group_subgroups_by_name_only: {len(exact_matched_group_subgroups_by_name_only)}:\n", exact_matched_group_subgroups_by_name_only)

            # print("done")
            filter_possible_dataset_paths = set()
            

            # exact_matched_datasets = list(exact_matched_datasets)
            # exact_matched_datasets.extend(list(filter_possible_dataset_paths))
            # return exact_matched_datasets
            # return  list(exact_datasets_matched_by_whole_path), list(exact_datasets_matched_by_name_only), list( exact_immediate_group_subgroup_match_by_name_only), list(exact_matched_group_subgroups_by_whole_path), list(exact_matched_group_subgroups_by_name_only)
            final_result_list = []
            final_result_list.append(list(exact_datasets_matched_by_whole_path))
            final_result_list.append(list(exact_datasets_matched_by_name_only))
            final_result_list.append(list( exact_immediate_group_subgroup_match_by_name_only))
            final_result_list.append(list(exact_matched_group_subgroups_by_whole_path))
            final_result_list.append(list(exact_matched_group_subgroups_by_name_only))
            final_result_list.append(all_paths)
            final_result_list.append(list(root_groups))

            return final_result_list
    except Exception as e:
        print("\nException occurred while match_exact_dataset_full_partial_match, error message: ", e)
        return []



# current token matching with paths based on the monograms
def match_exact_dataset_full_partial_match(hdf5_file_path, paths_to_check):
    try:
        with h5py.File(hdf5_file_path, 'r') as hdf_file:
            exact_matched_datasets = set()
            exact_matched_datasets_by_name = set()
            exact_immediate_group_name = set()
            exact_matched_group_subgroups = set()
            exact_matched_group_subgroups_by_name = set()
             # Traverse and collect all dataset paths and attribute names
            def collect_paths(name, obj):
                
                if isinstance(obj, h5py.Dataset):
                    if check_exact_dataset_path_match(name, paths_to_check) and len(name)>0:
                        exact_matched_datasets.add(name)
                    elif check_exact_dataset_name_match(name, paths_to_check) and len(name)>0:
                        exact_matched_datasets_by_name.add(name)

                    group_name=name.split('/')
                    group_name.pop()
                    group_name = ('/').join(group_name)

                    if check_exact_group_subgroup_path_match(name, paths_to_check) and len(group_name)>0:
                        exact_matched_group_subgroups.add(group_name)
                    elif check_exact_group_subgroup_name_match(name, paths_to_check) and len(group_name)>0:
                        exact_matched_group_subgroups_by_name.add(group_name)
                
                """elif isinstance(obj, h5py.Group):
                    if check_exact_group_subgroup_path_match(name, paths_to_check):
                        exact_matched_group_subgroups.add(name)
                    elif check_exact_group_subgroup_name_match(name, paths_to_check):
                        exact_matched_group_subgroups_by_name.add(name)"""



            hdf_file.visititems(collect_paths)

            print(f"\n\nexact_matched_datasets: {len(exact_matched_datasets)}:\n", exact_matched_datasets)
            print(f"exact_matched_datasets_by_name: {len(exact_matched_datasets_by_name)}:\n", exact_matched_datasets_by_name)
            print(f"exact_matched_group_subgroups: {len(exact_matched_group_subgroups)}:\n", exact_matched_group_subgroups)
            print(f"exact_matched_group_subgroups_by_name: {len(exact_matched_group_subgroups_by_name)}:\n", exact_matched_group_subgroups_by_name)

            # print("done")
            filter_possible_dataset_paths = set()
            """
            if len(exact_matched_datasets_by_name)>0 and len(exact_matched_group_subgroups)>0:
                for dataset_by in exact_matched_datasets_by_name:
                    for group_subgroup in exact_matched_group_subgroups:
                        if dataset_by.startswith(group_subgroup):
                           filter_possible_dataset_paths.add(dataset_by)
            elif len(exact_matched_datasets_by_name)>0:
                for dataset_by in exact_matched_datasets_by_name:
                    exact_matched_datasets.add(dataset_by)
            """

            # exact_matched_datasets = list(exact_matched_datasets)
            # exact_matched_datasets.extend(list(filter_possible_dataset_paths))
            # return exact_matched_datasets
            return  list(exact_matched_datasets), list(exact_matched_datasets_by_name), list(exact_matched_group_subgroups), list(exact_matched_group_subgroups_by_name)

    except Exception as e:
        print("\nException occurred while match_exact_dataset_full_partial_match, error message: ", e)
        return []
    

# current resulting formatting function
# this is the new method to take input of the final dataset, add all attributes present in the database
def format_datasets_from_final_set_add_example_prompt_if_latitude_longtitude_not_present(data_file_path, final_dataset_list):
    text = ""
    attribute_latitude_present = False
    attribute_longditude_present = False
    text_containing_latitude_longtitude="\n The latitude and longtitude should read from the below information: \n"

    try:
        with h5py.File(data_file_path, 'r') as hdf5_file:
            for dataset_path in final_dataset_list:
                data = hdf5_file[dataset_path]
                text += f"Dataset: {dataset_path}\n"
                if data.attrs:   
                    text += "\tAttributes: " + ", ".join(data.attrs) + "\n"
                    
                    for attribute in data.attrs:
                        if len(attribute)>0 and 'lat' in utils.normalize(attribute):
                            attribute_latitude_present=True
                        if len(attribute)>0 and 'lon' in utils.normalize(attribute):
                            attribute_longditude_present=True
    except Exception as e:
        print("Exception")
    
    if attribute_latitude_present==False and attribute_longditude_present==False:
        text+="\n"+text_containing_latitude_longtitude
        text+='\n'+'The projection is GEO, so we can construct the lat/lon arrays ourselves.\n'
        text+='scaleX = 360.0 / data.shape[1]\n'
        text+='scaleY = 180.0 / data.shape[0]\n'
        text+='longitude = np.arange(data.shape[1]) * scaleX - 180 + scaleX/2\n'
        text+='latitude = np.arange(data.shape[0]) * scaleY - 90 + scaleY/2'

    return text


# for the normal plotting without latitude and longitude

# current testing formatting function
# this is the new method to take input of the final dataset, add all attributes present in the database
def format_datasets_from_final_set_and_latitude_longitude_list_without_latitude_longitude(data_file_path, final_dataset_list, latitude_longitude_list):
    text = ""
    text_containing_latitude_longtitude="\n The latitude and longtitude should read from the below information: \n"

    try:
        with h5py.File(data_file_path, 'r') as hdf5_file:
            for dataset_path in final_dataset_list:
                data = hdf5_file[dataset_path]
                text += f"Dataset: {dataset_path}\n"
                if data.attrs:   
                    text += "\tAttributes: " + ", ".join(data.attrs) + "\n"
    except Exception as e:
        print("Exception")
    
    

    return text

# formatting datasets and attributes
def format_datasets_from_final_dataset_list(data_file_path, final_dataset_list):
    # text = "Datasets: "
    text = ''
    attribute_present = False
    dataset_shape_map = {}
    attributes = set()
    try:
        with h5py.File(data_file_path, 'r') as hdf5_file:
            for dataset_path in final_dataset_list:
                data = hdf5_file[dataset_path]
                data_shape = data.shape
                # text += f"{dataset_path}###{data_shape}###"
                # text += f"{dataset_path}  \n\t{data_shape}\n"
                text += f"{dataset_path}\n"
                dataset_shape_map[dataset_path]=data_shape
                if data.attrs:
                    # for attribute in data.attrs:
                        # attributes.add(attribute)   
                    text += "\t" + ", ".join(data.attrs) +"\n"
                    # text += ", ".join(data.attrs) +"\n"
                    attribute_present = True
             
            
            
            return text, attribute_present
    except Exception as e:
        print("Exception occurred in the format_datasets_from_final_dataset_list, error: ", e)
        return None, None
    
    
# find the slicing data
# Sample dictionary with string keys and tuple values
def find_slicing_data_information(dataset_with_shapes):
    print('\n\n----------------------Datasets Shape information-------------------------------')
    for k, v in dataset_with_shapes.items():
        print(f"{k}: {v}")


    dataset_shape_map = {}
    if len(dataset_with_shapes)==1:
        print('Only one dataset')
        return dataset_shape_map
    



    # Step 1: Get the first tuple to use as a reference
    first_tuple = next(iter(dataset_with_shapes.values()))
    print(f'First tuple: ', first_tuple)

    # Step 2: Check if all tuples are the same as the first tuple
    all_same = all(value == first_tuple for value in dataset_with_shapes.values())

    if all_same:
        print('All datasets are the same size')
        return dataset_shape_map
    
   




# current testing formatting function
# this is the new method to take input of the final dataset, add all attributes present in the database
def format_datasets_from_final_set_and_latitude_longitude_list(data_file_path, final_dataset_list, latitude_longitude_list):
    text = ""
    text_containing_latitude_longtitude="\n The latitude and longtitude should read from the below information: \n"

    try:
        with h5py.File(data_file_path, 'r') as hdf5_file:
            for dataset_path in final_dataset_list:
                data = hdf5_file[dataset_path]
                text += f"Dataset: {dataset_path}\n"
                if data.attrs:   
                    text += "\tAttributes: " + ", ".join(data.attrs) + "\n"
                    """
                    for attribute in data.attrs:
                        if len(attribute)>0 and 'lat' in utils.normalize(attribute):
                            attribute_latitude_present=True
                        if len(attribute)>0 and 'lon' in utils.normalize(attribute):
                            attribute_longditude_present=True
                    """
    except Exception as e:
        print("Exception")
    
    if len(latitude_longitude_list)<1:
        text+="\n"+text_containing_latitude_longtitude
        text+='\n'+'The projection is GEO, so we can construct the lat/lon arrays ourselves.\n'
        text+='scaleX = 360.0 / data.shape[1]\n'
        text+='scaleY = 180.0 / data.shape[0]\n'
        text+='longitude = np.arange(data.shape[1]) * scaleX - 180 + scaleX/2\n'
        text+='latitude = np.arange(data.shape[0]) * scaleY - 90 + scaleY/2'
    else:
        text+="\nThe below information related to latitude and longitude paths:"
        for latitude_longitude_path in latitude_longitude_list:
            print('Test: ', latitude_longitude_path)
            text+="\n"+latitude_longitude_path

    return text


# this is the new method to take input of the final dataset, add all attributes present in the database
def find_latitudes_and_longditudes_based_on_final_dataset(data_file_path, final_dataset_list):
   
    latitude_list = []
    longditude_list = []

    try:
        with h5py.File(data_file_path, 'r') as hdf5_file:
            for dataset_path in final_dataset_list:
                data = hdf5_file[dataset_path]
                if data.attrs:   
                    # text += "\tAttributes: " + ", ".join(data.attrs) + "\n"
                    for attribute in data.attrs:
                        if 'lat' in attribute:
                            print(f'\n\nlatitude probable path: {dataset_path}/{attribute}')
                            latitude_list.append(f'{dataset_path}/{attribute}')
                        if 'lon' in attribute:
                            print(f'longditude probable path: {dataset_path}/{attribute}')
                            longditude_list.append(f'{dataset_path}/{attribute}')
    except Exception as e:
        print("Exception")
    
        """    
        if attribute_latitude_present==False and attribute_longditude_present==False:
        text+="\n"+text_containing_latitude_longtitude
        text+='\n'+'The projection is GEO, so we can construct the lat/lon arrays ourselves.\n'
        text+='scaleX = 360.0 / data.shape[1]\n'
        text+='scaleY = 180.0 / data.shape[0]\n'
        text+='longitude = np.arange(data.shape[1]) * scaleX - 180 + scaleX/2\n'
        text+='latitude = np.arange(data.shape[0]) * scaleY - 90 + scaleY/2'
        """

    return latitude_list, longditude_list



def summarize_latitude_longditude_information_and_print(file_path):
    print(f"Path: {file_path}")
    latitude_longditude = []
    known_attribute = ['long_name','longName', 'longTermCalibrationFactor_hh', 'longTermCalibrationFactor_vv', 'longTermCalibrationFactor_vh', 'longTermCalibrationFactor_hv']
    try:
        with h5py.File(file_path, 'r') as f:
            def collect_structure(name, obj):
               
                """Callback function to collect file structure"""
                if isinstance(obj, h5py.Group):
                   if ('lat' in name or 'lon' in name) and name not in known_attribute:
                        print(f'Group/Sub-group name: {name}')
                        latitude_longditude.append(f'Group/Sub-group name: {name}') 
                 
                   if obj.attrs.keys():
                       for key in obj.attrs.keys():
                           if ('lat' in key or 'lon' in key) and key not in known_attribute:
                                print(f'Group/Sub-group name: {name}, Key: {key}')
                                latitude_longditude.append(f'Group/Sub-group name: {name}, Key: {key}') 
                 
                elif isinstance(obj, h5py.Dataset):
                    if ('lat' in name or 'lon' in name) and name not in known_attribute:
                        print(f'Dataset name: {name}')
                        latitude_longditude.append(f'Dataset name: {name}') 
                    if obj.attrs:
                       for key, value in obj.attrs.items():
                           if ('lat' in key or 'lon' in key) and not key in known_attribute:
                                print(f'Dataset name: {name}, Key: {key}')
                                latitude_longditude.append(f'Dataset name: {name}, Key: {key}')  
               
                    
            # Traverse the file and collect its structure
            f.visititems(collect_structure)

        return latitude_longditude
    except Exception as e:
        print(f"Error reading HDF5 file: {e}")


# this is the new method to take input of the final dataset, add all attributes present in the database
def find_latitudes_and_longditudes_based_on_final_dataset(data_file_path, final_dataset_list):
   
    latitude_list = []
    longditude_list = []

    try:
        with h5py.File(data_file_path, 'r') as hdf5_file:
            for dataset_path in final_dataset_list:
                data = hdf5_file[dataset_path]
                if data.attrs:   
                    # text += "\tAttributes: " + ", ".join(data.attrs) + "\n"
                    for attribute in data.attrs:
                        if 'lat' in attribute:
                            print(f'\n\nlatitude probable path: {dataset_path}/{attribute}')
                            latitude_list.append(f'{dataset_path}/{attribute}')
                        if 'lon' in attribute:
                            print(f'longditude probable path: {dataset_path}/{attribute}')
                            longditude_list.append(f'{dataset_path}/{attribute}')
    except Exception as e:
        print("Exception")
    
      

    return latitude_list, longditude_list



def find_latitude_longditude_information_for_given_dataset_list(file_path, dataset_list):
    """
    dataset_list has both the dataset and latitude, longitude information
    step 1: if dataset list already contains the latitude or longitude information
        1. at first need to check if the dataset_list already has the latitude and longitude information
        2. if both latitude and longitude present then skip latitude longitude finding
        3. if any one of them present, then find the another one
            3.1. such as example if latitude present, find the longitude and vice versa
    
    step 2: if the dataset present not the latitude and longitude
        4. start from the group where latitude and longitude present
        5. find the paths of latitude and longitude
        6. if not found step back to one previous parent path and try to find the latitude and longitude  
    
    step 3:
        7. if still not latitude and longitude not found find if possible with lat and lon
    """


    print(f"Path: {file_path}")
    copy_dataset_list = dataset_list
    latitude_longditude = set()
    known_attribute = ['long_name','longName', 'longTermCalibrationFactor_hh', 'longTermCalibrationFactor_vv', 'longTermCalibrationFactor_vh', 'longTermCalibrationFactor_hv']
    try:
        with h5py.File(file_path, 'r') as hdf5_file:
            # step 1
            for dataset_path in dataset_list:
                    # print(f"\n\nDataset path: {dataset_path}")
                    paths = dataset_path.split('/')
                    already_latitude_longitude = False
                    path = paths[len(paths)-1]
                    # for path in paths:
                    if 'latitude' == utils.normalize(path) or 'longitude' == utils.normalize(path):
                        latitude_longditude.add(dataset_path)
                        # if dataset_path in copy_dataset_list:
                            # print(f"\n{dataset_path} should be removed")
                        
                        
                        paths.pop()
                        if len(paths)>0:
                            current_path = '/'.join(paths)
                        else:
                            current_path = '/'
                        # current_path = '/'.join(paths)
                        # print(f"\ncurrent_path: {current_path}")
                        current_path_data_object = hdf5_file[current_path]
                        # if current_path_data_object.attrs.keys():
                        if current_path_data_object.items():
                            for key, obj in current_path_data_object.items():
                                # print('\nKey: ', key)
                                current_latitude_longitude=key.split('/')
                                match_rightmost_name = current_latitude_longitude[len(current_latitude_longitude)-1]
                                # print("Rightmost path: ", match_rightmost_name)
                                if 'latitude' == utils.normalize(match_rightmost_name) or 'longitude' == utils.normalize(match_rightmost_name):
                                    latitude_longditude_path = f'{current_path}/{match_rightmost_name}'
                                    latitude_longditude_path = latitude_longditude_path.replace('//', '')
                                    # latitude_longditude.add(f'{current_path}/{match_rightmost_name}')
                                    latitude_longditude.add(latitude_longditude_path)
                                    # print(f'step1 latitude and longitude added: {current_path}/{match_rightmost_name}')

            # remove the extracted latitude and longitude from the final dataset list
            if latitude_longditude is not None:
                for lat_lon in list(latitude_longditude):
                    if lat_lon in copy_dataset_list:
                        copy_dataset_list.remove(lat_lon)
            
            # step 2
            if len(dataset_list)>0 and len(latitude_longditude)<1:
                parent = 1
                print(f'\n\n-----------------------{parent}----------------')
                for dataset_path in dataset_list:
                    paths=dataset_path.split('/')
                    if len(paths)>=parent:
                        for i in range(1, parent+1):
                            paths.pop()
                    else:
                        continue
                    
                    if len(paths)>0:
                        current_path = '/'.join(paths)
                    else:
                        current_path = '/'
                    # print(f"\ncurrent_path: {current_path}")
                    current_path_data_object = hdf5_file[current_path]
                    # if current_path_data_object.attrs.keys():
                    if current_path_data_object.items():
                        for key, obj in current_path_data_object.items():
                            if isinstance(obj, h5py.Dataset):
                                # print('\nKey: ', key)
                                current_latitude_longitude=key.split('/')
                                match_rightmost_name = current_latitude_longitude[len(current_latitude_longitude)-1]
                                # print("Rightmost path: ", match_rightmost_name)
                                if 'latitude' == utils.normalize(match_rightmost_name) or 'longitude' == utils.normalize(match_rightmost_name):
                                    latitude_longditude_path = f'{current_path}/{match_rightmost_name}'
                                    latitude_longditude_path = latitude_longditude_path.replace('//', '')
                                    # latitude_longditude.add(f'{current_path}/{match_rightmost_name}')
                                    latitude_longditude.add(latitude_longditude_path)
                                    # print(f'step2 latitude and longitude added: {current_path}/{match_rightmost_name}')
                        
            # step 3
            # try all possible cases
            if len(dataset_list)>0 and len(latitude_longditude)<1:
                    
                parent = 1
                print(f'\n\n-----------------------{parent}----------------')
                for dataset_path in dataset_list:
                    paths=dataset_path.split('/')
                    if len(paths)>=parent:
                        for i in range(1, parent+1):
                            paths.pop()
                    else:
                        continue
                    
                    if len(paths)>0:
                        current_path = '/'.join(paths)
                    else:
                        current_path = '/'
                    # print(f"\ncurrent_path: {current_path}")
                    current_path_data_object = hdf5_file[current_path]
                    # if current_path_data_object.attrs.keys():
                    if current_path_data_object.items():
                        for key, obj in current_path_data_object.items():
                            if isinstance(obj, h5py.Dataset):
                                # print('\nKey: ', key)
                                current_latitude_longitude=key.split('/')
                                match_rightmost_name = current_latitude_longitude[len(current_latitude_longitude)-1]
                                # print("Rightmost path: ", match_rightmost_name)
                                # if 'lat' in utils.normalize(match_rightmost_name) or 'lon' in utils.normalize(match_rightmost_name):
                                if '_lat' in match_rightmost_name.lower() or '_lon' in match_rightmost_name.lower():
                                    latitude_longditude_path = f'{current_path}/{match_rightmost_name}'
                                    latitude_longditude_path = latitude_longditude_path.replace('//', '')
                                    # latitude_longditude.add(f'{current_path}/{match_rightmost_name}')
                                    latitude_longditude.add(latitude_longditude_path)
                                    # print(f'step3 latitude and longitude added: {current_path}/{match_rightmost_name}')
            
            # step 4
            # try all possible cases
            if len(dataset_list)>0 and len(latitude_longditude)<1:
                    
                parent = 2
                print(f'\n\n-----------------------{parent}----------------')
                for dataset_path in dataset_list:
                    paths=dataset_path.split('/')
                    if len(paths)>=parent:
                        for i in range(1, parent+1):
                            paths.pop()
                    else:
                        continue
                    
                    if len(paths)>0:
                        current_path = '/'.join(paths)
                    else:
                        current_path = '/'
                    # print(f"\ncurrent_path: {current_path}")
                    current_path_data_object = hdf5_file[current_path]
                    # if current_path_data_object.attrs.keys():
                    if current_path_data_object.items():
                        for key, obj in current_path_data_object.items():
                            if isinstance(obj, h5py.Dataset):
                                # print('\nKey: ', key)
                                current_latitude_longitude=key.split('/')
                                match_rightmost_name = current_latitude_longitude[len(current_latitude_longitude)-1]
                                # print("Rightmost path: ", match_rightmost_name)
                                # if 'lat' in utils.normalize(match_rightmost_name) or 'lon' in utils.normalize(match_rightmost_name):
                                # if '_lat' in match_rightmost_name.lower() or '_lon' in match_rightmost_name.lower():
                                if 'latitude' == utils.normalize(match_rightmost_name) or 'longitude' == utils.normalize(match_rightmost_name):
                                    latitude_longditude_path = f'{current_path}/{match_rightmost_name}'
                                    latitude_longditude_path = latitude_longditude_path.replace('//', '')
                                    # latitude_longditude.add(f'{current_path}/{match_rightmost_name}')
                                    latitude_longditude.add(latitude_longditude_path)
                                    # print(f'step3 latitude and longitude added: {current_path}/{match_rightmost_name}')
        
        if latitude_longditude is not None:
            for lat_lon in list(latitude_longditude):
                if lat_lon in copy_dataset_list:
                    copy_dataset_list.remove(lat_lon)

        print(f"\nFinal dataset with latitude and longitude: size: {len(dataset_list)}\n", dataset_list)
        print(f"\nFinal dataset without latitude and longitude: size: {len(copy_dataset_list)}\n", copy_dataset_list)
        print(f"\nFinal latitude and longitude: size: {len(latitude_longditude)}\n", latitude_longditude)
        final_latitude_longditude = []
        if latitude_longditude is not None and len(latitude_longditude)>0:
            for lat_lon in latitude_longditude:
                final_latitude_longditude.append(lat_lon)

        return final_latitude_longditude, copy_dataset_list
    except Exception as e:
        print(f"Error reading HDF5 file: {e}")


def summarize_hdf5_print_dataset_paths_attribute_and_attribute_from_groups(file_path):
    """
    This function reads an HDF5, HE5, or H5 file and returns a summary of its content as a dictionary.
    Args:
        file_path (str): The path to the HDF5 file.
    Returns:
        dict: A dictionary summarizing the file structure and datasets.
    """
    # summary = {'groups': [], 'datasets': {}}
    datasets_attributes = {'attributes': {}, 'description': {}}
    
    try:
        with h5py.File(file_path, 'r') as f:
            def collect_structure(name, obj):
                """Callback function to collect file structure"""
                if isinstance(obj, h5py.Dataset):
                    datasets_attributes['description'][name] = {
                        'shape': obj.shape,
                        'dtype': str(obj.dtype),
                        'data': obj[()]
                        # 'first_5_elements': obj[0:5] if obj.size > 0 else None
                    }
                    if obj.attrs:
                        keys = []
                        for key, value in obj.attrs.items():
                            keys.append(key)
                        datasets_attributes['attributes'][name]=keys
                    
                elif isinstance(obj, h5py.Group):
                    if obj.attrs:
                        keys = []
                        for key, value in obj.attrs.items():
                            keys.append(key)
                        datasets_attributes['attributes'][name]=keys
                        # datasets_attributes['description'][name]
                    
            # Traverse the file and collect its structure
            f.visititems(collect_structure)
        print(datasets_attributes)
        return datasets_attributes
    except Exception as e:
        print(f"Error reading HDF5 file: {e}")
        return None



def summarize_hdf5_print_dataset_metadata_information(file_path):
    """
    This function reads an HDF5, HE5, or H5 file and returns a summary of its content as a dictionary.
    Args:
        file_path (str): The path to the HDF5 file.
    Returns:
        dict: A dictionary summarizing the file structure and datasets.
    """
    # summary = {'groups': [], 'datasets': {}}
    datasets_attributes = {'attributes': {}, 'description': {}}
    
    try:
        with h5py.File(file_path, 'r') as f:
            def collect_structure(name, obj):
                """Callback function to collect file structure"""
                # print('Dataset or group name: ', name)
                if isinstance(obj, h5py.Dataset) and 'meta' in name.lower():
                    print('Meta data: ', name)

                    datasets_attributes['description'][name] = {
                        'shape': obj.shape,
                        'dtype': str(obj.dtype),
                        'data': obj[()]
                        # 'first_5_elements': obj[0:5] if obj.size > 0 else None
                    }

                    if obj.attrs:
                        keys = []
                        for key, value in obj.attrs.items():
                            keys.append(f'Key: {key}, Value: {value}')
                        datasets_attributes['attributes'][name]=keys
                    
                elif isinstance(obj, h5py.Group):
                    if obj.attrs:
                        keys = []
                        for key, value in obj.attrs.items():
                            keys.append(f'Key: {key}, Value: {value}')
                        datasets_attributes['attributes'][name]=keys
                        # datasets_attributes['description'][name]
                    
            # Traverse the file and collect its structure
            f.visititems(collect_structure)
        # print(datasets_attributes)
        return datasets_attributes
    except Exception as e:
        print(f"Error reading HDF5 file: {e}")