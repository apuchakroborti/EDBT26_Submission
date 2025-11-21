"""
To handle errors during Python script execution from another script, categorize them, 
and save the error information into a CSV file for later analysis and graph generation, you can follow these steps:

---

### Plan
1. **Run the Target Script**:
   Use `subprocess` or similar libraries to run the target Python script and capture its output, including errors.

2. **Parse Errors**:
   Match errors in the captured output against predefined categories using regular expressions.

3. **Save to CSV**:
   Save the categorized errors along with additional metadata like timestamp and script name.

4. **Generate Graphs**:
   Use libraries like `matplotlib` or `seaborn` to visualize the error frequency per category.

---

### Code Example

```python
"""
import subprocess
import re
import csv
import os
from datetime import datetime
import time
from common_util_script import ArgumentParser as argumentParsar

import argparse
from common_util_script import Utils as utils

import glob
import re
import os
import pandas as pd
from pathlib import Path

# Error categorization mapping
ERROR_CATEGORIES = {
    "Dataset related error": [
        r"KeyError: .*Unable to open object",
        r"ValueError: Invalid location identifier",
    ],
    "Attribute related error": [
        r"AttributeError: 'numpy\.ndarray'",
        r"KeyError: .*Can't open attribute",
        r"TypeError: masked_invalid\(\) got an unexpected keyword argument 'fill_value'",
        r"AttributeError: 'NoneType' object has no attribute 'set_ylim'",
        r"AttributeError: 'NoneType' object has no attribute *",
        r"Unable to synchronously open attribute (can't locate attribute: 'LongName')",
        r"Unable to synchronously open object",
        r"AttributeError: 'str' object has no attribute 'decode'."
    ],
    "Slicing error": [
        r"TypeError: Dimensions of C",
        r"TypeError: Dimensions of C Other Error",
        r"ValueError: RGBA sequence should have length 3 or 4", 
        r"ValueError: 'c' argument", 
        r"ValueError: not enough values to unpack", 
        r"ValueError: x and y must have same first dimension",
        r"ValueError: Illegal slicing argument for scalar dataspace", 

    ],
    "Other Error": [
        r"IndexError",
        r"FileNotFoundError",
        r"ValueError: cannot convert float NaN to integer",
       
    ]
}

# Function to categorize errors
def categorize_error(error_message):
    for category, patterns in ERROR_CATEGORIES.items():
        for pattern in patterns:
            if re.search(pattern, error_message):
                return category
    return "Uncategorized Error"

# created on Nov 17, 2024
# Function to categorize errors
def conditional_categorize_error(error_message):
    print(f'Primary Error message is:\n{error_message}')
    error_message = error_message.replace("Standard output is: An error occurred: ", "")
    error_message = error_message.replace("Standard output is: Error: Key not found in HDF5 file:", "")
    error_message = error_message.replace("Standard output is: Error: Dataset or attribute not found: ", "")
    error_message = error_message.replace("Standard output is: Error reading HDF5 file: ", "")
    error_message = error_message.replace("Standard output is: An unexpected error occurred: ", "")
    print(f'New Error message is:\n{error_message}')

    if (error_message.startswith('KeyError: \"Unable to open object') or
        error_message.startswith('KeyError: \'Unable to synchronously open object') or
        error_message.startswith('KeyError: Unable to synchronously open object') or
        error_message.startswith('KeyError: \'Unable to open object') or  
        error_message.startswith('ValueError: Invalid location identifier') or
        error_message.startswith('NameError: name') or
        error_message.startswith('KeyError: \'/TIME\'') or
        error_message.startswith('KeyError: \"Unable to synchronously open object (object') or
        error_message.startswith('KeyError: \'Unable to synchronously open object (message type not found)\'') or
        error_message.startswith('KeyError: Unable to synchronously open object (message type not found)') or
        error_message.startswith('KeyError: \"Unable to synchronously open object (object \'data\' doesn\'t exist)\"') or
        error_message.startswith('KeyError: \"Unable to synchronously open object (object \'lat\' doesn\'t exist)\"') or
        error_message.startswith('KeyError: \"Unable to synchronously open object (object') or
        error_message.startswith('KeyError: \"Unable to synchronously open object (object \'RetrievedSignal\' doesn\'t exist)\"') or
        error_message.startswith('ValueError: SST dataset not found in HDF5 file') or
        error_message.startswith('Standard output is: An error occurred: \"Unable to synchronously open object (object') or
        error_message.startswith('Standard output is: An error occurred: Unable to synchronously open object (object') or  
        error_message.startswith('An error occurred: \'Unable to synchronously open object (component not found)\'') or
        error_message.startswith('An error occurred: Unable to synchronously open object (component not found)') or
        error_message.startswith('KeyError: Unable to synchronously open object (component not found)') or
        error_message.startswith('Standard output is: Error: Could not find latitude and longitude data in HDF5 file') or
        error_message.startswith('Could not extract latitude and longitude data. Plotting skipped.') or
        error_message.startswith('Error: \"Dataset \'/sm\' not found.\"') or
        error_message.startswith('Standard output is: The \'Lst\' dataset was not found in the L2 file.')
        
        ):
        
        print('\nError Category: ', 'Dataset_Paths_Related_Error_Count')
        print('Error Message: ', error_message)

        return 'Dataset_Paths_Related_Error_Count', 'Datasets_Paths_Related_Error_messages', error_message
    
    elif (  error_message.startswith('AttributeError: \'numpy.ndarray\'') or
            error_message.startswith('AttributeError:') or
            error_message.startswith('Standard output is: Data field not found in the file') or          
            error_message.startswith('KeyError: \"\"Can\'t open attribute') or 
            error_message.startswith('KeyError: \"Can\'t open attribute') or 
            error_message.startswith('TypeError: masked_invalid() got an unexpected keyword argument \'fill_value\'') or
            error_message.startswith('AttributeError: \'int\' object has no attribute \'decode\'') or
            error_message.startswith('AttributeError: \'Dataset\' object has no attribute \'value\'') or
            error_message.startswith('AttributeError: PathCollection.set()') or
            error_message.startswith('AttributeError: \'NoneType\' object has no attribute') or
            error_message.startswith('Unable to synchronously open attribute (can\'t locate attribute:') or
            error_message.startswith('KeyError: "Unable to synchronously open attribute (can\'t locate attribute:') or
            error_message.startswith('AttributeError: \'int\' object has no attribute \'decode\'') or
            error_message.startswith('AttributeError: \'str\' object has no attribute \'decode\'.') or 
            error_message.startswith('KeyError: \'_FillValue\'') or
            error_message.startswith('\'numpy.ndarray\' object has no attribute \'attrs\'') or
            error_message.startswith('AttributeError: \'numpy.ndarray\' object has no attribute \'attrs\'') or

            error_message.startswith('\'numpy.ndarray\' object has no attribute \'attrs\'') or
            error_message.startswith('\'numpy.ndarray\' object has no attribute \'attrs\'') or
            error_message.startswith('\'numpy.ndarray\' object has no attribute \'attrs\'') or
            error_message.startswith('\'numpy.ndarray\' object has no attribute \'attrs\'') 
          ):
        
        print('\nError Category: ', 'Attribute_Related_Error_Count')
        print('Error Message: ', error_message)

        return 'Attribute_Related_Error_Count', 'Attribute_Related_Error_messages', error_message
    
    elif (error_message.startswith('TypeError: Dimensions of C') or 
          error_message.startswith('TypeError: Dimensions of C Other Error') or 
          error_message.startswith('ValueError: RGBA sequence should have length 3 or 4') or
          error_message.startswith('ValueError: \'c\' argument') or
          error_message.startswith('ValueError: not enough values to unpack') or
          error_message.startswith('ValueError: x and y must have same first dimension') or
          error_message.startswith('ValueError: Illegal slicing argument for scalar dataspace') or
          error_message.startswith('ValueError: x and y must be the same size') or 
          error_message.startswith('TypeError: Length of x (36) must match number of columns in z (21)') or
          error_message.startswith('IndexError: too many indices for array: array is 1-dimensional, but 2 were indexed') or
          error_message.startswith('ValueError: not enough values to unpack (expected 2, got 1)') or
          error_message.startswith('TypeError: Length of y (11) must match number of rows in z (72)') or
          error_message.startswith('TypeError: Invalid shape (138434,) for image data') or
          error_message.startswith('KeyError: \'Unable to synchronously open object (component not found)\'') or
          error_message.startswith('ValueError: not enough values to unpack') or
          error_message.startswith('TypeError: Invalid shape') or
          error_message.startswith('TypeError: Invalid shape (8, 1440, 2880) for image data') or
          error_message.startswith('TypeError: Invalid shape (17137,) for image data') or
          error_message.startswith('An error occurred: c argument has')
          ):
        
        print('\nError Category: ', 'Slicing_Related_Error_Count')
        print('Error Message: ', error_message)
        
        return 'Slicing_Related_Error_Count', 'Slicing_Related_Error_messages', error_message
    elif (error_message.startswith('IndexError') or 
          error_message.startswith('FileNotFoundError') or 
          error_message.startswith('ValueError: cannot convert float NaN to integer') or
          error_message.startswith('NameError: name \'h5py\' is not defined') or
          error_message.startswith('IndexError: index ')
        ):

        print('\nError Category: ', 'Other_Errors_Count')
        print('Error Message: ', error_message)
        
        return 'Other_Errors_Count', 'Other_Errors_messages', error_message
    else:
        
        print('\nError Category: ', 'Other_Errors_Count')
        print('Error Message: ', error_message)
        
        return 'Other_Errors_Count', 'Other_Errors_messages', error_message

# created NOv 17, 2024
# Function to run a script and capture its errors
def run_script(script_path):
    try:
        # Run the script and capture stdout and stderr
        result = subprocess.run(
            ["python", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)

# created earlier
def run_python_script(script_path, output_subdir, dataset_name):
    print('Evaluation:: run_python_script ...')
    # TODO need to investigate why this function not status and error properly
    """
    Runs a Python script with the specified HDF5 file as an argument.
    
    Args:
        script_path (str): Path to the Python script.
        data_file (str): Path to the HDF5 file.
    
    Returns:
        tuple: (status, error_message) where status is 'Pass' or 'Fail', and error_message is the error string or None.
    """
    try:
        # Run the Python script with the HDF5 file as an argument
        # result = subprocess.run(['python3', script_path, data_file], check=True, capture_output=True, text=True)
        result = subprocess.run(['python3', script_path], check=True, capture_output=True, text=True, timeout=120)
        # need to check if the image is generated and save in the directory
        script_base_name = os.path.basename(script_path)
        # image_data_file = script_path[0, len(script_base_name)-3]
        image_data_file =script_base_name.replace('.py', '')

        png_files = glob.glob(os.path.join(os.path.dirname(script_path), "*.png"))
        print(f'Evaluation:: run_python_script:: png files from script directory:\n{png_files}')
        if png_files is None:
            png_files = []    
        


        image_found = False
        if dataset_name == 'CLIMATE':
             # collecting and storing png files 
            data_dir_base_path = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
            target_dir_base_path = f"{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag"    
    
            subdirectories = [  f'{data_dir_base_path}/ACL_DIRS/ASF',
                            f'{data_dir_base_path}/ACL_DIRS/AURA_DATA_VC',
                            f'{data_dir_base_path}/ACL_DIRS/GES_DISC',
                            f'{data_dir_base_path}/ACL_DIRS/ICESat_2',
                            f'{data_dir_base_path}/ACL_DIRS/LAADS',
                            f'{data_dir_base_path}/ACL_DIRS/LaRC',
                            f'{data_dir_base_path}/ACL_DIRS/LP_DAAC',
                            f'{data_dir_base_path}/ACL_DIRS/NSIDC',
                            f'{data_dir_base_path}/ACL_DIRS/PO_DAAC',
                            f'{data_dir_base_path}',
                            f'{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting'
                        ]
            # source_dirs, script_execution_base_path, target_dir_base_path, new_dir_name
            new_dir_name = 'iterative_'+output_subdir
            utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name)
            # should be updated
            # data_directory = f'/Users/apukumarchakroborti/gsu_research/adm_research_spring_2025/llms_generated_python_scripts/error_categorization_report/generated_image_from_running_evaluation/{new_dir_name}'
            data_directory = f'/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag/generated_image_from_running_evaluation/{new_dir_name}'
        
        
            print('Data Directory: \n', data_directory)
        
            png_files_from_main_script_dir = glob.glob(os.path.join(data_directory, "*.png"))
            print(f'Evaluation:: run_python_script:: png files:\n{png_files_from_main_script_dir}')
            # collecting and storing png files end
            if png_files_from_main_script_dir is not None and len(png_files_from_main_script_dir)>0:
                png_files.extend(png_files_from_main_script_dir)
            
            image_data_file_length = len(image_data_file)
            image_data_file = image_data_file[0:image_data_file_length//2]
            print(f'Half file name: {image_data_file}')

            if len(png_files)>0:
                for file in png_files:
                    if os.path.basename(file).startswith(image_data_file):
                        print(f'Image Found for: {image_data_file}')
                        image_found = True
                        return 'Pass', ''
                else:
                    print(f'No image found witht the name: {image_data_file}')
        elif dataset_name == 'MATPLOTAGENT':
            new_dir_name = output_subdir
            data_dir_base_path = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
            target_dir_base_path = f"{data_dir_base_path}/matplot_agent_data/plot_generation/error_categorization_evaluation_result"    
    
            subdirectories = [      
                        f'{data_dir_base_path}/matplot_agent_data/plot_generation/csv_to_h5_data',
                        f'{data_dir_base_path}',
                        f'{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting'
            ]
            utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, 'iterative_'+new_dir_name)
            data_directory = f'{data_dir_base_path}/matplot_agent_data/plot_generation/error_categorization_evaluation_result/generated_image_from_running_evaluation/iterative_{new_dir_name}'
            print('Data Directory: \n', data_directory)
            png_files_from_main_script_dir = glob.glob(os.path.join(data_directory, "*.png"))    
            print('MATPLOTAGENT All PNG files: \n', png_files_from_main_script_dir)

            png_files_only_file_name = []
            if len(png_files_from_main_script_dir)>0:
                for file in png_files_from_main_script_dir:
                    names = file.split('/')
                    png_files_only_file_name.append(names[len(names)-1])
            print('MATPLOTAGENT All PNG files with only file names: \n', png_files_only_file_name)

            image_data_file_length = len(image_data_file)
            image_data_file_name_split = image_data_file.split('_') 
            image_data_file_name_prefix = image_data_file_name_split[0]
            print(f'Image number: {image_data_file}')
            print(f'Image prefix number: {image_data_file_name_prefix}')

            # Check if the image is found   
            if len(png_files_only_file_name)>0:
                for file in png_files_only_file_name:
                    if file.startswith(image_data_file_name_prefix):
                        print(f'Image Found for prefix number: {image_data_file_name_prefix}')
                        image_found = True
                        return 'Pass', None
                else:
                    print(f'No image found witht the name: {image_data_file}')

            
        elif dataset_name == 'FASTMRIBRAIN':
            new_dir_name = 'iterative_'+output_subdir
            data_dir_base_path = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
            target_dir_base_path = f"{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag"    
    
            subdirectories = [  f'{data_dir_base_path}/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5',
                            f'{data_dir_base_path}',
                            f'{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting'
                        ]
            # source_dirs, script_execution_base_path, target_dir_base_path, new_dir_name
            utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name)
            # should be updated
            # data_directory = f'/Users/apukumarchakroborti/gsu_research/adm_research_spring_2025/llms_generated_python_scripts/error_categorization_report/generated_image_from_running_evaluation/{new_dir_name}'
            data_directory = f'/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag/generated_image_from_running_evaluation/{new_dir_name}'
    
            print('Data Directory: \n', data_directory)
    
            png_files_from_main_script_dir = glob.glob(os.path.join(data_directory, "*.png"))
    
    
            print('All PNG files: \n', png_files_from_main_script_dir)
            png_files_only_file_name = []
            if len(png_files_from_main_script_dir)>0:
                for file in png_files_from_main_script_dir:
                    names = file.split('/')
                    png_files_only_file_name.append(names[len(names)-1])
            print('All PNG files with only file names: \n', png_files_only_file_name)            
            
            
            image_data_file_length = len(image_data_file)
            image_data_file_name_split = image_data_file.split('_') 
            image_data_file_name_prefix = image_data_file_name_split[0]
            print(f'Image number: {image_data_file}')
            print(f'Image prefix number: {image_data_file_name_prefix}')

            if len(png_files_only_file_name)>0:
                for file in png_files_only_file_name:
                    if file.startswith(image_data_file_name_prefix):
                        print(f'Image Found for prefix number: {image_data_file_name_prefix}')
                        image_found = True
                        return 'Pass', None
                else:
                    print(f'No image found witht the name: {image_data_file}')
        
        elif dataset_name == 'VTK' :
            new_dir_name = output_subdir
            data_dir_base_path = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
            target_dir_base_path = f"{data_dir_base_path}/vtk_python_scripts_experiment/error_categorization_evaluation_result"    
            python_script_dir = os.path.dirname(script_path)
            subdirectories = [   
                            f'{python_script_dir}',
                            f'{data_dir_base_path}',
                            f'{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting'
                    ]
            # source_dirs, script_execution_base_path, target_dir_base_path, new_dir_name
            utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, 'iterative_'+new_dir_name)
            # should be updated
            # data_directory = f'/Users/apukumarchakroborti/gsu_research/adm_research_spring_2025/llms_generated_python_scripts/error_categorization_report/generated_image_from_running_evaluation/{new_dir_name}'
            data_directory = f'/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/vtk_python_scripts_experiment/error_categorization_evaluation_result/generated_image_from_running_evaluation/iterative_{new_dir_name}'
            print('Data Directory: \n', data_directory)
    
            png_files_from_main_script_dir = glob.glob(os.path.join(data_directory, "*.png"))
            png_files_only_file_name = []

            if len(png_files_from_main_script_dir)>0:
                for file in png_files_from_main_script_dir:
                    names = file.split('/')
                    png_files_only_file_name.append(names[len(names)-1])
            print('All PNG files with only file names: \n', png_files_only_file_name)  

            image_data_file_length = len(image_data_file)
            image_data_file_name_split = image_data_file.split('_') 
            image_data_file_name_prefix = image_data_file_name_split[0]
            print(f'Image number: {image_data_file}')
            print(f'Image prefix number: {image_data_file_name_prefix}')

            if len(png_files_only_file_name)>0:
                for file in png_files_only_file_name:
                    if file.startswith(image_data_file_name_prefix):
                        print(f'Image Found for prefix: {image_data_file_name_prefix}')
                        image_found = True
                        return 'Pass', None
                else:
                    print(f'No image found witht the name: {image_data_file}')

        if image_found==False:
            print('No Image')
            message = ''
            if result.stdout:
                message+="Standard output is: "+result.stdout+"\n"
            if result.stderr:
                message+="Standard error is: "+result.stderr+"\n"
            print('Message: ', message)
            return 'Fail', message
        
        # if len(png_files)>0:
        #     for file in png_files:
        #         if os.path.basename(file).startswith(image_data_file):
        #             print(f'Evaluation:: run_python_script:: Passed script:\n{script_path}')
        #             return 'Pass', ''
        else:
            message = ''
            if result.stdout:
                message+="Error output is: "+result.stdout+"\n"
            if result.stderr:
                message+="Standard error is: "+result.stderr+"\n"
            print('Message: ', message)
            return 'Fail', message

        # return 'Fail', 'No image found'
        # print(f'Result after executing python script: {result}')
        # if 'Success_and_End_of_Script!' in result.stdout:
        #     return 'Pass', None  # If it runs successfully, return 'Pass'
        # else:
        #     print(f'Failed by stdout: {result.stdout}')
        #     return 'Fail', result.stdout

    except subprocess.TimeoutExpired as e:
        print("⏰ Timeout! Script took too long to finish.")
        
        em = 'Timeout'
        if e.stdout:
            em += f',Standard output is: {str(e.stdout)}'
            print("Partial output:\n", em)
        if e.stderr:
            em+=f', Standard error is: {str(e.stderr)}'
            print("Partial output:\n", em)
        return 'Fail', em
    except subprocess.CalledProcessError as e:
        print(f'Fail from subprocess.CalledProcessError ... ')
        if e is None or e.stderr is None:
            return 'Fail', 'No error message'
        if e.stderr is not None:
            print(f'Fail from subprocess.CalledProcessError, error: {e.stderr}')
            return 'Fail', e.stderr  # If an error occurs, return 'Fail' and the error message
        return 'Fail', 'No error message'
    except Exception as e:
        print(f'Fail from Exception, error: {e}')
        if e is None:
            return 'Fail', 'No error message'
        return 'Fail', e


