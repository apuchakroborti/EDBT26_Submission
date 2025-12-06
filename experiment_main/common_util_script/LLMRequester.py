import os
import requests
import json
from . import Utils as utils

# URL = 'http://localhost:11434/api/generate'
# Previous Yi Dings server
# URL = 'http://ai-lab2.dyn.gsu.edu:11434/api/generate'

# New Yi Dings server
# URL = 'http://ai-lab2.dyn.gsu.edu:8080/api/generate'

# under development
# created on January 29, 2025
# def add_datapaths_saving_information_to_the_prompt
def add_datapaths_saving_information_to_the_prompt(all_data_paths):
    print('add_datapaths_saving_information_to_the_prompt...\n')
    prompt = "Create a memory reference such as PATHS and Clear the PATHS reference if there any existing reference named PATHS, Save the below paths, attributes, and its shape information into memory of PATHS reference: \n"+all_data_paths+"\n"

    return prompt

# under development
# currently being developed, Jan 29, 2025
# this is for storing all the datapaths into LLM model's memory and asking LLM to get from that
def generate_request_for_generating_source_code_using_LLM_memory_with_zero_shot_CoT_with_corrector(user_input, data_structure_information, full_data_path, attribute_present, model):    
    print('Inside generate_request_for_generating_source_code_separate_prompt_method_with_zero_shot_CoT_with_corrector_step_by_step\n\n')
    prompt = add_datapaths_saving_information_to_the_prompt(data_structure_information)
        
    prompt = prompt+generate_request_for_generating_source_code_with_zero_shot_CoT_best_success_with_memory(user_input, data_structure_information, full_data_path, attribute_present)
    
    print("Prompt: \n", prompt)
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "seed": 12344,
            "temperature": 0.0
        }
    }
    return data

# created on Feb 14, 2025
# this method is to regerate the python script based on the current python script and erros message
def generate_request_for_generating_source_code_using_LLM_memory_with_zero_shot_CoT_with_corrector_iterative_error_resolve(user_input, data_structure_information, full_data_path, attribute_present, model, generated_python_script, error_message):    
    print('Inside generate_request_for_generating_source_code_separate_prompt_method_with_zero_shot_CoT_with_corrector_step_by_step\n\n')
    
    prompt = generate_request_for_generating_source_code_with_zero_shot_CoT_iterative_error_resolving(user_input, data_structure_information, full_data_path, attribute_present, generated_python_script, error_message)
    
    print("Prompt: \n", prompt)
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        # "response_format": "code_only",#this works for openAI only
        "options": {
            "seed": 12344,
            "temperature": 0.0
        }
    }
    return data

# created on Feb 14
# this is for the iterative error resolving
def generate_request_for_generating_source_code_with_zero_shot_CoT_iterative_error_resolving(user_input, data_structure_information, full_data_path, attribute_present, python_script, error_message):
    print('Inside generate_request_for_generating_source_code_with_zero_shot_CoT_iterative_error_resolving\n')
    
    user_input_description = 'The generated below python code has some errors mentioned in the ERROR_MESSAGE=, please analyze the PYTHON_CODE= and ERROR_MESSAGE= and Rewrite the entire PYHTHON_CODE with this error fixed'
    user_input_description+=' and return the whole new python code as a response and make sure you only send the whole python code without adding any extra description\n'
    user_input_description+='PYTHON_CODE=\n'
    user_input_description+= python_script+'\n'
    user_input_description+='ERROR_MESSAGE=\n'+error_message

    prompt = f"\nWhile rewriting the PYTHON_CODE= based on the below information, keep the FULL_DATA_PATH={full_data_path} that is used to access the data file as it is:\n"
    prompt+=user_input_description
    if len(data_structure_information)>0: 
        prompt+= f"\nWhile rewriting the python code consider the information about the DATA_STRUCTURE=\n{data_structure_information}"
    prompt+="\nNote: the initial goal of PYTHON_CODE= is to save the plotting output as a png file by extracting basename from the value of FULL_DATA_PATH= and also the image should be saved to the same directory as FULL_DATA_PATH="
    prompt+="\nSend only the code, no explanations or additional text."
    
    return prompt


# created on June 29, 2025
# this method is to regerate the python script based on the current python script and erros message
def generate_request_for_generating_source_code_with_SO_corrector_iterative_error_resolve(data_structure_information, full_data_path, model, generated_python_script, error_message, query_augmentation):    
    print('Inside generate_request_for_generating_source_code_with_SO_corrector_iterative_error_resolve\n\n')
    
    prompt = generate_request_for_generating_source_code_with_error_msg_and_SO_iterative_error_resolving(data_structure_information=data_structure_information, 
                                                                                                         full_data_path=full_data_path, 
                                                                                                         python_script=generated_python_script, 
                                                                                                         error_message=error_message, 
                                                                                                         query_augmentation=query_augmentation)
    
    print("Prompt: \n", prompt)
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        # "response_format": "code_only",#this works for openAI only
        "options": {
            "seed": 12344,
            "temperature": 0.0
        }
    }
    return data

# created on Jul 06, 2025
# this method is to regerate the python script based on the current python script and erros message
def generate_request_for_generating_source_code_with_MATPLOTAGENT_RAG_corrector_iterative_error_resolve(data_structure_information, full_data_path, model, generated_python_script, error_message, query_augmentation):    
    print('Inside generate_request_for_generating_source_code_with_MATPLOTAGENT_RAG_corrector_iterative_error_resolve\n\n')
 
    prompt = generate_request_for_generating_source_code_with_error_msg_and_SO_iterative_error_resolving(data_structure_information=data_structure_information, full_data_path=full_data_path, 
                                                                                                         python_script=generated_python_script, error_message=error_message, 
                                                                                                         query_augmentation=query_augmentation)
    
    print("Prompt: \n", prompt)
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        # "response_format": "code_only",#this works for openAI only
        "options": {
            "seed": 12344,
            "temperature": 0.0
        }
    }
    return data

# created on June 29, 2025
# this is for the iterative error resolving
def generate_request_for_generating_source_code_with_error_msg_and_SO_iterative_error_resolving(data_structure_information, full_data_path, python_script, error_message, query_augmentation):
    print('Inside generate_request_for_generating_source_code_with_error_msg_and_SO_iterative_error_resolving\n')
    
    prompt=f"You are a Python programming expert.\n"
    prompt+="I have a Python script that produces an error at runtime. Below, I have included:\n"
    prompt+="   - The original Python script\n"
    prompt+="   - The exact error message\n"
    
    prompt+="Your task:\n"
    prompt+="   1. Carefully analyze the provided Python script and the error message.\n"
    prompt+="   2. Use the relevant suggestions (if applicable) to understand the likely cause and potential fixes.\n"
    prompt+="   3. Rewrite the entire Python script with the error fixed.\n"
    prompt+="   4. Ensure the script is logically correct, runnable, and preserves the original intent.\n"
    prompt+="   5. Do not include explanation — only provide the corrected script.\n"
    
    prompt+="\nOriginal Python Script:\n"    
    prompt+=f"{python_script}"

    prompt+="\nError Message:\n"    
    prompt+=f"{error_message}"

    
    if len(data_structure_information)>0: 
        prompt+= f"\nWhile rewriting the python code consider the information about the DATA_STRUCTURE=\n{data_structure_information}"
    # this is for the climate, matplotagent, and fastmribrain
    if len(full_data_path)>0:
        prompt+=f"\nNote: the initial goal of Original Python Script is to save the plotting output as a png file by extracting basename" 
        prompt+=f" and also the image should be saved to the same directory and the basename and directory should be from {full_data_path}"
    # this is for the vtk
    else:
        prompt+= f"\nNow generate a complete Python script that fulfills this query and includes the step that saves the rendering result as an image file with the same provided data file base name in the current directory.\n"

    return prompt

# under development
# currently being used, Date: Jan 29, 2025
def generate_request_for_generating_source_code_with_zero_shot_CoT_best_success_with_memory(user_input, data_structure_information, full_data_path, attribute_present):
    print('Inside generate_request_for_generating_source_code_with_zero_shot_CoT_best_success\n')
    prompt = "Generate the python code and return only the python code based on the description below:\n"
    prompt+=user_input 
    prompt+= "\n#Follow the instructions step by step:"
    prompt+= "\ndo import the library h5py as this programs need to read HDF5, .hdf5, .h5, .H5, .he5, or .HE5 data"
    prompt+= "\nset the input data file path from FULL_DATA_PATH="+full_data_path
    
    # this is for asking LLM to collect information from the memory
    prompt+= "\nDo not set or access any dataset by assumption, set datasets paths only from the memory reference of named PATHS information such as dataset paths, available attributes and shapes.\n"
  
    prompt+= "\nif this python script needs any type of plotting, graph labeling, give them related names from prompt"
    prompt+= "\nAt the end, save the output plot file to the same directory as FULL_DATA_PATH with .png extention"

    return prompt

# created on February 26, 2025
def generate_request_for_generating_source_code_with_zero_shot_CoT_best_success_manual_plot_saving_with_directory(user_input, data_structure_information, full_data_path, attribute_present):
    print('Inside generate_request_for_generating_source_code_with_zero_shot_CoT_best_success_manual_plot_saving_with_directory\n')
    prompt = "Generate the python code based on the description below:\n"
    prompt+=user_input 
    prompt+= "\n#Follow the instructions step by step:"
    prompt+= "\nDo import the library h5py as this programs need to read HDF5, .hdf5, .h5, .H5, .he5, or .HE5 data"
    prompt+= "\nSet the input data file path from the mentioned FULL_DATA_PATH="+full_data_path
    prompt+= "\nDo not set or access any dataset by assumption, set datasets paths only from the below available new line separated datasets and attributes added using a tab space in the following line:\n"
    prompt+=data_structure_information
    if attribute_present:
        prompt+= "\nWhile reading attribute follow the convention below:\n"
        prompt+= "file[data_set_path_name].attrs[attribute_name]"

    prompt+= "\nwhile accessing datasets all time use full paths added as examples above"
    prompt+= "\nif this python script needs any type of plotting, graph labeling, give them related names from prompt"
    prompt+= "\nFinally, the generated python script should save the plotted file with the same base name from FULL_DATA_PATH and also to the same directory as FULL_DATA_PATH with .png extention"
    prompt+="\nNote: Send only the code, no explanations or additional text."

    return prompt



