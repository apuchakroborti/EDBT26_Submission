import csv
import os

# File path for the CSV file
# common_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'
# FILE_PATH = 'sci_data_prompting/tracking_file/code_generation_status.csv'
# JSON_FILE_PATH = 'sci_data_prompting/tracking_file'

import json

# Initial dictionary

def initialize_json(common_base_directory, JSON_FILE_PATH, directory_file_name):
    print(f'Inside initialize_json...')
    print(f'common_base_directory: {common_base_directory}')
    print(f'JSON_FILE_PATH: {JSON_FILE_PATH}')
    print(f'directory_file_name: {directory_file_name}')
    try:
        data = {    }
        # os.makedirs(os.path.dirname(f'{common_directory}/{JSON_FILE_PATH}/{directory_file_name}.json'), exist_ok=True)
        
        # Save dictionary to a JSON file
        if not os.path.exists(f'{common_base_directory}/{JSON_FILE_PATH}/{directory_file_name}.json'):
            with open(f'{common_base_directory}/{JSON_FILE_PATH}/{directory_file_name}.json', 'w') as file:
                json.dump(data, file)
    except Exception as e:
        print('Exception occurred in insert_or_update_key, error message: ', e)


# Function to insert or update a key-value pair in the dictionary file
def insert_or_update_key(common_base_directory, JSON_FILE_PATH, directory_file_name, key, value):
    print(f'\nInside Insert_or_update_key...')
    print(f'common_base_directory: {common_base_directory}')
    print(f'JSON_FILE_PATH: {JSON_FILE_PATH}')
    print(f'directory_file_name: {directory_file_name}')
    print(f'directory_file_name: {key}')
    print(f'directory_file_name: {value}')

    try:

        # Load the existing dictionary from the file
        with open(f'{common_base_directory}/{JSON_FILE_PATH}/{directory_file_name}.json', 'r') as file:
            data = json.load(file)

        # Insert new key or update existing key
        data[key] = value

        # Save the updated dictionary back to the file
        with open(f'{common_base_directory}/{JSON_FILE_PATH}/{directory_file_name}.json', 'w') as file:
            json.dump(data, file)
        print(f"Updated dictionary: {data}")

    except Exception as e:
        print('Exception occurred in insert_or_update_key, error message: ', e)

# Example usage
# insert_or_update_key('data.json', 'key3', 'new_value')  # Adds or updates key3 with value 'new_value'


# Function to read value based on a key
def check_tracking_status_is_done(common_base_directory, JSON_FILE_PATH, directory_file_name, key):
    print(f'\nInside check_tracking_status_is_done...')
    print(f'common_base_directory: {common_base_directory}')
    print(f'JSON_FILE_PATH: {JSON_FILE_PATH}')
    print(f'directory_file_name: {directory_file_name}')
    print(f'directory_file_name: {key}')
    
    try:
        tracking_map = {}
        # Load the dictionary from the file
        with open(f'{common_base_directory}/{JSON_FILE_PATH}/{directory_file_name}.json', 'r') as file:
            data = json.load(file)
            tracking_map = data

        # Return the value for the specified key if it exists
        # return data.get(key, f"Key '{key}' not found in the dictionary.")
        return tracking_map.get(key) == "done"
    except Exception as e:
        print('Exception occurred in check_tracking_status_is_done, error message: ', e)


# Example usage
# value = read_value('data.json', 'key1')  # Replace 'key1' with the desired key
# print(f"The value for 'key1' is: {value}")


def initialize_csv(common_base_directory, FILE_PATH):
    # Check if the file already exists; if not, create it with headers
    if not os.path.exists(FILE_PATH):
        with open(common_base_directory+'/'+FILE_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["String", "Status"])

def check_string_status(common_base_directory, FILE_PATH, string):
    # Check if the given string has a status of "done" in the CSV file
    with open(common_base_directory+'/'+FILE_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["String"] == string and row["Status"] == "done":
                return True  # Found a "done" status for the string
    return False  # No "done" status found for the string

def insert_string_started(common_base_directory, FILE_PATH, string):
    # Insert the string with "started" status if "done" status is not present
    if not check_string_status(string):
        with open(common_base_directory+'/'+FILE_PATH, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([string, "started"])
        print(f'Inserted "{string}" with status "started".')
    else:
        print(f'Skipping insertion: "{string}" already has a status of "done".')

def insert_string_done(common_base_directory, FILE_PATH, string):
    # Insert the string with "started" status if "done" status is not present
    if not check_string_status(string):
        with open(common_base_directory+'/'+FILE_PATH, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([string, "done"])
        print(f'Inserted "{string}" with status "done".')
    else:
        print(f'Skipping insertion: "{string}" already has a status of "done".')

# Initialize CSV file with headers (if not present)
# initialize_csv()

# Example usage
# insert_string("example_string_1")
# insert_string("example_string_2")
# insert_string("example_string_1")  # This will be skipped if "done" status is already present