# created on February 27
def run_python_script_for_evaluation(script_path, png_files_only_file_name, dataset_name):
    """
    Runs a Python script with the specified HDF5 file as an argument.
    
    Args:
        script_path (str): Path to the Python script.
        data_file (str): Path to the HDF5 file.
    
    Returns:
        tuple: (status, error_message) where status is 'Pass' or 'Fail', and error_message is the error string or None.
    """
    try:
        # Run the Python script with the HDF5 file as an argument
        # result = subprocess.run(['python3', script_path, data_file], check=True, capture_output=True, text=True)
        result = subprocess.run(['python3', script_path], check=True, capture_output=True, text=True, timeout=120)
        
        # need to check if the image is generated and save in the directory
        script_base_name = os.path.basename(script_path)
        # image_data_file = script_path[0, len(script_base_name)-3]
        image_data_file =script_base_name.replace('.py', '')
        
        
        print('All PNG files with only file names: \n', png_files_only_file_name)
        
        
        image_found = False
        if dataset_name == 'CLIMATE':
            image_data_file_length = len(image_data_file)
            image_data_file = image_data_file[0:image_data_file_length//2]
            print(f'Half file name: {image_data_file}')

            if len(png_files_only_file_name)>0:
                for file in png_files_only_file_name:
                    if file.startswith(image_data_file):
                        print(f'Image Found for: {image_data_file}')
                        image_found = True
                        return 'Pass', None
                else:
                    print(f'No image found witht the name: {image_data_file}')
        elif dataset_name == 'MATPLOTAGENT' or dataset_name == 'FASTMRIBRAIN':
            image_data_file_length = len(image_data_file)
            image_data_file_name_split = image_data_file.split('_') 
            image_data_file_name_prefix = image_data_file_name_split[0]
            print(f'Image number: {image_data_file}')
            print(f'Image prefix number: {image_data_file_name_prefix}')


            if len(png_files_only_file_name)>0:
                for file in png_files_only_file_name:
                    if file.startswith(image_data_file_name_prefix):
                        print(f'Image Found for prefix number: {image_data_file_name_prefix}')
                        image_found = True
                        return 'Pass', None
                else:
                    print(f'No image found witht the name: {image_data_file}')
        elif dataset_name == 'VTK' :
            image_data_file_length = len(image_data_file)
            image_data_file_name_split = image_data_file.split('_') 
            image_data_file_name_prefix = image_data_file_name_split[0]
            print(f'Image number: {image_data_file}')
            print(f'Image prefix number: {image_data_file_name_prefix}')

            if len(png_files_only_file_name)>0:
                for file in png_files_only_file_name:
                    if file.startswith(image_data_file_name_prefix):
                        print(f'Image Found for prefix: {image_data_file_name_prefix}')
                        image_found = True
                        return 'Pass', None
                else:
                    print(f'No image found witht the name: {image_data_file}')


        if image_found==False:
            print('No Image')
            message = ''
            if result.stdout:
                message+="Standard output is: "+result.stdout+"\n"
            if result.stderr:
                message+="Standard error is: "+result.stderr+"\n"
            print('Message: ', message)
            return 'Fail', message
    except UnicodeDecodeError as e:
        print(len(str(e)))  # ✅ Safe
        print(f'UnicodeDecodeError Exception, message: {e}')
        return 'Fail', str(e)

    except subprocess.TimeoutExpired as e:
        print("⏰ Timeout! Script took too long to finish.")
        
        em = 'Timeout'
        if e.stdout:
            em += f',Standard output is: {str(e.stdout)}'
            print("Partial output:\n", em)
        if e.stderr:
            em+=f', Standard error is: {str(e.stderr)}'
            print("Partial output:\n", em)
        return 'Fail', em
    except subprocess.CalledProcessError as e:
        print(f'Fail from subprocess.CalledProcessError, error: {e.stderr}')
        return 'Fail', e.stderr  # If an error occurs, return 'Fail' and the error message
    except Exception as e:
        print(f'Fail from Exception, error: {e}')
        return 'Fail', e


# created on February 27
def run_python_script_for_evaluation_for_matplot_agent_fastmri_brain(script_path, png_files_only_file_name=''):
    """
    Runs a Python script with the specified HDF5 file as an argument.
    
    Args:
        script_path (str): Path to the Python script.
        data_file (str): Path to the HDF5 file.
    
    Returns:
        tuple: (status, error_message) where status is 'Pass' or 'Fail', and error_message is the error string or None.
    """
    try:
        # Run the Python script with the HDF5 file as an argument
        # result = subprocess.run(['python3', script_path, data_file], check=True, capture_output=True, text=True)
        result = subprocess.run(['python3', script_path], check=True, capture_output=True, text=True)
        return 'Pass', None
        # print(f'Result after executing python script: {result}')
        # if 'Success_and_End_of_Script!' in result.stdout:
        #     return 'Pass', None  # If it runs successfully, return 'Pass'
        # else:
        #     print(f'Failed by stdout: {result.stdout}')
        #     return 'Fail', result.stdout
        # return 'Pass', None
    except PermissionError:
        print('Permission error is overlooked')
        return 'Pass', None
    except subprocess.CalledProcessError as e:
        print(f'Fail from subprocess.CalledProcessError, error: {e.stderr}')
        return 'Fail', e.stderr  # If an error occurs, return 'Fail' and the error message
    except Exception as e:
        print(f'Fail from Exception, error: {e}')
        return 'Fail', e

# Function to save errors to a CSV file
def save_errors_to_csv(error_count_data_map, csv_file):

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        # writer.writerow(["Timestamp", "Script", "Error Message", "Category"])
        writer.writerow(["Model", "Pass Count", "Fail Count", 
                         "Dataset Paths Related Error Count", 
                        #  "Datasets related error messages" 
                         "Attribute Related Error Count", 
                        #  "Attribute Related Error messages",
                         "Slicing Related Error Count", 
                        #  "Slicing Related Error messages", 
                         "Other Errors count", 
                        #  "Other Error Messages"
                         ])
        
        row = []
        row.append(error_count_data_map['LLM_Model'])
        row.append(error_count_data_map['Pass_Count'])
        row.append(error_count_data_map['Fail_Count'])
        row.append(error_count_data_map['Dataset_Paths_Related_Error_Count']) 
        # error_count_data_map['Datasets_Paths_Related_Error_messages'], 
        row.append(error_count_data_map['Attribute_Related_Error_Count']) 
        # error_count_data_map['Attribute_Related_Error_messages'],
        row.append(error_count_data_map['Slicing_Related_Error_Count']) 
        # error_count_data_map['Slicing_Related_Error_messages'], 
        row.append(error_count_data_map['Other_Errors_Count']
        # error_count_data_map['Other_Errors_messages']
        )
        writer.writerow(row)
        # Write error data
        # for row in error_data:
            # writer.writerow(row)

# Function to save errors to a CSV file
def save_errors_to_csv_with_default_report_file_name(error_count_data_map, target_dir):
    csv_file = target_dir/'error_categorization_report.csv'
    print(f'\n\n------CSV saved to path: \n {csv_file}')
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["Model", "Pass Count", "Fail Count", 
                         "Dataset Paths Related Error Count", 
                         "Attribute Related Error Count", 
                         "Slicing Related Error Count", 
                         "Other Errors count", 
                         ])
        
        row = []
        row.append(error_count_data_map['LLM_Model'])
        row.append(error_count_data_map['Pass_Count'])
        row.append(error_count_data_map['Fail_Count'])
        row.append(error_count_data_map['Dataset_Paths_Related_Error_Count']) 
        row.append(error_count_data_map['Attribute_Related_Error_Count']) 
        row.append(error_count_data_map['Slicing_Related_Error_Count']) 
        row.append(error_count_data_map['Other_Errors_Count']
        )
        writer.writerow(row)

# Function to save errors to a CSV file
def iterative_save_errors_to_csv_with_default_report_file_name(error_count_data_map, target_dir, iteration):
    csv_file = ''
    if iteration==-1:
        csv_file = target_dir/f'error_categorization_report.csv'    
    else:
        csv_file = target_dir/f'error_categorization_report_{iteration}.csv'
    print(f'\n\n------CSV saved to path: \n {csv_file}')
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["Model", "Pass Count", "Fail Count", 
                         "Dataset Paths Related Error Count", 
                         "Attribute Related Error Count", 
                         "Slicing Related Error Count", 
                         "Other Errors count", 
                         ])
        
        row = []
        # total_number_script = error_count_data_map['Pass_Count'] + error_count_data_map['Fail_Count']
        row.append(error_count_data_map['LLM_Model'])
        row.append(error_count_data_map['Pass_Count'])
        row.append(error_count_data_map['Fail_Count'])
        row.append(error_count_data_map['Dataset_Paths_Related_Error_Count']) 
        row.append(error_count_data_map['Attribute_Related_Error_Count']) 
        row.append(error_count_data_map['Slicing_Related_Error_Count']) 
        row.append(error_count_data_map['Other_Errors_Count']
        )
        writer.writerow(row)

# created earlier
def find_python_scripts(script_dir, iterative_error_resolve):
    print(f'Inside find_python_scripts ...\nScript DIr: {script_dir}' ,'\n')
    """
    Search for Python scripts in a specified directory.    
    Args:
        script_dir (str): Directory where Python scripts are located.    
    Returns:
        dict: Dictionary where keys are base filenames (without extension), and values are the full paths to Python scripts.
    """
    py_scripts = {}
    for root, _, files in os.walk(script_dir):
        print('root: ', root, '\n')
        for file in files:
            if file.endswith('.py'):
                print(f'File: {file}')
                # to skip the file generated for iterative testing
                # if file.endswith(('_0.py', '_1.py', '_2.py', '_3.py')):
                    # continue
                # if iterative_error_resolve==False and file.endswith(('_0.py', '_1.py', '_2.py', '_3.py')):
                    # continue
                if file.endswith(('_0.py')):
                    base_name = os.path.splitext(file)[0]  # Get base filename without extension
                    py_scripts[base_name] = os.path.join(root, file)
                    print('py_scripts[base_name]: ', py_scripts[base_name], '\n')
    return py_scripts

