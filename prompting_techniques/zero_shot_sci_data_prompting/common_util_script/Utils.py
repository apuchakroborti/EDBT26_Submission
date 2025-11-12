import os
import re
def extract_substring(text, start_delim, end_delim):
    start_idx = text.find(start_delim)
    if start_idx == -1:
        return None
    
    start_idx += len(start_delim)
    end_idx = text.find(end_delim, start_idx)
    if end_idx == -1:
        return None
    
    return text[start_idx:end_idx]



import json

def get_list_from_json(group_and_dataset_list_json_data):
    try:
        # Convert JSON string into Python list
        data_list = json.loads(group_and_dataset_list_json_data)
        print("Utils.get_list_from_json: data_list", data_list)
        return data_list
    except Exception as e:
        try:
            data_list = extract_values_from_json_unknown_objects(group_and_dataset_list_json_data)
            print("\n\n\nextract_values_from_json_unknown_objects: ", data_list)
            return data_list
        except Exception as e:
            print("Exception occurred at Utils.get_list_from_json, message: ", e)
            return []

def make_list_comma_separated_item(data_list):
    # Add single quotes around each item and join with commas
    comma_separated = ', '.join(f"'{item}'" for item in data_list)

    # Print the result
    # print(comma_separated)
    return comma_separated



"""# Example slash-separated list of paths
slash_separated_list = [
    "/group1/subgroup1/dataset1",
    "/group2/subgroup2/dataset2",
    "/group3/subgroup3/dataset3"
]"""

# Function to split the paths and combine individual items into a list
def split_and_combine(slash_separated_list):
    combined_list = []
    
    try:
        for path in slash_separated_list:
            # Split each path by the '/' delimiter and extend the combined list
            split_items = path.split('/')
            # Remove any empty strings from the list (resulting from leading slashes)
            split_items = [item for item in split_items if item]
            combined_list.extend(split_items)
        
        return combined_list
    except Exception as e:
        print(f"Exception occurred while split_and_combine: message: {e}") 
"""# Example usage
result = split_and_combine(slash_separated_list)

# Print the result
print(result)"""

import re

# updated function to extract python code from model response
def extract_python_code(text):
    # Regular expression to match the code block between ```python and ```
    # match = re.search(r'```python\s+(.*?)```', text, re.DOTALL)
    match = re.search(r'```python\s*\n(.*?)```', text, re.DOTALL)
    if match:
        return match.group(1).strip()  # Return the code, trimmed of leading/trailing whitespace
    else:
        return None  # Return None if no code block is found

# get the code from the response
def extract_python_code_from_response(response_string):
    response_string = response_string.strip()
    start_delim_0 = "<<<"
    end_delim_0 = ">>>"

    start_delim_1 = "```python\n"
    start_delim_2 = "```Python\n"
    start_delim_3 = "```\n"
    start_delim_4 = " ```python\n"
    start_delim_5 = "\t```python\n"
    end_delim = "```"

    result_0 = extract_substring(response_string, start_delim_0, end_delim_0)
    result_1 = extract_substring(response_string, start_delim_1, end_delim)
    result_2 = extract_substring(response_string, start_delim_2, end_delim)
    result_3 = extract_substring(response_string, start_delim_3, end_delim)
    result_4 = extract_substring(response_string, start_delim_4, end_delim)
    result_5 = extract_substring(response_string, start_delim_5, end_delim)
    result_6 = extract_python_code(response_string)
    

    if result_0:
        return result_0
    elif result_1:
        return result_1
    elif result_2:
        return result_2
    elif result_3:
        return result_3
    elif result_4:
        return result_4
    elif result_5:
        return result_5
    elif result_6:
        return result_6
    else:
        print("source code not found or only source code returned")
        # Example usage
        clean_text = remove_think_tags(response_string)
        clean_text = clean_text.replace('Here is the rewritten Python code with the error fixed:', '')
        clean_text = clean_text.replace('```', '') 
        return clean_text


import re

def remove_think_tags(text):
    """Removes text inside <think>...</think> tags, including the tags themselves."""
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()



# save file with full path
def save_file(file_path, file_data):
    print('Generated python code saved to: \n', file_path)
    with open(file_path, 'w') as f:
        f.write(file_data)


def get_base_filename(filename):
    """
    Extract the base part of the filename before any special extension such as '_h5', 'HDF5', 'he5', or 'h5'.
    """
    base_name = os.path.splitext(filename)[0]
    base_name = re.sub(r'(_h5|.HDF5|.he5|.h5|.H5|.hdf5)$', '', base_name, flags=re.IGNORECASE)
    return base_name


def extract_xml_from_llm_response(datasets_response_as_xml_string):
    print(datasets_response_as_xml_string)
    start_delim_1 = "```\n"
    # start_delim_2 = "```\n"
    # start_delim_3 = "```\n"
    end_delim = "```"

    # start_delim_1 = "\n<datasets>\n"
    # start_delim_2 = "```\n"
    # start_delim_3 = "```\n"
    # end_delim = "```"
    # end_delim = "\n</datasets>\n"


    result_1 = extract_substring(datasets_response_as_xml_string['response'], start_delim_1, end_delim)
    # result_2 = extract_substring(datasets_response_as_xml_string['response'], start_delim_2, end_delim)
    # result_3 = extract_substring(datasets_response_as_xml_string['response'], start_delim_3, end_delim)
    if result_1:
        return result_1
    else:
        return datasets_response_as_xml_string
    

def convert_response_into_json_path_list(group_dataset_response):
    # print("\n\ngroup_dataset_response: \n", group_dataset_response)
    start_delim_1 = "```\n"
    start_delim_2 = "```json"
    start_delim_3 = "```\n\n"
    end_delim = "```"

    start_delim_4 = "```json\n[\n"
    end_delim_4 ="]\n```"
    result_1 = False
    result_2 = False
    result_3 = False
    result_4 = False
    result_5 = False
    try:
        result_1 = extract_substring(group_dataset_response, start_delim_1, end_delim)
        result_2 = extract_substring(group_dataset_response, start_delim_2, end_delim)
        result_3 = extract_substring(group_dataset_response, start_delim_3, end_delim)
        result_4 = extract_substring(group_dataset_response, start_delim_4, end_delim_4)
        # result_5 = get_datasets_using_regex_from_text(group_dataset_response)
    except Exception as e:
        print("Exception occurred at Utils.convert_response_into_json_path_list, message: ", e)

    if result_1:
        # print("Utils.convert_response_into_json_path_list, result: \n", result_1)
        return result_1
    elif result_2:
        # print("Utils.convert_response_into_json_path_list, result: \n", result_2)
        return result_2
    elif result_3:
        # print("Utils.convert_response_into_json_path_list, result: \n", result_3)
        return result_3
    elif result_4:
        # print("Utils.convert_response_into_json_path_list, result: \n", result_4)
        return result_4
    elif result_5:
        # print("Utils.convert_response_into_json_path_list, result: \n", result_5)
        return result_5
    else:
        print("source code not found")
        return ""
    

def extract_values_from_json_unknown_objects(obj):
    print("\n\nObject: ", obj)
    if not obj:
        return []
    """ Recursively extracts all values from JSON-like object into a list """
    values = []
    
    if isinstance(obj, dict):
        # If it's a dictionary, get values and recurse
        for value in obj.values():
            values.extend(extract_values_from_json_unknown_objects(value))
    elif isinstance(obj, list):
        # If it's a list, iterate and recurse
        for item in obj:
            values.extend(extract_values_from_json_unknown_objects(item))
    else:
        # Otherwise, it's a simple value, so append it
        values.append(obj)
    
    return values

# Extracting all values from the dataset
# result = extract_values(dataset)

# Output the result
# print(result)


import re
def get_datasets_using_regex_from_text(text_contains_datasets):
    # Sample input text containing the Python code
    print(text_contains_datasets)

    # Regex to extract all values within the 'datasets' list, including anything between the square brackets
    pattern = r'datasets\s*=\s*\[\s*(.*?)\s*\]'

    # Find the 'datasets' content within the input text
    match = re.search(pattern, text_contains_datasets, re.DOTALL)

    if match:
        # Extract the datasets content and split by lines to handle multiple entries
        dataset_content = match.group(1).split(',')

        # Clean up and strip any unwanted characters (quotes, spaces, comments)
        dataset_paths = [item.split('#')[0].strip().strip('"').strip() for item in dataset_content if item.strip()]

        # Print extracted dataset values
        print("Utils.get_datasets_using_regex_from_text Extracted dataset values:", dataset_paths)
        return dataset_paths
    else:
        print("Utils.get_datasets_using_regex_from_text: No datasets found.")
        return []


import json

"""# Example data
input_4 = {
    'datasets': [
        {
            'name': 'aerosol_optical_thickness_550_ocean',
            'path': 'DeepBlue-SeaWiFS-1.0_L3_20100101_v004-20130604T131317Z.h5'
        }
    ]
}"""

# get_datasets_using_regex_from_text(str(input_4))

# """
# Function to flatten the datasets into a list of keys and values
def flatten_datasets_to_list(data):
    print("\nInside Utils.flatten_datasets_to_list, data: ", data)
    datasets = data.get('datasets', [])
    flattened_list = []

    # Iterate through each item in datasets
    for item in datasets:
        print(item)
        if isinstance(item, dict):
            for key, value in item.items():
                flattened_list.extend([key, value])
        else:
            flattened_list.append(item)
    
    return flattened_list