# currently being used, Date: Jan 08, 2024
# created on Nov 17, 2024
def generate_request_for_generating_source_code_with_zero_shot_CoT_best_success(user_input, data_structure_information, full_data_path, attribute_present):
    print('Inside generate_request_for_generating_source_code_with_zero_shot_CoT_best_success\n')
    prompt = "Generate the python code based on the description below:\n"
    prompt+=user_input 
    prompt+= "\n#Follow the instructions step by step:"
    prompt+= "\ndo import the library h5py as this programs need to read HDF5, .hdf5, .h5, .H5, .he5, or .HE5 data"
    prompt+= "\nset the input data file path from FULL_DATA_PATH="+full_data_path
    prompt+= "\nDo not set or access any dataset by assumption, set datasets paths only from the below available new line separated datasets and attributes added using a tab space in the following line:\n"
    prompt+=data_structure_information
    if attribute_present:
        prompt+= "\nWhile reading attribute follow the convention below:\n"
        prompt+= "file[data_set_path_name].attrs[attribute_name]"

    prompt+= "\nwhile accessing datasets all time use full paths added as examples above"
    prompt+= "\nif this python script needs any type of plotting, graph labeling, give them related names from prompt"
    prompt+= "\nAt the end, save the output plot file to the same directory as FULL_DATA_PATH with .png extention"
    prompt+="\nSend only the code, no explanations or additional text."

    return prompt

# this is for resolving specific errors by changing prompt
def generate_request_for_generating_source_code_separate_prompt_method_with_zero_shot_CoT_with_corrector_step_by_step(user_input, data_structure_information, full_data_path, attribute_present, model, python_script, error_message):    
    print('Inside generate_request_for_generating_source_code_separate_prompt_method_with_zero_shot_CoT_with_corrector_step_by_step\n\n')
    
    # this is the modified version of generate_request_for_generating_source_code_with_zero_shot_CoT_best_success with image plotting and saving direction
    prompt = generate_request_for_generating_source_code_with_zero_shot_CoT_best_success_manual_plot_saving_with_directory(user_input, data_structure_information, full_data_path, attribute_present)
    
    print("Prompt: \n", prompt)
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "seed": 12344,
            "temperature": 0.0
        }
    }
    return data

# Current testing method
# date 10.31.2024 morning
def generate_request_for_generating_intent_attribute_condition(user_input_content, model):    
    prompt = "Determine the intenet, if the intent is search or filter data find the attribute name and condition and return the response under "
    prompt+= "<<<intent of the text, attribute of the condition, condition>>> "
    prompt+= " based on the description below: \n"+user_input_content+"\n"
    
    print("Prompt: \n", prompt )
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "seed": 12344,
            "temperature": 0.0
        }
    }
    return data



# Current testing method
# date 10.31.2024 morning
def generate_request_for_generating_source_code_with_zero_shot_CoT_with_corrector(user_input, data_structure_information, full_data_path, attribute_present, model):    
    s = "Generate the python code and add the code inside ```python ``` based on the description below: \n"+user_input+"\n"
    s+="#Follow the instructions step by step:\n"
    s+="do import the library h5py as this programs need to read HDF5, .hdf5, .h5, .H5, .he5, or .HE5 data\n"
    s+="set the input data file path from FULL_DATA_PATH="+full_data_path+"\n"
    if attribute_present:
        s+="Do not set or access any dataset by assumption, set datasets paths only from the below available new line separated datasets and attributes added using a tab space in the following line:\n"+ data_structure_information+"\n"
        s+='While reading attribute follow the convention below:\n'+ 'file[data_set_path_name].attrs[attribute_name]\n'
    else:
        s+="Do not set or access any dataset by assumption, set datasets paths only from the below available comma separated datasets information:\n"+ data_structure_information+"\n"
    s+='\n At the end, save the output plot file to the same directory as FULL_DATA_PATH with .png extention\n'

    print("Prompt: \n", s )
    
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

# created Nov 03 2024
# this is for resolving specific errors by changing prompt
def generate_request_for_generating_source_code_with_zero_shot_CoT_with_corrector_resolve_specific_error(user_input, data_structure_information, full_data_path, attribute_present, model):    
    s = "Generate the python code and add the code inside ```python ``` based on the description below: \n"+user_input+"\n"
    s+="#Follow the instructions step by step:\n"
    s+="do import the library h5py as this programs need to read HDF5, .hdf5, .h5, .H5, .he5, or .HE5 data\n"
    s+="set the input data file path from FULL_DATA_PATH="+full_data_path+"\n"
    if attribute_present:
        s+="Do not set or access any dataset by assumption, set datasets paths only from the below available new line separated datasets and attributes added using a tab space in the following line:\n"+ data_structure_information+"\n"
        s+='While reading attribute follow the convention below:\n'+ 'file[data_set_path_name].attrs[attribute_name]\n'
    else:
        s+="Do not set or access any dataset by assumption, set datasets paths only from the below available comma separated datasets information:\n"+ data_structure_information+"\n"

    # resolving errors related to using path varibales in accessing data
    s+="\n while accessing datasets all time use full paths added as examples above"
    
    # this is for resolving errors related colorbar labeling and accessing string data from the datasets
    s+="\n if this python script needs any type of plotting, graph labeling, give them related names from the user description"
    
    
    s+='\n At the end, save the output plot file to the same directory as FULL_DATA_PATH with .png extention\n'

    print("Prompt: \n", s)
    
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


# created on Nov 17 for simplicity
def generate_prompt_for_generating_source_code_with_zero_shot_CoT_with_corrector_step_by_step_v2(user_input, data_structure_information, full_data_path, attribute_present):    
    prompt = "Generate the python code and add the code inside <<< >>> based on the user queries mentioned in the description=, "
    prompt+= "At first Do import the library h5py as this program needs to read HDF5, .hdf5, .h5, .H5, .he5, or .HE5 data and os any folder or filer creation operation is needed\n"
    prompt+= " then load the datasets mentioned in the data_paths_information= , Do not set or access any dataset by assumption, also check notes= attached after data_paths_information= \n"
    prompt+= "Also set the input data file path from FULL_DATA_PATH=\n"+full_data_path
    prompt+= "\ndescription=\n"+user_input+"\n"
    prompt+= "\ndata_paths_information=\n"+data_structure_information
    if attribute_present:
        prompt+="\n\nnotes= \nthe above data_paths_information= contains datasets acutual paths information set paths from here which is required according to the description= "
        prompt+=" and in the following line the available attributes for the specific data above datasets"
   
        prompt+= 'While reading attribute follow the convention below:\n'+ 'file[data_set_path_name].attrs[attribute_name]\n'
    else:
        prompt+= "\nnotes= \nDo not set or access any dataset by assumption, set datasets paths only from the above new line separated information mentioned in the data_paths_information="

    prompt+= "if this python script needs any type of plotting, graph labeling, give them related names from the user description\n"
    
    prompt+= 'At the end, save the output plot file to the same directory as FULL_DATA_PATH with .png extention\n'

    return prompt


# created on Nov 17 for simplicity
def generate_prompt_for_generating_source_code_zero_shot_with_corrector_simple_rbr(user_input, data_structure_information, full_data_path, attribute_present):    
    prompt = "Generate the python code and add the code inside <<< >>> based on the user queries mentioned in the description=\n"
    prompt+= "datasets actual information in the data_paths_information= \n"
    prompt+= "Do import the library h5py if the full_data_file_path= has extension .hdf5, .h5, .H5, .he5, or .HE5\n"
    # prompt+= " then load the datasets mentioned in the data_paths_information= , Do not set or access any dataset by assumption, also check notes= attached after data_paths_information= \n"
    prompt+= "Also set the input data file path from FULL_DATA_FILE_PATH=\n"+full_data_path
    prompt+= "\nwhole user description=\n"+user_input+"\n"
    prompt+= "data_paths_information=\n"+data_structure_information

    if attribute_present:
        # prompt+="\n\nnotes= \nthe above data_paths_information= contains datasets acutual paths information set paths from here which is required according to the description= "
        prompt+= "\nattribute information added using new line and tab after each dataset in the data_paths_information="
        prompt+= "\nattribute reading notes=\n'+ 'file[data_set_path_name].attrs[attribute_name]"
    else:
        prompt+= "\ndatasets reading notes= \nDo not set or access any dataset by assumption"

    prompt+= "\nwhile required give simple name to the plots"
    prompt+= '\nAt the end, save the output plot file to the same directory as FULL_DATA_FILE_PATH with .png extention'

    return prompt


# created Nov 16 2024
# for zero-shot Cot prompt generation
def generate_prompt_for_generating_source_code_with_zero_shot_CoT_with_corrector_step_by_step(user_input, data_structure_information, full_data_path, attribute_present):    
    prompt = "Generate the python code and add the code inside <<< >>> based on the description below description=: \n"+user_input+"\n"
    prompt+= " At first gather the requirements based on the description, dependant data and information, and FULL_DATA_PATHS, at the end use the required information to generate the code step by step\n"
  
    prompt+= "do import the library h5py as this program needs to read HDF5, .hdf5, .h5, .H5, .he5, or .HE5 data\n"
    prompt+= "set the input data file path from FULL_DATA_PATH="+full_data_path+"\n"
    if attribute_present:
        prompt+= "Do not set or access any dataset by assumption, "
        prompt+= "set datasets paths only from the below available new line separated datasets correct paths information from the given exact data file below:\n"
        prompt+= data_structure_information+"\n"
        # this line is added to separate the attributes
        prompt+= "Access the attributes listed below if only required to access based on the above description\n"

        prompt+= 'While reading attribute follow the convention below:\n'+ 'file[data_set_path_name].attrs[attribute_name]\n'
    else:
        prompt+= "Do not set or access any dataset by assumption, set datasets paths only from the below new line separated information, data_paths_information=:\n"+ data_structure_information+"\n"

    # resolving errors related to using path varibales in accessing data
    prompt+= "\n while accessing datasets all time use full paths added as examples above"
    
    # this is for resolving errors related colorbar labeling and accessing string data from the datasets
    prompt+= "if this python script needs any type of plotting, graph labeling, give them related names from the user description\n"
    
    prompt+= 'At the end, save the output plot file to the same directory as FULL_DATA_PATH with .png extention\n'

    return prompt


