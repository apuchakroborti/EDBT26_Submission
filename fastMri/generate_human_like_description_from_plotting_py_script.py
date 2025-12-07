import requests
import json
import os
import glob
import random

URL = 'http://ai-lab2.dyn.gsu.edu:11434/api/generate'
# URL = 'http://localhost:11434/api/generate'


# def generate_request_for_describing_source_code(sample, seed, model="llama3:70b"):
def generate_request_for_describing_source_code(sample, seed, model):
    s = "Explain the following python code step-by-step: \n" + sample 
    s+="\n Include as many implementation details as possible but don't add any python code examples directly." 
    s+="\n Keep names of all parent groups of each dataset so that each dataset can be identified within the HDF5 hierarchy."
    data = {
        "model": model,
        "prompt": s,
        "stream": False,
        "options": {
            "seed": seed,
            "temperature": 0.5
        }
    }
    return data

# def generate_request_for_condensing_description_20_percent(sample, seed, model="llama3:70b"):
def generate_request_for_condensing_description_20_percent(sample, seed, model):
    s = "Reduce 40% of the text in the following description while keeping as many implementation details as possible: \n" + sample
    s+= "\n Keep names of all parent groups of each dataset so that each dataset can be identified within the HDF5 hierarchy."
    s+="\nMake this description like prompt from real human user"
    data = {
        "model": model,
        "prompt": s,
        "stream": False,
        "options": {
            "seed": seed,
            "temperature": 0.5
        }
    }
    return data



# direct code to description generator model
def generate_request_for_describing_source_code_directly(sample, seed, model):
    s = "Explain the following python code step-by-step: \n" + sample 
    s+="\n Do not add any library name to import"
    s+="\n Include as many implementation details as possible such as what the programs perspective but don't add any python code examples directly." 
    s+="\n Keep names of all parent groups of each dataset so that each dataset can be identified within the HDF5 or H5 or HE5 hierarchy."
    data = {
        "model": model,
        "prompt": s,
        "stream": False,
        "options": {
            "seed": seed,
            "temperature": 0.5
        }
    }
    return data


# def generate_request_for_condensing_description_20_percent(sample, seed, model="llama3:70b"):
def generate_request_for_condensing_description_mentioned_percent(sample, seed, model):
    # s = "Reduce 40 percent of the text in the following description while keeping as many implementation details as possible: \n" + sample
    
    s = "Reduce 10 percent of the text in the following description while keeping as many implementation details as possible: \n" + sample
    s+= "\n don't keep any python libray in the text"
    s+= "\n Keep names of all parent groups of each dataset so that each dataset can be identified within the HDF5 or H5 or HE5 hierarchy."
    s+="\nMake this description like prompt from real human user"
    data = {
        "model": model,
        "prompt": s,
        "stream": False,
        "options": {
            "seed": seed,
            "temperature": 0.5
        }
    }
    return data