# Convert datasets to a flattened list of keys and values
# flattened_datasets = flatten_datasets_to_list(data)

# Print the result
# print("Flattened datasets:", flattened_datasets)

import json

def check_datasets_object(input_data):
    try:
        print("\n\nInside Utils.check_datasets_object: .....")
        print("Utils.check_datasets_object, input_data: ", input_data)
        if "datasets" in input_data:
            if isinstance(input_data["datasets"], dict):
                return True
        return False
    except Exception as e:
        print("Exception occurred at Utils.check_datasets_object, message: ", e)
        return False  

"""
def check_datasets_object(input_data):
    print("\n\nInside Utils.check_datasets_object: .....")
    print("Utils.check_datasets_object, input_data: ", input_data)
    # Ensure input_data is a dictionary (if it's a JSON string, convert it)
    try:
        if isinstance(input_data, str):
            try:
                input_data = json.loads(input_data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return False

        # Check if 'datasets' key exists in the input dictionary
        if isinstance(input_data, dict) and "datasets" in input_data:
            datasets = input_data["datasets"]
            
            # Case 1: 'datasets' is a list of dictionaries
            if isinstance(datasets, list) and all(isinstance(dataset, dict) for dataset in datasets):
                for dataset in datasets:
                    if 'name' not in dataset or 'path' not in dataset:
                        print("A dictionary in 'datasets' is missing 'name' or 'path'.")
                        return False
                print("'datasets' is a valid list of dictionaries.")
                return True

            # Case 2: 'datasets' is a list of strings
            elif isinstance(datasets, list) and all(isinstance(dataset, str) for dataset in datasets):
                print("'datasets' is a valid list of strings.")
                return True

            # If the list contains mixed types
            else:
                print("'datasets' contains mixed types or invalid data.")
                return False
        else:
            print("'datasets' key is missing or input is not a valid dictionary.")
            return False
    except Exception as e:
        print("Exception occurred at Utils.check_datasets_object, message: ", e)  
"""    


"""
def check_datasets_object(input_data):
    print("\n\nInside Utils.check_datasets_object: .....")
    # Check if 'datasets' key exists in the input dictionary
    try:
        if "datasets" in input_data:
            datasets = input_data["datasets"]
            
            # Case 1: 'datasets' is a list of dictionaries
            if all(isinstance(dataset, dict) for dataset in datasets):
                for dataset in datasets:
                    if 'name' not in dataset or 'path' not in dataset:
                        print("A dictionary in 'datasets' is missing 'name' or 'path'.")
                        return False
                print("'datasets' is a valid list of dictionaries.")
                return True

            # Case 2: 'datasets' is a list of strings
            elif all(isinstance(dataset, str) for dataset in datasets):
                print("'datasets' is a valid list of strings.")
                return True

            # If the list contains mixed types
            else:
                print("'datasets' contains mixed types.")
                return False
        else:
            print("'datasets' key is missing.")
            return False
    except Exception as e:
        print("Exception occurred at Utils.check_datasets_object, message: ", e)
"""

"""
def check_datasets_object(input_data):
    print("\n\nInside Utils.check_datasets_object: .....")
    # Check if 'datasets' key exists in the input dictionary
    try:
        if "datasets" in input_data:
            datasets = input_data["datasets"]
            
            # Check if 'datasets' is a list
            if isinstance(datasets, list):
                # Check if each item in the list is a dictionary
                for dataset in datasets:
                    if not isinstance(dataset, dict):
                        print("An item in 'datasets' is not a dictionary.")
                        return False
                # If all checks passed
                print("'datasets' is a list of dictionaries.")
                return True
            else:
                print("'datasets' is not a list.")
                return False
        else:
            print("'datasets' key is missing.")
            return False
    except Exception as e:
        print("Exception occurred at Utils.check_datasets_object, message: ", e)

"""

"""# Example input
input_data = {
  "datasets": [
    {
      "name": "SalesDataQ1",
      "path": "/data/sales_data/q1"
    },
    {
      "name": "CustomerProfiles",
      "path": "/data/customer_profiles/"
    },
    {
      "name": "MarketResearchReport",
      "path": "/research/market_research/report.csv"
    }
  ]
}"""

# Call the function to check the input
# result = check_datasets_object(input_data)

# Output the result
# print("Result:", result)



def extract_unique_strings(data, result=None):
    if result is None:
        result = set()

    # Regex to match strings with only special characters (e.g., "/")
    special_chars_pattern = re.compile(r'^[^a-zA-Z0-9]+$')

    if isinstance(data, dict):
        for key, value in data.items():
            # Add the key to the set
            result.add(key)
            # If value is a string and doesn't consist of only special characters
            if isinstance(value, str) and not special_chars_pattern.match(value):
                result.add(value)
            # Recursively handle nested dictionaries and lists
            elif isinstance(value, (dict, list)):
                extract_unique_strings(value, result)
    
    elif isinstance(data, list):
        for item in data:
            extract_unique_strings(item, result)
    
    return list(result)


def replace_string(original_string, old_substring, new_substring):
    """
    Replace occurrences of 'old_substring' with 'new_substring' in the 'original_string'.
    
    Args:
    original_string (str): The string where the replacement will occur.
    old_substring (str): The substring to be replaced.
    new_substring (str): The substring to replace with.
    
    Returns:
    str: The modified string with the replacements.
    """
    if old_substring in original_string:
        print(old_substring, " is present")
        return original_string.replace(old_substring, new_substring)
    else:
        print(f"'{old_substring}' not found in the original string.")
        return original_string
    # return original_string.replace(old_substring, new_substring)

# Example usage:
# input_string = "Hello, World! World is beautiful."
# result = replace_string(input_string, "World", "Earth")
# print(result)  # Output: Hello, Earth! Earth is beautiful.



def remove_redundant_paths(paths_list):
    # Sort paths by length (longer paths first, so we can remove shorter ones if they are subsets)
    paths_list.sort(key=len, reverse=True)
    
    # Initialize a list to store the non-redundant paths
    result = []
    
    # Iterate through the sorted paths
    for path in paths_list:
        # Check if the current path is a subset of any path already in the result
        if not any(p.startswith(path + '/') or p == path for p in result):
            result.append(path)
    
    # Sort the result back by path name if you want to maintain original order
    # result.sort()
    
    return result

"""
# Input list of paths
paths_list = [
    'HDFEOS', 'HDFEOS/ADDITIONAL', 'HDFEOS/ADDITIONAL/FILE_ATTRIBUTES', 'HDFEOS/ZAS', 
    'HDFEOS/ZAS/HIRDLS', 'HDFEOS/ZAS/HIRDLS/Data Fields', 'HDFEOS/ZAS/HIRDLS/Data Fields/Day', 
    'HDFEOS/ZAS/HIRDLS/Data Fields/Latitude', 'HDFEOS/ZAS/HIRDLS/Data Fields/LocalSolarTimeAscending', 
    'HDFEOS/ZAS/HIRDLS/Data Fields/LocalSolarTimeDescending', 'HDFEOS/ZAS/HIRDLS/Data Fields/Month', 
    'HDFEOS/ZAS/HIRDLS/Data Fields/NO2Ascending', 'HDFEOS/ZAS/HIRDLS/Data Fields/NO2AscendingCovariance', 
    'HDFEOS/ZAS/HIRDLS/Data Fields/NO2AscendingDataCount', 'HDFEOS/ZAS/HIRDLS/Data Fields/NO2AscendingPrecision', 
    'HDFEOS/ZAS/HIRDLS/Data Fields/NO2Descending', 'HDFEOS/ZAS/HIRDLS/Data Fields/NO2DescendingCovariance', 
    'HDFEOS/ZAS/HIRDLS/Data Fields/NO2DescendingDataCount', 'HDFEOS/ZAS/HIRDLS/Data Fields/NO2DescendingPrecision', 
    'HDFEOS/ZAS/HIRDLS/Data Fields/Pressure', 'HDFEOS/ZAS/HIRDLS/Data Fields/SolarZenithAngleAscending', 
    'HDFEOS/ZAS/HIRDLS/Data Fields/SolarZenithAngleDescending', 'HDFEOS/ZAS/HIRDLS/Data Fields/Time', 
    'HDFEOS/ZAS/HIRDLS/Data Fields/Year', 'HDFEOS/ZAS/HIRDLS/nCoeffs', 'HDFEOS/ZAS/HIRDLS/nLats', 
    'HDFEOS/ZAS/HIRDLS/nLevels', 'HDFEOS/ZAS/HIRDLS/nTimes', 'HDFEOS INFORMATION', 
    'HDFEOS INFORMATION/StructMetadata.0', 'HDFEOS INFORMATION/coremetadata.0', 
    'HDFEOS/ZAS/HIRDLS/nCoeffs/NAME', 'HDFEOS/ZAS/HIRDLS/Data Fields/Day/Units'
]

# Get the non-redundant paths
result = remove_redundant_paths(paths_list)

# Print the results
print("\n".join(result))
"""


from collections import defaultdict