# created Nov 16 2024
# for zero-shot Cot prompt generation
def generate_prompt_for_generating_source_code_with_zero_shot_CoT_step_by_step(user_input, full_data_path):    
    prompt = "Generate the python code and add the code inside <<< >>> based on the description below description=: \n"+user_input+"\n"
    prompt+= "At first gather the requirements based on the description, dependant data and information, and FULL_DATA_PATH, at the end use the required information to generate the code step by step\n"
    prompt+= "Do import the library h5py as this program needs to read HDF5, .hdf5, .h5, .H5, .he5, or .HE5 data\n"
    prompt+= "Set the input data file path from FULL_DATA_PATH="+full_data_path+"\n"
    
    # this is for resolving errors related colorbar labeling and accessing string data from the datasets
    prompt+= "If this python script needs any type of plotting, graph labeling, give them related names from the user description\n"
    
    prompt+= 'At the end, save the output plot file to the same directory as FULL_DATA_PATH with with the basename from the FULL_DATA_PATH with .png extention\n'

    return prompt


# created Nov 09 2028
# created Nov 03 2024
# this is for resolving specific errors by changing prompt
def generate_request_for_generating_source_code_with_zero_shot_CoT_with_corrector_step_by_step(user_input, data_structure_information, full_data_path, attribute_present, model):    
    # s = "Generate the python code and add the code inside ```python ``` based on the description below description=: \n"+user_input+"\n"
    s = "Generate the python code and add the code inside <<< >>> based on the description below description=: \n"+user_input+"\n"
    s+= "#Follow the instructions step by step:\n"
    
    s+= "do import the library h5py as this program needs to read HDF5, .hdf5, .h5, .H5, .he5, or .HE5 data\n"
    s+= "set the input data file path from FULL_DATA_PATH="+full_data_path+"\n"
    if attribute_present:
        s+= "Do not set or access any dataset by assumption, "
        s+= "set datasets paths only from the below available new line separated datasets paths information below:\n"
        s+= data_structure_information+"\n"
        # this line is added to separate the attributes
        s+= "Access the attributes listed below if only required to access based on the above description\n"

        s+= 'While reading attribute follow the convention below:\n'+ 'file[data_set_path_name].attrs[attribute_name]\n'
    else:
        s+= "Do not set or access any dataset by assumption, set datasets paths only from the below new line separated information, data_paths_information=:\n"+ data_structure_information+"\n"

    # resolving errors related to using path varibales in accessing data
    s+= "\n while accessing datasets all time use full paths added as examples above"
    
    # this is for resolving errors related colorbar labeling and accessing string data from the datasets
    s+= "\n if this python script needs any type of plotting, graph labeling, give them related names from the user description"
    
    s+= '\n At the end, save the output plot file to the same directory as FULL_DATA_PATH with .png extention\n'

    print("Prompt: \n", s)
    
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




# created Nov 14 2024
# this is for getting initial results without corrector
def generate_request_for_generating_source_code_with_zero_shot_CoT_separate_method_step_by_step(user_input, full_data_path, model):    
    prompt = generate_prompt_for_generating_source_code_with_zero_shot_CoT_step_by_step(user_input, full_data_path)

    print("Prompt: \n", prompt)
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "seed": 12344,
            "temperature": 0.0
        }
    }
    return data


# created Nov 14 2024
# this is for getting initial results without corrector
def generate_request_for_generating_source_code_with_zero_shot_CoT_without_corrector_step_by_step(user_input, full_data_path, model):    
    s = "Generate the python code and add the code inside <<< >>>  based on the description below description=: \n"+user_input+"\n"
    s+= "#Follow the instructions step by step:\n"
    s+= "do import the library h5py as this program needs to read HDF5, .hdf5, .h5, .H5, .he5, or .HE5 data\n"
    s+= "set the input data file path from FULL_DATA_PATH="+full_data_path+"\n"
    
    # resolving errors related to using path varibales in accessing data
    
    # this is for resolving errors related colorbar labeling and accessing string data from the datasets
    s+= "\n if this python script needs any type of plotting, graph labeling, give them related names from the user description"
    
    s+= '\n At the end, save the output plot file to the same directory as FULL_DATA_PATH with .png extention\n'

    print("Prompt: \n", s)
    
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


def generate_request_for_generating_source_code_with_data(sample, dataset_information, full_data_path, model="llama3:latest"):
    s = "Generate the python code based on the following description: \n" + sample +"\n Please read the data from the following directory: \n"+full_data_path+"\n Also Please use the following dataset paths to set the paths correctly: \n"+dataset_information 
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


def generate_request_for_generating_source_code_with_data_structure(sample, dataset_information, data_structure_information, full_data_path, model):
    s = "Generate the python code based on the following description: \n"+sample
    s +='\n Add this data directory path below to run the above code. '
    s +=  "\nRead the data from the following directory, this path such as data_path or FILE_NAME or INPUT_FILE or FILE should be used this following path: \n"+ full_data_path

    s+= "\ndo import h5py library if the program needs to read data with extensions HDF5, hdf5, h5, H5, he5, and HE5."
    s += "\nWhile reading groups and dataset information from data this hierarchical structure should be analyzed to set the paths, the list inside curly brace are dataset attributes: \n"+data_structure_information

    print("Prompt: \n", s )
    
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

def generate_request_for_generating_source_code_with_data_rule_base_reasoning(user_input, data_structure_information, full_data_path, model):
    s = "Generate the python code based on the DESCRIPTION, read the input data path from FULL_DATA_PATH, also where generating code based on the DESCRIPTION set the group, dataset, "
    s +=" and attribute paths from the ndata_set_attribute_information by match which one you required, also import the library h5py for the FULL_DATA_PATH with extensions HDF5, hdf5, h5, H5, he5, and HE5 "
    s+='\nAlso while reading attribute follow the convention mentioned in the ATTRBITE_READ section such as file[path of the specific dataset].attrs[name of the attribute], if any attribute path not found no path should be assumed, just find alternative way\n'
    # current working
    s+="\nALso, while setting dataset and attributes first first verify if it is present in the ndata_set_attribute_information\n"
    s+='\n The output plot file should be the same as FULL_DATA_PATH just with png extentions\n'

    s +="\nDESCRIPTION=\n"+user_input
    s +=  "\nFULL_DATA_PATH= \n"+ full_data_path
    s+="\ndata_set_attribute_information= \n"+data_structure_information

    s+='\nATTRIBUTE_READ=\n'+'file[data_set_path_name].attrs[attribute_name]'


    print("Prompt: \n", s )
    
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


def generate_request_for_generating_source_code_with_data_structure_debugging_and_reset_paths(code, full_data_path, model):
    s = "Debug the following python code and regenrate the python code: \n\n"
    s+=code+"\n\n"

    s+="Use the following data paths to correct the code where it read or access group or dataset or attributes: \n"
    s+=full_data_path

    print("\n\nRepair Prompt: \n", s )
    
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


# def generate_request_for_generating_source_code(sample, model="llama3:70b"):
# latest means 8b
def generate_request_for_extracting_datasets_from_description(sample, model="llama3:latest"):
    
    s = "Please create a list of all groups, dataset, and attributes with full paths from the following description and retrun in a json array format, the json variable name should be datasets, don't send response without json format and should be wrap indise ```json\n```: \n" + sample


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

def generate_request_for_extracting_datasets_and_attributes_from_description(sample, model):
    
    s = "Please create a list of all dataset and attributes with full paths from the following description and retrun in a json array format, the json variable name should be datasets, don't send response without json format and should be wrap indise ```json\n```: \n" + sample
    print("\nHuman like generated input text: \n", sample)
    
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


def generate_group_and_datasets_name_and_save(source_dir, target_dir, URL, old_ext='.txt'):
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
            
            start_delim_1 = "```\n"
            start_delim_2 = "```"
            start_delim_3 = "```\n\n"
            end_delim = "```"

            result_1 = utils.extract_substring(llm_gen_source_code['response'], start_delim_1, end_delim)
            result_2 = utils.extract_substring(llm_gen_source_code['response'], start_delim_2, end_delim)
            result_3 = utils.extract_substring(llm_gen_source_code['response'], start_delim_3, end_delim)
            
            
            # output_file_path = os.path.join(target_dir, f'{base_name}.py')
            output_file_path = os.path.join(target_dir, f'{base_name}.txt')
            with open(output_file_path, 'w') as f:
                    f.write(llm_gen_source_code['response'])
            
            if result_1:
                return result_1
            elif result_2:
                return result_2
            elif result_3:
                return result_3
            else:
                print("source code not found")
                return ""

            
def generate_code_and_save(source_dir, target_dir, URL, old_ext='.txt'):
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

            result_1 = utils.extract_substring(llm_gen_source_code['response'], start_delim_1, end_delim)
            result_2 = utils.extract_substring(llm_gen_source_code['response'], start_delim_2, end_delim)
            result_3 = utils.extract_substring(llm_gen_source_code['response'], start_delim_3, end_delim)
            
            
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




def get_group_dataset_and_attribute_name(user_input_content, model, URL):
    try:
        datasets_from_user_input = generate_request_for_extracting_datasets_from_description(user_input_content, model)
        datasets_from_user_input = json.dumps(datasets_from_user_input).encode("utf-8")
        datasets_from_user_response = requests.post(URL, data=datasets_from_user_input)
                    
        datasets_from_user_response  = datasets_from_user_response.json()

        datasets_from_user_response = utils.convert_response_into_json_path_list(datasets_from_user_response['response'])
        print("\nLLMRequester.get_group_and_dataser_name: after convert_response_into_json_path_list: \n", datasets_from_user_response)
        
        datasets_from_user_response_json = json.loads(datasets_from_user_response)
        # print("\nLLMRequester.get_group_and_dataser_name: after json loads: \n", datasets_from_user_response_json)     
        
        # print("\nLLMRequester.get_group_and_dataser_name: datasets: \n", datasets_from_user_response_json['datasets'])    

        extract_list_data_from_llm_response = utils.extract_unique_strings(datasets_from_user_response_json['datasets'])
        print("\nLLMRequester.get_group_and_dataser_name: after extract_unique_strings: \n", extract_list_data_from_llm_response)        
        
        # print("LLMRequester.get_group_and_dataser_name:extract_list_data_from_llm_response: \n", extract_list_data_from_llm_response)
       
        return extract_list_data_from_llm_response
    except Exception as e:
        print("Exception occurred at LLMRequester.get_group_and_dataser_name, message: ", e)
        return []