def save_description_with_out_dir(file_path, description, output_dir):
    """
    This function saves the description to a text file with the same base name as the input file in the specified directory.
    
    Args:
        file_path (str): The path to the input HDF5 file.
        description (str): The description to save.
        output_dir (str): The directory to save the text file in.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create the directory if it does not exist

    base_name = os.path.splitext(os.path.basename(file_path))[0]  # Remove the file extension
    txt_file_path = os.path.join(output_dir, f"{base_name}.txt")  # Create the full path for the .txt file
    
    try:
        with open(txt_file_path, 'w') as f:
            f.write(description)
        print(f"Description saved to {txt_file_path}")
    except Exception as e:
        print(f"Error saving description: {e}")

# this is the current established description generator, at first code to descriptions then reduce the description 40%
def find_and_process_files_with_output_dir(common_directory, subdirectories, extensions, output_dir, script_sub_dir, model):
    """
    This function searches for files with specified extensions in a common directory and predefined subdirectories,
    summarizes and saves descriptions for each file.
    
    Args:
        common_directory (str): The common directory to search in.
        subdirectories (list): A list of subdirectories to search within the common directory.
        extensions (list): A list of file extensions to look for.
    """
    for subdir in subdirectories:
        search_path = os.path.join(common_directory, subdir+"/"+script_sub_dir, '*')
        for ext in extensions:
            files = glob.glob(f"{search_path}.{ext}")
            for file_path in files:
                print(f"Processing file: {file_path}")
                # summary = summarize_hdf5(file_path)
                # description = describe_summary(summary)
                # save_description(file_path, description)
                with open(file_path, "r") as f:
                    original_source_code = f.read()
                    print('\noriginal_source_code: \n', original_source_code)
                    
                    seed = random.randint(1, 20000)
                    code_description_gen = generate_request_for_describing_source_code(original_source_code, seed, model)
                    code_description_gen = json.dumps(code_description_gen).encode("utf-8")
                    code_description = requests.post(URL, data=code_description_gen)
                    code_description  = code_description.json()
                    print('code_description: \n', code_description)
        
                    seed = random.randint(1, 20000)
                    condensed_code_description_gen = generate_request_for_condensing_description_20_percent(code_description['response'], seed, model)
                    # condensed_code_description_gen = generate_request_for_condensing_description_60_percent(code_description['response'], seed, model)
                    condensed_code_description_gen = json.dumps(condensed_code_description_gen).encode("utf-8")
                    condensed_code_description = requests.post(URL, data=condensed_code_description_gen)
                    condensed_code_description  = condensed_code_description.json()

                    save_description_with_out_dir(file_path, condensed_code_description['response'], output_dir)
    


# current testing functions created for testing direct code to description generations by keeping only the dataset information, the tasks need to be done
def find_and_process_files_with_output_dir_direct_code_to_important_query_info(common_directory, subdirectories, extensions, output_dir, script_sub_dir, model):
    print('common_directory: ', common_directory)
    print('subdirectories: ', subdirectories)
    print('output_dir: ', output_dir)
    print('script_sub_dir: ', script_sub_dir)

    """
    This function searches for files with specified extensions in a common directory and predefined subdirectories,
    summarizes and saves descriptions for each file.
    
    Args:
        common_directory (str): The common directory to search in.
        subdirectories (list): A list of subdirectories to search within the common directory.
        extensions (list): A list of file extensions to look for.
    """
    for subdir in subdirectories:
        search_path = os.path.join(common_directory, subdir+"/", '*')
        print('search_path: ',search_path)

        for ext in extensions:
            files = glob.glob(f"{search_path}.{ext}")
            for file_path in files:
                print(f"Processing file: {file_path}")
                # summary = summarize_hdf5(file_path)
                # description = describe_summary(summary)
                # save_description(file_path, description)
                with open(file_path, "r") as f:
                    original_source_code = f.read()
                    print('\noriginal_source_code: \n', original_source_code)
                    
                    seed = random.randint(1, 20000)
                    code_description_gen = generate_request_for_describing_source_code_directly(original_source_code, seed, model)
                    code_description_gen = json.dumps(code_description_gen).encode("utf-8")
                    code_description = requests.post(URL, data=code_description_gen)
                    code_description  = code_description.json()
                    print('code_description: \n', code_description)
        
                    # save_description_with_out_dir(file_path, code_description['response'], output_dir)

                    
                    seed = random.randint(1, 20000)
                    condensed_code_description_gen = generate_request_for_condensing_description_mentioned_percent(code_description['response'], seed, model)
                    condensed_code_description_gen = json.dumps(condensed_code_description_gen).encode("utf-8")
                    condensed_code_description = requests.post(URL, data=condensed_code_description_gen)
                    condensed_code_description  = condensed_code_description.json()
                    

                    save_description_with_out_dir(file_path, condensed_code_description['response'], output_dir)


if __name__ == '__main__':
    # Replace with your common directory path
    common_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'  
    # subdirectories = ['ASF', 'GES_DISC', 'GHRC', 'ICESat_2', 'LAADS', 'LaRC', 'LP_DAAC', 'NSIDC', 'Ocen_Biology', 'PO_DAAC']  # Replace with your predefined subdirectory names
    # subdirectories = ['LP_DAAC', 'NSIDC']  # Replace with your predefined subdirectory names
    # data_dir = 'ACL_DIRS'
    # subdirectories = ['ASF', 'GES_DISC', 'GHRC', 'ICESat_2', 'LAADS', 'LaRC', 'LP_DAAC', 'NSIDC', 'Ocen_Biology', 'PO_DAAC', 'AURA_DATA_VC']  # Replace with your predefined subdirectory names
    # subdirectories = ['ASF', 'GES_DISC', 'GHRC', 'ICESat_2', 'LAADS', 'LaRC', 'LP_DAAC', 'NSIDC', 'Ocen_Biology', 'PO_DAAC', 'AURA_DATA_VC']  # Replace with your predefined subdirectory names
    # subdirectories = ['plot_generation/examples_plot_generation_from_scientific_data']
    subdirectories = ['mri_nyu_data/splitted_graphs']
    script_sub_dir = 'python_script'

    extensions = ['py']
    # output_subdir = '/zero_shot_output/summaries'  # The name of the directory to save output files
    # output_description_subdir = 'generated_user_input_human_like_text'  # The name of the directory to save output files
    # output_description_subdir = 'plot_generation/examples_plot_generation_from_scientific_data_description'  # The name of the directory to save output files
    output_description_subdir = common_directory+'/mri_nyu_data/llm_generated_user_queries'
    
    model_list = ['llama3:70b','llama3:latest', 'deepseek-coder-v2', 'deepseek-coder-v2:latest']
    
    # llama3:70b
    model = model_list[0]
    
    # find_and_process_files_with_output_dir(common_directory+"/"+data_dir, subdirectories, extensions, common_directory+"/"+output_description_subdir, script_sub_dir, model[0])

    find_and_process_files_with_output_dir_direct_code_to_important_query_info(common_directory, subdirectories, extensions, common_directory+"/"+output_description_subdir, script_sub_dir, model)