# Function to extract base paths and their rightmost components
def extract_paths_with_attributes(paths_list):
    base_paths = defaultdict(set)

    for path in paths_list:
        # Split the path into components
        components = path.split('/')
        
        # Join all but the last component to form the base path
        base_path = '/'.join(components[:-1])
        
        # Add the full last component to the corresponding base path
        rightmost_component = components[-1]
        base_paths[base_path].add(rightmost_component)

        # If the last component has further subcomponents (e.g., AscDescMode/Title)
        if '/' in rightmost_component:
            base_paths[base_path].add(rightmost_component)

    # Prepare the output as a list of formatted strings
    output_list = [f"{base_path}: {{{', '.join(attributes)}}}" for base_path, attributes in base_paths.items()]

    return output_list
"""
# Input list of paths
paths_list = [
    'HDFEOS/SWATHS/BrO-APriori/Geolocation Fields/OrbitGeodeticAngle',
    'HDFEOS/SWATHS/BrO-APriori/Geolocation Fields/LineOfSightAngle',
    'HDFEOS/SWATHS/BrO-APriori/Geolocation Fields/SolarZenithAngle',
    'HDFEOS/SWATHS/BrO-APriori/Geolocation Fields/LocalSolarTime',
    'HDFEOS/SWATHS/BrO-APriori/Geolocation Fields/ChunkNumber',
    'HDFEOS/SWATHS/BrO/Geolocation Fields/OrbitGeodeticAngle',
    'HDFEOS/SWATHS/BrO-APriori/Geolocation Fields/Longitude',
    'HDFEOS/SWATHS/BrO-APriori/Geolocation Fields/Pressure',
    'HDFEOS/SWATHS/BrO/Geolocation Fields/LineOfSightAngle',
    'HDFEOS/SWATHS/BrO/Geolocation Fields/SolarZenithAngle',
    'HDFEOS/SWATHS/BrO-APriori/Geolocation Fields/Latitude',
    'HDFEOS/SWATHS/BrO/Geolocation Fields/LocalSolarTime',
    'HDFEOS/SWATHS/BrO-APriori/Data Fields/L2gpPrecision',
    'HDFEOS/SWATHS/BrO-APriori/Data Fields/AscDescMode',
    'HDFEOS/SWATHS/BrO-APriori/Data Fields/Convergence',
    'HDFEOS/SWATHS/BrO-APriori/Geolocation Fields/Time',
    'HDFEOS/SWATHS/BrO/Geolocation Fields/ChunkNumber',
    'HDFEOS/SWATHS/BrO-APriori/Data Fields/L2gpValue',
    'HDFEOS/SWATHS/BrO/Data Fields/AscDescMode/Title',
    'HDFEOS/SWATHS/BrO/Data Fields/AscDescMode/Units',
    'HDFEOS/SWATHS/BrO/Geolocation Fields/Longitude',
    'HDFEOS/SWATHS/BrO/Geolocation Fields/Pressure',
    'HDFEOS/SWATHS/BrO/Geolocation Fields/Latitude',
    'HDFEOS/SWATHS/BrO-APriori/Data Fields/Quality',
    'HDFEOS/SWATHS/BrO-APriori/Data Fields/Status',
    'HDFEOS/SWATHS/BrO/Data Fields/L2gpPrecision',
    'HDFEOS/SWATHS/BrO/Data Fields/Convergence',
    'HDFEOS/SWATHS/BrO/Geolocation Fields/Time',
    'HDFEOS/SWATHS/BrO/Data Fields/L2gpValue',
    'HDFEOS/SWATHS/BrO/Data Fields/Quality',
    'HDFEOS/SWATHS/BrO-APriori/nTimesTotal',
    'HDFEOS/SWATHS/BrO/Data Fields/Status',
    'HDFEOS/SWATHS/BrO-APriori/nLevels',
    'HDFEOS/SWATHS/BrO-APriori/nTimes',
    'HDFEOS/SWATHS/BrO/nTimesTotal',
    'HDFEOS/SWATHS/BrO/nLevels',
    'HDFEOS/SWATHS/BrO/nTimes'
]

# Get the base paths with their rightmost components
output = extract_paths_with_attributes(paths_list)

# Print the output list
print(output)

Output:
[
    'HDFEOS/SWATHS/BrO-APriori/Geolocation Fields: {OrbitGeodeticAngle, LineOfSightAngle, SolarZenithAngle, LocalSolarTime, ChunkNumber, Longitude, Pressure, Latitude, Time}',
    'HDFEOS/SWATHS/BrO-APriori/Data Fields: {L2gpPrecision, AscDescMode, Convergence, L2gpValue, Quality, Status}',
    'HDFEOS/SWATHS/BrO/Geolocation Fields: {OrbitGeodeticAngle, LineOfSightAngle, SolarZenithAngle, LocalSolarTime, ChunkNumber, Longitude, Pressure, Latitude, Time}',
    'HDFEOS/SWATHS/BrO/Data Fields: {AscDescMode/Title, AscDescMode/Units, L2gpPrecision, Convergence, L2gpValue, Quality, Status}',
    'HDFEOS/SWATHS/BrO-APriori: {nTimesTotal, nLevels, nTimes}',
    'HDFEOS/SWATHS/BrO: {nTimesTotal, nLevels, nTimes}'
]
"""

def split_and_extend_paths(paths_list):
    new_list = []
    
    # Iterate through the input list
    for path in paths_list:
        # If the item contains '/', split it by '/'
        if '/' in path:
            # Split the path and extend the new list with the non-empty components
            # new_list.extend([part for part in path.split('/') if part])

            # Split the paths by space, hyphen, and / and extend the paths list
            new_list.extend([part for part in re.split(r'[ /-]+', path) if part])
        else:
            # If no '/', just add the item to the new list
            new_list.append(path)
    
    # Return the new extended list
    return new_list

"""
# Input list of paths
paths_list = ['/gt1l', 'full_path', '/gt1l/segment_lat', 'segment_lon', 'group', 
              'segment_geoid', 'attributes', '/gt1l/segment_geoid', 
              '/gt1l/segment_lon', 'segment_lat', 'dataset']

# Get the new list
result = split_and_extend_paths(paths_list)

# Print the resulting list
print(result)
"""


import re

# Remove non-letter characters and convert to lowercase
def normalize(s):
        return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

def match_strings(str1, str2):
    # Normalize both strings and compare
    return normalize(str1) == normalize(str2)

"""
# Example usage
str1 = "fill_value"
str2 = "_FillValue"

if match_strings(str1, str2):
    print(f"'{str1}' and '{str2}' match.")
else:
    print(f"'{str1}' and '{str2}' do not match.")
"""

import re


# Define the text you want to tokenize
# text = "We need to read data from the dataset. After accessing the paths, we will plot a graph. Attribute extraction is required."

import re

# Define the list of keywords
priority_words = ['read data', 'dataset', 'paths', 'plot', 'graph', 'access', 'path', 'attribute', 'group', 'from source']

# Define the text you want to tokenize
# text = """We need to read data from the dataset. 
# After accessing the paths, we will plot a graph. Attribute extraction is required."""

# Function to prioritize tokenization based on keywords
def tokenize_with_priority(text, priority_words):
    # Create a pattern for priority words (join them with | for "or")
    # pattern = '|'.join(map(re.escape, priority_words))
    
    # Use regular expression to split the text around priority words, while keeping the words
    # tokens = re.split(f'({pattern})', text)
    tokens = re.split(f'\t', text)

    # Further split any token that is not a priority word (on spaces, hyphens, etc.)
    final_tokens = []
    for token in tokens:
        if token in priority_words:
            final_tokens.append(token)
        else:
            # Split by spaces, hyphens, commas, and newlines, and remove empty tokens
            final_tokens.extend(re.split(r'[ \-/,]+', token))

    # Remove empty strings and \n characters, and keep only unique tokens
    unique_tokens = list(set([tok for tok in final_tokens if tok.strip() and tok != '\n']))

    return unique_tokens

# Tokenize the text
# tokens = tokenize_with_priority(text, priority_words)

# Print the tokenized result
# print(tokens)


def tokenize_with_space_and_sort_reversed(text):
    # Create a pattern for priority words (join them with | for "or")
    # pattern = '|'.join(map(re.escape, priority_words))
    
    # Use regular expression to split the text around priority words, while keeping the words
    # tokens = re.split(f'({pattern})', text)
    tokens = text.split()
    
    unique_tokens = list(set([tok for tok in tokens if tok.strip() and tok != '\n']))
    unique_tokens = sorted(unique_tokens, key=len, reverse=True)


    return unique_tokens


def make_dictionary_of_score(tokens, real_datasets):
    whole_score_paths_dic = {}
    
    final_five_paths = []
    for token in tokens:
        for dataset in real_datasets:
            if token in dataset:
                if dataset in whole_score_paths_dic:
                    whole_score_paths_dic[dataset]=whole_score_paths_dic[dataset]+1
                else:
                    whole_score_paths_dic[dataset]=1

    # Sample dictionary
    # my_dict = {'a': 10, 'b': 5, 'c': 20, 'd': 15, 'e': 25, 'f': 8, 'g': 3}

    # Sorting the dictionary by value in descending order and getting the top 5
    if whole_score_paths_dic is not None:
        whole_score_paths_dic = dict(sorted(whole_score_paths_dic.items(), key=lambda item: item[1], reverse=True))
        # print("\n sorted dictionary: \n", whole_score_paths_dic)
        if len(whole_score_paths_dic)>5:
            top_five = list(whole_score_paths_dic)[:5]
            final_five_paths = top_five
        else:
            top_five = whole_score_paths_dic
        final_five_paths = list(whole_score_paths_dic.keys())

        print(top_five)

    # print("\nTo five paths based on score: \n", final_five_paths)


    return final_five_paths