# created on date: 29 Sep 2024 at 9:30 PM
def get_dataset_and_attribute_name(user_input_content, model, URL):
    try:
        datasets_from_user_input = generate_request_for_extracting_datasets_and_attributes_from_description(user_input_content, model)
        datasets_from_user_input = json.dumps(datasets_from_user_input).encode("utf-8")
        datasets_from_user_response = requests.post(URL, data=datasets_from_user_input)
                    
        datasets_from_user_response  = datasets_from_user_response.json()

        datasets_from_user_response = utils.convert_response_into_json_path_list(datasets_from_user_response['response'])
        print("\nLLMRequester.get_dataset_and_attribute_name: after convert_response_into_json_path_list: \n", datasets_from_user_response)
        
        datasets_from_user_response_json = json.loads(datasets_from_user_response)
        # print("\nLLMRequester.get_group_and_dataser_name: after json loads: \n", datasets_from_user_response_json)     
        
        # print("\nLLMRequester.get_group_and_dataser_name: datasets: \n", datasets_from_user_response_json['datasets'])    

        extract_list_data_from_llm_response = utils.extract_unique_strings(datasets_from_user_response_json['datasets'])
        print("\nLLMRequester.get_dataset_and_attribute_name: after extract_unique_strings: \n", extract_list_data_from_llm_response)        
        
        return extract_list_data_from_llm_response
    except Exception as e:
        print("Exception occurred at LLMRequester.get_group_and_dataser_name, message: ", e)
        return []


def generate_code_and_save_with_data_information(user_input_file_path, dataset_information, full_data_path, target_dir, URL, old_ext='.txt'):
    print("user_input_file_path: ", user_input_file_path)
    print("dataset_information: ", dataset_information)
    print("full_data_path: ", full_data_path)


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
          
    # Change the extension
    base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension
    print("base_name = os.path.splitext(user_input_file_path)[0]: ", base_name)
            
    # generate code and save
    with open(user_input_file_path, 'r') as f:
        description = f.read()
    
    source_code_gen = generate_request_for_generating_source_code_with_data(description, dataset_information, full_data_path, "llama3:latest")
    source_code_gen = json.dumps(source_code_gen).encode("utf-8")
    llm_gen_source_code = requests.post(URL, data=source_code_gen)
    #print(llm_gen_source_code)
    llm_gen_source_code  = llm_gen_source_code.json()
    #print(llm_gen_source_code)
    # print(llm_gen_source_code['response'])
    
    start_delim_1 = "```python\n"
    start_delim_2 = "```Python\n"
    start_delim_3 = "```\n"
    end_delim = "```"

    result_1 = utils.extract_substring(llm_gen_source_code['response'], start_delim_1, end_delim)
    result_2 = utils.extract_substring(llm_gen_source_code['response'], start_delim_2, end_delim)
    result_3 = utils.extract_substring(llm_gen_source_code['response'], start_delim_3, end_delim)
    
    print("target_dir", target_dir)
    print("base_name", base_name)
    output_file_path = os.path.join(target_dir, f'{base_name}.py')
    print("output_file_path", output_file_path, end="\n\n")
    
    if result_1:
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



def generate_code_and_save_with_data_structure_information(user_input_file_path, dataset_information, data_structure_information, full_data_path, target_dir, URL, old_ext='.txt'):
  

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
          
    # Change the extension
    base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension
    # print("base_name = os.path.splitext(user_input_file_path)[0]: ", base_name)
            
    # generate code and save
    with open(user_input_file_path, 'r') as f:
        description = f.read()
    
    # source_code_gen = generate_request_for_generating_source_code_with_data(description, dataset_information, full_data_path, "llama3:latest")
    source_code_gen = generate_request_for_generating_source_code_with_data_structure(description, dataset_information, data_structure_information, full_data_path, "llama3:latest")
    source_code_gen = json.dumps(source_code_gen).encode("utf-8")
    llm_gen_source_code = requests.post(URL, data=source_code_gen)
    #print(llm_gen_source_code)
    llm_gen_source_code  = llm_gen_source_code.json()
    #print(llm_gen_source_code)
    # print(llm_gen_source_code['response'])
    response_code = utils.extract_python_code_from_response(llm_gen_source_code['response'])
    if response_code is not None:
        output_file_path = os.path.join(target_dir, f'{base_name}.py')
        utils.save_file(output_file_path, response_code)


def generate_code_and_save_with_data_structure_information_with_repair(user_input_file_path, description, dataset_information, data_structure_information, full_data_path, target_dir, model, URL, old_ext='.txt'):
    try:
        # print("user_input_file_path: ", user_input_file_path)
        # print("dataset_information: ", dataset_information)
        # print("full_data_path: ", full_data_path)


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
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension  
        source_code_gen = generate_request_for_generating_source_code_with_data_structure(description, dataset_information, data_structure_information, full_data_path, model)

        source_code_gen = json.dumps(source_code_gen).encode("utf-8")
        llm_gen_source_code = requests.post(URL, data=source_code_gen)
        #print(llm_gen_source_code)
        llm_gen_source_code  = llm_gen_source_code.json()
        #print(llm_gen_source_code)
        # 
        response_code = utils.extract_python_code_from_response(llm_gen_source_code['response'])
        print("\n\nFirst Generated code: \n", response_code)
        
        
        if response_code is not None:
            
            # print("\n\nSecond Generated code: \n", regen_response_code)
            regen_response_code = response_code
            if regen_response_code is not None:
                output_file_path = os.path.join(target_dir, f'{base_name}.py')
                utils.save_file(output_file_path, response_code)
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_code_and_save_with_data_structure_information_with_repair, message: ", e)



# def generate_code_and_save_with_data_rule_based_reasoning(user_input_file_path, description, dataset_information, data_structure_information, full_data_path, target_dir, model, old_ext='.txt'):
def generate_code_and_save_with_data_rule_based_reasoning(user_input_file_path, user_input_description, data_structure_information, full_data_path, target_dir, model, URL, old_ext='.txt'):
    try:
        # print("user_input_file_path: ", user_input_file_path)
        # print("dataset_information: ", dataset_information)
        # print("full_data_path: ", full_data_path)


        # Create the target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension
        # print("base_name = os.path.splitext(user_input_file_path)[0]: ", base_name)
                 
        source_code_gen = generate_request_for_generating_source_code_with_data_rule_base_reasoning(user_input_description, data_structure_information, full_data_path, model)

        source_code_gen = json.dumps(source_code_gen).encode("utf-8")
        llm_gen_source_code = requests.post(URL, data=source_code_gen)
        #print(llm_gen_source_code)
        llm_gen_source_code  = llm_gen_source_code.json()
        print('Raw output: \n',llm_gen_source_code)
        # 
        response_code = utils.extract_python_code_from_response(llm_gen_source_code['response'])
        print("\n\nFirst Generated code: \n", response_code)
        
        
        if response_code is not None:
            
            # print("\n\nSecond Generated code: \n", regen_response_code)
            regen_response_code = response_code
            if regen_response_code is not None:
                output_file_path = os.path.join(target_dir, f'{base_name}.py')
                utils.save_file(output_file_path, response_code)
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_code_and_save_with_data_rule_based_reasoning, message: ", e)



# def generate_code_and_save_with_data_rule_based_reasoning(user_input_file_path, description, dataset_information, data_structure_information, full_data_path, target_dir, model, old_ext='.txt'):
def generate_code_and_save_with_data_zero_shot_CoT(user_input_file_path, user_input_description, data_structure_information, full_data_path, target_dir, attribute_present, model, is_memory, URL, dataset, old_ext='.txt'):
    try:
     
        # Create the target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension
        # this is currently being used for generating final code without LLM memory
        source_code_gen = ''
        
        # with corrector
        if is_memory==False:
            # user_input, data_structure_information, full_data_path, attribute_present, model, python_script, error_message
            source_code_gen = generate_request_for_generating_source_code_separate_prompt_method_with_zero_shot_CoT_with_corrector_step_by_step(user_input_description, data_structure_information, full_data_path, attribute_present, model, python_script='', error_message='')
        
        # with memory
        else:
            # currently under development with LLM memory                                                                    user_input,             data_structure_information, full_data_path, attribute_present, model
            source_code_gen = generate_request_for_generating_source_code_using_LLM_memory_with_zero_shot_CoT_with_corrector(user_input_description, data_structure_information, full_data_path, attribute_present, model)

        prompt = source_code_gen['prompt']
        prompt='"""'+prompt+'"""'

        source_code_gen = json.dumps(source_code_gen).encode("utf-8")
        llm_gen_source_code = requests.post(URL, data=source_code_gen)
        # llm_gen_source_code= {'response': 'test'}
        #print(llm_gen_source_code)
        llm_gen_source_code  = llm_gen_source_code.json()
        print('Raw output: \n',llm_gen_source_code)
        # 
        response_code = utils.extract_python_code_from_response(llm_gen_source_code['response'])
        print("\n\nFirst Generated code: \n", response_code)
        
        
        if response_code is not None:
            
            regen_response_code = response_code
            if regen_response_code is not None:
                output_file_path = os.path.join(target_dir, f'{base_name}.py')
                utils.save_file(output_file_path, prompt+'\n\n'+response_code)
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_code_and_save_with_data_zero_shot_CoT, message: ", e)