import os
import glob


def get_python_files_dict(directory):
    print(f'Script directory for evaluation:\n{directory}')
    """Returns a dictionary of Python files ending with '_0.py' in the given directory.
    Key: Filename without extension
    Value: Full file path
    """
    directory = os.path.abspath(directory)  # Ensure absolute path
    # pattern = os.path.join(directory, "*_0.py")  # Match files ending with '_0.py'
    pattern = os.path.join(directory, "*.py")
    py_scripts = {}  # Dictionary to store results
    for file in glob.glob(pattern):  # Iterate over matching files
        base_name = os.path.splitext(os.path.basename(file))[0]  # Get base filename
        py_scripts[base_name] = file  # Store full path

    return py_scripts

def get_iterative_python_files_dict(directory, iteration):
    print(f'Script directory for evaluation:\n{directory}')
    """Returns a dictionary of Python files ending with '_0.py' in the given directory.
    Key: Filename without extension
    Value: Full file path
    """
    directory = os.path.abspath(directory)  # Ensure absolute path
    # pattern = os.path.join(directory, "*_0.py")  # Match files ending with '_0.py'
    pattern = os.path.join(directory, "*.py")
    py_scripts = {}  # Dictionary to store results
    for file in glob.glob(pattern):  # Iterate over matching files
        # to skip the file generated for iterative testing
        # if file.endswith(('_0.py', '_1.py', '_2.py', '_3.py')):
            # continue
        if file.endswith((f'_{iteration}.py')):
            base_name = os.path.splitext(os.path.basename(file))[0]  # Get base filename
            print(f'Python Script base name: {base_name}')
            py_scripts[base_name] = file  # Store full path

    return py_scripts


# Main program
def main(common_directory, output_file, python_script_dir, model, iterative_error_resolve, corrector, dataset):
    # Script to execute
    # script_path = "target_script.py"  # Replace with the actual script path
    # csv_file = "error_log.csv"
    
   
    # script_dir = common_directory + python_script_dir
    script_dir = python_script_dir
    print('common_directory: ', common_directory, '\n')
    print('python_script_dir: ', python_script_dir, '\n')
    print('script_dir: ', script_dir, '\n')
    print(f'Dataset: {dataset}')

    # py_scripts = find_python_scripts(script_dir, iterative_error_resolve)
    # Example usage:
    directory_path =script_dir  # Replace with your actual directory
    python_files_dict = get_python_files_dict(common_directory+"/"+directory_path)
    py_scripts = python_files_dict
    next_evaluation_scritps = python_files_dict
    print(python_files_dict)
    
    csv_map = {'LLM_Model': model,
               'Pass_Count': 0,
               'Fail_Count': 0, 
                'Dataset_Paths_Related_Error_Count': 0, 
                'Datasets_Paths_Related_Error_messages': '', 
                'Attribute_Related_Error_Count': 0, 
                'Attribute_Related_Error_messages': '',
                'Slicing_Related_Error_Count': 0, 
                'Slicing_Related_Error_messages': '', 
                'Other_Errors_Count': 0, 
                'Other_Errors_messages': ''
               }

    model_name = model.replace(':', '_')
    model_name = model_name.replace('-', '_')
    print(f'Evaluation model name: {model_name}')

    with_without_corrector='without'
    if corrector==True:
        with_without_corrector='with'

    # if these two dataset direct evaluation without image checking:
    if dataset=='MATPLOTAGENT' or dataset=='FASTMRIBRAIN':
        print('Inside separate evaluation method for MATPLOTAGENT and FAST_MRI_BRAIN')
        for py_script in py_scripts:
            script_path = py_scripts[py_script]
            print(f'Script path: {script_path}')
            # time.sleep(4)
            # for iterative there will be multiple scripts ends with _ number
            # let's remove the _number scripts
            python_script_file_base_name = os.path.basename(py_script)
            print(f'Script base name: {os.path.basename(py_script)} ')
            # Run the script and capture errors
            # stdout, stderr = run_script(script_path)
            status, stderr = run_python_script_for_evaluation_for_matplot_agent_fastmri_brain(script_path)
        

            if status=='Pass':
                csv_map['Pass_Count'] = csv_map['Pass_Count'] +1
                print('Pass')
            else:
                print('Fail')
                csv_map['Fail_Count'] = csv_map['Fail_Count'] +1
                # Parse errors and categorize
                # error_data = []
                if stderr and len(stderr)>0:
                    # for error_line in stderr.splitlines():
                    last_line_error = stderr.splitlines()
                    last_line_error = last_line_error[len(last_line_error)-1]
                    # last_line_error=last_line_error.replace('\'','')
                    # last_line_error=last_line_error.replace('\"','')
                    
                    category, error_message, error_message_details = conditional_categorize_error(last_line_error)
                    csv_map[category] = csv_map[category] +1
                    csv_map[error_message] = csv_map[error_message] +'\n'+ error_message_details

                    # error_data.append([datetime.now(), script_path, error_line, category])
                else:
                    csv_map['Other_Errors_Count'] = csv_map['Other_Errors_Count'] + 1


        save_errors_to_csv(csv_map, output_file)
        return


    # At first executing the scripts and gathering the images
    new_dir_name=''
    if dataset=='CLIMATE':
        print(f'Pre executing scripts for the CLIMATE dataset, length of py scripts: {len(py_scripts)}')
        png_files_only_file_name=[]
        for py_script in py_scripts:
            try:
                print(f'Pre executing script: {py_script}')
                script_path = py_scripts[py_script]
                status, stderr = run_python_script_for_evaluation(script_path, png_files_only_file_name)
                print(f'Success: {py_script}\n\n')
            except Exception as e:
                print(f'Error while pre executing scripts:{py_script} Error: {e}\n\n')
        subdirectories = [' ', 'NSIDC', ' ', 'PO_DAAC', ' ', 'ASF', 'GES_DISC', 'GHRC', 'ICESat_2', 'LAADS', 'LaRC', 'LP_DAAC',  'Ocen_Biology', 'AURA_DATA_VC']
        data_dir='ACL_DIRS'
        source_dirs = subdirectories  # List of source directories
        source_dirs.append('../prompting_techniques/zero_shot_sci_data_prompting')
        base_path = "/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data"  # Base path for new directory
        # new_dir_name=f'{model_name}_zero_shot_CoT_{with_without_corrector}_corrector_expert_level_queries_human_error_insertions_remove_image_from_query_evaluation_images_final'
        # for expert
        new_dir_name=f'{model_name}_zero_shot_CoT_{with_without_corrector}_corrector_expert_level_queries_human_modified_queries_with_accurate_information_based_on_original_scripts'
        # data_dir = 'ACL_DIRS'
        utils.collect_and_store_png(source_dirs, base_path, new_dir_name, data_dir)
    # Fetch all generated PNG files
    # data_directory = f'/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/generated_image_from_running_evaluation/{model_name}_{with_without_corrector}_corrector_expert_level_queries_human_error_insertions_remove_image_from_query'
    
    # data_directory = f'/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/generated_image_from_running_evaluation/{model_name}_{with_without_corrector}_corrector_expert_level_queries_human_error_insertions_remove_image_from_query'
    data_directory = f'/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/generated_image_from_running_evaluation/{new_dir_name}'

    print('Data Directory: \n', data_directory)
    # data_directory = os.path.dirname(script_path)
    # print(f'Data directory: {data_directory}')
    
    # png_files = glob.glob(os.path.join(data_directory, "*.png"))
    
    # main_script_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/zero_shot_sci_data_prompting'
    png_files_from_main_script_dir = glob.glob(os.path.join(data_directory, "*.png"))
    
    # if len(png_files_from_main_script_dir)>0:
    #     print(f'{main_script_dir}\nThis main directory also has images\n')
    #     png_files.extend(png_files_from_main_script_dir)
    
    print('All PNG files: \n', png_files_from_main_script_dir)
    png_files_only_file_name = []
    if len(png_files_from_main_script_dir)>0:
        for file in png_files_from_main_script_dir:
            names = file.split('/')
            png_files_only_file_name.append(names[len(names)-1])
    print('All PNG files with only file names: \n', png_files_only_file_name)

    for evaluation_script in next_evaluation_scritps:
        # time.sleep(4)
        # for iterative there will be multiple scripts ends with _ number
        # let's remove the _number scripts
        evaluation_python_script_file_base_name = os.path.basename(evaluation_script)
        print(f'\n\nRunning Script base name: {os.path.basename(evaluation_script)} ')
        # if py_script.endswith('_0.py') or py_script.endswith('_1.py') or py_script.endswith('_2.py') or py_script.endswith('_3.py'):
        #     print('Skipping...', py_script)
        #     continue 
        # if python_script_file_base_name.endswith('_0') or python_script_file_base_name.endswith('_1') or python_script_file_base_name.endswith('_2') or python_script_file_base_name.endswith('_3'):
        #     print('Skipping...', py_script)
        #     print(f'Skiping python script file base name {python_script_file_base_name} ...')
        #     continue 
        # this is for evaluation zero shot from iterative evaluation
        # if evaluation_python_script_file_base_name.endswith('_0'):
        #     script_path = py_scripts[py_script]
        #     print(f"\nRunning script {script_path}...")
        
        evaluation_script_path = next_evaluation_scritps[evaluation_script]
        # to check the maximum numbered generated script
        if iterative_error_resolve == True:
            print('Going to check for multiple generated script...')
            result = check_if_has_length_difference(script_dir+"/"+py_script)
            if result == True:
                print(f'unusual script length change for the file: {py_script}')
                csv_map['Other_Errors_Count'] = csv_map['Other_Errors_Count'] + 1
                csv_map['Fail_Count'] = csv_map['Fail_Count'] +1
                continue


        # Run the script and capture errors
        # stdout, stderr = run_script(script_path)
        status, stderr = run_python_script_for_evaluation(evaluation_script_path, png_files_only_file_name)
      

        if status=='Pass':
            csv_map['Pass_Count'] = csv_map['Pass_Count'] +1
            print('Pass')
        else:
            print('Fail')
            csv_map['Fail_Count'] = csv_map['Fail_Count'] +1
            # Parse errors and categorize
            # error_data = []
            if stderr and len(stderr)>0:
                # for error_line in stderr.splitlines():
                last_line_error = stderr.splitlines()
                last_line_error = last_line_error[len(last_line_error)-1]
                # last_line_error=last_line_error.replace('\'','')
                # last_line_error=last_line_error.replace('\"','')
                
                category, error_message, error_message_details = conditional_categorize_error(last_line_error)
                csv_map[category] = csv_map[category] +1
                csv_map[error_message] = csv_map[error_message] +'\n'+ error_message_details

                # error_data.append([datetime.now(), script_path, error_line, category])
            else:
                csv_map['Other_Errors_Count'] = csv_map['Other_Errors_Count'] + 1


        
       
    save_errors_to_csv(csv_map, output_file)
    """
    # Save to CSV
    if error_data:
        # save_errors_to_csv(error_data, csv_file)
        save_errors_to_csv(error_data, output_file)
        print(f"Errors categorized and saved to {output_file}.")
    else:
        print("No errors found.")
    
    """


# created on Feb 22, 2025

    
def check_if_has_length_difference(python_script_full_path):
    print(f'Checking file path: {python_script_full_path}')
    # Full path of a script (example, change as needed)
    # full_path = python_script_full_path

    # Extract the directory and base name without numbers
    script_dir = os.path.dirname(python_script_full_path)  # Get script directory
    filename = os.path.basename(python_script_full_path)  # Extract filename
    print('File name:', filename)
    base_name = filename

    # Example usage
    # script_dir = "/path/to/scripts"  # Change this to your directory
    # base_name = "TES-Aura_L2-O3-Nadir_r0000002433_F08_12.he5"  # Change this to your base filename

    result = find_and_read_latest_files(script_dir, base_name)
    return result




def find_and_read_latest_files(script_dir, base_name):
    try:
        print(f'from the find_and_read_latest_files script_dir: {script_dir},\n base_name: {base_name} ')
        """
        Finds and reads the base file and the highest-numbered _N.py file.
        
        :param script_dir: The directory containing the scripts.
        :param base_name: The base name of the script file (without _N.py).
        """
        # Ensure directory exists
        if not os.path.isdir(script_dir):
            print(f"Error: Directory '{script_dir}' does not exist.")
            return True
        
        # Pattern to match files with _N.py (where N is a number)
        file_pattern = os.path.join(script_dir, f"{base_name}_*.py")
        
        # Find all matching files
        matching_files = glob.glob(file_pattern)

        # Extract numbers from filenames
        numbered_files = []
        for file_path in matching_files:
            print('Reading the numbered files....')
            match = re.search(rf"{re.escape(base_name)}_(\d+)\.py$", file_path)
            if match:
                numbered_files.append((int(match.group(1)), file_path))
        
        print(f'Number of numbered python scripts generated: {len(numbered_files)}')
        if not numbered_files:
            print("No numbered script files found.")
            return True
        elif len(numbered_files)==1:
            print(f"Number of numbered files found: {len(numbered_files)}")
            return False
        print('Before sort...')
        # Sort by number and get the highest one
        numbered_files.sort(reverse=True)
        print(f'Sorted files: {numbered_files}')
        max_file = numbered_files[0][1]  # File with the highest number

        # Read the base file
        # base_file_path = os.path.join(script_dir, f"{base_name}.py")
        base_file_path = os.path.join(script_dir, f"{base_name}_0.py")
        
        base_file_content_length = 0
        
        if os.access(base_file_path, os.R_OK):  # Check read permission
            print(f"\nReading file is ok: {base_file_path}")
        else:
            print(f"\nReading file is locked: {base_file_path}")

        if os.path.exists(base_file_path):
            print(f"\nReading file: {base_file_path}")
            # with open(base_file_path, 'r', encoding='utf-8') as f:
            with open(base_file_path, 'r')as f:
                base_file_content=''
                for line in f:
                    base_file_content+= line
                base_file_content_length = len(base_file_content)
                # print(f.read())

        max_file_content_length = 0    
        if os.path.exists(max_file):
            print(f"\nReading file: {max_file}")
            with open(max_file, 'r') as f:
                max_file_content=''
                for line in f:
                    max_file_content+= line
                max_file_content_length = len(max_file_content)
                # print(f.read())
        
        print(f'Max file {os.path.basename(max_file)} and content length: {max_file_content_length}')
        print(f'Base file {os.path.basename(base_file_path)} and content length: {base_file_content_length}')

        if (max_file_content_length/base_file_content_length)<=0.5:
            return True
        else:
            return False
    except Exception as e:
        print(f'Exception occurred while evaluation scripts, script base name: {base_name}, error: {e}') 
        return True
        

def show_data_using_table_view(file_path):

    # Read the CSV file
    data = pd.read_csv(file_path)

    # Display the table view
    print(data)
    import matplotlib.pyplot as plt

    # Create a table view
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust size as needed
    ax.axis('off')  # Turn off the axis

    # Create a table
    table = plt.table(
        cellText=data.values,
        colLabels=data.columns,
        cellLoc='center',
        loc='center'
    )

    # Customize table appearance
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(data.columns))))
    plt.savefig(file_path + '.py.png')
    plt.show()