from difflib import get_close_matches
def get_all_closed_paths_sn_matcher(input_tokens, all_paths):
    matching_paths = set()
    
    # For each token in input text, try to find matching paths
    for token in input_tokens:
        # Get close matches for the token in the list of paths
        matched = get_close_matches(token, all_paths, n=5, cutoff=0.6)
        matching_paths.update(matched)

    return list(matching_paths)



def extend_list_by_making_paths_into_single_words(combined_paths, result=None):
    if result is None:
        result = set()

    
    for path in combined_paths:
        paths = path.split('/')
        for p in paths:
            result.add(p)

    return list(result)



# testing string fuzzy matching library
from rapidfuzz import process

# Sample lists of strings
# list1 = ['apple', 'orange', 'banana', 'grape']
# list2 = ['apple', 'berry', 'banana', 'pineapple', 'grapefruit']

# Function to find the most common strings between two lists based on similarity
def find_common_strings(list1, list2, threshold=80):
    common_strings = []
    all_matching_output = []

    common_strings_by_extract = []
    all_matching_output_by_extract = []
    
    # For each string in list1, find the best match from list2
    for item in list1:
        # Find the best match for 'item' in list2
        best_match = process.extractOne(item, list2, score_cutoff=threshold)
        
        # If a match with sufficient similarity is found, add it to the common list
        if best_match:
            common_strings.append(best_match[0])
            all_matching_output.extend(best_match)

        # testing about extract function
        best_match_by_extract = process.extract(item, list2, score_cutoff=threshold)
        
        # If a match with sufficient similarity is found, add it to the common list
        if best_match_by_extract:
            common_strings_by_extract.append(best_match_by_extract[0])
            all_matching_output_by_extract.extend(best_match_by_extract)
    
    return common_strings, all_matching_output, common_strings_by_extract, all_matching_output_by_extract

# Find the common strings
# common_strings = find_common_strings(list1, list2)

# Output the results
# print("Common strings based on similarity:", common_strings)
 

#  decision maker about the final list of datasets
def decision_maker_about_the_final_list_of_datasets(exact_matched_datasets, exact_matched_datasets_by_name, exact_matched_group_subgroups, exact_matched_group_subgroups_by_name, rapid_fuzz_best_matched_output):
    final_set = set ()

    # take all exact matched dataset paths
    if len(exact_matched_datasets)>0:
        for dataset in exact_matched_datasets:
            final_set.add(dataset)

    # add the exact matched datasets by name to the final set if the lenths are samll
    if len(final_set)<1 and len(exact_matched_datasets)>0 and len(exact_matched_datasets) <= 5 and len(exact_matched_datasets_by_name)<=5:
        for dataset in exact_matched_datasets_by_name:
            final_set.add(dataset)

    # take all exact matched dataset paths matched by name if the length is small
    if len(final_set)<1 and len(exact_matched_datasets)<1 and len(exact_matched_datasets_by_name)<=5:
        for dataset in exact_matched_datasets_by_name:
            final_set.add(dataset)


     # filter the exact matched datasets by name if the lenght is bigger based on the exact group names and also the exact match group name size is small
    if len(final_set)<1 and len(exact_matched_datasets)<1 and len(exact_matched_datasets_by_name)>10 and len(exact_matched_group_subgroups) >0 and len(exact_matched_group_subgroups)<=5:
        for group in exact_matched_group_subgroups:
            for dataset in exact_matched_datasets_by_name:
                if dataset.startswith(group):
                    final_set.add(dataset)
    
      # filter the exact matched datasets by name if the lenght is bigger based on the exact group names and also the exact match group name size is small
    if len(final_set)<1 and len(exact_matched_datasets)<1 and len(exact_matched_datasets_by_name)>10 and len(exact_matched_group_subgroups)<1 and len(exact_matched_group_subgroups_by_name) >0 and len(exact_matched_group_subgroups_by_name)<=5:
        for group in exact_matched_group_subgroups_by_name:
            for dataset in exact_matched_datasets_by_name:
                if dataset.startswith(group):
                    final_set.add(dataset)


    if len(final_set)<1 and len(rapid_fuzz_best_matched_output)<=10:
        num = 5
        for dataset in rapid_fuzz_best_matched_output:
                final_set.add(dataset)
                if num<1:
                    break
                num-=1

    # if nothing matched with direct dataset or group name then take help from rapid fuzzy match
    if len(final_set)<1 and len(exact_matched_group_subgroups)>0:
        for group in exact_matched_group_subgroups_by_name:
            for dataset in rapid_fuzz_best_matched_output:
                if dataset.startswith(group):
                    final_set.add(dataset)

    if len(final_set)<1 and len(exact_matched_group_subgroups)<1 and len(exact_matched_group_subgroups_by_name) >0:
        for group in exact_matched_group_subgroups_by_name:
            for dataset in rapid_fuzz_best_matched_output:
                if dataset.startswith(group):
                    final_set.add(dataset)

    if len(final_set)>0:
        return list(final_set)
    else:
        return list(rapid_fuzz_best_matched_output)
    



def generate_2grams(text):
    # Split text into words
    words = text.split()
    
    # Create 2-grams
    bigrams = [" ".join(words[i:i+2]) for i in range(len(words) - 1)]
    
    return bigrams

# Example usage
# input_text = "This is an example of a 2-gram tokenizer."
# print(generate_2grams(input_text))





# this is for replacing incorrect datasets and attributes names from user input directly
# created 03 Nov 2024
def replace_user_input_attributes_with_origial_attributes(sequential_tokens, original_datasets_attributes_list):
    punctuations_list = []
    i = 0
    result = []
    
    while i < len(sequential_tokens):
        # Try to find a bigram match
        
        bigram_match_flag = False
        if i< len(sequential_tokens)-1:
            if not (sequential_tokens[i]=='/' or sequential_tokens[i + 1]=='/'):
                bigram = sequential_tokens[i] + " " + sequential_tokens[i + 1]
                for dataset_attribute in original_datasets_attributes_list:
                    if normalize(bigram)==normalize(dataset_attribute):
                        # print(f'{normalize(bigram)}=={normalize(dataset_attribute)}')
                        result.append(dataset_attribute)
                        bigram_match_flag=True
                        i += 2
                        break

        # If no bigram match, try a single token match
        if bigram_match_flag==False:
            monogram_match_flag = False            
            for dataset_attribute in original_datasets_attributes_list:
                if normalize(sequential_tokens[i])==normalize(dataset_attribute):
                    # print(f'{sequential_tokens[i]}=={normalize(dataset_attribute)}')
                    result.append(dataset_attribute)
                    i+=1
                    monogram_match_flag = True
                    break
            
            if monogram_match_flag==False:
                # Concatenate with the next token if no single token match
                # if i+1 == len(sequential_tokens) - 1:
                    # result.append(sequential_tokens[i] + " " + sequential_tokens[i + 1])
                result.append(sequential_tokens[i])
                i+=1
                # result.append(sequential_tokens[i + 1])
                    # result.append(sequential_tokens[i])
                    # i += 2
                # else:
                    # result.append(sequential_tokens[i])
        
        # i += 1
    
    # return " ".join(result)
    # print('\n------------result-----------------:\n', result)
    return reconstruct_text_by_keeping_the_spaces(result)

# Example usage
# tokens = ["apple", "pie", "is", "delicious", "apple"]
# match_list = ["apple pie", "delicious"]
# print(merge_tokens(tokens, match_list))


# split user input into tokens based on space,
# To split the text by spaces first, and then by additional punctuation characters (', ", ., ,, ?, (, ), :, ;, !, -, <, >, /), 
# you can extend the regular expression pattern to include these symbols as well:
import re

def split_text_based_on_space_and_punctuations(text):
    # Step 1: Split by spaces
    space_split = text.split()

    # Step 2: Further split by various punctuation marks
    result = []
    for part in space_split:
        # Split by specified punctuation marks while keeping them as separate elements
        # tokens = re.split(r"([\"\'.,?!()<>:;!-/])", part)
        
        # split by space only
        tokens = re.split(r"([\"\'\`.,?!()<>:;!-/])", part)
        
        
        result.extend([token for token in tokens if token])  # Remove any empty tokens

    return result

# Example usage
# text = 'Hello "world"! How are you today? Let\'s split (properly) by - punctuation.'
# print(split_text(text))