# created on Feb 13, 2025
# to resolve error iteratively
# def generate_code_and_save_with_data_rule_based_reasoning(user_input_file_path, description, dataset_information, data_structure_information, full_data_path, target_dir, model, old_ext='.txt'):
def generate_code_and_save_with_data_zero_shot_CoT_iterative_error_resolve(user_input_file_path, user_input_description, data_structure_information, full_data_path, target_dir, attribute_present, model, is_memory, python_script, error_message, iteration, URL):
    try:
        # print("user_input_file_path: ", user_input_file_path)
      
        # Create the target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension
        # print("base_name = os.path.splitext(user_input_file_path)[0]: ", base_name)
        
        # this is currently being used for generating final code without LLM memory
        source_code_gen = ''
        # with corrector function only
        if is_memory==True:
            print('LLMRequester:: with memory code generation ...')
            print('')
            # currently under development with LLM memory                                                                    user_input,             data_structure_information, full_data_path, attribute_present, model
            source_code_gen = generate_request_for_generating_source_code_using_LLM_memory_with_zero_shot_CoT_with_corrector(user_input_description, data_structure_information, full_data_path, attribute_present, model)
        elif len(python_script) <= 0 and is_memory==False:
            print('LLMRequester:: with corrector code generation ...')
            # default with corrector code generation
            source_code_gen = generate_request_for_generating_source_code_separate_prompt_method_with_zero_shot_CoT_with_corrector_step_by_step(user_input_description, data_structure_information, full_data_path, attribute_present, model, python_script='', error_message='' )
        else:
            # with corrector iterative code generation
            print('LLMRequester:: with corrector Iterative error resolvinging ...')
            source_code_gen = generate_request_for_generating_source_code_using_LLM_memory_with_zero_shot_CoT_with_corrector_iterative_error_resolve(user_input_description, data_structure_information, full_data_path, attribute_present, model, python_script, error_message)

        prompt = source_code_gen['prompt']
        prompt='"""'+prompt+'"""'

        source_code_gen = json.dumps(source_code_gen).encode("utf-8")
        llm_gen_source_code = requests.post(URL, data=source_code_gen)
        # llm_gen_source_code= {'response': 'test'}
        #print(llm_gen_source_code)
        llm_gen_source_code  = llm_gen_source_code.json()
        print('Raw output: \n',llm_gen_source_code)
        # 
        # 
        if len(python_script)> 0 and len(error_message) > 0:
            print('Iterative resolving error steps, generated code: ')
        response_code = utils.extract_python_code_from_response(llm_gen_source_code['response'])
        print("\n\nFirst Generated code: \n", response_code)
        
        
        if response_code is not None:
            
            # print("\n\nSecond Generated code: \n", regen_response_code)

            regen_response_code = response_code
            if regen_response_code is not None:
                output_file_path = os.path.join(target_dir, f'{base_name}.py')
                # response_code+="\nprint(\"Success_and_End_of_Script!\")"
                
                utils.save_file(output_file_path, prompt+'\n\n'+response_code)

                # lets save the iterative generated code
                output_file_path = os.path.join(target_dir, f'{base_name}_{iteration}.py')
                utils.save_file(output_file_path, response_code)
                
                # return the newly generated python script path
                return output_file_path, response_code
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_code_and_save_with_data_rule_based_reasoning, message: ", e)
import time
# created on June 29, 2025
# to resolve error iteratively
def generate_code_and_save_code_with_RAG_iterative_error_resolve(user_input_file_path, user_input_description, dataset_attrubute_fullpath_list_result, full_data_path, target_dir, model, python_script, error_message, iteration, URL, examples_for_query_augmentation, temperature):
    try:
        print('LLMRequester::Inside generate_code_and_save_code_with_RAG_iterative_error_resolve ...')
        print("user_input_file_path: ", user_input_file_path)
        print("full_data_path: ", full_data_path)

        # Create the target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension
                 
        # this is currently being used for generating final code without LLM memory
        source_code_gen = ''
        
        if len(python_script) <= 0:
            print('LLMRequester:: with corrector code generation ...')
            #                                                                              user_input,             examples_code_for_query_augmentation, full_data_path, model, dataset_attrubute_fullpath_list_result
            source_code_gen_request = generate_request_for_generating_source_code_with_rag(user_input_description, examples_for_query_augmentation, full_data_path, model, dataset_attrubute_fullpath_list_result, temperature)
        else:
            # with corrector iterative code generation
            print('LLMRequester:: with corrector Iterative error resolvinging ...')
            source_code_gen_request = generate_request_for_generating_source_code_with_SO_corrector_iterative_error_resolve(dataset_attrubute_fullpath_list_result, full_data_path, model, python_script, error_message, examples_for_query_augmentation)
        
        prompt = source_code_gen_request['prompt']
        prompt='"""'+prompt+'"""'

        source_code_gen_request = json.dumps(source_code_gen_request).encode("utf-8")
        
        llm_gen_source_code_response = requests.post(URL, data=source_code_gen_request)

        llm_gen_source_code_response  = llm_gen_source_code_response.json()
        print('Raw output: \n', llm_gen_source_code_response)
         
         
        response_code = utils.extract_python_code_from_response(llm_gen_source_code_response['response'])
        print("\n\nFirst Generated code: \n", response_code)
        
        
        if response_code is not None:            
            regen_response_code = response_code
            if regen_response_code is not None:
                output_file_path = os.path.join(target_dir, f'{base_name}.py')
              
                utils.save_file(output_file_path, prompt+'\n\n'+response_code)

                # lets save the iterative generated code
                output_file_path = os.path.join(target_dir, f'{base_name}_{iteration}.py')
                utils.save_file(output_file_path, response_code)
                
                # return the newly generated python script path
                print('LLMRequester:: Leaving generate_code_and_save_code_with_RAG_iterative_error_resolve ...')
                return output_file_path, response_code
            else:
                print('LLMRequester:: Leaving generate_code_and_save_code_with_RAG_iterative_error_resolve-->Response code is None')
                return 'None', 'None'
        else:
            print('LLMRequester:: Leaving outer generate_code_and_save_code_with_RAG_iterative_error_resolve-->Response code is None')
            return 'None', 'None'
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_code_and_save_code_with_RAG_iterative_error_resolve, message: ", e)
        return 'None', 'None'


# created on Jul 06, 2025
# to resolve error iteratively
def generate_code_and_save_code_MATPLOTAGENT_RAG_iterative_error_resolve(user_input_file_path, user_input_description, dataset_attrubute_fullpath_list_result, full_data_path, target_dir, model, python_script, error_message, iteration, URL, examples_for_query_augmentation, temperature):
    try:
        print('LLMRequester::Inside generate_code_and_save_code_with_RAG_iterative_error_resolve ...')
        print("user_input_file_path: ", user_input_file_path)
        print("full_data_path: ", full_data_path)

        # Create the target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension
        # print("base_name = os.path.splitext(user_input_file_path)[0]: ", base_name)
                 
        # this is currently being used for generating final code without LLM memory
        source_code_gen = ''
        
        if len(python_script) <= 0:
            print('LLMRequester:: with corrector code generation ...')
            #                                                                              user_input,             examples_code_for_query_augmentation, full_data_path, model, dataset_attrubute_fullpath_list_result
            source_code_gen_request = generate_request_for_generating_source_code_with_rag(user_input_description, examples_for_query_augmentation, full_data_path, model, dataset_attrubute_fullpath_list_result, temperature)
        else:
            # with corrector iterative code generation
            print('LLMRequester:: with corrector Iterative error resolvinging ...')
            # source_code_gen_request = generate_request_for_generating_source_code_using_LLM_memory_with_zero_shot_CoT_with_corrector_iterative_error_resolve(user_input_description, data_structure_information, full_data_path, attribute_present, model, python_script, error_message)
            source_code_gen_request = generate_request_for_generating_source_code_with_MATPLOTAGENT_RAG_corrector_iterative_error_resolve(dataset_attrubute_fullpath_list_result, full_data_path, model, python_script, error_message, examples_for_query_augmentation)
        
        prompt = source_code_gen_request['prompt']
        prompt='"""'+prompt+'"""'

        source_code_gen_request = json.dumps(source_code_gen_request).encode("utf-8")
        llm_gen_source_code_response = requests.post(URL, data=source_code_gen_request)

        llm_gen_source_code_response  = llm_gen_source_code_response.json()
        print('Raw output: \n', llm_gen_source_code_response)
         
        response_code = utils.extract_python_code_from_response(llm_gen_source_code_response['response'])
        print("\n\nFirst Generated code: \n", response_code)
        
        
        if response_code is not None:            
            regen_response_code = response_code
            if regen_response_code is not None:
                output_file_path = os.path.join(target_dir, f'{base_name}.py')
           
                utils.save_file(output_file_path, prompt+'\n\n'+response_code)

                # lets save the iterative generated code
                output_file_path = os.path.join(target_dir, f'{base_name}_{iteration}.py')
                utils.save_file(output_file_path, response_code)
                
                # return the newly generated python script path
                print('LLMRequester:: Leaving generate_code_and_save_code_MATPLOTAGENT_RAG_iterative_error_resolve ...')
                return output_file_path, response_code
            else:
                print('LLMRequester:: Leaving generate_code_and_save_code_MATPLOTAGENT_RAG_iterative_error_resolve -->Response code is None')
                return 'None', 'None'
        else:
            print('LLMRequester:: Leaving outer generate_code_and_save_code_MATPLOTAGENT_RAG_iterative_error_resolve-->Response code is None')
            return 'None', 'None'
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_code_and_save_code_MATPLOTAGENT_RAG_iterative_error_resolve, message: ", e)
        return 'None', 'None'

# created on Jul 06, 2025
# to resolve error iteratively
def generate_code_and_save_code_VTK_RAG_iterative_error_resolve(user_input_file_path, user_input_description, dataset_attrubute_fullpath_list_result, full_data_path, target_dir, model, python_script, error_message, iteration, URL, examples_for_query_augmentation):
    try:
        print('LLMRequester::Inside generate_code_and_save_code_with_RAG_iterative_error_resolve ...')
        print("user_input_file_path: ", user_input_file_path)
        print("full_data_path: ", full_data_path)

        # Create the target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension
        # print("base_name = os.path.splitext(user_input_file_path)[0]: ", base_name)
                 
        # this is currently being used for generating final code without LLM memory
        source_code_gen = ''
        
        if len(python_script) <= 0:
            print('LLMRequester:: with corrector code generation ...')
            source_code_gen_request = generate_request_for_generating_vtk_related_python_scripts_without_rag(user_input_description, full_data_path, model, dataset_attrubute_fullpath_list_result)
        else:
            # with corrector iterative code generation
            print('LLMRequester:: with corrector Iterative error resolvinging ...')
            source_code_gen_request = generate_request_for_generating_source_code_with_MATPLOTAGENT_RAG_corrector_iterative_error_resolve(dataset_attrubute_fullpath_list_result, full_data_path, model, python_script, error_message, examples_for_query_augmentation)
        
        prompt = source_code_gen_request['prompt']
        prompt='"""'+prompt+'"""'

        source_code_gen_request = json.dumps(source_code_gen_request).encode("utf-8")
        llm_gen_source_code_response = requests.post(URL, data=source_code_gen_request)

        llm_gen_source_code_response  = llm_gen_source_code_response.json()
        print('Raw output: \n', llm_gen_source_code_response)
         
        response_code = utils.extract_python_code_from_response(llm_gen_source_code_response['response'])
        print("\n\nFirst Generated code: \n", response_code)
        
        
        if response_code is not None:            
            regen_response_code = response_code
            if regen_response_code is not None:
                output_file_path = os.path.join(target_dir, f'{base_name}.py')
          
                utils.save_file(output_file_path, prompt+'\n\n'+response_code)

                # lets save the iterative generated code
                output_file_path = os.path.join(target_dir, f'{base_name}_{iteration}.py')
                utils.save_file(output_file_path, response_code)
                
                # return the newly generated python script path
                print('LLMRequester:: Leaving generate_code_and_save_code_VTK_RAG_iterative_error_resolve ...')
                return output_file_path, response_code
            else:
                print('LLMRequester:: Leaving generate_code_and_save_code_VTK_RAG_iterative_error_resolve -->Response code is None')
                return 'None', 'None'
        else:
            print('LLMRequester:: Leaving outer generate_code_and_save_code_VTK_RAG_iterative_error_resolve-->Response code is None')
            return 'None', 'None'
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_code_and_save_code_VTK_RAG_iterative_error_resolve, message: ", e)
        return 'None', 'None'