def evaluation_of_CLIMATE_python_scripts_by_checking_generated_image(common_base_directory, target_dir, python_script_dir, model_name):
    FULL_PYTHON_SCRIPT_DIRECTORY = common_base_directory+"/"+directory_path
    print(f'evaluation_of_CLIMATE_python_scripts_by_checking_generated_image, FULL_PYTHON_SCRIPT_DIRECTORY: {FULL_PYTHON_SCRIPT_DIRECTORY}')

    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    
   
    script_dir = python_script_dir
    print('common_directory: ', common_base_directory, '\n')
    print('python_script_dir: ', python_script_dir, '\n')
    print('script_dir: ', script_dir, '\n')

    directory_path =script_dir  # Replace with your actual directory
    python_files_dict = get_python_files_dict(common_base_directory+"/"+directory_path)
    py_scripts = python_files_dict
    next_evaluation_scritps = python_files_dict
    print(f'All python scripts to be evaluated:\n{python_files_dict}')
    
    csv_map = {'LLM_Model': model_name,
               'Pass_Count': 0,
               'Fail_Count': 0, 
                'Dataset_Paths_Related_Error_Count': 0, 
                'Datasets_Paths_Related_Error_messages': '', 
                'Attribute_Related_Error_Count': 0, 
                'Attribute_Related_Error_messages': '',
                'Slicing_Related_Error_Count': 0, 
                'Slicing_Related_Error_messages': '', 
                'Other_Errors_Count': 0, 
                'Other_Errors_messages': ''
               }

    print(f'Evaluation model name: {model_name}')


    # At first executing the scripts and gathering the images
    new_dir_name = python_script_dir
    print(f'\n--------Pre executing scripts for the CLIMATE dataset, length of py scripts: {len(py_scripts)} ----------')
    png_files_only_file_name=[]
    for py_script in py_scripts:
        try:
            print(f'Pre executing script: {py_script}')
            script_path = py_scripts[py_script]
            status, stderr = run_python_script_for_evaluation(script_path, png_files_only_file_name, 'CLIMATE')
            print(f'Success: {py_script}\n\n')
        except Exception as e:
            print(f'Error while pre executing scripts:{py_script} Error: {e}\n\n')
    
    # script_execution_base_path = "/Users/apukumarchakroborti/gsu_research/llam_test"
    data_dir_base_path = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
    target_dir_base_path = f"{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag"    
    
    subdirectories = [      f'{data_dir_base_path}/ACL_DIRS/ASF',
                            f'{data_dir_base_path}/ACL_DIRS/AURA_DATA_VC',
                            f'{data_dir_base_path}/ACL_DIRS/GES_DISC',
                            f'{data_dir_base_path}/ACL_DIRS/ICESat_2',
                            f'{data_dir_base_path}/ACL_DIRS/LAADS',
                            f'{data_dir_base_path}/ACL_DIRS/LaRC',
                            f'{data_dir_base_path}/ACL_DIRS/LP_DAAC',
                            f'{data_dir_base_path}/ACL_DIRS/NSIDC',
                            f'{data_dir_base_path}/ACL_DIRS/PO_DAAC',
                            f'{data_dir_base_path}',
                            f'{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting'
                        ]
    # source_dirs, script_execution_base_path, target_dir_base_path, new_dir_name
    utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name)
    # should be updated
    # data_directory = f'/Users/apukumarchakroborti/gsu_research/adm_research_spring_2025/llms_generated_python_scripts/error_categorization_report/generated_image_from_running_evaluation/{new_dir_name}'
    data_directory = f'/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag/generated_image_from_running_evaluation/{new_dir_name}'
    
    
    print('Data Directory: \n', data_directory)
    
    png_files_from_main_script_dir = glob.glob(os.path.join(data_directory, "*.png"))
    
    
    print('All PNG files: \n', png_files_from_main_script_dir)
    png_files_only_file_name = []
    if len(png_files_from_main_script_dir)>0:
        for file in png_files_from_main_script_dir:
            names = file.split('/')
            png_files_only_file_name.append(names[len(names)-1])
    print('All PNG files with only file names: \n', png_files_only_file_name)

    for evaluation_script in next_evaluation_scritps:
        
        evaluation_python_script_file_base_name = os.path.basename(evaluation_script)
        print(f'\n\nRunning Script base name: {os.path.basename(evaluation_script)} ')
        
        evaluation_script_path = next_evaluation_scritps[evaluation_script]
        
        status, stderr = run_python_script_for_evaluation(evaluation_script_path, png_files_only_file_name, 'CLIMATE')
        print(f'Execution result:\nstatus: {status}\nstderr: {stderr}')
      

        if status=='Pass':
            csv_map['Pass_Count'] = csv_map['Pass_Count'] +1
            print('Pass')
        else:
            print('Fail')
            csv_map['Fail_Count'] = csv_map['Fail_Count'] +1
            if stderr and len(stderr)>0:
                # last_line_error = stderr.splitlines()
                last_line_error = [line for line in stderr.splitlines() if line.strip()]

                print(f'splitted error message: {last_line_error}')

                last_line_error = last_line_error[len(last_line_error)-1]
                print(f'last line error message: {last_line_error}')

                category, error_message, error_message_details = conditional_categorize_error(last_line_error)
                csv_map[category] = csv_map[category] +1
                csv_map[error_message] = csv_map[error_message] +'\n'+ error_message_details

            else:
                csv_map['Other_Errors_Count'] = csv_map['Other_Errors_Count'] + 1
    # out of for loop
    save_errors_to_csv_with_default_report_file_name(csv_map, target_dir)
    utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name)


def evaluation_of_MATPLOTAGENT_python_scripts_by_checking_generated_image(common_base_directory, target_dir, python_script_dir, model_name):
    
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    
   
    script_dir = python_script_dir
    print('common_directory: ', common_base_directory, '\n')
    print('python_script_dir: ', python_script_dir, '\n')
    print('script_dir: ', script_dir, '\n')

    directory_path =script_dir  # Replace with your actual directory
    python_files_dict = get_python_files_dict(common_base_directory+"/"+directory_path)
    py_scripts = python_files_dict
    next_evaluation_scritps = python_files_dict
    print(f'All python scripts to be evaluated:\n{python_files_dict}')
    
    csv_map = {'LLM_Model': model_name,
               'Pass_Count': 0,
               'Fail_Count': 0, 
                'Dataset_Paths_Related_Error_Count': 0, 
                'Datasets_Paths_Related_Error_messages': '', 
                'Attribute_Related_Error_Count': 0, 
                'Attribute_Related_Error_messages': '',
                'Slicing_Related_Error_Count': 0, 
                'Slicing_Related_Error_messages': '', 
                'Other_Errors_Count': 0, 
                'Other_Errors_messages': ''
               }

    print(f'Evaluation model name: {model_name}')


    # At first executing the scripts and gathering the images
    new_dir_name = python_script_dir
    print(f'\n--------Pre executing scripts for the MATPLOTAGENT dataset related python scripts, length of py scripts: {len(py_scripts)} ----------')
    png_files_only_file_name=[]
    for py_script in py_scripts:
        try:
            print(f'Pre executing script: {py_script}')
            script_path = py_scripts[py_script]
            status, stderr = run_python_script_for_evaluation(script_path, png_files_only_file_name, 'MATPLOTAGENT')
            print(f'Success: {py_script}\n\n')
        except Exception as e:
            print(f'Error while pre executing scripts:{py_script} Error: {e}\n\n')
    
    # script_execution_base_path = "/Users/apukumarchakroborti/gsu_research/llam_test"
    data_dir_base_path = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
    target_dir_base_path = f"{data_dir_base_path}/matplot_agent_data/plot_generation/error_categorization_evaluation_result"    
    
    subdirectories = [      
                        f'{data_dir_base_path}/matplot_agent_data/plot_generation/csv_to_h5_data',
                        f'{data_dir_base_path}',
                        f'{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting'
                    ]
    # source_dirs, script_execution_base_path, target_dir_base_path, new_dir_name
    utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name)
    # should be updated
    # data_directory = f'/Users/apukumarchakroborti/gsu_research/adm_research_spring_2025/llms_generated_python_scripts/error_categorization_report/generated_image_from_running_evaluation/{new_dir_name}'
    data_directory = f'{data_dir_base_path}/matplot_agent_data/plot_generation/error_categorization_evaluation_result/generated_image_from_running_evaluation/{new_dir_name}'    
    print('Data Directory: \n', data_directory)
    
    png_files_from_main_script_dir = glob.glob(os.path.join(data_directory, "*.png"))    
    print('All PNG files: \n', png_files_from_main_script_dir)

    png_files_only_file_name = []
    if len(png_files_from_main_script_dir)>0:
        for file in png_files_from_main_script_dir:
            names = file.split('/')
            png_files_only_file_name.append(names[len(names)-1])
    print('All PNG files with only file names: \n', png_files_only_file_name)

    for evaluation_script in next_evaluation_scritps:        
        evaluation_python_script_file_base_name = os.path.basename(evaluation_script)
        print(f'\n\nRunning Script base name: {os.path.basename(evaluation_script)} ')
        
        evaluation_script_path = next_evaluation_scritps[evaluation_script]        
        status, stderr = run_python_script_for_evaluation(evaluation_script_path, png_files_only_file_name, 'MATPLOTAGENT')
        print(f'Execution result:\nstatus: {status}\nstderr: {stderr}')      

        if status=='Pass':
            csv_map['Pass_Count'] = csv_map['Pass_Count'] +1
            print('Pass')
        else:
            print('Fail')
            csv_map['Fail_Count'] = csv_map['Fail_Count'] +1
            if stderr and len(stderr)>0:
                # last_line_error = stderr.splitlines()
                last_line_error = [line for line in stderr.splitlines() if line.strip()]

                print(f'splitted error message: {last_line_error}')

                last_line_error = last_line_error[len(last_line_error)-1]
                print(f'last line error message: {last_line_error}')

                category, error_message, error_message_details = conditional_categorize_error(last_line_error)
                csv_map[category] = csv_map[category] +1
                csv_map[error_message] = csv_map[error_message] +'\n'+ error_message_details

            else:
                csv_map['Other_Errors_Count'] = csv_map['Other_Errors_Count'] + 1
    # out of for loop
    save_errors_to_csv_with_default_report_file_name(csv_map, target_dir)
    utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name)



def evaluation_of_FASTMRIBRAIN_python_scripts_by_checking_generated_image(common_base_directory, target_dir, python_script_dir, model_name):
    
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    
   
    script_dir = python_script_dir
    print('common_directory: ', common_base_directory, '\n')
    print('python_script_dir: ', python_script_dir, '\n')
    print('script_dir: ', script_dir, '\n')

    directory_path =script_dir  # Replace with your actual directory
    python_files_dict = get_python_files_dict(common_base_directory+"/"+directory_path)
    py_scripts = python_files_dict
    next_evaluation_scritps = python_files_dict
    print(f'All python scripts to be evaluated:\n{python_files_dict}')
    
    csv_map = {'LLM_Model': model_name,
               'Pass_Count': 0,
               'Fail_Count': 0, 
                'Dataset_Paths_Related_Error_Count': 0, 
                'Datasets_Paths_Related_Error_messages': '', 
                'Attribute_Related_Error_Count': 0, 
                'Attribute_Related_Error_messages': '',
                'Slicing_Related_Error_Count': 0, 
                'Slicing_Related_Error_messages': '', 
                'Other_Errors_Count': 0, 
                'Other_Errors_messages': ''
               }

    print(f'Evaluation model name: {model_name}')


    # At first executing the scripts and gathering the images
    new_dir_name = python_script_dir
    print(f'\n--------Pre executing scripts for the CLIMATE dataset, length of py scripts: {len(py_scripts)} ----------')
    png_files_only_file_name=[]
    for py_script in py_scripts:
        try:
            print(f'Pre executing script: {py_script}')
            script_path = py_scripts[py_script]
            status, stderr = run_python_script_for_evaluation(script_path, png_files_only_file_name, 'FASTMRIBRAIN')
            print(f'Success: {py_script}\n\n')
        except Exception as e:
            print(f'Error while pre executing scripts:{py_script} Error: {e}\n\n')
    
    # script_execution_base_path = "/Users/apukumarchakroborti/gsu_research/llam_test"
    data_dir_base_path = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
    # target_dir_base_path = f"{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag"
    target_dir_base_path = f"{data_dir_base_path}/mri_nyu_data/error_categorization_evaluation_result/non_iterative_evaluation_results"      
    
    subdirectories = [      f'{data_dir_base_path}/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5',
                            f'{data_dir_base_path}',
                            f'{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting'
                        ]
    # source_dirs, script_execution_base_path, target_dir_base_path, new_dir_name
    utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name)
    # should be updated
    # data_directory = f'/Users/apukumarchakroborti/gsu_research/adm_research_spring_2025/llms_generated_python_scripts/error_categorization_report/generated_image_from_running_evaluation/{new_dir_name}'
    data_directory = f'/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag/generated_image_from_running_evaluation/{new_dir_name}'
    
    
    print('Data Directory: \n', data_directory)
    
    png_files_from_main_script_dir = glob.glob(os.path.join(data_directory, "*.png"))
    
    
    print('All PNG files: \n', png_files_from_main_script_dir)
    png_files_only_file_name = []
    if len(png_files_from_main_script_dir)>0:
        for file in png_files_from_main_script_dir:
            names = file.split('/')
            png_files_only_file_name.append(names[len(names)-1])
    print('All PNG files with only file names: \n', png_files_only_file_name)

    for evaluation_script in next_evaluation_scritps:
        
        evaluation_python_script_file_base_name = os.path.basename(evaluation_script)
        print(f'\n\nRunning Script base name: {os.path.basename(evaluation_script)} ')
        
        evaluation_script_path = next_evaluation_scritps[evaluation_script]
        
        status, stderr = run_python_script_for_evaluation(evaluation_script_path, png_files_only_file_name, 'FASTMRIBRAIN')
        print(f'Execution result:\nstatus: {status}\nstderr: {stderr}')
      

        if status=='Pass':
            csv_map['Pass_Count'] = csv_map['Pass_Count'] +1
            print('Pass')
        else:
            print('Fail')
            csv_map['Fail_Count'] = csv_map['Fail_Count'] +1
            if stderr and len(stderr)>0:
                # last_line_error = stderr.splitlines()
                last_line_error = [line for line in stderr.splitlines() if line.strip()]

                print(f'splitted error message: {last_line_error}')

                last_line_error = last_line_error[len(last_line_error)-1]
                print(f'last line error message: {last_line_error}')

                category, error_message, error_message_details = conditional_categorize_error(last_line_error)
                csv_map[category] = csv_map[category] +1
                csv_map[error_message] = csv_map[error_message] +'\n'+ error_message_details

            else:
                csv_map['Other_Errors_Count'] = csv_map['Other_Errors_Count'] + 1
    # out of for loop
    save_errors_to_csv_with_default_report_file_name(csv_map, target_dir)
    utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name)