# reconstruct the text by removing spaces 
def reconstruct_text_by_keeping_the_spaces(tokens):
    text = ""
    punctuation = {"'", "`", '"', "(", ")", "!", "-", "<", ">", "/"}
    extensions = {".HDF5", ".hdf5", ".HE5", ".he5", ".H5", ".h5"}  # Add more extensions as needed
    

    for i, token in enumerate(tokens):
        # Handle cases for extensions
        print(f'tokens[i - 1]{tokens[i - 1]}, (tokens[i - 1] + token): {tokens[i - 1] + token}')
        if i > 0 and tokens[i - 1] == '.' and (tokens[i - 1] + token) in extensions:
            print('-----------Extension----------')
            text += token  # Append without space
        elif token in {".", ":", ",", ";", "?"}:
            # Add required spaces after specific punctuation
            text += token + " "
        elif token == "/":
            # Append without a leading space for "/"
            text += token
        elif i == 0 or tokens[i - 1] in punctuation or tokens[i - 1] == ".":
            # If first word or after punctuation
            text += token
        else:
            # print('-----------Else Extension----------')
            text += " " + token

    return text.strip()
    """for i, token in enumerate(tokens):
        # Handle cases for extensions
        if i > 0 and tokens[i - 1] == '.' and (tokens[i - 1] + token) in extensions:
            text += token  # Append without space
        elif token in {".", ":", ",", ";", "?"}:
            # If token is punctuation that requires spacing afterward
            text += token + " "
        elif i == 0 or tokens[i - 1] in punctuation or tokens[i - 1] == ".":
            # If first word or after punctuation
            text += token
        else:
            text += " " + token

    return text.strip()"""

# Example usage
# tokens = ['Hello', '.', 'This', 'is', 'a', 'file', '.', 'txt', 'Check', 'out', 'the', 'graph', ':', 'it', 'is', 'interesting', '?']
# print(reconstruct_text(tokens))


"""def reconstruct_text_by_keeping_the_spaces(tokens):
    text = ""
    punctuation = {"'", '"', ".", ",", "?", "(", ")", ":", ";", "!", "-", "<", ">", "/"}
    extensions = {".HDF5", ".hdf5", ".HE5", ".he5", ".H5", ".h5"}  # Add more extensions as needed
    
    for i, token in enumerate(tokens):
        # Check if the token is a file extension
        if i > 0 and tokens[i - 1] == '.':
            if (tokens[i - 1] + token) in extensions:
                text += token  # Append extension without extra space
            else:
                text = text + token+' '
        elif i == 0 or token in punctuation or tokens[i - 1] in punctuation:
            text += token
        else:
            text += " " + token
            
    return text"""

# Example usage
# tokens = ['file', '.', 'txt', 'and', 'image', '.', 'jpg', '!', 'Are', 'you', 'sure', '?']
# print(reconstruct_text(tokens))

import re

"""def tokenize_and_replace(text, match_list):
    
    punctuations = set(". , ; : ? ! ( ) ' \" < > -".split())
    path_separator = "/"

    start = 0
    end = start 
    result = ''
    while start < len(text):
        if text[end]=='.':
            

        if text[end] in punctuations:"""





def tokenize_and_replace(text, match_list):
    
    word_scoring = {
        'monogram': '',
        'bigram': '',
        'matching_words_and_scores': {}
    }    
    
    result = []
    punctuations = set(". , ; : ? ! ( ) ' \" < > -".split())
    path_separator = "/"

    start = 0
    while start < len(text):
        while start < len(text) and text[start].isspace():
            start += 1
            result.append(' ')
        if start >= len(text):
            break
        
        end = start
        # Handle punctuation and path separator as individual tokens
        if text[start] in punctuations or text[start] == path_separator:
            result.append(text[start])
            start += 1
            continue
        
        # Identify a single token
        while end < len(text) and text[end] not in punctuations and text[end] != path_separator and not text[end].isspace():
            end += 1
        single_token = text[start:end]
        
        # Check for a double token
        next_start = end
        while next_start < len(text) and text[next_start].isspace():
            next_start += 1
        next_end = next_start
        while next_end < len(text) and text[next_end] not in punctuations and text[next_end] != path_separator and not text[next_end].isspace():
            next_end += 1
        double_token = f"{single_token} {text[next_start:next_end]}"
        
        # Check and replace double token if it exists in match list
        double_token_match_found = False
        for dataset_attribute in match_list:
            # related to edit distance calculations
            # word_scoring['bigram'] = double_token
            # word_scoring['bigram'] = double_token


            if normalize(double_token)==normalize(dataset_attribute):
                print(f'double token matching: {double_token}== {dataset_attribute}')
        # if double_token in match_list:
                # replace_index = match_list.index(double_token)
                # result.append(match_list[replace_index])
                result.append(dataset_attribute)
                # res = ''.join(result)
                # print(f'Current result: {res}')
                start = next_end
                # start = end+len(double_token)
                double_token_match_found=True
                break
        
        single_token_match_found = False
        if not double_token_match_found:
            for dataset_attribute in match_list:
                if normalize(single_token)==normalize(dataset_attribute):
                    # print(f'single token matching: {single_token} == {dataset_attribute}')
                    res=''.join(result)
                    # print(f'Current result: {res}')
                # elif single_token in match_list:
                # replace_index = match_list.index(single_token)
                # result.append(match_list[replace_index])
                    result.append(dataset_attribute)
                    start = end
                    # start = end+len(single_token)
                    single_token_match_found = True
                    break
        if double_token_match_found==False and single_token_match_found==False:
            result.append(single_token)
            res=''.join(result)
            # print(f'Else Current result: {res}')

            start = end

    return ''.join(result)


# created on Nov 08, 2024
# adding Levenshtein scoring based matching with normalized equal condition 
def tokenize_and_replace_with_Levenshtein(text, match_list):
    
    word_scoring = {
        'monogram': '',
        'bigram': '',
        'matching_words_and_scores': {}
    }    
    
    result = []
    punctuations = set(". , ; : ? ! ( ) ' \" < > -".split())
    path_separator = "/"

    start = 0
    while start < len(text):
        while start < len(text) and text[start].isspace():
            start += 1
            result.append(' ')
        if start >= len(text):
            break
        
        end = start
        # Handle punctuation and path separator as individual tokens
        if text[start] in punctuations or text[start] == path_separator:
            result.append(text[start])
            start += 1
            continue
        
        # Identify a single token
        while end < len(text) and text[end] not in punctuations and text[end] != path_separator and not text[end].isspace():
            end += 1
        single_token = text[start:end]
        
        # Check for a double token
        next_start = end
        while next_start < len(text) and text[next_start].isspace():
            next_start += 1
        next_end = next_start
        while next_end < len(text) and text[next_end] not in punctuations and text[next_end] != path_separator and not text[next_end].isspace():
            next_end += 1
        double_token = f"{single_token} {text[next_start:next_end]}"
        
        # Check and replace double token if it exists in match list
        double_token_match_found = False
        for dataset_attribute in match_list:
            # related to edit distance calculations
            # word_scoring['bigram'] = double_token
            # word_scoring['bigram'] = double_token


            if normalize(double_token)==normalize(dataset_attribute):
                print(f'double token matching: {double_token}== {dataset_attribute}')
                # replace_index = match_list.index(double_token)
                # result.append(match_list[replace_index])
                result.append(dataset_attribute)
                # res = ''.join(result)
                # print(f'Current result: {res}')
                start = next_end
                # start = end+len(double_token)
                double_token_match_found=True
                break
       
        
        
       
        
        single_token_match_found = False
        if not double_token_match_found:
            for dataset_attribute in match_list:
                if normalize(single_token)==normalize(dataset_attribute):
                    print(f'single token matching: {single_token} == {dataset_attribute}')
                    # res=''.join(result)
                    # print(f'Current result: {res}')
                # elif single_token in match_list:
                # replace_index = match_list.index(single_token)
                # result.append(match_list[replace_index])
                    result.append(dataset_attribute)
                    start = end
                    # start = end+len(single_token)
                    single_token_match_found = True
                    break
            
            
            

        if double_token_match_found==False and single_token_match_found==False:
             # this is for the lavenshtein edit distance matching
            if not double_token_match_found:
                for dataset_attribute in match_list:
                    if levenshtein_similarity(normalize(double_token), normalize(dataset_attribute))>0.87:
                        print(f'with levenshtein with normalize double token matching: {double_token}== {dataset_attribute}')
                        # replace_index = match_list.index(double_token)
                        # result.append(match_list[replace_index])
                        result.append(dataset_attribute)
                        # res = ''.join(result)
                        # print(f'Current result: {res}')
                        start = next_end
                        # start = end+len(double_token)
                        double_token_match_found=True
                        break

            # this is for the lavenshtein edit distance
            if not double_token_match_found:
                for dataset_attribute in match_list:
                    if levenshtein_similarity(double_token, dataset_attribute)>0.80:
                        print(f'with levenshtein without normalize double token matching: {double_token}== {dataset_attribute}')
                        # replace_index = match_list.index(double_token)
                        # result.append(match_list[replace_index])
                        result.append(dataset_attribute)
                        # res = ''.join(result)
                        # print(f'Current result: {res}')
                        start = next_end
                        # start = end+len(double_token)
                        double_token_match_found=True
                        break

            if single_token_match_found==False:
                for dataset_attribute in match_list:
                    if levenshtein_similarity(normalize(single_token), normalize(dataset_attribute))>0.85:
                        print(f'with lavenshtein with normalize single token matching: {single_token} == {dataset_attribute}')
                        result.append(dataset_attribute)
                        start = end
                        # start = end+len(single_token)
                        single_token_match_found = True
                        break
            if single_token_match_found==False:
                for dataset_attribute in match_list:
                    if levenshtein_similarity(single_token, dataset_attribute)>0.80:
                        print(f'with lavenshtein without normalize single token matching: {single_token} == {dataset_attribute}')
                        result.append(dataset_attribute)
                        start = end
                        # start = end+len(single_token)
                        single_token_match_found = True
                        break
            if double_token_match_found==False and single_token_match_found==False:
                result.append(single_token)
                # res=''.join(result)
                # print(f'Else Current result: {res}')

                start = end

    return ''.join(result)