# created on Jul 06, 2025
# to resolve error iteratively
def generate_code_and_save_code_FASTMRIBRAIN_RAG_iterative_error_resolve(user_input_file_path, user_input_description, dataset_attrubute_fullpath_list_result, full_data_path, target_dir, model, python_script, error_message, iteration, URL, examples_for_query_augmentation, temperature):
    try:
        print('LLMRequester::Inside generate_code_and_save_code_with_RAG_iterative_error_resolve ...')
        print("user_input_file_path: ", user_input_file_path)
        print("full_data_path: ", full_data_path)

        # Create the target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension
        # print("base_name = os.path.splitext(user_input_file_path)[0]: ", base_name)
                 
        # this is currently being used for generating final code without LLM memory
        source_code_gen = ''
        
        if len(python_script) <= 0:
            print('LLMRequester:: with corrector code generation ...')
            #                                                                              user_input,             examples_code_for_query_augmentation, full_data_path, model, dataset_attrubute_fullpath_list_result
            source_code_gen_request = generate_request_for_generating_source_code_with_rag(user_input_description, examples_for_query_augmentation, full_data_path, model, dataset_attrubute_fullpath_list_result, temperature)
        else:
            # with corrector iterative code generation
            print('LLMRequester:: with corrector Iterative error resolvinging ...')
            # source_code_gen_request = generate_request_for_generating_source_code_using_LLM_memory_with_zero_shot_CoT_with_corrector_iterative_error_resolve(user_input_description, data_structure_information, full_data_path, attribute_present, model, python_script, error_message)
            source_code_gen_request = generate_request_for_generating_source_code_with_MATPLOTAGENT_RAG_corrector_iterative_error_resolve(dataset_attrubute_fullpath_list_result, full_data_path, model, python_script, error_message, examples_for_query_augmentation)
        
        prompt = source_code_gen_request['prompt']
        prompt='"""'+prompt+'"""'

        source_code_gen_request = json.dumps(source_code_gen_request).encode("utf-8")
        llm_gen_source_code_response = requests.post(URL, data=source_code_gen_request)

        llm_gen_source_code_response  = llm_gen_source_code_response.json()
        print('Raw output: \n', llm_gen_source_code_response)
         
        response_code = utils.extract_python_code_from_response(llm_gen_source_code_response['response'])
        print("\n\nFirst Generated code: \n", response_code)
        
        
        if response_code is not None:            
            regen_response_code = response_code
            if regen_response_code is not None:
                output_file_path = os.path.join(target_dir, f'{base_name}.py')
                # response_code+="\nprint(\"Success_and_End_of_Script!\")"
                # for time recording
                # utils.save_file(output_file_path, response_code)

                utils.save_file(output_file_path, prompt+'\n\n'+response_code)

                # lets save the iterative generated code
                output_file_path = os.path.join(target_dir, f'{base_name}_{iteration}.py')
                utils.save_file(output_file_path, response_code)
                
                # return the newly generated python script path
                print('LLMRequester:: Leaving generate_code_and_save_code_MATPLOTAGENT_RAG_iterative_error_resolve ...')
                return output_file_path, response_code
            else:
                print('LLMRequester:: Leaving generate_code_and_save_code_MATPLOTAGENT_RAG_iterative_error_resolve -->Response code is None')
                return 'None', 'None'
        else:
            print('LLMRequester:: Leaving outer generate_code_and_save_code_MATPLOTAGENT_RAG_iterative_error_resolve-->Response code is None')
            return 'None', 'None'
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_code_and_save_code_MATPLOTAGENT_RAG_iterative_error_resolve, message: ", e)
        return 'None', 'None'

# def generate_code_and_save_with_data_rule_based_reasoning(user_input_file_path, description, dataset_information, data_structure_information, full_data_path, target_dir, model, old_ext='.txt'):
def generate_code_and_save_without_data_zero_shot_CoT(user_input_file_path, user_input_description, full_data_path, target_dir, model, python_script, error_message, iteration, URL, dataset, dataset_attrubute_fullpath_list_result):
    try:
     
        # Create the target directory if it doesn't exist
        print('Target directory: \n', target_dir)
        if not os.path.exists(target_dir):
            print('Target directory not present, created: \n', target_dir)
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension
        # print("base_name = os.path.splitext(user_input_file_path)[0]: ", base_name)
                 
        # current without corrector
        if len(python_script)>0:
            # this is for the iterative error resolving
            # parameters:                                                                                                                            user_input_description, data_structure_information, full_data_path, attribute_present, model, python_script, error_message
            source_code_gen = generate_request_for_generating_source_code_using_LLM_memory_with_zero_shot_CoT_with_corrector_iterative_error_resolve(user_input_description, '',                         full_data_path, '',                model, python_script, error_message)
        else:
            source_code_gen = generate_request_for_generating_source_code_with_zero_shot_CoT_separate_method_step_by_step(user_input_description, full_data_path, model)

        
        prompt = source_code_gen['prompt']
        prompt='"""'+prompt+'"""'

        source_code_gen = json.dumps(source_code_gen).encode("utf-8")
        llm_gen_source_code = requests.post(URL, data=source_code_gen)
        llm_gen_source_code  = llm_gen_source_code.json()
        print('Raw output: \n',llm_gen_source_code)
        # 
        response_code = utils.extract_python_code_from_response(llm_gen_source_code['response'])
        print("\n\nFirst Generated code: \n", response_code)
        
        
        if response_code is not None:
            
            regen_response_code = response_code
            if regen_response_code is not None:
                output_file_path = os.path.join(target_dir, f'{base_name}.py')
  
                utils.save_file(output_file_path, prompt+'\n\n'+response_code)
                if dataset=='ITERATIVE_ERROR_RESOLVE_CLIMATE':
                    # this is for saving all of the generated code for each step
                    # lets save the iterative generated code
                    output_file_path = os.path.join(target_dir, f'{base_name}_{iteration}.py')
                    utils.save_file(output_file_path, response_code)
                
                # return the newly generated python script path
                return output_file_path, response_code
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_code_and_save_without_data_zero_shot_CoT, message: ", e)
        return None, None

# def generate_code_and_save_with_data_rule_based_reasoning(user_input_file_path, description, dataset_information, data_structure_information, full_data_path, target_dir, model, old_ext='.txt'):
def generate_code_and_save_without_data_and_rag_and_SO(user_input_file_path, user_input_description, full_data_path, target_dir, model, python_script, error_message, iteration, URL, dataset, dataset_attrubute_fullpath_list_result, query_augmentation, temperature):
    try:
        print("LLRequestor :: generate_code_and_save_without_data_and_rag_and_SO --> user_input_file_path: ", user_input_file_path)
        print("LLRequestor :: generate_code_and_save_without_data_and_rag_and_SO --> full_data_path: ", full_data_path)

        # Create the target directory if it doesn't exist
        print('Target directory: \n', target_dir)
        if not os.path.exists(target_dir):
            print('Target directory not present, created: \n', target_dir)
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension
                 
        # current without corrector
        source_code_gen_request = {}
        if len(python_script)<=0:
            source_code_gen_request = generate_request_for_generating_source_code_without_rag(user_input_description, full_data_path, model, dataset_attrubute_fullpath_list_result, temperature)
            
        else:            
            # this is for the iterative error resolving
            # parameters:                                                                                                     data_structure_information, full_data_path, model, generated_python_script, error_message, query_augmentation
            source_code_gen_request = generate_request_for_generating_source_code_with_SO_corrector_iterative_error_resolve(dataset_attrubute_fullpath_list_result, full_data_path, model, python_script, error_message, query_augmentation)
 
        prompt = source_code_gen_request['prompt']
        prompt='"""'+prompt+'"""'

        source_code_gen_request = json.dumps(source_code_gen_request).encode("utf-8")
        llm_gen_source_code_response = requests.post(URL, data=source_code_gen_request)
        
        llm_gen_source_code_response  = llm_gen_source_code_response.json()
        print('Raw output: \n',llm_gen_source_code_response)
        # 
        response_code = utils.extract_python_code_from_response(llm_gen_source_code_response['response'])
        print("\n\nFirst Generated code: \n", response_code)
        
        
        if response_code is not None:
            regen_response_code = response_code
            if regen_response_code is not None:
                output_file_path = os.path.join(target_dir, f'{base_name}.py')
    
                utils.save_file(output_file_path, prompt+'\n\n'+response_code)
                if dataset=='ITERATIVE_ERROR_RESOLVE_CLIMATE':
                    # this is for saving all of the generated code for each step
                    # lets save the iterative generated code
                    output_file_path = os.path.join(target_dir, f'{base_name}_{iteration}.py')
                    utils.save_file(output_file_path, response_code)
                
                # return the newly generated python script path
                return output_file_path, response_code
        else:
            print(' LLMRequest.generate_code_and_save_without_data_and_rag_and_SO response code is Null')
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_code_and_save_without_data_and_rag_and_SO, message: ", e)

#                                                                            user_input_file_full_path, user_input_content, output_dir+'/'+output_subdir, model)
def zero_shot_CoT_generate_request_for_generating_intent_attribute_condition(user_input_file_full_path, user_input_content, target_dir, model, URL, old_ext='.txt'):
    try:
        # print("user_input_file_path: ", user_input_file_path)
        # print("dataset_information: ", dataset_information)
        # print("full_data_path: ", full_data_path)

        # Create the target directory if it doesn't exist
        print('Target directory: \n', target_dir)
        if not os.path.exists(target_dir):
            print('Target directory not present, created: \n', target_dir)
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_full_path))[0]  # Get the base file name without extension

        # generate user intent from user queries
        source_code_gen = generate_request_for_generating_intent_attribute_condition(user_input_content, model)
        
        prompt = source_code_gen['prompt']
        prompt='"""'+prompt+'"""'

        source_code_gen = json.dumps(source_code_gen).encode("utf-8")
        llm_gen_source_code = requests.post(URL, data=source_code_gen)
        # llm_gen_source_code= {'response': 'test'}
        # print(llm_gen_source_code)
        llm_gen_source_code  = llm_gen_source_code.json()
        print('Raw output: \n',llm_gen_source_code)
        # 
        response_code = utils.extract_python_code_from_response(llm_gen_source_code['response'])
        print("\n\nFirst Generated code: \n", response_code)
        
        return response_code
        
      
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_code_and_save_without_data_zero_shot_CoT, message: ", e)
        return None