def evaluation_of_VTK_python_scripts_by_checking_generated_image(common_base_directory, target_dir, python_script_dir, model_name, all_files_source_directory, program_execution_base_directory):
    
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    
    #at first move all data files to the generated script directory
    extensions = ['.txt', '.pgm', '.3ds', '.vtk', '.vtp', '.mhd', '.zraw', '.raw', '.mha', '.tri']      
    # utils.move_files_by_extension(all_files_source_directory, python_script_dir, extensions)
    utils.move_files_by_extension(all_files_source_directory, program_execution_base_directory, extensions)
    
    
    script_dir = python_script_dir
    print('common_directory: ', common_base_directory, '\n')
    print('python_script_dir: ', python_script_dir, '\n')
    print('script_dir: ', script_dir, '\n')

    directory_path =script_dir  # Replace with your actual directory
    python_files_dict = get_python_files_dict(common_base_directory+"/"+directory_path)
    py_scripts = python_files_dict
    next_evaluation_scritps = python_files_dict
    print(f'All python scripts to be evaluated:\n{python_files_dict}')
    
    csv_map = {'LLM_Model': model_name,
               'Pass_Count': 0,
               'Fail_Count': 0, 
                'Dataset_Paths_Related_Error_Count': 0, 
                'Datasets_Paths_Related_Error_messages': '', 
                'Attribute_Related_Error_Count': 0, 
                'Attribute_Related_Error_messages': '',
                'Slicing_Related_Error_Count': 0, 
                'Slicing_Related_Error_messages': '', 
                'Other_Errors_Count': 0, 
                'Other_Errors_messages': ''
               }

    print(f'Evaluation model name: {model_name}')


    # At first executing the scripts and gathering the images
    new_dir_name = python_script_dir
    print(f'\n--------Pre executing scripts for the CLIMATE dataset, length of py scripts: {len(py_scripts)} ----------')
    png_files_only_file_name=[]
    for py_script in py_scripts:
        try:
            print(f'Pre executing script: {py_script}')
            script_path = py_scripts[py_script]
            status, stderr = run_python_script_for_evaluation(script_path, png_files_only_file_name, 'VTK')
            print(f'Success: {py_script}\n\n')
        except Exception as e:
            print(f'Error while pre executing scripts:{py_script} Error: {e}\n\n')
    
    # script_execution_base_path = "/Users/apukumarchakroborti/gsu_research/llam_test"
    data_dir_base_path = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
    target_dir_base_path = f"{data_dir_base_path}/vtk_python_scripts_experiment/error_categorization_evaluation_result"    
    
    subdirectories = [      f'{python_script_dir}',
                            f'{data_dir_base_path}',
                            f'{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting'
                    ]
    # source_dirs, script_execution_base_path, target_dir_base_path, new_dir_name
    utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name)
    # should be updated
    # data_directory = f'/Users/apukumarchakroborti/gsu_research/adm_research_spring_2025/llms_generated_python_scripts/error_categorization_report/generated_image_from_running_evaluation/{new_dir_name}'
    data_directory = f'/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/vtk_python_scripts_experiment/error_categorization_evaluation_result/generated_image_from_running_evaluation/{new_dir_name}'
    
    
    print('Data Directory: \n', data_directory)
    
    png_files_from_main_script_dir = glob.glob(os.path.join(data_directory, "*.png"))
    
    
    print('All PNG files: \n', png_files_from_main_script_dir)
    png_files_only_file_name = []
    if len(png_files_from_main_script_dir)>0:
        for file in png_files_from_main_script_dir:
            names = file.split('/')
            png_files_only_file_name.append(names[len(names)-1])
    print('All PNG files with only file names: \n', png_files_only_file_name)

    for evaluation_script in next_evaluation_scritps:
        
        evaluation_python_script_file_base_name = os.path.basename(evaluation_script)
        print(f'\n\nRunning Script base name: {os.path.basename(evaluation_script)} ')
        
        evaluation_script_path = next_evaluation_scritps[evaluation_script]
        
        status, stderr = run_python_script_for_evaluation(evaluation_script_path, png_files_only_file_name, 'VTK')
        print(f'Execution result:\nstatus: {status}\nstderr: {stderr}')
      

        if status=='Pass':
            csv_map['Pass_Count'] = csv_map['Pass_Count'] +1
            print('Pass')
        else:
            print('Fail')
            csv_map['Fail_Count'] = csv_map['Fail_Count'] +1
            if stderr and len(stderr)>0:
                # last_line_error = stderr.splitlines()
                last_line_error = [line for line in stderr.splitlines() if line.strip()]

                print(f'splitted error message: {last_line_error}')

                last_line_error = last_line_error[len(last_line_error)-1]
                print(f'last line error message: {last_line_error}')

                category, error_message, error_message_details = conditional_categorize_error(last_line_error)
                csv_map[category] = csv_map[category] +1
                csv_map[error_message] = csv_map[error_message] +'\n'+ error_message_details

            else:
                csv_map['Other_Errors_Count'] = csv_map['Other_Errors_Count'] + 1
    # out of for loop
    save_errors_to_csv_with_default_report_file_name(csv_map, target_dir)
    utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name)

    #At the end move all data files to the generated script directory 
    utils.move_files_by_extension(program_execution_base_directory, all_files_source_directory, extensions)

# def evaluation_of_ITERATIVE_VTK_python_scripts_by_checking_generated_image(common_base_directory, target_dir, python_script_dir, model_name):
def evaluation_of_ITERATIVE_VTK_python_scripts_by_checking_generated_image(llm_generated_python_scripts_ase_directory, target_dir, python_script_dir, model_name, all_files_source_directory, target_base_dir):
    FULL_PYTHON_SCRIPT_DIRECTORY = llm_generated_python_scripts_ase_directory+'/'+python_script_dir
    print(f'evaluation_of_ITERATIVE_VTK_python_scripts_by_checking_generated_image, FULL_PYTHON_SCRIPT_DIRECTORY: \n{FULL_PYTHON_SCRIPT_DIRECTORY}')

    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)    
   
    script_dir = python_script_dir
    print('llm_generated_python_scripts_ase_directory: ', llm_generated_python_scripts_ase_directory, '\n')
    print('python_script_dir: ', python_script_dir, '\n')
    print('all_files_source_directory: ', all_files_source_directory, '\n')

    #at first move all data files to the generated script directory
    extensions = ['.txt', '.pgm', '.3ds', '.vtk', '.vtp', '.mhd', '.zraw', '.raw', '.mha', '.tri']      
    # utils.move_files_by_extension(all_files_source_directory, python_script_dir, extensions)
    # all_files_source_directory = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/vtk_data'
    utils.move_files_by_extension(all_files_source_directory, target_base_dir, extensions)

    directory_path =script_dir  # Replace with your actual directory
    
    total_scripts = 40
    total_pass_count = 0
    total_fail_count = 0
    total_Dataset_Paths_Related_Error_Count = 0
    total_Attribute_Related_Error_Count = 0
    total_Slicing_Related_Error_Count =0
    total_Other_Errors_Count =0
    
                   
    num_iteration = 7
    for iteration in range(0, num_iteration):
    # for iteration in range(0, num_iteration):
        python_files_dict = get_iterative_python_files_dict(FULL_PYTHON_SCRIPT_DIRECTORY, iteration)
        py_scripts = python_files_dict
        next_evaluation_scritps = python_files_dict
        print(f'All python scripts to be evaluated:\n{python_files_dict}')
        
        csv_map = {'LLM_Model': model_name,
                'Pass_Count': 0,
                'Fail_Count': 0, 
                'Dataset_Paths_Related_Error_Count': 0, 
                'Datasets_Paths_Related_Error_messages': '', 
                'Attribute_Related_Error_Count': 0, 
                'Attribute_Related_Error_messages': '',
                'Slicing_Related_Error_Count': 0, 
                'Slicing_Related_Error_messages': '', 
                'Other_Errors_Count': 0, 
                'Other_Errors_messages': ''
                }

        print(f'Evaluation model name: {model_name}')


        # At first executing the scripts and gathering the images
        new_dir_name = python_script_dir
        print(f'\n--------Pre executing scripts for the CLIMATE dataset, length of py scripts: {len(py_scripts)} ----------')
        png_files_only_file_name=[]
        for py_script in py_scripts:
            try:
                print(f'Pre executing script: {py_script}')
                script_path = py_scripts[py_script]
                status, stderr = run_python_script_for_evaluation(script_path, png_files_only_file_name, 'VTK')
                print(f'Success: {py_script}\n\n')
            except Exception as e:
                print(f'Error while pre executing scripts:{py_script} Error: {e}\n\n')
        
        # script_execution_base_path = "/Users/apukumarchakroborti/gsu_research/llam_test"
        data_dir_base_path = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
        target_dir_base_path = f"{data_dir_base_path}/vtk_python_scripts_experiment/error_categorization_evaluation_result"     
        
        subdirectories = [   
                            f'{python_script_dir}',
                            f'{data_dir_base_path}',
                            f'{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting'
                    ]
        
        subdirectories.append(FULL_PYTHON_SCRIPT_DIRECTORY)
        # source_dirs, script_execution_base_path, target_dir_base_path, new_dir_name
        utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name+f'_{iteration}')
        # should be updated
        # data_directory = f'/Users/apukumarchakroborti/gsu_research/adm_research_spring_2025/llms_generated_python_scripts/error_categorization_report/generated_image_from_running_evaluation/{new_dir_name}'
        data_directory = f'/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/vtk_python_scripts_experiment/error_categorization_evaluation_result/generated_image_from_running_evaluation/{new_dir_name}_{iteration}'
        print('Data Directory: \n', data_directory)
        
        png_files_from_main_script_dir = glob.glob(os.path.join(data_directory, "*.png"))
        
        
        print('All PNG files: \n', png_files_from_main_script_dir)
        png_files_only_file_name = []
        if len(png_files_from_main_script_dir)>0:
            for file in png_files_from_main_script_dir:
                names = file.split('/')
                png_files_only_file_name.append(names[len(names)-1])
        print('All PNG files with only file names: \n', png_files_only_file_name)

        for evaluation_script in next_evaluation_scritps:
            
            evaluation_python_script_file_base_name = os.path.basename(evaluation_script)
            print(f'\n\nRunning Script base name: {os.path.basename(evaluation_script)} ')
            
            evaluation_script_path = next_evaluation_scritps[evaluation_script]
            
            status, stderr = run_python_script_for_evaluation(evaluation_script_path, png_files_only_file_name, 'VTK')
            print(f'Execution result:\nstatus: {status}\nstderr: {stderr}')
        

            if status=='Pass':
                csv_map['Pass_Count'] = csv_map['Pass_Count'] +1
                print('Pass')
            else:
                print('Fail')
                csv_map['Fail_Count'] = csv_map['Fail_Count'] +1
                if stderr and len(stderr)>0:
                    # last_line_error = stderr.splitlines()
                    last_line_error = [line for line in stderr.splitlines() if line.strip()]

                    print(f'splitted error message: {last_line_error}')

                    last_line_error = last_line_error[len(last_line_error)-1]
                    print(f'last line error message: {last_line_error}')

                    category, error_message, error_message_details = conditional_categorize_error(last_line_error)
                    csv_map[category] = csv_map[category] +1
                    csv_map[error_message] = csv_map[error_message] +'\n'+ error_message_details

                else:
                    csv_map['Other_Errors_Count'] = csv_map['Other_Errors_Count'] + 1
        # out of for loop
        # save_errors_to_csv_with_default_report_file_name(csv_map, target_dir)
        iterative_save_errors_to_csv_with_default_report_file_name(csv_map, target_dir, iteration)
        utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name+f'_{iteration}')
        total_pass_count+= csv_map['Pass_Count']
        total_fail_count= csv_map['Fail_Count']
        total_Dataset_Paths_Related_Error_Count= csv_map['Dataset_Paths_Related_Error_Count'] 
        total_Attribute_Related_Error_Count= csv_map['Attribute_Related_Error_Count']
        total_Slicing_Related_Error_Count=csv_map['Slicing_Related_Error_Count']
        total_Other_Errors_Count=csv_map['Other_Errors_Count']
    
    error_count_data_map = {}
    # passed_scripts_without_iteration = 40 - total_pass_count - total_fail_count
    error_count_data_map['LLM_Model'] = model_name
    # error_count_data_map['Pass_Count'] = total_pass_count+passed_scripts_without_iteration
    error_count_data_map['Pass_Count'] = total_pass_count
    error_count_data_map['Fail_Count'] = total_fail_count
    error_count_data_map['Dataset_Paths_Related_Error_Count'] = total_Dataset_Paths_Related_Error_Count 
    error_count_data_map['Attribute_Related_Error_Count'] = total_Attribute_Related_Error_Count
    error_count_data_map['Slicing_Related_Error_Count'] = total_Slicing_Related_Error_Count
    error_count_data_map['Other_Errors_Count'] = total_Other_Errors_Count
    iterative_save_errors_to_csv_with_default_report_file_name(error_count_data_map, target_dir, -1)    
       
    #At the end move all data files to the generated script directory 
    utils.move_files_by_extension(target_base_dir, all_files_source_directory, extensions)    