import Levenshtein
def levenshtein_similarity(text1, text2):
    distance = Levenshtein.distance(text1, text2)
    max_len = max(len(text1), len(text2))
    return 1 - distance / max_len



def get_attribute_name_condition_condition_value(user_intent):
    user_intent = user_intent.split(',')
    print('Splited user intent: ', user_intent)
    attribute_name = ''
    condition = ''
    condition_value = ''
    
    print('Length of user inten: ', len(user_intent))

    if len(user_intent)>1:
        attribute_name = user_intent[1].strip()
    if len(user_intent)>2:
        conditions = user_intent[2].strip()
        conditions = conditions.split()
        print('Conditions: ', conditions)
        if len(conditions)>=2:
            condition = conditions[0]
            condition_value = conditions[1]
    
    print(f"attribute_name: {attribute_name}, condition: {condition}, condition_value: {condition_value}")
    return attribute_name, condition, condition_value



"""
# Next code suggested by 

import re

def replace_tokens(text, match_list):
    # Tokenize text based on punctuation and spaces but keep punctuation in the text
    tokens = re.findall(r'\S+|\s+|[.,;:?!()\'"<>-]|/', text)
    
    i = 0
    while i < len(tokens):
        # Process double tokens (two-word phrases)
        if i < len(tokens) - 2 and tokens[i+1] == " ":
            double_token = tokens[i] + " " + tokens[i+2]
            if double_token in match_list:
                replace_index = match_list.index(double_token)
                tokens[i] = match_list[replace_index]
                tokens[i+1] = ""
                tokens[i+2] = ""
                i += 3
                continue
        
        # Process single tokens
        single_token = tokens[i]
        if single_token in match_list:
            replace_index = match_list.index(single_token)
            tokens[i] = match_list[replace_index]
        
        i += 1

    # Reconstruct the text with replacements
    replaced_text = ''.join(tokens)
    return replaced_text

# Example usage
text = "This is a test text, with paths/ and punctuation! Check for words."
match_list = [
    "exam content",  # Replacement for "test text"
    "quiz",          # Replacement for "test"
    "symbols"        # Replacement for "punctuation"
]

# Run the function
replaced_text = replace_tokens(text, match_list)
print(replaced_text)


"""


# Example text and matching list
# text = "This is a test text, with paths/ and punctuation! Check for words."
# match_list = [
    # "exam content",  # replacement for "test text"
    # "quiz",          # replacement for "test"
    # "symbols"        # replacement for "punctuation"
# ]

# Run the function
# replaced_text = tokenize_and_replace(text, match_list)
# print(replaced_text)



"""
def tokenize_and_process(text):
    single_tokens = []
    double_tokens = []

    # Define punctuation and symbols to check
    punctuations = set(". , ; : ? ! ( ) ' \" < > -".split())
    path_separator = "/"

    # Initialize pointers
    start = 0
    while start < len(text):
        # Skip whitespace
        while start < len(text) and text[start].isspace():
            start += 1
        if start >= len(text):
            break
        
        # Single word or punctuation token
        end = start
        if text[start] in punctuations or text[start] == path_separator:
            single_tokens.append(text[start])
            start += 1
            continue
        else:
            while end < len(text) and text[end] not in punctuations and text[end] != path_separator and not text[end].isspace():
                end += 1
            
            token = text[start:end]
            single_tokens.append(token)
            
            # Check for double word tokens
            next_start = end
            while next_start < len(text) and text[next_start].isspace():
                next_start += 1
            next_end = next_start
            while next_end < len(text) and text[next_end] not in punctuations and text[next_end] != path_separator and not text[next_end].isspace():
                next_end += 1
            
            if next_start < len(text):
                double_token = f"{token} {text[next_start:next_end]}"
                double_tokens.append(double_token)
        
        # Skip to next segment
        start = end

    return single_tokens, double_tokens
"""
# Example text
# text = "This is a test text, with /paths/ and punctuation! Check for words."

# Process tokens
# single_tokens, double_tokens = tokenize_and_process(text)

# print("Single Tokens:", single_tokens)
# print("Double Tokens:", double_tokens)


"""
import re

def tokenize_and_process(text):
    single_tokens = []
    double_tokens = []
    
    # Define punctuation and symbols to check
    punctuations = set(". , ; : ? ! ( ) ' \" < > -".split())
    path_separator = "/"

    # Initialize pointers
    start = 0
    while start < len(text):
        # Find the next word or punctuation
        end = start
        while end < len(text) and text[end] not in punctuations and text[end] != path_separator:
            end += 1

        # Single word token
        token = text[start:end].strip()
        if token:
            single_tokens.append(token)
        
        # Double word token
        if end + 1 < len(text):
            next_end = end + 1
            while next_end < len(text) and text[next_end] not in punctuations and text[next_end] != path_separator:
                next_end += 1
            double_token = f"{token} {text[end+1:next_end].strip()}"
            double_tokens.append(double_token)

        # Replace operations on specific tokens
        if token in ["replace_this_word", "other_word"]:  # Specify tokens to replace
            text = text.replace(token, "replacement_word")
        if double_token in ["double_word_example"]:
            text = text.replace(double_token, "replacement_double_word")
        
        # Skip to next word or punctuation
        start = end + 1

    return single_tokens, double_tokens, text
"""

# Example text
# text = "This is a test text, with /paths/ and punctuation! Check for words."

# Process tokens and updated text
# single_tokens, double_tokens, updated_text = tokenize_and_process(text)

# print("Single Tokens:", single_tokens)
# print("Double Tokens:", double_tokens)
# print("Updated Text:", updated_text)


import shutil
from pathlib import Path

def collect_and_store_png(source_dirs, base_path, new_dir_name, data_dir):
    # Ensure base_path is absolute
    base_path = Path(base_path).resolve()
    print(f'base path: {base_path}')

    # Create unique directory (append _v2, _v3, etc. if it already exists)
    target_dir = base_path/ 'generated_image_from_running_evaluation' / new_dir_name
    print(f'target dir: {target_dir}')

    counter = 2
    while target_dir.exists():
        target_dir = base_path/ 'generated_image_from_running_evaluation' / f"{new_dir_name}_v{counter}"
        counter += 1
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"Saving PNG files to: {target_dir}")

    # Collect and copy PNG files
    for directory in source_dirs:
        directory = Path(base_path/data_dir/directory).resolve()
        print("Directory: ", directory)
        if directory.exists():
            for png_file in directory.glob("*.png"):  # Search for PNG files
                print(f'Moving file {png_file} to {target_dir / png_file.name}')
                shutil.move(png_file, target_dir / png_file.name)  # Copy to target

    print("PNG collection and transfer complete!")


def collect_and_store_png_without_data_dir(source_dirs, target_dir_base_path, new_dir_name):
    try:
        # Ensure base_path is absolute
        target_dir_base_path = Path(target_dir_base_path).resolve()
        print(f'base path: {target_dir_base_path}')

        # Create unique directory (append _v2, _v3, etc. if it already exists)
        target_dir = target_dir_base_path/ 'generated_image_from_running_evaluation' / new_dir_name
        print(f'target dir: {target_dir}')

    
        target_dir.mkdir(parents=True, exist_ok=True)

        print(f"Saving PNG files to: {target_dir}")

        # Collect and copy PNG files
        for directory in source_dirs:
        
            directory = Path(directory)
            print("Directory: ", directory)
            
            for png_file in directory.glob("*.png"):  # Search for PNG files
                print(f'Moving file {png_file} to {target_dir / png_file.name}')
                shutil.move(png_file, target_dir / png_file.name)  # Copy to target

        print("PNG collection and transfer complete!")
    except Exception as e:
        print('Exception occurred while collecting and transferging png files!')



import os
import glob

def remove_success_message(directory):
    directory = os.path.abspath(directory)  # Ensure absolute path
    python_files = glob.glob(os.path.join(directory, "*.py"))  # Find all .py files

    for file in python_files:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace print("Success_and_End_of_Script!") with an empty string
        modified_content = content.replace('print("Success_and_End_of_Script!")', "")

        # Only overwrite if changes were made
        if content != modified_content:
            with open(file, "w", encoding="utf-8") as f:
                f.write(modified_content)
            print(f"Updated: {file}")
        else:
            print(f"No change: {file}")

# Example usage
remove_success_message("/path/to/your/directory")  # Replace with your directory path

import os
import shutil

import os
import shutil