# May 17, 2025
def get_prompt_template_of_sub_queries_based_on_primary_query(user_query, model, temperature):
    query_template = f"""
        You are an assistant designed to break down a complex data science or geospatial analysis task 
        into smaller, focused sub-queries. Each sub-query must target a specific technical domain 
        so that relevant documentation, examples, or code can be retrieved using a vector database.

        Given the user query, return 3 clearly separated sub-queries:

        1. HDF5 Dataset Access:
        Focus only on `h5py` such as accessing file with extensions H5, h5, HE5, he5, HDF5, or hdf5, 
        accessing datasets or attributes, dataset paths (like `/Grid/cloudWater`), and metadata.

        2. NumPy-based Data Preprocessing:
        Focus only on how to handle `_FillValue`, apply masks using NumPy (`np.where`, `np.ma.masked_where`), and compute or filter data using `min`, `max`, or 
        other preprocessing logic.

        3. Map Plotting and Visualization:
        Focus only on how to use `matplotlib`, `mpl_toolkits.basemap`, or `cartopy` to visualize geospatial data, configure projections, draw coastlines, 
        meridians, parallels, and apply colorbars or titles.

        
        User Query:
            {user_query}

        ---
        Note: return only the the response of sub-queries only based on the below format, not explanation, not python code, and node additional text needed
        Return format:

        HDF5 Dataset Access Sub-query:
        <generated sub-query>

        NumPy Data Preprocessing Sub-query:
        <generated sub-query>

        Plotting and Visualization Sub-query:
        <generated sub-query>
        """
    # print("Prompt: \n", query_template)
    
    data = {
        "model": model,
        "prompt": query_template,
        "stream": False,
        # "response_format": "code_only",#this works for openAI only
        "options": {
            "seed": 12344,
            "temperature": temperature
        }
    }
    print("Request with Prompt: \n", data)
    return data

# created May 17, 2025
def generate_multi_agents_request_for_sub_query_generation(user_input_file_full_path, user_input_content, target_dir, model, URL, temperature):
    print(f'LLMRequester::generate_multi_agents_request_for_sub_query_generation: user_input_file_full_path:\n{user_input_file_full_path}')
    print(f'LLMRequester::generate_multi_agents_request_for_sub_query_generation: user_input_content:\n{user_input_content}')
    print(f'LLMRequester::generate_multi_agents_request_for_sub_query_generation: target_dir:\n{target_dir}, model, URL, temperature')
    print(f'LLMRequester::generate_multi_agents_request_for_sub_query_generation: user_input_file_full_path: model: {model}')
    print(f'LLMRequester::generate_multi_agents_request_for_sub_query_generation: URL: {URL}, temperature: {temperature}')

    try:       

        # Create the target directory if it doesn't exist
        print('Target directory: \n', target_dir)
        if not os.path.exists(target_dir):
            print('Target directory not present, created: \n', target_dir)
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_full_path))[0]  # Get the base file name without extension

        # generate user intent from user queries
        user_sub_queries_gen = get_prompt_template_of_sub_queries_based_on_primary_query(user_input_content, model, temperature)
        
        prompt = user_sub_queries_gen['prompt']
        prompt='"""'+prompt+'"""'

        print(f'Sending the post request')
        user_sub_queries_gen = json.dumps(user_sub_queries_gen).encode("utf-8")
        print(f'user_sub_queries_gen:\n{user_sub_queries_gen}')
        llm_user_sub_queries_gen = requests.post(URL, data=user_sub_queries_gen)
        print(f'llm_user_sub_queries_gen:\n{llm_user_sub_queries_gen}')
        
        llm_user_sub_queries_gen  = llm_user_sub_queries_gen.json()
        print('Raw output: \n',llm_user_sub_queries_gen)

        response_llm_user_sub_queries_gen = llm_user_sub_queries_gen['response']
        output_file_path = os.path.join(target_dir, f'{base_name}.txt')
        # create the directory if not exists
        # os.makedirs(output_file_path, exist_ok=True)

        utils.save_file(output_file_path, prompt+'\n\n'+response_llm_user_sub_queries_gen) 

        print("\nGenerated response saved to the directory: \n", output_file_path)

        print("\n\nFirst Generated code: \n", response_llm_user_sub_queries_gen)
        
        # return response_llm_user_sub_queries_gen
        
       
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_multi_agents_request_for_sub_query_generation, message: ", e)



def generate_code_and_save_with_rag(user_input_file_path, user_input_description, examples_for_query_augmentation, full_data_path, target_dir, model, URL, dataset_attrubute_fullpath_list_result, temperature):
    try:
        # Create the target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension
                   
        # this is currently being used for generating final code without LLM memory
        source_code_gen = ''        
        # with corrector
        source_code_gen = generate_request_for_generating_source_code_with_rag(user_input_description, examples_for_query_augmentation, full_data_path, model, dataset_attrubute_fullpath_list_result, temperature)
        
        prompt = source_code_gen['prompt']
        prompt='"""'+prompt+'"""'

        source_code_gen = json.dumps(source_code_gen).encode("utf-8")
        llm_gen_source_code = requests.post(URL, data=source_code_gen)
      
        llm_gen_source_code  = llm_gen_source_code.json()
        print('Raw output: \n',llm_gen_source_code)
        # 
        response_code = utils.extract_python_code_from_response(llm_gen_source_code['response'])
        print("\n\nFirst Generated code: \n", response_code)
        
        output_file_path= ''
        if response_code is not None:           
            regen_response_code = response_code
            if regen_response_code is not None:
                output_file_path = os.path.join(target_dir, f'{base_name}.py')
                utils.save_file(output_file_path, prompt+'\n\n'+response_code)
        
        return output_file_path, response_code        
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_code_and_save_with_rag, message: ", e)
        return None, None


def generate_code_and_save_without_rag(user_input_file_path, user_input_description, full_data_path, target_dir, model, URL, dataset_attrubute_fullpath_list_result, temperature):
    try:
        # Create the target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension
                   
        # this is currently being used for generating final code without LLM memory
        source_code_gen = ''        
        # with corrector  --> user_input, full_data_path, model, dataset_attrubute_fullpath_list_result
        source_code_gen = generate_request_for_generating_source_code_without_rag(user_input_description, full_data_path, model, dataset_attrubute_fullpath_list_result, temperature)
        
        prompt = source_code_gen['prompt']
        prompt='"""'+prompt+'"""'

        source_code_gen = json.dumps(source_code_gen).encode("utf-8")
        llm_gen_source_code = requests.post(URL, data=source_code_gen)
      
        llm_gen_source_code  = llm_gen_source_code.json()
        print('Raw output: \n',llm_gen_source_code)
        # 
        response_code = utils.extract_python_code_from_response(llm_gen_source_code['response'])
        print("\n\nFirst Generated code: \n", response_code)
        
        output_file_path = ''
        if response_code is not None:           
            regen_response_code = response_code
            if regen_response_code is not None:
                output_file_path = os.path.join(target_dir, f'{base_name}.py')
                utils.save_file(output_file_path, prompt+'\n\n'+response_code)
        
        return output_file_path, response_code
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_code_and_save_with_rag, message: ", e)
        return None, None


# created on February 26, 2025
def generate_prompt_for_generating_source_code_with_rag(user_input, examples_code_for_query_augmentation, full_data_path, dataset_attrubute_fullpath_list_result):
    print('Inside generate_request_for_generating_source_code_with_zero_shot_CoT_best_success_manual_plot_saving_with_directory\n')
    
    
    prompt = f"You are an expert Python developer and assistant.\n" 
    prompt+= f"Based on the user's request, generate Python code that accomplishes the task.\n" 
    prompt+= f"Use the structure and logic from similar examples if provided.\n" 
    prompt+= f"Include detailed comments in the code to explain each step clearly:\n"
    prompt+= f"Set the input data file path from the mentioned FULL_DATA_PATH= {full_data_path}\n"
    prompt+= f"### User Query:\n"
    prompt+= f"{user_input}"
        
    if len(dataset_attrubute_fullpath_list_result)>0:
        prompt+=f"\nWhile acessing datasets and attributes have a look on the list below:\n"
        prompt+="###Dataset and Attribute paths:\n"
        prompt+=f"{dataset_attrubute_fullpath_list_result}"
        
    prompt+= f"\nFinally, the generated python script should save the plotted file with the same base name from FULL_DATA_PATH and also to the same directory as FULL_DATA_PATH with .png extention\n"
    prompt+= "Note: Send only the code, no explanations or additional text.\n"
    
    augmentation = ''
    if len(examples_code_for_query_augmentation)>0:
        augmentation= "### Related Examples for Augmentation:\n"
        augmentation+= f"{examples_code_for_query_augmentation}"
        
    prompt+=augmentation
    return prompt

def generate_request_for_generating_source_code_with_rag(user_input, examples_code_for_query_augmentation, full_data_path, model, dataset_attrubute_fullpath_list_result, temperature):    
    print('Inside generate_request_for_generating_source_code_with_rag\n\n')    
    prompt = generate_prompt_for_generating_source_code_with_rag(user_input, examples_code_for_query_augmentation, full_data_path, dataset_attrubute_fullpath_list_result)
    
    print("Prompt: \n", prompt)
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "seed": 12344,
            "temperature": temperature
        }
    }
    return data


