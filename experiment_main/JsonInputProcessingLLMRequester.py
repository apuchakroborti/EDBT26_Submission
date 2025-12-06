import os
import requests
import json
# from . import Utils as utils

# URL = 'http://localhost:11434/api/generate'
URL = 'http://ai-lab2.dyn.gsu.edu:11434/api/generate'


# def generate_request_for_generating_source_code(sample, model="llama3:70b"):
# latest means 8b
# gpt-3.5-turbo


# Zero-Shot Chain of thought
# copied from original LLMRrequestor
def generate_request_for_generating_source_code_with_zero_shot_CoT_with_corrector(user_input, data_structure_information, full_data_path, attribute_present, model):
    # s = "Generate the python code based on the DESCRIPTION, read the input data path from FULL_DATA_PATH, also where generating code based on the DESCRIPTION set the group, dataset, "
    
    s = "Generate the python code and add the code inside ```python ``` based on the description below: \n"+user_input+"\n"
    s+="#Follow the instructions step by step:\n"
    # s+="do import the library h5py for the FULL_DATA_PATH with extensions .HDF5, .hdf5, .h5, .H5, .he5, or .HE5 \n"
    s+="do import the library h5py as this programs need to read HDF5, .hdf5, .h5, .H5, .he5, or .HE5 data\n"
    s+="set the input data file path from FULL_DATA_PATH="+full_data_path+"\n"
    if attribute_present:
        s+="Do not set or access any dataset by assumption, set datasets paths only from the below available comma separated datasets and attributes added using a tab space in the following line:\n"+ data_structure_information+"\n"
    else:
        s+="Do not set or access any dataset by assumption, set datasets paths only from the below available comma separated datasets information:\n"+ data_structure_information+"\n"
    s+='save the output plot file to the same directory as FULL_DATE_PATH with .png extention\n'

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

def generate_request_for_generating_source_code_with_zero_shot_CoT_without_corrector(user_input, full_data_path, model):
    # s = "Generate the python code based on the DESCRIPTION, read the input data path from FULL_DATA_PATH, also where generating code based on the DESCRIPTION set the group, dataset, "
    
    s = "Generate the python code and add the code inside ```python ``` based on the description below: \n"+user_input+"\n"
    s+="#Follow the instructions step by step:\n"
    s+="do import the library h5py for the FULL_DATA_PATH with extensions .HDF5, .hdf5, .h5, .H5, .he5, or .HE5 \n"
    s+="set the input data file path from FULL_DATA_PATH="+full_data_path+"\n"
    # s+="take help while setting datasets paths from the below information:\n"+ data_structure_information+"\n"
    s+='save the output plot file to the same directory as FULL_DATE_PATH with .png extention\n'

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



# copied from original LLMRrequestor
def generate_request_for_generating_source_code_with_data_rule_base_reasoning_copied(user_input, data_structure_information, full_data_path, model):
    # s = "Generate the python code based on the DESCRIPTION, read the input data path from FULL_DATA_PATH, also where generating code based on the DESCRIPTION set the group, dataset, "
    s = "Generate the python code and add the code inside ```python ``` based on the DESCRIPTION, set the input data file path from FULL_DATA_PATH"
    s +="\n set the group, dataset, or attribute paths from the data_set_attribute_information by matching which one you required "
    s +=" do import the library h5py for the FULL_DATA_PATH with extensions HDF5, hdf5, h5, H5, he5, or HE5 "
    s+='\naccess atribute mention by following convention mention in ATTRBITE_READ section, if any attribute path not found do not set any incorrect paths by assumptions\n'
    # current working
    # s+='\nAlso while reading attribute follow the convention mentioned in the ATTRBITE_READ section, if any attribute path not found no path should be assumed, just find alternative way\n'
    # s+="\nMoreover, Don't read any dataset and attribute which not required for the plotting\n"
    s+="\nALso, while setting dataset and attributes first first verify if it is present in the ndata_set_attribute_information\n"
    s+='\n The output plot file should be the same as FULL_DATE_PATH just with png extentions\n'

    s +="\nDESCRIPTION=\n"+user_input
    # s +='\n Add this data directory path below to run the above code. '
    s +=  "\nFULL_DATA_PATH= \n"+ full_data_path
    s+="\ndata_set_attribute_information= \n"+data_structure_information

    # s+= "\ndo import h5py library if the program needs to read data with extensions HDF5, hdf5, h5, H5, he5, and HE5."
    # s +=  "\nAlso Please use the following dataset paths to set the paths correctly: \n"+dataset_information
    # s += "\nWhile reading groups and dataset information from data this hierarchical structure should be analyzed to set the paths: \n"+data_structure_information
    # + "\n Make sure the input file can be specified as a command line parameter by importing and utilizing the sys module."
    # to reduce the input path list
    # s += "\nWhile reading groups and dataset information from data this hierarchical structure should be analyzed to set the paths, the list inside curly brace are dataset attributes: \n"+data_structure_information
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


def form_request_to_generate_code_from_text(sample, model="deepseek-coder-v2"):
    print('Model: ', model)
    s = "Generate Python code according to the description mentioned in INPUT and add the python code inside ```python  ```."
    s+="\nassume mentioned every column name as dataset name from hdf5, h5, or he5 data"    
    s+="\nINPUT=\n"+sample
   
    print('Prompt: \n', s)
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



def generate_request_convert_text_input_to_human_generated_and_add_external_data_path(sample, model="gpt-3.5-turbo"):
    s = "Please convert the below text INPUT into human generated text."
    s+="\nAnd instead of reading data from static arrays, it should ask to read data from a file named '/Users/apukumarchakroborti/gsu_research/llam_test/ACL_DIRS/ASF/SMAP_L1C_S0_HIRES_02298_A_20150707T160502_R13080_001.h5'"
    s+="\nThe dataset should be 'Sigma0_Data/cell_sigma0_hh_fore'"
    s+="\nINPUT=\n"+sample
   
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


def generate_request_for_generating_source_code_of_ploting_with_data(sample, model="gpt-3.5-turbo"):
    s = "Generate the python code based on the following description: \n" + sample
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