def evaluation_of_ITERATIVE_CLIMATE_python_scripts_by_checking_generated_image(common_base_directory, target_dir, python_script_dir, model_name):
    FULL_PYTHON_SCRIPT_DIRECTORY = common_base_directory+"/"+python_script_dir
    print(f'evaluation_of_ITERATIVE_CLIMATE_python_scripts_by_checking_generated_image, FULL_PYTHON_SCRIPT_DIRECTORY: {FULL_PYTHON_SCRIPT_DIRECTORY}')

    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)    
   
    script_dir = python_script_dir
    print('common_directory: ', common_base_directory, '\n')
    print('python_script_dir: ', python_script_dir, '\n')
    print('script_dir: ', script_dir, '\n')

    directory_path =script_dir  # Replace with your actual directory
    
    
    total_scripts = 61
    total_pass_count = 0
    total_fail_count = 0
    total_Dataset_Paths_Related_Error_Count = 0
    total_Attribute_Related_Error_Count = 0
    total_Slicing_Related_Error_Count =0
    total_Other_Errors_Count =0
    
    num_iteration = 7
    for iteration in range(0, num_iteration):
    # for iteration in range(0, num_iteration):
        python_files_dict = get_iterative_python_files_dict(common_base_directory+"/"+directory_path, iteration)
        py_scripts = python_files_dict
        next_evaluation_scritps = python_files_dict
        print(f'All python scripts to be evaluated:\n{python_files_dict}')
        
        csv_map = {'LLM_Model': model_name,
                'Pass_Count': 0,
                'Fail_Count': 0, 
                'Dataset_Paths_Related_Error_Count': 0, 
                'Datasets_Paths_Related_Error_messages': '', 
                'Attribute_Related_Error_Count': 0, 
                'Attribute_Related_Error_messages': '',
                'Slicing_Related_Error_Count': 0, 
                'Slicing_Related_Error_messages': '', 
                'Other_Errors_Count': 0, 
                'Other_Errors_messages': ''
                }

        print(f'Evaluation model name: {model_name}')


        # At first executing the scripts and gathering the images
        new_dir_name = python_script_dir
        print(f'\n--------Pre executing scripts for the CLIMATE dataset, length of py scripts: {len(py_scripts)} ----------')
        png_files_only_file_name=[]
        for py_script in py_scripts:
            try:
                print(f'Pre executing script: {py_script}')
                script_path = py_scripts[py_script]
                status, stderr = run_python_script_for_evaluation(script_path, png_files_only_file_name, 'CLIMATE')
                print(f'Success: {py_script}\n\n')
            except Exception as e:
                print(f'Error while pre executing scripts:{py_script} Error: {e}\n\n')
        
        # script_execution_base_path = "/Users/apukumarchakroborti/gsu_research/llam_test"
        data_dir_base_path = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
        target_dir_base_path = f"{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag"    
        
        subdirectories = [      f'{data_dir_base_path}/ACL_DIRS/ASF',
                                f'{data_dir_base_path}/ACL_DIRS/AURA_DATA_VC',
                                f'{data_dir_base_path}/ACL_DIRS/GES_DISC',
                                f'{data_dir_base_path}/ACL_DIRS/ICESat_2',
                                f'{data_dir_base_path}/ACL_DIRS/LAADS',
                                f'{data_dir_base_path}/ACL_DIRS/LaRC',
                                f'{data_dir_base_path}/ACL_DIRS/LP_DAAC',
                                f'{data_dir_base_path}/ACL_DIRS/NSIDC',
                                f'{data_dir_base_path}/ACL_DIRS/PO_DAAC',
                                f'{data_dir_base_path}',
                                f'{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting'
                            ]
        subdirectories.append(FULL_PYTHON_SCRIPT_DIRECTORY)
        # source_dirs, script_execution_base_path, target_dir_base_path, new_dir_name
        utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name+f'_{iteration}')
        # should be updated
        # data_directory = f'/Users/apukumarchakroborti/gsu_research/adm_research_spring_2025/llms_generated_python_scripts/error_categorization_report/generated_image_from_running_evaluation/{new_dir_name}'
        data_directory = f'/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag/generated_image_from_running_evaluation/{new_dir_name}'+f'_{iteration}'
        print('Data Directory: \n', data_directory)
        
        png_files_from_main_script_dir = glob.glob(os.path.join(data_directory, "*.png"))
        
        
        print('All PNG files: \n', png_files_from_main_script_dir)
        png_files_only_file_name = []
        if len(png_files_from_main_script_dir)>0:
            for file in png_files_from_main_script_dir:
                names = file.split('/')
                png_files_only_file_name.append(names[len(names)-1])
        print('All PNG files with only file names: \n', png_files_only_file_name)

        for evaluation_script in next_evaluation_scritps:
            
            evaluation_python_script_file_base_name = os.path.basename(evaluation_script)
            print(f'\n\nRunning Script base name: {os.path.basename(evaluation_script)} ')
            
            evaluation_script_path = next_evaluation_scritps[evaluation_script]
            
            status, stderr = run_python_script_for_evaluation(evaluation_script_path, png_files_only_file_name, 'CLIMATE')
            print(f'Execution result:\nstatus: {status}\nstderr: {stderr}')
        

            if status=='Pass':
                csv_map['Pass_Count'] = csv_map['Pass_Count'] +1
                print('Pass')
            else:
                print('Fail')
                csv_map['Fail_Count'] = csv_map['Fail_Count'] +1
                if stderr and len(stderr)>0:
                    # last_line_error = stderr.splitlines()
                    last_line_error = [line for line in stderr.splitlines() if line.strip()]

                    print(f'splitted error message: {last_line_error}')

                    last_line_error = last_line_error[len(last_line_error)-1]
                    print(f'last line error message: {last_line_error}')

                    category, error_message, error_message_details = conditional_categorize_error(last_line_error)
                    csv_map[category] = csv_map[category] +1
                    csv_map[error_message] = csv_map[error_message] +'\n'+ error_message_details

                else:
                    csv_map['Other_Errors_Count'] = csv_map['Other_Errors_Count'] + 1
        # out of for loop
        # save_errors_to_csv_with_default_report_file_name(csv_map, target_dir)
        iterative_save_errors_to_csv_with_default_report_file_name(csv_map, target_dir, iteration)
        utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name+f'_{iteration}')
        
        total_pass_count+= csv_map['Pass_Count']
        total_fail_count= csv_map['Fail_Count']
        total_Dataset_Paths_Related_Error_Count= csv_map['Dataset_Paths_Related_Error_Count'] 
        total_Attribute_Related_Error_Count= csv_map['Attribute_Related_Error_Count']
        total_Slicing_Related_Error_Count=csv_map['Slicing_Related_Error_Count']
        total_Other_Errors_Count=csv_map['Other_Errors_Count']
    
    error_count_data_map = {}
    # passed_scripts_without_iteration = 40 - total_pass_count - total_fail_count
    error_count_data_map['LLM_Model'] = model_name
    # error_count_data_map['Pass_Count'] = total_pass_count+passed_scripts_without_iteration
    error_count_data_map['Pass_Count'] = total_pass_count
    error_count_data_map['Fail_Count'] = total_fail_count
    error_count_data_map['Dataset_Paths_Related_Error_Count'] = total_Dataset_Paths_Related_Error_Count 
    error_count_data_map['Attribute_Related_Error_Count'] = total_Attribute_Related_Error_Count
    error_count_data_map['Slicing_Related_Error_Count'] = total_Slicing_Related_Error_Count
    error_count_data_map['Other_Errors_Count'] = total_Other_Errors_Count
    iterative_save_errors_to_csv_with_default_report_file_name(error_count_data_map, target_dir, -1) 

def evaluation_of_ITERATIVE_MATPLOTAGENT_python_scripts_by_checking_generated_image(common_base_directory, target_dir, python_script_dir, model_name):
    FULL_PYTHON_SCRIPT_DIRECTORY = common_base_directory+"/"+python_script_dir
    print(f'evaluation_of_ITERATIVE_MATPLOTAGENT_python_scripts_by_checking_generated_image, FULL_PYTHON_SCRIPT_DIRECTORY: {FULL_PYTHON_SCRIPT_DIRECTORY}')

    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)    
   
    script_dir = python_script_dir
    print('common_directory: ', common_base_directory, '\n')
    print('python_script_dir: ', python_script_dir, '\n')
    print('script_dir: ', script_dir, '\n')

    directory_path =script_dir  # Replace with your actual directory
    
    
    total_scripts = 12
    total_pass_count = 0
    total_fail_count = 0
    total_Dataset_Paths_Related_Error_Count = 0
    total_Attribute_Related_Error_Count = 0
    total_Slicing_Related_Error_Count =0
    total_Other_Errors_Count =0
    
    num_iteration = 7
    for iteration in range(0, num_iteration):
    # for iteration in range(0, num_iteration):
        python_files_dict = get_iterative_python_files_dict(common_base_directory+"/"+directory_path, iteration)
        py_scripts = python_files_dict
        next_evaluation_scritps = python_files_dict
        print(f'All python scripts to be evaluated:\n{python_files_dict}')
        
        csv_map = {'LLM_Model': model_name,
                'Pass_Count': 0,
                'Fail_Count': 0, 
                'Dataset_Paths_Related_Error_Count': 0, 
                'Datasets_Paths_Related_Error_messages': '', 
                'Attribute_Related_Error_Count': 0, 
                'Attribute_Related_Error_messages': '',
                'Slicing_Related_Error_Count': 0, 
                'Slicing_Related_Error_messages': '', 
                'Other_Errors_Count': 0, 
                'Other_Errors_messages': ''
                }

        print(f'Evaluation model name: {model_name}')


        # At first executing the scripts and gathering the images
        new_dir_name = python_script_dir
        print(f'\n--------Pre executing scripts for the MATPLOTAGENT dataset, length of py scripts: {len(py_scripts)} ----------')
        png_files_only_file_name=[]
        for py_script in py_scripts:
            try:
                print(f'Pre executing script: {py_script}')
                script_path = py_scripts[py_script]
                status, stderr = run_python_script_for_evaluation(script_path, png_files_only_file_name, 'MATPLOTAGENT')
                print(f'Success: {py_script}\n\n')
            except Exception as e:
                print(f'Error while pre executing scripts:{py_script} Error: {e}\n\n')
        
        # script_execution_base_path = "/Users/apukumarchakroborti/gsu_research/llam_test"
        data_dir_base_path = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
        target_dir_base_path = f"{data_dir_base_path}/matplot_agent_data/plot_generation/error_categorization_evaluation_result/iterative_error_resolve"    
        
        subdirectories = [      f'{data_dir_base_path}/matplot_agent_data/plot_generation/csv_to_h5_data',
                                f'{data_dir_base_path}',
                                f'{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting'
                            ]
        subdirectories.append(FULL_PYTHON_SCRIPT_DIRECTORY)
        # source_dirs, script_execution_base_path, target_dir_base_path, new_dir_name
        utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name+f'_{iteration}')
        # should be updated
        # data_directory = f'/Users/apukumarchakroborti/gsu_research/adm_research_spring_2025/llms_generated_python_scripts/error_categorization_report/generated_image_from_running_evaluation/{new_dir_name}'
        data_directory = f'/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/matplot_agent_data/plot_generation/error_categorization_evaluation_result/iterative_error_resolve/generated_image_from_running_evaluation/{new_dir_name}'+f'_{iteration}'
        print('Data Directory: \n', data_directory)
        
        png_files_from_main_script_dir = glob.glob(os.path.join(data_directory, "*.png"))
        
        
        print('All PNG files: \n', png_files_from_main_script_dir)
        png_files_only_file_name = []
        if len(png_files_from_main_script_dir)>0:
            for file in png_files_from_main_script_dir:
                names = file.split('/')
                png_files_only_file_name.append(names[len(names)-1])
        print('All PNG files with only file names: \n', png_files_only_file_name)

        for evaluation_script in next_evaluation_scritps:
            
            evaluation_python_script_file_base_name = os.path.basename(evaluation_script)
            print(f'\n\nRunning Script base name: {os.path.basename(evaluation_script)} ')
            
            evaluation_script_path = next_evaluation_scritps[evaluation_script]
            
            status, stderr = run_python_script_for_evaluation(evaluation_script_path, png_files_only_file_name, 'MATPLOTAGENT')
            print(f'Execution result:\nstatus: {status}\nstderr: {stderr}')
        

            if status=='Pass':
                csv_map['Pass_Count'] = csv_map['Pass_Count'] +1
                print('Pass')
            else:
                print('Fail')
                csv_map['Fail_Count'] = csv_map['Fail_Count'] +1
                if stderr and len(stderr)>0:
                    # last_line_error = stderr.splitlines()
                    last_line_error = [line for line in stderr.splitlines() if line.strip()]

                    print(f'splitted error message: {last_line_error}')

                    last_line_error = last_line_error[len(last_line_error)-1]
                    print(f'last line error message: {last_line_error}')

                    category, error_message, error_message_details = conditional_categorize_error(last_line_error)
                    csv_map[category] = csv_map[category] +1
                    csv_map[error_message] = csv_map[error_message] +'\n'+ error_message_details

                else:
                    csv_map['Other_Errors_Count'] = csv_map['Other_Errors_Count'] + 1
        # out of for loop
        # save_errors_to_csv_with_default_report_file_name(csv_map, target_dir)
        iterative_save_errors_to_csv_with_default_report_file_name(csv_map, target_dir, iteration)
        utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name+f'_{iteration}')
        total_pass_count+= csv_map['Pass_Count']
        total_fail_count= csv_map['Fail_Count']
        total_Dataset_Paths_Related_Error_Count= csv_map['Dataset_Paths_Related_Error_Count'] 
        total_Attribute_Related_Error_Count= csv_map['Attribute_Related_Error_Count']
        total_Slicing_Related_Error_Count=csv_map['Slicing_Related_Error_Count']
        total_Other_Errors_Count=csv_map['Other_Errors_Count']
    
    error_count_data_map = {}
    # passed_scripts_without_iteration = 40 - total_pass_count - total_fail_count
    error_count_data_map['LLM_Model'] = model_name
    # error_count_data_map['Pass_Count'] = total_pass_count+passed_scripts_without_iteration
    error_count_data_map['Pass_Count'] = total_pass_count
    error_count_data_map['Fail_Count'] = total_fail_count
    error_count_data_map['Dataset_Paths_Related_Error_Count'] = total_Dataset_Paths_Related_Error_Count 
    error_count_data_map['Attribute_Related_Error_Count'] = total_Attribute_Related_Error_Count
    error_count_data_map['Slicing_Related_Error_Count'] = total_Slicing_Related_Error_Count
    error_count_data_map['Other_Errors_Count'] = total_Other_Errors_Count
    iterative_save_errors_to_csv_with_default_report_file_name(error_count_data_map, target_dir, -1)    