# created on Jun 07, 2025
def generate_prompt_for_generating_source_code_without_rag(user_input, full_data_path, dataset_attrubute_fullpath_list_result):
    print('Inside generate_request_for_generating_source_code_with_zero_shot_CoT_best_success_manual_plot_saving_with_directory\n')
    
    prompt = f"You are an expert Python developer and assistant.\n" 
    prompt+= f"Based on the user's request, generate Python code that accomplishes the task.\n" 
    prompt+= f"Use the structure and logic from similar examples if provided.\n" 
    prompt+= f"Include detailed comments in the code to explain each step clearly:\n"
    prompt+= f"Set the input data file path from the mentioned FULL_DATA_PATH= {full_data_path}\n"
    prompt+= f"### User Query:\n"
    prompt+= f"{user_input}"

    if len(dataset_attrubute_fullpath_list_result)>0:
        prompt+=f"\nWhile acessing datasets and attributes have a look on the list below:\n"
        prompt+="###Dataset and Attribute paths:\n"
        prompt+=f"{dataset_attrubute_fullpath_list_result}"
    
    prompt+= f"\nFinally, the generated python script should save the plotted file with the same base name from FULL_DATA_PATH and also to the same directory as FULL_DATA_PATH with .png extention\n"
    prompt+= "Note: Send only the code, no explanations or additional text.\n"
    
    return prompt

def generate_request_for_generating_source_code_without_rag(user_input, full_data_path, model, dataset_attrubute_fullpath_list_result, temperature):    
    print('Inside generate_request_for_generating_source_code_without_rag...\n\n')    
    
    prompt = generate_prompt_for_generating_source_code_without_rag(user_input, full_data_path, dataset_attrubute_fullpath_list_result)
    
    print("Prompt: \n", prompt)
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "seed": 12344,
            "temperature": temperature
        }
    }
    return data

def generate_code_and_save_VTK_related_python_scripts_without_rag(user_input_file_path, user_input_description, full_data_path, target_dir, model, URL, dataset_attrubute_fullpath_list_result):
    try:
        # Create the target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_path))[0]  # Get the base file name without extension
                   
        # this is currently being used for generating final code without LLM memory
        source_code_gen = ''        
        # with corrector  --> user_input, full_data_path, model, dataset_attrubute_fullpath_list_result
        source_code_gen = generate_request_for_generating_vtk_related_python_scripts_without_rag(user_input_description, full_data_path, model, dataset_attrubute_fullpath_list_result)
        
        prompt = source_code_gen['prompt']
        prompt='"""'+prompt+'"""'

        source_code_gen = json.dumps(source_code_gen).encode("utf-8")
        llm_gen_source_code = requests.post(URL, data=source_code_gen)
      
        llm_gen_source_code  = llm_gen_source_code.json()
        print('Raw output: \n',llm_gen_source_code)
        # 
        response_code = utils.extract_python_code_from_response(llm_gen_source_code['response'])
        response_code = utils.remove_heading_space_first_line(response_code)
        print("\n\nFirst Generated code: \n", response_code)
        
        
        if response_code is not None:           
            regen_response_code = response_code
            if regen_response_code is not None:
                output_file_path = os.path.join(target_dir, f'{base_name}.py')
                utils.save_file(output_file_path, prompt+'\n\n'+response_code)

                output_file_path_without_ite = os.path.join(target_dir, f'{base_name}_0.py')
                utils.save_file(output_file_path_without_ite, response_code)

                return output_file_path, response_code
            
        return 'None', 'None'
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_code_and_save_VTK_related_python_scripts_without_rag, message: ", e)
        return None, None



def generate_request_for_generating_vtk_related_python_scripts_without_rag(user_input, full_data_path, model, dataset_attrubute_fullpath_list_result):    
    print('Inside generate_request_for_generating_vtk_related_python_scripts_without_rag ...\n\n')    
        
    prompt = f"You are an expert Python developer. A simplified user query will be provided below that describes the functionality of a Python script in plain English.\n" 
    prompt+= f"Your task is to:\n" 
    prompt+= f" 1. Generate the full Python script based on this description.\n" 
    prompt+= f" 2. Use appropriate libraries and logic to implement what the query describes.\n"
    prompt+= f" 3. Ensure that the script, if it involves rendering or visual output, saves the rendering result as a PNG file with the same provided data file base name in the current directory where the script is run.\n"
    prompt+= f" 4. The script should be ready to run, with no placeholder code or missing components.\n"
    prompt+= f"### User Query:\n"
    prompt+= f" {user_input}"  
    
    prompt+= f"\nNow generate a complete Python script that fulfills this query and includes the step that saves the rendering result as an image file with the same provided data file base name in the current directory.\n"
    
    print("Prompt: \n", prompt)
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "seed": 12344,
            "temperature": 0.0
        }
    }
    return data


# created June 24, 2025
def generate_request_for_VTK_related_user_query_generation(user_input_file_full_path, user_input_content, target_dir, model, URL, is_errors):
    try:   

        # Create the target directory if it doesn't exist
        print('Target directory: \n', target_dir)
        if not os.path.exists(target_dir):
            print('Target directory not present, created: \n', target_dir)
            os.makedirs(target_dir)
            
        # Change the extension
        base_name = os.path.splitext(os.path.basename(user_input_file_full_path))[0]  # Get the base file name without extension

        # generate user intent from user queries
        user_sub_queries_gen = ''
        if is_errors == False:
            user_sub_queries_gen = get_prompt_template_of_VTK_related_expert_user_queries_based_on_python_scripts(user_input_content, model)
        else:
            # user_sub_queries_gen = get_prompt_template_of_VTK_related_simple_user_queries_based_on_python_scripts(user_input_content, model)
            user_sub_queries_gen = get_prompt_template_of_VTK_related_simple_user_queries_based_on_expert_user_queries(user_input_content, model)
        
        prompt = user_sub_queries_gen['prompt']
        prompt='"""'+prompt+'"""'

        user_sub_queries_gen = json.dumps(user_sub_queries_gen).encode("utf-8")
        llm_user_sub_queries_gen = requests.post(URL, data=user_sub_queries_gen)
        
        llm_user_sub_queries_gen  = llm_user_sub_queries_gen.json()
        print('Raw output: \n',llm_user_sub_queries_gen)

        response_llm_user_sub_queries_gen = llm_user_sub_queries_gen['response']
        output_file_path = os.path.join(target_dir, f'{base_name}.txt')
        utils.save_file(output_file_path, response_llm_user_sub_queries_gen) 
        
        print("\n\nFirst Generated User Query: \n", response_llm_user_sub_queries_gen)
        
        # return response_llm_user_sub_queries_gen
        
       
    except Exception as e:
        print("Exception occurred at LLMRequest.generate_multi_agents_request_for_sub_query_generation, message: ", e)

# June 24, 2025
def get_prompt_template_of_VTK_related_expert_user_queries_based_on_python_scripts(python_script, model):
    query_template = f"Describe the following Python script in a clear, human-written, step-by-step style."
    query_template+= "The description must include:\n"
    query_template+= "  - The exact names of the Python libraries to be imported\n"
    query_template+= "  - The exact file name(s) or path(s) that should be defined\n"
    query_template+= "  - The exact variable and object names used in the code\n"
    query_template+= "  - A breakdown of what each step does\n"
    query_template+= "Do not include any explanations, comments, or the original code. Return only the description, written like human documentation for someone who needs to reproduce the same script later.\n"
    query_template+= f"\n   Python Script:\n{python_script}\n"
      
    print("Prompt: \n", query_template)
    
    data = {
        "model": model,
        "prompt": query_template,
        "stream": False,
        # "response_format": "code_only",#this works for openAI only
        "options": {
            "seed": 12344,
            "temperature": 0.0
        }
    }
    return data

# June 24, 2025
def get_prompt_template_of_VTK_related_simple_user_queries_based_on_python_scripts(python_script, model):
    
    query_template = f"You are a helpful assistant tasked with explaining what a Python script does in simple, everyday language for someone with no programming experience.\n"

    query_template+= " Given the script, write a detailed explanation that:\n"
    query_template+= "  - Clearly describes the purpose of the script.\n"
    query_template+= "  - Explains each part of what the script does step by step, as if you're walking someone through how the process works in real life.\n"
    query_template+= "  - Avoids all technical terms: do not mention any library, function, or programming concept by name.\n"
    query_template+= "  - Focuses on the actions being done (e.g., \"It goes through a list\", \"It checks if something is missing\", \"It keeps track of certain values\", etc.).\n"
    query_template+= "  - Describes the flow of the logic, including how the data is handled, processed, filtered, or summarized.\n"
    query_template+= "  - Uses plain, conversational language while still being complete and specific.\n"
    query_template+= f"\n   Python Script:\n{python_script}\n"

    query_template+= " Your explanation should fully describe the methodology and behavior of the script in a way that is understandable to someone who is curious about what the script does but has never written a line of code.\n" 
      
    print("Prompt: \n", query_template)
    
    data = {
        "model": model,
        "prompt": query_template,
        "stream": False,
        # "response_format": "code_only",#this works for openAI only
        "options": {
            "seed": 12344,
            "temperature": 0.0
        }
    }
    return data


def get_prompt_template_of_VTK_related_simple_user_queries_based_on_expert_user_queries(expert_user_query, model):
    query_template = f"You will be given a detailed explanation of a Python script. Your task is to rewrite this explanation into a more concise version—about 80% of the original length—while preserving key functional insights.\n"

    query_template+= " You must:\n"

    query_template+= " 1. Summarize overly detailed technical information (e.g., full library import chains, function argument structures, intermediary transformation details) into high-level explanations.\n"
    query_template+= " 2. Preserve and explicitly mention** the following elements without abstraction:\n"
    query_template+= "  - The exact data file name(s) mentioned (e.g., `.3ds`, `.mhd`, `.vtk`, `.pgm`, `.vtp`)\n"
    query_template+= "  - The camera position, focal point, view direction, or any visualization-specific settings\n"
    query_template+= "  - Any rendering/visualization step (e.g., use of background colors, camera resets, render window updates)\n"
    query_template+= " 3. Describe the goal and methodology of the code clearly, maintaining its original logic.\n"
    query_template+= " 4. Avoid listing exact library names or class names unless they are central to understanding.\n"
    query_template+= " ### Example Input:\n"
    query_template+= f" {expert_user_query}\n"
    query_template+= " ### Output Instructions:\n"
    query_template+= " Return the rewritten version in natural language. Do not include any code. Keep the explanation accurate but more concise." 
    query_template+= " Use clear and coherent language to explain how the script works at a high level while focusing on what it does rather than how every component is wired internally.\n"

    print("Prompt: \n", query_template)
    
    data = {
        "model": model,
        "prompt": query_template,
        "stream": False,
        # "response_format": "code_only",#this works for openAI only
        "options": {
            "seed": 12344,
            "temperature": 0.0
        }
    }
    return data