def move_files_by_extension(source_dir, target_dir, extensions):
    """
    Move files with specific extensions from source_dir to target_dir.

    Args:
        source_dir (str): Path to the source directory.
        target_dir (str): Path to the target directory.
        extensions (list of str): List of file extensions to move (e.g., ['.txt', '.jpg']).
    """
    # Normalize extensions to lowercase and ensure they start with a dot
    extensions = [ext.lower() if ext.startswith('.') else f".{ext.lower()}" for ext in extensions]

    if not os.path.isdir(source_dir):
        raise ValueError(f"Source directory '{source_dir}' does not exist.")

    os.makedirs(target_dir, exist_ok=True)

    for filename in os.listdir(source_dir):
        src_file_path = os.path.join(source_dir, filename)

        if os.path.isfile(src_file_path):
            _, ext = os.path.splitext(filename)
            if ext.lower() in extensions:
                dst_file_path = os.path.join(target_dir, filename)
                shutil.move(src_file_path, dst_file_path)
                print(f"Moved: {src_file_path} -> {dst_file_path}")

def remove_heading_space_first_line(code_text):
    """
    Removes leading spaces or tabs from the first line of a Python code string.
    
    Parameters:
        code_text (str): Multiline string of Python code.
    
    Returns:
        str: Modified code with first line trimmed on the left.
    """
    lines = code_text.splitlines()
    if not lines:
        return code_text  # Return as is if empty

    lines[0] = lines[0].lstrip()  # Remove leading spaces/tabs from first line
    return "\n".join(lines)


def extract_key_lines_from_chained_exceptions(error_message):
    try:
        # Marker for chained exception
        marker = "During handling of the above exception, another exception occurred:"
        
        # Split into parts based on that marker
        parts = error_message.strip().split(marker)
        
        errors = ''
        last_line_of_error = ''
        
        for part in parts:
            lines = part.strip().splitlines()
            lines = [line.strip() for line in lines if line.strip()]  # remove empty lines

            third_line = lines[2] if len(lines) >= 3 else None
            last_line = lines[-1] if lines else None

            # results.append({
            #     "third_line": third_line,
            #     "last_line": last_line
            # })
            errors+=f'Details: {last_line}\n'
            errors+=f'Cause: {third_line}'
            last_line_of_error = last_line

        return errors, last_line_of_error
    except Exception as e:
        print(f'Exception ocurred while parsing error message, message: {e}')
        errors+=f'Details: Python Script Execution Failed\n'
        errors+=f'Cause: No meaningful exception mesage is found!'
        return errors, 'None'


import time
import csv
import os

def track_and_log_runtimes(output_csv, llm_model_name, runtime_corrector, runtime_rag, runtime_llm):
    # Track runtimes
    # start_corrector = time.time()
    # corrector()
    # end_corrector = time.time()

    # start_rag = time.time()
    # rag()
    # end_rag = time.time()

    # start_llm = time.time()
    # llm_model()
    # end_llm = time.time()

    # # Calculate durations in seconds
    # runtime_corrector = round(end_corrector - start_corrector, 4)
    # runtime_rag = round(end_rag - start_rag, 4)
    # runtime_llm = round(end_llm - start_llm, 4)

    # # Example model name (can be changed)
    # llm_model_name = "gpt-4o"

    # Check if the file exists
    file_exists = os.path.isfile(output_csv)

    # Write or append the row
    with open(output_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['llm_model_name', 'corrector', 'rag', 'llm_model'])
        writer.writerow([llm_model_name, runtime_corrector, runtime_rag, runtime_llm])

    print(f"Runtime recorded in '{output_csv}'.")

# Example usage:
# track_and_log_runtimes("results_log.csv")

import os

def rename_iteration_files(directory, iteration):
    """
    Renames all files in the given directory ending with _<iteration>.py
    to _<iteration+1>.py.
    
    Parameters:
        directory (str): Path to the directory containing the files.
        iteration (int): The current iteration number to be replaced.
    """
    current_suffix = f"_{iteration}.py"
    next_suffix = f"_{iteration + 1}.py"

    for filename in os.listdir(directory):
        if filename.endswith(current_suffix):
            old_path = os.path.join(directory, filename)
            new_filename = filename.replace(current_suffix, next_suffix)
            new_path = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_filename}")

# Example usage:
# rename_iteration_files("/path/to/your/scripts", 5)

import os

def extract_python_scripts_from_log(log_file_path, output_dir):
    """
    Extracts Python code blocks from a structured log file and saves them
    as separate .py files in the specified output directory.
    
    Parameters:
        log_file_path (str): Path to the log file.
        output_dir (str): Directory where extracted Python scripts will be saved.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()

    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()

        # Detect start of a new code block
        if line.startswith("input_file: "):
            # Extract file base name (e.g., file_name.txt)
            input_filename = line.split("input_file: ")[1].strip()
            base_name = os.path.splitext(input_filename)[0]
            if base_name.endswith('_4') or base_name.endswith('_2'):
                base_name = base_name[0:len(base_name)-2]
            
            script_filename = f"{base_name}_0.py"
            print(f'script_filename: {script_filename}')
            script_path = os.path.join(output_dir, script_filename)

            # Look for "First Generated code:"
            while idx < len(lines) and not lines[idx].strip().startswith("First Generated code:"):
                idx += 1

            idx += 1  # Move to the first line of the Python code
            code_lines = []

            # Collect code lines until "Generated python code saved to:" is found
            while idx < len(lines):
                current_line = lines[idx]
                if current_line.strip().startswith("Generated python code saved to:"):
                    break
                code_lines.append(current_line)
                idx += 1

            # Save the collected code to a .py file
            with open(script_path, 'w') as py_file:
                code_lines[0]=code_lines[0].lstrip()
                py_file.writelines(code_lines)
            print(f"Saved: {script_path}")

        idx += 1

import os
import shutil

def copy_python_files(source_dir, target_dir):
    """
    Copies all .py files from the source directory to the target directory.

    Parameters:
        source_dir (str): The path to the source directory.
        target_dir (str): The path to the target directory.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(source_dir):
        if filename.endswith(".py"):
            src_file = os.path.join(source_dir, filename)
            dst_file = os.path.join(target_dir, filename)
            shutil.copy(src_file, dst_file)
            print(f"Copied: {filename} → {target_dir}")

import os

def remove_python_files_with_suffix(directory, suffix="_0.py"):
    """
    Deletes all Python files in the given directory that end with the specified suffix.

    Parameters:
        directory (str): Path to the directory to search.
        suffix (str): File name suffix to match (default: "_0.py").
    """
    for filename in os.listdir(directory):
        if filename.endswith(suffix):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")



import os