def evaluation_of_ITERATIVE_FASTMRIBRAIN_python_scripts_by_checking_generated_image(common_base_directory, target_dir, python_script_dir, model_name):
    FULL_PYTHON_SCRIPT_DIRECTORY = common_base_directory+"/"+python_script_dir
    print(f'evaluation_of_ITERATIVE_FASTMRIBRAIN_python_scripts_by_checking_generated_image, FULL_PYTHON_SCRIPT_DIRECTORY: {FULL_PYTHON_SCRIPT_DIRECTORY}')

    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)    
   
    script_dir = python_script_dir
    print('common_directory: ', common_base_directory, '\n')
    print('python_script_dir: ', python_script_dir, '\n')
    print('script_dir: ', script_dir, '\n')

    directory_path =script_dir  # Replace with your actual directory
    
    
    
    
    total_scripts = 11
    total_pass_count = 0
    total_fail_count = 0
    total_Dataset_Paths_Related_Error_Count = 0
    total_Attribute_Related_Error_Count = 0
    total_Slicing_Related_Error_Count =0
    total_Other_Errors_Count =0
    
    
    num_iteration = 7
    for iteration in range(0, num_iteration):
    # for iteration in range(0, num_iteration):
        python_files_dict = get_iterative_python_files_dict(common_base_directory+"/"+directory_path, iteration)
        py_scripts = python_files_dict
        next_evaluation_scritps = python_files_dict
        print(f'All python scripts to be evaluated:\n{python_files_dict}')
        
        csv_map = {'LLM_Model': model_name,
                'Pass_Count': 0,
                'Fail_Count': 0, 
                'Dataset_Paths_Related_Error_Count': 0, 
                'Datasets_Paths_Related_Error_messages': '', 
                'Attribute_Related_Error_Count': 0, 
                'Attribute_Related_Error_messages': '',
                'Slicing_Related_Error_Count': 0, 
                'Slicing_Related_Error_messages': '', 
                'Other_Errors_Count': 0, 
                'Other_Errors_messages': ''
                }

        print(f'Evaluation model name: {model_name}')


        # At first executing the scripts and gathering the images
        new_dir_name = python_script_dir
        print(f'\n--------Pre executing scripts for the MATPLOTAGENT dataset, length of py scripts: {len(py_scripts)} ----------')
        png_files_only_file_name=[]
        for py_script in py_scripts:
            try:
                print(f'Pre executing script: {py_script}')
                script_path = py_scripts[py_script]
                status, stderr = run_python_script_for_evaluation(script_path, png_files_only_file_name, 'FASTMRIBRAIN')
                print(f'Success: {py_script}\n\n')
            except Exception as e:
                print(f'Error while pre executing scripts:{py_script} Error: {e}\n\n')
        
        # script_execution_base_path = "/Users/apukumarchakroborti/gsu_research/llam_test"
        data_dir_base_path = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
        target_dir_base_path = f"{data_dir_base_path}/mri_nyu_data/error_categorization_evaluation_result/iterative_evaluation_results"    
        
        subdirectories = [  f'{data_dir_base_path}/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5',
                            f'{data_dir_base_path}',
                            f'{data_dir_base_path}/prompting_techniques/zero_shot_sci_data_prompting'
                        ]
        subdirectories.append(FULL_PYTHON_SCRIPT_DIRECTORY)
        # source_dirs, script_execution_base_path, target_dir_base_path, new_dir_name
        utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name+f'_{iteration}')
        # should be updated
        # data_directory = f'/Users/apukumarchakroborti/gsu_research/adm_research_spring_2025/llms_generated_python_scripts/error_categorization_report/generated_image_from_running_evaluation/{new_dir_name}'
        data_directory = f'/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/mri_nyu_data/error_categorization_evaluation_result/iterative_evaluation_results/generated_image_from_running_evaluation/{new_dir_name}'+f'_{iteration}'
        print('Data Directory: \n', data_directory)
        
        png_files_from_main_script_dir = glob.glob(os.path.join(data_directory, "*.png"))
        
        
        print('All PNG files: \n', png_files_from_main_script_dir)
        png_files_only_file_name = []
        if len(png_files_from_main_script_dir)>0:
            for file in png_files_from_main_script_dir:
                names = file.split('/')
                png_files_only_file_name.append(names[len(names)-1])
        print('All PNG files with only file names: \n', png_files_only_file_name)

        for evaluation_script in next_evaluation_scritps:
            
            evaluation_python_script_file_base_name = os.path.basename(evaluation_script)
            print(f'\n\nRunning Script base name: {os.path.basename(evaluation_script)} ')
            
            evaluation_script_path = next_evaluation_scritps[evaluation_script]
            
            status, stderr = run_python_script_for_evaluation(evaluation_script_path, png_files_only_file_name, 'FASTMRIBRAIN')
            print(f'Execution result:\nstatus: {status}\nstderr: {stderr}')
        

            if status=='Pass':
                csv_map['Pass_Count'] = csv_map['Pass_Count'] +1
                print('Pass')
            else:
                print('Fail')
                csv_map['Fail_Count'] = csv_map['Fail_Count'] +1
                if stderr and len(stderr)>0:
                    # last_line_error = stderr.splitlines()
                    last_line_error = [line for line in stderr.splitlines() if line.strip()]

                    print(f'splitted error message: {last_line_error}')

                    last_line_error = last_line_error[len(last_line_error)-1]
                    print(f'last line error message: {last_line_error}')

                    category, error_message, error_message_details = conditional_categorize_error(last_line_error)
                    csv_map[category] = csv_map[category] +1
                    csv_map[error_message] = csv_map[error_message] +'\n'+ error_message_details

                else:
                    csv_map['Other_Errors_Count'] = csv_map['Other_Errors_Count'] + 1
        # out of for loop
        # save_errors_to_csv_with_default_report_file_name(csv_map, target_dir)
        iterative_save_errors_to_csv_with_default_report_file_name(csv_map, target_dir, iteration)
        utils.collect_and_store_png_without_data_dir(subdirectories, target_dir_base_path, new_dir_name+f'_{iteration}')

        total_pass_count+= csv_map['Pass_Count']
        total_fail_count= csv_map['Fail_Count']
        total_Dataset_Paths_Related_Error_Count= csv_map['Dataset_Paths_Related_Error_Count'] 
        total_Attribute_Related_Error_Count= csv_map['Attribute_Related_Error_Count']
        total_Slicing_Related_Error_Count=csv_map['Slicing_Related_Error_Count']
        total_Other_Errors_Count=csv_map['Other_Errors_Count']
    
    error_count_data_map = {}
    # passed_scripts_without_iteration = 40 - total_pass_count - total_fail_count
    error_count_data_map['LLM_Model'] = model_name
    # error_count_data_map['Pass_Count'] = total_pass_count+passed_scripts_without_iteration
    error_count_data_map['Pass_Count'] = total_pass_count
    error_count_data_map['Fail_Count'] = total_fail_count
    error_count_data_map['Dataset_Paths_Related_Error_Count'] = total_Dataset_Paths_Related_Error_Count 
    error_count_data_map['Attribute_Related_Error_Count'] = total_Attribute_Related_Error_Count
    error_count_data_map['Slicing_Related_Error_Count'] = total_Slicing_Related_Error_Count
    error_count_data_map['Other_Errors_Count'] = total_Other_Errors_Count
    iterative_save_errors_to_csv_with_default_report_file_name(error_count_data_map, target_dir, -1) 



