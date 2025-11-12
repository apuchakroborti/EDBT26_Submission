import os
import glob
import re



import requests
import json
import os
# import glob

def get_base_filename(filename):
    """
    Extract the base part of the filename before any special extension such as '_h5', 'HDF5', 'he5', or 'h5'.
    """
    base_name = os.path.splitext(filename)[0]
    # base_name = re.sub(r'(_h5|.HDF5|.he5|.h5|.H5|.hdf5)$', '', base_name, flags=re.IGNORECASE)
    return base_name

# def generate_request_for_generating_source_code(sample, model="llama3:70b"):
# latest means 8b
def generate_request_for_generating_source_code(sample, model="llama3:latest"):
    s = "Generate the python code based on the following description: \n" + sample 
    # + "\n Make sure the input file can be specified as a command line parameter by importing and utilizing the sys module."
    data = {
        "model": model,
        "prompt": s,
        "stream": False,
        "options": {
            "seed": 12344,
            "temperature": 0.0
        }
    }
    return data

def match_and_merge_files(dir1, dir2, output_dir):
    """
    Match and merge text files from two directories and save them in an output directory.
    
    Args:
        dir1 (str): The path to the first directory with the base file names.
        dir2 (str): The path to the second directory with similar names but with extra strings.
        output_dir (str): The path to the output directory to save merged files.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get list of text files from both directories
    files_dir1 = glob.glob(os.path.join(dir1, '*.txt'))
    # print('files_dir1 ',files_dir1)
    
    files_dir2 = glob.glob(os.path.join(dir2, '*.txt'))
    # print('files_dir2 ',files_dir2)


    # Create a dictionary to store base filenames from dir2 for easy lookup
    dir2_dict = {get_base_filename(os.path.basename(f)): f for f in files_dir2}
    # print('dir2_dict', dir2_dict)

    for file1 in files_dir1:
        # print(file1)
        base_name1 = get_base_filename(os.path.basename(file1))
        # print('base_name1', base_name1)

        # Check if there is a matching file in dir2
        modified_base_name=base_name1.replace('_', '.')
       
        for key_file2 in dir2_dict:
            modified_key_file2 = key_file2.replace('_', '.')
            if modified_base_name==modified_key_file2:
                print()
                print(modified_key_file2)
                print(modified_base_name)
                # if base_name1 in dir2_dict:
                # file2 = dir2_dict[base_name1]
                file2 = dir2_dict[key_file2]
                # print(f"Merging: {os.path.basename(file1)} and {os.path.basename(file2)}")
                
                # Merge the content of the two files
                with open(file1, 'r') as f1, open(file2, 'r') as f2:
                    content1 = f1.read()
                    # content1 = content1.split("- First 5 elements:")[0]
                    # content1 = content1.replace("Summary of HDF5 file:", "")


                    content2 = f2.read()
                    
                    
                    merged_content = content2 + "\n\nThis is the summaries of the file should be read when generate for code this: \n" + content1  # Adjust how you want to merge
                    # print('mconten', merged_content)
                # Save the merged content to the output directory with the name from dir1
                output_file_path = os.path.join(output_dir, os.path.basename(file1))
                with open(output_file_path, 'w') as f_out:
                    f_out.write(merged_content)
                    
                # print(f"Saved merged file as: {output_file_path}")
            else:
                if len(modified_base_name)==len(modified_key_file2):
                    print("\n")
                    print(modified_base_name)
                    print(modified_key_file2)
                    print(f"No match found for: {os.path.basename(file1)}")

def generate_group_and_dataset_paths_and_save(source_dir, target_dir, old_ext='.txt'):
    """
    Reads all files with the specified old extension from the source directory, changes the file extension,
    and saves them into the target directory with the new extension.
    
    Args:
        source_dir (str): The directory containing the original files.
        target_dir (str): The directory to save the renamed files.
        old_ext (str): The old file extension (e.g., '.txt').
        new_ext (str): The new file extension (e.g., '.md').
    """
    # Create the target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Iterate over all files in the source directory
    for filename in os.listdir(source_dir):
        # Check if the file has the old extension
        if filename.endswith(old_ext):
            # Construct full file path
            source_file_path = os.path.join(source_dir, filename)
            
            # Change the extension
            base_name = os.path.splitext(filename)[0]  # Get the base file name without extension
            
            # generate code and save
            with open(source_file_path, 'r') as f:
                description = f.read()
            
            # source_code_gen = generate_request_for_generating_source_code(description, "llama3:70b")
            # latest means 8b
            source_code_gen = generate_request_for_generating_source_code(description, "llama3:latest")

            source_code_gen = json.dumps(source_code_gen).encode("utf-8")
            llm_gen_source_code = requests.post(URL, data=source_code_gen)
            #print(llm_gen_source_code)
            llm_gen_source_code  = llm_gen_source_code.json()
            print(llm_gen_source_code)
            print(llm_gen_source_code['response'])
            
            start_delim_1 = "```python\n"
            start_delim_2 = "```Python\n"
            start_delim_3 = "```\n"
            end_delim = "```"

            result_1 = extract_substring(llm_gen_source_code['response'], start_delim_1, end_delim)
            result_2 = extract_substring(llm_gen_source_code['response'], start_delim_2, end_delim)
            result_3 = extract_substring(llm_gen_source_code['response'], start_delim_3, end_delim)
            
            
            output_file_path = os.path.join(target_dir, f'{base_name}.py')
            # file_num+=1
            
            if result_1:
                #print(result)
                with open(output_file_path, 'w') as f:
                    f.write(result_1)
            elif result_2:
                with open(output_file_path, 'w') as f:
                    f.write(result_2)
            elif result_3:
                with open(output_file_path, 'w') as f:
                    f.write(result_3)
            else:
                print("source code not found")

# URL = 'http://localhost:11434/api/generate'

URL = 'http://ai-lab2.dyn.gsu.edu:11434/api/generate'

def extract_substring(text, start_delim, end_delim):
    start_idx = text.find(start_delim)
    if start_idx == -1:
        return None
    
    start_idx += len(start_delim)
    end_idx = text.find(end_delim, start_idx)
    if end_idx == -1:
        return None
    
    return text[start_idx:end_idx]

# def generate_request_for_generating_source_code(sample, model="llama3:70b"):
# latest means 8b
def generate_request_for_extracting_datasets_from_description(sample, model="llama3:latest"):
    s = "Find the group and dataset names on the following description: \n" + sample + "\n Make sure response should under <datasets><full path of datasets mentioned in the description></datasets>"
    data = {
        "model": model,
        "prompt": s,
        "stream": False,
        "options": {
            "seed": 12344,
            "temperature": 0.0
        }
    }
    return data






def generate_group_and_datasets_name_and_save(source_dir, target_dir, old_ext='.txt'):
    """
    Reads all files with the specified old extension from the source directory, changes the file extension,
    and saves them into the target directory with the new extension.
    
    Args:
        source_dir (str): The directory containing the original files.
        target_dir (str): The directory to save the renamed files.
        old_ext (str): The old file extension (e.g., '.txt').
        new_ext (str): The new file extension (e.g., '.md').
    """
    # Create the target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Iterate over all files in the source directory
    for filename in os.listdir(source_dir):
        # Check if the file has the old extension
        if filename.endswith(old_ext):
            # Construct full file path
            source_file_path = os.path.join(source_dir, filename)
            
            # Change the extension
            base_name = os.path.splitext(filename)[0]  # Get the base file name without extension
            
            # generate code and save
            with open(source_file_path, 'r') as f:
                description = f.read()
            
            # source_code_gen = generate_request_for_generating_source_code(description, "llama3:70b")
            # latest means 8b
            source_code_gen = generate_request_for_extracting_datasets_from_description(description, "llama3:latest")

            source_code_gen = json.dumps(source_code_gen).encode("utf-8")
            llm_gen_source_code = requests.post(URL, data=source_code_gen)
            #print(llm_gen_source_code)
            llm_gen_source_code  = llm_gen_source_code.json()
            print(llm_gen_source_code)
            print(llm_gen_source_code['response'])
            
            # start_delim_1 = "```python\n"
            # start_delim_2 = "```Python\n"
            # start_delim_3 = "```\n"
            # end_delim = "```"

            # result_1 = extract_substring(llm_gen_source_code['response'], start_delim_1, end_delim)
            # result_2 = extract_substring(llm_gen_source_code['response'], start_delim_2, end_delim)
            # result_3 = extract_substring(llm_gen_source_code['response'], start_delim_3, end_delim)
            
            
            # output_file_path = os.path.join(target_dir, f'{base_name}.py')
            output_file_path = os.path.join(target_dir, f'{base_name}.txt')
            with open(output_file_path, 'w') as f:
                    f.write(llm_gen_source_code['response'])
            
            
            """
            if result_1:
                #print(result)
                with open(output_file_path, 'w') as f:
                    f.write(result_1)
            elif result_2:
                with open(output_file_path, 'w') as f:
                    f.write(result_2)
            elif result_3:
                with open(output_file_path, 'w') as f:
                    f.write(result_3)
            else:
                print("source code not found")
            """



# extract group and datasets names from prompt description using LLM
# common_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'  # Replace with your common directory path

# dir1 = common_directory+'/original_python_script_description_with_20_p_reduc'  # Directory containing the base filenames
# dir2 = common_directory+'/original_python_script_description_with_20_p_reduc'  # Directory containing the similar filenames
# output_dir = common_directory+'/chain_of_repair_input'  # Directory to save merged files
# output_dir = common_directory+"/zero_shot_input_with_data_locally"
# match_and_merge_files(dir1, dir2, output_dir)
# generate_group_and_datasets_name_and_save(dir1, output_dir)



# Example usage
# common_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'  # Replace with your common directory path

# dir1 = common_directory+'/data_summaries'  # Directory containing the base filenames
# dir2 = common_directory+'/original_python_script_description_with_20_p_reduc'  # Directory containing the similar filenames
# output_dir = common_directory+'/zero_shot_input_llama70b_with_data_des'  # Directory to save merged files
# output_dir = common_directory+"/zero_shot_input_with_data_locally"
# match_and_merge_files(dir1, dir2, output_dir)

# chain of repair input preparation
# common_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'  # Replace with your common directory path
# dir1 = common_directory+'/example_group_dataset_fetching_from_description_using_llm'  # Directory containing the base filenames
# dir2 = common_directory+'/original_python_script_description_with_20_p_reduc'  # Directory containing the similar filenames
# output_dir = common_directory+'/chain_of_repair_input_llama3_latest'  # Directory to save merged files
# output_dir = common_directory+"/zero_shot_input_with_data_locally"
# match_and_merge_files(dir1, dir2, output_dir)




# source_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/zero_shot_input_with_data_locally'
# target_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/zero_shot_output_llama70b_with_data_des'
# target_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/zero_shot_output_llama8b_with_data_des_locally'




# Example usage
# For the zero shot with data description
# source_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/zero_shot_input_llama70b_with_data_des'
# source_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/zero_shot_input_with_data_locally'
# target_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/zero_shot_output_llama70b_with_data_des'
# target_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/zero_shot_output_llama8b_with_data_des_locally'


# For the zero shot but without data description
# source_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/original_python_script_description_with_20_p_reduc_locally'
# target_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/zero_shot_output_llama70b_without_data_des'

# source_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/original_python_script_description_with_20_p_reduc'
# target_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/zero_shot_output_llama8b_latest_without_data_des_locally'

# generate_code_and_save(source_directory, target_directory, old_ext='.txt')

# with data llama3:latest


def generate_code_and_save(source_dir, target_dir, old_ext='.txt'):
    """
    Reads all files with the specified old extension from the source directory, changes the file extension,
    and saves them into the target directory with the new extension.
    
    Args:
        source_dir (str): The directory containing the original files.
        target_dir (str): The directory to save the renamed files.
        old_ext (str): The old file extension (e.g., '.txt').
        new_ext (str): The new file extension (e.g., '.md').
    """
    # Create the target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Iterate over all files in the source directory
    for filename in os.listdir(source_dir):
        # Check if the file has the old extension
        if filename.endswith(old_ext):
            # Construct full file path
            source_file_path = os.path.join(source_dir, filename)
            
            # Change the extension
            base_name = os.path.splitext(filename)[0]  # Get the base file name without extension
            
            # generate code and save
            with open(source_file_path, 'r') as f:
                description = f.read()
            
            source_code_gen = generate_request_for_generating_source_code(description, "llama3:latest")
            source_code_gen = json.dumps(source_code_gen).encode("utf-8")
            llm_gen_source_code = requests.post(URL, data=source_code_gen)
            #print(llm_gen_source_code)
            llm_gen_source_code  = llm_gen_source_code.json()
            #print(llm_gen_source_code)
            print(llm_gen_source_code['response'])
            
            start_delim_1 = "```python\n"
            start_delim_2 = "```Python\n"
            start_delim_3 = "```\n"
            end_delim = "```"

            result_1 = extract_substring(llm_gen_source_code['response'], start_delim_1, end_delim)
            result_2 = extract_substring(llm_gen_source_code['response'], start_delim_2, end_delim)
            result_3 = extract_substring(llm_gen_source_code['response'], start_delim_3, end_delim)
            
            
            output_file_path = os.path.join(target_dir, f'{base_name}.py')
            # file_num+=1
            
            if result_1:
                #print(result)
                with open(output_file_path, 'w') as f:
                    f.write(result_1)
            elif result_2:
                with open(output_file_path, 'w') as f:
                    f.write(result_2)
            elif result_3:
                with open(output_file_path, 'w') as f:
                    f.write(result_3)
            else:
                print("source code not found")





source_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/chain_of_repair_input_llama3_latest'
target_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/output_chain_of_repair'

generate_code_and_save(source_directory, target_directory, old_ext='.txt')