def extract_python_scripts_from_log_for_climate(log_file_path, output_dir):
    """
    Extracts Python code blocks from a structured log file and saves them
    as separate .py files in the specified output directory.

    Parameters:
        log_file_path (str): Path to the log file.
        output_dir (str): Directory where extracted Python scripts will be saved.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()

    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()

        # Detect start of a new code block
        if line.startswith("Processing file:"):
            
            input_filename = line.split("Processing file:")[1].strip()
            print(f'input_filename: {input_filename}')
            # base_name = os.path.splitext(input_filename)[0]
            base_name = os.path.basename(input_filename)
            print(f'base name: {base_name}')

            script_filename = f"{base_name}_0.py"
            print(f'script_filename: {script_filename}')
            script_path = os.path.join(output_dir, script_filename)

            # Look for "First Generated code:"
            while idx < len(lines) and not lines[idx].strip().startswith("First Generated code:"):
                idx += 1

            idx += 1  # Move to the first line of the Python code
            code_lines = []

            # Collect code lines until "Generated python code saved to:" is found
            while idx < len(lines):
                current_line = lines[idx]
                if current_line.strip().startswith("Generated python code saved to:"):
                    break
                code_lines.append(current_line)
                idx += 1

            # Save the collected code to a .py file
            if code_lines:
                code_lines[0] = code_lines[0].lstrip()  # Clean leading space on first line
                with open(script_path, 'w') as py_file:
                    py_file.writelines(code_lines)
                print(f"Saved: {script_path}")

        idx += 1

def find_the_missed_base_image():
    import os
    import difflib

    def get_filenames(directory):
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    def similarity(a, b):
        return difflib.SequenceMatcher(None, a, b).ratio()

    def match_files(dir1, dir2, threshold=0.5):
        files1 = get_filenames(dir1)
        files1 = sorted(files1)
        files2 = get_filenames(dir2)

        results = []

        for f1 in files1:
            best_match = None
            best_score = 0.0

            for f2 in files2:
                score = similarity(f1, f2)
                if score > best_score:
                    best_score = score
                    best_match = f2

            if best_score >= threshold:
                results.append((f1, best_match, f"{best_score:.2f}", "FOUND"))
            else:
                results.append((f1, None, f"{best_score:.2f}", "ABSENT"))

        return results

    # Example usage:
    # dir1 = "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/user_queries/generated_user_queries/deepseek_r1_70b_generated_expert_queries_from_human_expert_queries_final_manually_corrected"
    # dir2 = "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/evaluation_by_clip_algorithm/climate_base_images"

    dir2 = "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/user_queries/generated_user_queries/deepseek_r1_70b_generated_expert_queries_from_human_expert_queries_final_manually_corrected"
    dir1 = "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/evaluation_by_clip_algorithm/climate_base_images"

    results = match_files(dir1, dir2)

    for f1, match, score, status in results:
        print(f"{f1:<30} --> {match or '---':<30} | Score: {score} | {status}")



if __name__ == '__main__':
    
    find_the_missed_base_image()
    
    
    # #increasing the script name
    # exisiting_climate_python_script_dir_list_base_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/python-script-output'
    # exisiting_climate_python_script_dir_list = [
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_corrector",
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_with_corrector",
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_without_corrector",
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_without_corrector",
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_corrector",
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_with_corrector",
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_without_corrector",
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_without_corrector"
    # ]
    
    # for python_script_dir in exisiting_climate_python_script_dir_list:
    #     for index in range(5, -1, -1):
    #         print(f'Current_index: {index}')
    #         rename_iteration_files(exisiting_climate_python_script_dir_list_base_dir+'/'+python_script_dir, index)


    # fastmribrain iterative log files
    # climate_source_common_directory = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/iterative_python_code_generation_logs'
    # climate_python_script_dir_list = [
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_corrector.log",
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_with_corrector.log",
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_without_corrector.log",
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_without_corrector.log",
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_corrector.log",
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_with_corrector.log",
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_without_corrector.log",
    #     "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_without_corrector.log"
    # ]
    # climate_target_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/python-script-output'

    # for log_file_path in climate_python_script_dir_list:
    #     output_dir = log_file_path.replace('.log', '')
    #     # output_dir = output_dir.replace('__', '_')
    #     # remove_python_files_with_suffix(climate_source_common_directory+'/'+output_dir)
    #     # extract_python_scripts_from_log_for_climate(climate_source_common_directory+'/'+log_file_path, climate_source_common_directory+'/'+output_dir)

    #     # remove_python_files_with_suffix(climate_target_dir+'/'+output_dir)
    #     copy_python_files(climate_source_common_directory+'/'+output_dir, climate_target_dir+'/'+output_dir)



    # matplotagent_iterative_python_scripts_directory = [
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/llm_rag_generated_python_scripts/devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_corrector",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/llm_rag_generated_python_scripts/devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_with_corrector",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/llm_rag_generated_python_scripts/devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_without_corrector",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/llm_rag_generated_python_scripts/devstral_24b_matplotagent_iterative_python_scripts_with_rag_without_corrector",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/llm_rag_generated_python_scripts/devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_corrector",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/llm_rag_generated_python_scripts/devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_errors_with_corrector",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/llm_rag_generated_python_scripts/devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_errors_without_corrector",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/llm_rag_generated_python_scripts/devstral_24b_matplotagent_iterative_python_scripts_without_rag_without_corrector"
    # ]
    # fastmribrain_iterative_python_scripts_directory = [
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/llm_rag_generated_python_scripts/devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_corrector",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/llm_rag_generated_python_scripts/devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_errors_with_corrector",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/llm_rag_generated_python_scripts/devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_errors_without_corrector",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/llm_rag_generated_python_scripts/devstral_24b_fastmribrain_iterative_python_scripts_with_rag_without_corrector",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/llm_rag_generated_python_scripts/devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_corrector",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/llm_rag_generated_python_scripts/devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_errors_with_corrector",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/llm_rag_generated_python_scripts/devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_errors_without_corrector",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/llm_rag_generated_python_scripts/devstral_24b_fastmribrain_iterative_python_scripts_without_rag_without_corrector"
    # ]
    # for python_script_dir in fastmribrain_iterative_python_scripts_directory:
    #     for index in range(5, -1, -1):
    #         print(f'Current_index: {index}')
    #         rename_iteration_files(python_script_dir, index)
    
    
    # this block is for extracting first generated python script from the log files, remove previous one and save
    # # matplotagent iterative log files
    # matplotagent_source_common_directory = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/iterative_python_scripts_generation_logs'
    # matplotagent_python_script_dir_list = [
    # "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_corrector.log",
    # "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_with_corrector.log",
    # "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_without_corrector.log",
    # "devstral_24b_matplotagent_iterative_python_scripts_with_rag_without_corrector.log",
    # "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_corrector.log",
    # "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_errors_with_corrector.log",
    # "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_errors_without_corrector.log",
    # "devstral_24b_matplotagent_iterative_python_scripts_without_rag_without_corrector.log"
    # ]
    # # log_file_path = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/vtk_python_scripts_experiment/logs/devstral_24b_vtk_iterative_python_scripts_generation_from_vtk_related_user_queries_simple_queries.log'
    # # output_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/vtk_python_scripts_experiment/llm_rag_generated_python_scripts/devstral_24b_vtk_iterative_python_scripts_without_rag_with_errors_without_corrector_ite_0'
    # matplotagent_target_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/llm_rag_generated_python_scripts'
    # for log_file_path in matplotagent_python_script_dir_list:
    #     output_dir = log_file_path.replace('.log', '')
    #     remove_python_files_with_suffix(matplotagent_source_common_directory+'/'+output_dir)
    #     extract_python_scripts_from_log(matplotagent_source_common_directory+'/'+log_file_path, matplotagent_source_common_directory+'/'+output_dir)
        
    #     remove_python_files_with_suffix(matplotagent_target_dir+'/'+output_dir)
    #     copy_python_files(matplotagent_source_common_directory+'/'+output_dir, matplotagent_target_dir+'/'+output_dir)
        
    
    

    # # fastmribrain iterative log files
    # fastmribrain_source_common_directory = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/iterative_python_scripts_generation_logs'
    # fastmribrain_python_script_dir_list = [
    #     "devstral_24b_fastmribrain_iterative_python_scripts_with_rag__with_corrector.log",
    #     "devstral_24b_fastmribrain_iterative_python_scripts_with_rag__with_errors_with_corrector.log",
    #     "devstral_24b_fastmribrain_iterative_python_scripts_with_rag__with_errors_without_corrector.log",
    #     "devstral_24b_fastmribrain_iterative_python_scripts_with_rag__without_corrector.log",
    #     "devstral_24b_fastmribrain_iterative_python_scripts_without_rag__with_corrector.log",
    #     "devstral_24b_fastmribrain_iterative_python_scripts_without_rag__with_errors_with_corrector.log",
    #     "devstral_24b_fastmribrain_iterative_python_scripts_without_rag__with_errors_without_corrector.log",
    #     "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_without_corrector.log"
    # ]
    # # log_file_path = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/vtk_python_scripts_experiment/logs/devstral_24b_vtk_iterative_python_scripts_generation_from_vtk_related_user_queries_simple_queries.log'
    # # output_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/vtk_python_scripts_experiment/llm_rag_generated_python_scripts/devstral_24b_vtk_iterative_python_scripts_without_rag_with_errors_without_corrector_ite_0'
    # fastmribrain_target_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/llm_rag_generated_python_scripts'

    # for log_file_path in fastmribrain_python_script_dir_list:
    #     output_dir = log_file_path.replace('.log', '')
    #     output_dir = output_dir.replace('__', '_')
    #     remove_python_files_with_suffix(fastmribrain_source_common_directory+'/'+output_dir)
    #     extract_python_scripts_from_log(fastmribrain_source_common_directory+'/'+log_file_path, fastmribrain_source_common_directory+'/'+output_dir)

    #     remove_python_files_with_suffix(fastmribrain_target_dir+'/'+output_dir)
    #     copy_python_files(fastmribrain_source_common_directory+'/'+output_dir, fastmribrain_target_dir+'/'+output_dir)


    # reading los files, searching verision 0 python code and dave
    # renaming files from iteration to iteration+1
    # python_script_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/vtk_python_scripts_experiment/llm_rag_generated_python_scripts/devstral_24b_vtk_iterative_python_scripts_without_rag_with_errors_without_corrector'
    # python_script_dir = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/vtk_python_scripts_experiment/llm_rag_generated_python_scripts/devstral_24b_vtk_iterative_python_scripts_without_rag_without_corrector'
    # for index in range(5, 0, -1):
    #     print(f'Current_index: {index}')
    #     rename_iteration_files(python_script_dir, index)
    # rename_iteration_files(python_script_dir, 0)
    # end
    # for the fastmribrain
    

   
    
    # directory_list =[
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/python-script-output/deepseek_r1_70b_without_corrector_expert_level_queries_human_error_insertions_remove_image_from_query",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/python-script-output/llama3_70b_without_corrector_expert_level_queries_human_error_insertions_remove_image_from_query",
    #     "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/python-script-output/magicoder_without_corrector_expert_level_queries_human_error_insertions_remove_image_from_query"
    # ]

    # for directory in directory_list:
    #     remove_success_message(directory)
    # # output_subdir = 'llama3_70b_with_corrector_with_memory_expert_level_queries_human_error_insertions_remove_image_from_query'
    # output_subdir = 'Mixed'
    # data_dir = 'ACL_DIRS'  # Replace with your common directory path        
    #     # Replace with your predefined subdirectory names
    # subdirectories = [' ', 'NSIDC', ' ', 'PO_DAAC', ' ', 'ASF', 'GES_DISC', 'GHRC', 'ICESat_2', 'LAADS', 'LaRC', 'LP_DAAC',  'Ocen_Biology', 'AURA_DATA_VC', '../prompting_techniques/zero_shot_sci_data_prompting/']
    #  # collect all images and store them into a new directory
    # # Example usage
    # source_dirs = subdirectories  # List of source directories
    # base_path = "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data"  # Base path for new directory
    # new_dir_name=output_subdir
    # # data_dir = 'ACL_DIRS'
    # collect_and_store_png(source_dirs, base_path, new_dir_name, data_dir)