if __name__ == "__main__":
    
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Select models to use correct LLM model")
    model, model_name, dataset, is_rag, URL, is_errors, with_corrector, is_online_search = argumentParsar.parse_argument(parser)  
    
    # this is for the macOS
    # common_base_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'
    
    # for the GSU sevrer
    common_base_directory = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
    
    python_script_dir = ''
    output_file = ''

    iterative_error_resolve = False

    # without corrector
    print('Inside With corrector ...\n')
    if dataset == 'CLIMATE_RAG_IMAGE':
        llm_generated_python_scripts_ase_directory = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/llm_rag_generated_python_scripts'
        list_of_python_scripts_sub_dirs = [
            # done
            "devstral_24b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector", #0
            "devstral_24b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector", #1
            "devstral_24b_python_scripts_without_rag_with_errors_without_corrector", #2
            "devstral_24b_python_scripts_without_rag_with_errors_with_corrector", # 3

            "devstral_24b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector", #4
            "devstral_24b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector", #5
            "devstral_24b_python_scripts_without_rag_without_corrector", #6
            "devstral_24b_python_scripts_without_rag_with_corrector", #7
            # done
            "gemma3_27b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector", #8
            "gemma3_27b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector", #9
            "gemma3_27b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector", #10
            "gemma3_27b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector", #11

            "gemma3_27b_python_scripts_without_rag_with_errors_without_corrector", #12
            "gemma3_27b_python_scripts_without_rag_with_errors_with_corrector", # 13
            "gemma3_27b_python_scripts_without_rag_without_corrector", #14
            "gemma3_27b_python_scripts_without_rag_with_corrector", #15
            # done
            "magicoder_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector", #16
            "magicoder_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector", #17
            "magicoder_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector", #18
            "magicoder_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector", #19

            "magicoder_python_scripts_without_rag_with_errors_without_corrector", #20
            "magicoder_python_scripts_without_rag_with_errors_with_corrector", # 21       
            "magicoder_python_scripts_without_rag_without_corrector", #22
            "magicoder_python_scripts_without_rag_with_corrector", #23
    
            # 
            "llama3_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector", #24
            "llama3_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector", #25 done
            "llama3_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector", #26 done
            "llama3_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector", #27 done

            "llama3_70b_python_scripts_without_rag_with_errors_without_corrector", #28 done
            "llama3_70b_python_scripts_without_rag_with_errors_with_corrector", #29 done         
            "llama3_70b_python_scripts_without_rag_without_corrector", #30 done
            "llama3_70b_python_scripts_without_rag_with_corrector", #31 done
            # 
            "deepseek_r1_32b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector", #32
            "deepseek_r1_32b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector", #33
            "deepseek_r1_32b_python_scripts_without_rag_with_errors_without_corrector", #34
            "deepseek_r1_32b_python_scripts_without_rag_with_errors_with_corrector", # 35

            "deepseek_r1_32b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector", #36
            "deepseek_r1_32b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector", #37
            "deepseek_r1_32b_python_scripts_without_rag_without_corrector", #38
            "deepseek_r1_32b_python_scripts_without_rag_with_corrector" #39  
        ]
        
        target_base_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
        for index in [23]:
        # for index in range(32, 40):
        # for index in range(0, 8):
            # current expert queries
            python_script_dir = list_of_python_scripts_sub_dirs[index]
            
            if python_script_dir.startswith('deepseek_r1_32b'):
                model_name = 'deepseek_r1_32b'
            elif python_script_dir.startswith('deepseek_r1_70b'):
                model_name = 'deepseek_r1_70b'
            elif python_script_dir.startswith('llama3_70b'):
                model_name = 'llama3_70b'
            elif python_script_dir.startswith('magicoder'):
                model_name = 'magicoder'
            elif python_script_dir.startswith('gemma3_27b'):
                model_name = 'gemma3_27b'
            elif python_script_dir.startswith('devstral_24b'):
                model_name = 'devstral_24b'
            elif python_script_dir.startswith('qwen3_32b'):
                model_name = 'qwen3_32b'
                
            
            # target_dir =f'{common_base_directory}/llms_generated_python_scripts/error_categorization_report/{python_script_dir}'
            target_dir =f'{target_base_dir}/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag/{python_script_dir}' 
            evaluation_of_CLIMATE_python_scripts_by_checking_generated_image(llm_generated_python_scripts_ase_directory, target_dir, python_script_dir, model_name)
    
    # MATPLOTAGENT DATASETS
    elif dataset == 'MATPLOTAGENT_RAG_IMAGE':
        print('Evaluating python scripts from the MATPLOTAGENT_RAG_IMAGE ...')
                    
        llm_generated_python_scripts_ase_directory = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/matplot_agent_data/plot_generation/llm_rag_generated_python_scripts'
        
        list_of_python_scripts_sub_dirs = [
            "deepseek_r1_32b_matplotagent_python_scripts_with_rag_with_corrector", #0
            "deepseek_r1_32b_matplotagent_python_scripts_with_rag_with_errors_with_corrector", #1
            "deepseek_r1_32b_matplotagent_python_scripts_with_rag_with_errors_without_corrector", #2
            "deepseek_r1_32b_matplotagent_python_scripts_with_rag_without_corrector", #3
            "deepseek_r1_32b_matplotagent_python_scripts_without_rag_with_corrector", #4
            "deepseek_r1_32b_matplotagent_python_scripts_without_rag_with_errors_with_corrector", #6
            "deepseek_r1_32b_matplotagent_python_scripts_without_rag_with_errors_without_corrector", #5            
            "deepseek_r1_32b_matplotagent_python_scripts_without_rag_without_corrector", #7
            
            # 
            "devstral_24b_matplotagent_python_scripts_with_rag_with_corrector", #8
            "devstral_24b_matplotagent_python_scripts_with_rag_with_errors_with_corrector", #9
            "devstral_24b_matplotagent_python_scripts_with_rag_with_errors_without_corrector", #10
            "devstral_24b_matplotagent_python_scripts_with_rag_without_corrector", #11
            "devstral_24b_matplotagent_python_scripts_without_rag_with_corrector", #12
            "devstral_24b_matplotagent_python_scripts_without_rag_with_errors_with_corrector", #13
            "devstral_24b_matplotagent_python_scripts_without_rag_with_errors_without_corrector", #14            
            "devstral_24b_matplotagent_python_scripts_without_rag_without_corrector", #15
            # 
            "gemma3_27b_matplotagent_python_scripts_with_rag_with_corrector", #16
            "gemma3_27b_matplotagent_python_scripts_with_rag_with_errors_with_corrector", #17
            "gemma3_27b_matplotagent_python_scripts_with_rag_with_errors_without_corrector", #18
            "gemma3_27b_matplotagent_python_scripts_with_rag_without_corrector", #19
            "gemma3_27b_matplotagent_python_scripts_without_rag_with_corrector", #20
            "gemma3_27b_matplotagent_python_scripts_without_rag_with_errors_with_corrector", #21
            "gemma3_27b_matplotagent_python_scripts_without_rag_with_errors_without_corrector", #22            
            "gemma3_27b_matplotagent_python_scripts_without_rag_without_corrector", #23
            #
            "llama3_70b_matplotagent_python_scripts_with_rag_with_corrector", #24
            "llama3_70b_matplotagent_python_scripts_with_rag_with_errors_with_corrector", #25
            "llama3_70b_matplotagent_python_scripts_with_rag_with_errors_without_corrector", #26
            "llama3_70b_matplotagent_python_scripts_with_rag_without_corrector", #27
            "llama3_70b_matplotagent_python_scripts_without_rag_with_corrector", #28
            "llama3_70b_matplotagent_python_scripts_without_rag_with_errors_with_corrector", #29
            "llama3_70b_matplotagent_python_scripts_without_rag_with_errors_without_corrector", #30            
            "llama3_70b_matplotagent_python_scripts_without_rag_without_corrector", #31
            # 
            "magicoder_matplotagent_python_scripts_with_rag_with_corrector", #32
            "magicoder_matplotagent_python_scripts_with_rag_with_errors_with_corrector", #33
            "magicoder_matplotagent_python_scripts_with_rag_with_errors_without_corrector", #34
            "magicoder_matplotagent_python_scripts_with_rag_without_corrector", #35
            "magicoder_matplotagent_python_scripts_without_rag_with_corrector", #36
            "magicoder_matplotagent_python_scripts_without_rag_with_errors_with_corrector", #37
            "magicoder_matplotagent_python_scripts_without_rag_with_errors_without_corrector", #38            
            "magicoder_matplotagent_python_scripts_without_rag_without_corrector", #39

        ]
        
        target_base_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
        # for index in [8, 11, 12, 15 ]:
        # for index in [32, 35, 36, 39 ]:
        for index in [24, 27, 28, 31]:
        # for index in range(0, 40):
        # for index in [0, 1, 2, 3, 4, 5, 6, 7, 20, 21, 22, 23, 36, 37, 38, 39]:
        # for index in range(8, 11):
        # for index in range(16, 24):
            # current expert queries
            python_script_dir = list_of_python_scripts_sub_dirs[index]
            
            if python_script_dir.startswith('deepseek_r1_32b'):
                model_name = 'deepseek_r1_32b'
            elif python_script_dir.startswith('deepseek_r1_70b'):
                model_name = 'deepseek_r1_70b'
            elif python_script_dir.startswith('llama3_70b'):
                model_name = 'llama3_70b'
            elif python_script_dir.startswith('magicoder'):
                model_name = 'magicoder'
            elif python_script_dir.startswith('gemma3_27b'):
                model_name = 'gemma3_27b'
            elif python_script_dir.startswith('devstral_24b'):
                model_name = 'devstral_24b'
            elif python_script_dir.startswith('qwen3_32b'):
                model_name = 'qwen3_32b'
                
            
            # target_dir =f'{common_base_directory}/llms_generated_python_scripts/error_categorization_report/{python_script_dir}'
            target_dir =f'{target_base_dir}/matplot_agent_data/plot_generation/error_categorization_evaluation_result/llm_generated_code_with_rag/{python_script_dir}' 
            evaluation_of_MATPLOTAGENT_python_scripts_by_checking_generated_image(llm_generated_python_scripts_ase_directory, target_dir, python_script_dir, model_name)
    
    elif dataset == 'FASTMRIBRAIN_RAG_IMAGE':                    
        llm_generated_python_scripts_ase_directory = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/mri_nyu_data/llm_rag_generated_python_scripts'
        
        list_of_python_scripts_sub_dirs = [
            "deepseek_r1_32b_fastmribrain_python_scripts_with_rag_with_corrector", #0
            "deepseek_r1_32b_fastmribrain_python_scripts_with_rag_with_errors_with_corrector", #1
            "deepseek_r1_32b_fastmribrain_python_scripts_with_rag_with_errors_without_corrector", #2
            "deepseek_r1_32b_fastmribrain_python_scripts_with_rag_without_corrector", #3
            "deepseek_r1_32b_fastmribrain_python_scripts_without_rag_with_corrector", #4
            "deepseek_r1_32b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector", #6
            "deepseek_r1_32b_fastmribrain_python_scripts_without_rag_with_errors_without_corrector", #5            
            "deepseek_r1_32b_fastmribrain_python_scripts_without_rag_without_corrector", #7
            
            # 
            "devstral_24b_fastmribrain_python_scripts_with_rag_with_corrector", #8
            "devstral_24b_fastmribrain_python_scripts_with_rag_with_errors_with_corrector", #1
            "devstral_24b_fastmribrain_python_scripts_with_rag_with_errors_without_corrector", #2
            "devstral_24b_fastmribrain_python_scripts_with_rag_without_corrector", #3
            "devstral_24b_fastmribrain_python_scripts_without_rag_with_corrector", #4
            "devstral_24b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector", #6
            "devstral_24b_fastmribrain_python_scripts_without_rag_with_errors_without_corrector", #5            
            "devstral_24b_fastmribrain_python_scripts_without_rag_without_corrector", #15
            # 
           "gemma3_27b_fastmribrain_python_scripts_with_rag_with_corrector", #16
            "gemma3_27b_fastmribrain_python_scripts_with_rag_with_errors_with_corrector", #17
            "gemma3_27b_fastmribrain_python_scripts_with_rag_with_errors_without_corrector", #18
            "gemma3_27b_fastmribrain_python_scripts_with_rag_without_corrector", #19
            "gemma3_27b_fastmribrain_python_scripts_without_rag_with_corrector", #20
            "gemma3_27b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector", #21
            "gemma3_27b_fastmribrain_python_scripts_without_rag_with_errors_without_corrector", #22            
            "gemma3_27b_fastmribrain_python_scripts_without_rag_without_corrector", #23
            #
            "llama3_70b_fastmribrain_python_scripts_with_rag_with_corrector", #24
            "llama3_70b_fastmribrain_python_scripts_with_rag_with_errors_with_corrector", #25
            "llama3_70b_fastmribrain_python_scripts_with_rag_with_errors_without_corrector", #26
            "llama3_70b_fastmribrain_python_scripts_with_rag_without_corrector", #27
            "llama3_70b_fastmribrain_python_scripts_without_rag_with_corrector", #28
            "llama3_70b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector", #29
            "llama3_70b_fastmribrain_python_scripts_without_rag_with_errors_without_corrector", #30            
            "llama3_70b_fastmribrain_python_scripts_without_rag_without_corrector", #31
            # 
            "magicoder_fastmribrain_python_scripts_with_rag_with_corrector", #32
            "magicoder_fastmribrain_python_scripts_with_rag_with_errors_with_corrector", #33
            "magicoder_fastmribrain_python_scripts_with_rag_with_errors_without_corrector", #34
            "magicoder_fastmribrain_python_scripts_with_rag_without_corrector", #35
            "magicoder_fastmribrain_python_scripts_without_rag_with_corrector", #36
            "magicoder_fastmribrain_python_scripts_without_rag_with_errors_with_corrector", #37
            "magicoder_fastmribrain_python_scripts_without_rag_with_errors_without_corrector", #38            
            "magicoder_fastmribrain_python_scripts_without_rag_without_corrector" #39
        ]
        
        target_base_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
        # gemma3
        for index in range(0, 40):
        # for index in [16, 17, 18, 19, 32, 33, 34, 35]:
        # for index in [16, 17, 18, 19, 32, 33, 34, 35]:
        # for index in range(8, 16):
        # for index in range(16, 24):
            # current expert queries
            python_script_dir = list_of_python_scripts_sub_dirs[index]
            
            if python_script_dir.startswith('deepseek_r1_32b'):
                model_name = 'deepseek_r1_32b'
            # elif python_script_dir.startswith('deepseek_r1_70b'):
            #     model_name = 'deepseek_r1_70b'
            elif python_script_dir.startswith('llama3_70b'):
                model_name = 'llama3_70b'
            elif python_script_dir.startswith('magicoder'):
                model_name = 'magicoder'
            elif python_script_dir.startswith('gemma3_27b'):
                model_name = 'gemma3_27b'
            elif python_script_dir.startswith('devstral_24b'):
                model_name = 'devstral_24b'
            # elif python_script_dir.startswith('qwen3_32b'):
            #     model_name = 'qwen3_32b'                
            
            # target_dir =f'{common_base_directory}/llms_generated_python_scripts/error_categorization_report/{python_script_dir}'
            # target_dir =f'{target_base_dir}/mri_nyu_data/error_categorization_evaluation_result/llm_generated_code_with_rag/{python_script_dir}'
            target_dir =f'{target_base_dir}/mri_nyu_data/error_categorization_evaluation_result/non_iterative_evaluation_results/{python_script_dir}' 
            evaluation_of_FASTMRIBRAIN_python_scripts_by_checking_generated_image(llm_generated_python_scripts_ase_directory, target_dir, python_script_dir, model_name)

    elif dataset == 'VTK_RAG_IMAGE':                    
        llm_generated_python_scripts_ase_directory = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/vtk_python_scripts_experiment/llm_rag_generated_python_scripts'
        
        list_of_python_scripts_sub_dirs = [
            # "deepseek_r1_70b_vtk_python_scripts_without_rag_without_corrector",
            "devstral_24b_vtk_python_scripts_without_rag_without_corrector"
            # "devstral_24b_vtk_python_scripts_without_rag_without_corrector" #0
            # "devstral_24b_vtk_python_scripts_without_rag_with_errors_without_corrector" #1                    
        ]
        
        target_base_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
        all_files_source_directory = f'{target_base_dir}/vtk_data'
        # for index in range(0, 40):
        for index in [0]:
        # for index in [16, 17, 18, 19, 32, 33, 34, 35]:
        # for index in range(8, 16):
        # for index in range(16, 24):
            # current expert queries
            python_script_dir = list_of_python_scripts_sub_dirs[index]
            
            if python_script_dir.startswith('deepseek_r1_32b'):
                model_name = 'deepseek_r1_32b'
            elif python_script_dir.startswith('deepseek_r1_70b'):
                model_name = 'deepseek_r1_70b'
            elif python_script_dir.startswith('llama3_70b'):
                model_name = 'llama3_70b'
            elif python_script_dir.startswith('magicoder'):
                model_name = 'magicoder'
            elif python_script_dir.startswith('gemma3_27b'):
                model_name = 'gemma3_27b'
            elif python_script_dir.startswith('devstral_24b'):
                model_name = 'devstral_24b'
            # elif python_script_dir.startswith('qwen3_32b'):
            #     model_name = 'qwen3_32b'                
            
            # target_dir =f'{common_base_directory}/llms_generated_python_scripts/error_categorization_report/{python_script_dir}'
            target_dir =f'{target_base_dir}/vtk_python_scripts_experiment/error_categorization_evaluation_result/{python_script_dir}' 
            evaluation_of_VTK_python_scripts_by_checking_generated_image(llm_generated_python_scripts_ase_directory, target_dir, python_script_dir, model_name, all_files_source_directory, target_base_dir)
    
    elif dataset == 'ITERATIVE_ERROR_RESOLVE_VTK_RAG_IMAGE':                    
        target_base_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'

        llm_generated_python_scripts_ase_directory = f'{target_base_dir}/vtk_python_scripts_experiment/llm_rag_generated_python_scripts'
        
        list_of_python_scripts_sub_dirs = [
            # "devstral_24b_vtk_iterative_python_scripts_without_rag_without_corrector"
            # "devstral_24b_vtk_iterative_python_scripts_without_rag_with_errors_without_corrector",
            # "gemma3_27b_vtk_iterative_python_scripts_without_rag_without_corrector",
            "deepseek_r1_32b_vtk_iterative_python_scripts_without_rag_without_corrector",
            "llama3_70b_vtk_iterative_python_scripts_without_rag_without_corrector",
            "magicoder_vtk_iterative_python_scripts_without_rag_without_corrector"                  
        ]
        
        all_files_source_directory = f'{target_base_dir}/vtk_data'
        
        # for index in range(0, 40):
        for index in [0, 1, 2]:
            # current expert queries
            python_script_dir = list_of_python_scripts_sub_dirs[index]            
            if python_script_dir.startswith('deepseek_r1_32b'):
                model_name = 'deepseek_r1_32b'
            elif python_script_dir.startswith('deepseek_r1_70b'):
                model_name = 'deepseek_r1_70b'
            elif python_script_dir.startswith('llama3_70b'):
                model_name = 'llama3_70b'
            elif python_script_dir.startswith('magicoder'):
                model_name = 'magicoder'
            elif python_script_dir.startswith('gemma3_27b'):
                model_name = 'gemma3_27b'
            elif python_script_dir.startswith('devstral_24b'):
                model_name = 'devstral_24b'             
            
            # target_dir =f'{common_base_directory}/llms_generated_python_scripts/error_categorization_report/{python_script_dir}'
            target_dir =f'{target_base_dir}/vtk_python_scripts_experiment/error_categorization_evaluation_result/{python_script_dir}'
            #                                                                       common_base_directory, target_dir, python_script_dir, model_name 
            evaluation_of_ITERATIVE_VTK_python_scripts_by_checking_generated_image(llm_generated_python_scripts_ase_directory, target_dir, python_script_dir, model_name, all_files_source_directory, target_base_dir)
    

    if dataset == 'ITERATIVE_CLIMATE_RAG_IMAGE':
                    
        llm_generated_python_scripts_ase_directory = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/prompting_techniques/zero_shot_sci_data_prompting/python-script-output'
        
        list_of_python_scripts_sub_dirs = [
            "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_corrector", #0#
            "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_with_corrector", #1#
            "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_without_corrector", #2#
            "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_without_corrector", #3#
            "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_corrector", #4#
            "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_with_corrector", #5
            "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_without_corrector", #6
            "devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_without_corrector" #7#
        ]
        
        target_base_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
        # for index in [0]:
            # current expert queries
        # python_script_dir = list_of_python_scripts_sub_dirs[index]
        python_script_dir = ''

        if is_rag == True:
            # with rag
            # without error
            if is_errors==False:
                python_script_dir = list_of_python_scripts_sub_dirs[3]
                if with_corrector == True:
                    python_script_dir = list_of_python_scripts_sub_dirs[0]

            # with errors
            else:
                python_script_dir = list_of_python_scripts_sub_dirs[2]
                if with_corrector == True:
                    python_script_dir = list_of_python_scripts_sub_dirs[1]
        else:
            # without rag
            # without errors
            if is_errors==False:
                python_script_dir = list_of_python_scripts_sub_dirs[7]
                if with_corrector == True:
                    python_script_dir = list_of_python_scripts_sub_dirs[4]
            # with errors
            else:
                python_script_dir = list_of_python_scripts_sub_dirs[6]
                if with_corrector == True:
                    python_script_dir = list_of_python_scripts_sub_dirs[5]

        if python_script_dir.startswith('deepseek_r1_32b'):
            model_name = 'deepseek_r1_32b'
        elif python_script_dir.startswith('deepseek_r1_70b'):
            model_name = 'deepseek_r1_70b'
        elif python_script_dir.startswith('llama3_70b'):
            model_name = 'llama3_70b'
        elif python_script_dir.startswith('magicoder'):
            model_name = 'magicoder'
        elif python_script_dir.startswith('gemma3_27b'):
            model_name = 'gemma3_27b'
        elif python_script_dir.startswith('devstral_24b'):
            model_name = 'devstral_24b'
        elif python_script_dir.startswith('qwen3_32b'):
            model_name = 'qwen3_32b'
                
            
        # target_dir =f'{common_base_directory}/llms_generated_python_scripts/error_categorization_report/{python_script_dir}'
        target_dir =f'{target_base_dir}/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag/{python_script_dir}' 
        evaluation_of_ITERATIVE_CLIMATE_python_scripts_by_checking_generated_image(llm_generated_python_scripts_ase_directory, target_dir, python_script_dir, model_name)
    
    if dataset == 'ITERATIVE_MATPLOTAGENT_RAG_IMAGE':
                    
        llm_generated_python_scripts_ase_directory = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/matplot_agent_data/plot_generation/llm_rag_generated_python_scripts'
        
        list_of_python_scripts_sub_dirs = [
            "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_corrector",
            "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_with_corrector",
            "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_without_corrector",
            "devstral_24b_matplotagent_iterative_python_scripts_with_rag_without_corrector",
            "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_corrector",
            "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_errors_with_corrector",
            "devstral_24b_matplotagent_iterative_python_scripts_without_rag_with_errors_without_corrector",
            "devstral_24b_matplotagent_iterative_python_scripts_without_rag_without_corrector"
        ]
        
        target_base_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
        for index in range(0, 8):
            # current expert queries
            python_script_dir = list_of_python_scripts_sub_dirs[index]
            
            if python_script_dir.startswith('deepseek_r1_32b'):
                model_name = 'deepseek_r1_32b'
            elif python_script_dir.startswith('deepseek_r1_70b'):
                model_name = 'deepseek_r1_70b'
            elif python_script_dir.startswith('llama3_70b'):
                model_name = 'llama3_70b'
            elif python_script_dir.startswith('magicoder'):
                model_name = 'magicoder'
            elif python_script_dir.startswith('gemma3_27b'):
                model_name = 'gemma3_27b'
            elif python_script_dir.startswith('devstral_24b'):
                model_name = 'devstral_24b'
            elif python_script_dir.startswith('qwen3_32b'):
                model_name = 'qwen3_32b'
                
            # target directory to store results
            target_dir = f'{target_base_dir}/matplot_agent_data/plot_generation/error_categorization_evaluation_result/iterative_error_resolve/{python_script_dir}' 
            evaluation_of_ITERATIVE_MATPLOTAGENT_python_scripts_by_checking_generated_image(llm_generated_python_scripts_ase_directory, target_dir, python_script_dir, model_name)
   
    # -------------------------------ITERATIVE_FASTMRIBRAIN_RAG_IMAGE -------------------------------
    if dataset == 'ITERATIVE_FASTMRIBRAIN_RAG_IMAGE':
                    
        llm_generated_python_scripts_ase_directory = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/mri_nyu_data/llm_rag_generated_python_scripts'
        
        list_of_python_scripts_sub_dirs = [
            "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_corrector",
            "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_errors_with_corrector",
            "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_errors_without_corrector",
            "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_without_corrector",
            "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_corrector",
            "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_errors_with_corrector",
            "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_with_errors_without_corrector",
            "devstral_24b_fastmribrain_iterative_python_scripts_without_rag_without_corrector"
        ]
        
        target_base_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
        for index in range(0, 8):
            # current expert queries
            python_script_dir = list_of_python_scripts_sub_dirs[index]
            
            if python_script_dir.startswith('deepseek_r1_32b'):
                model_name = 'deepseek_r1_32b'
            elif python_script_dir.startswith('deepseek_r1_70b'):
                model_name = 'deepseek_r1_70b'
            elif python_script_dir.startswith('llama3_70b'):
                model_name = 'llama3_70b'
            elif python_script_dir.startswith('magicoder'):
                model_name = 'magicoder'
            elif python_script_dir.startswith('gemma3_27b'):
                model_name = 'gemma3_27b'
            elif python_script_dir.startswith('devstral_24b'):
                model_name = 'devstral_24b'
            elif python_script_dir.startswith('qwen3_32b'):
                model_name = 'qwen3_32b'
                
            
            target_dir =f'{target_base_dir}/mri_nyu_data/error_categorization_evaluation_result/iterative_evaluation_results/{python_script_dir}' 
            evaluation_of_ITERATIVE_FASTMRIBRAIN_python_scripts_by_checking_generated_image(llm_generated_python_scripts_ase_directory, target_dir, python_script_dir, model_name)
