import os
import glob
import re
import requests
import json
import os
import sys
import json
import argparse

from common_util_script import DataSummarizer as dataSummarizer
from common_util_script import LLMRequester as llmRequester
from common_util_script import Utils as utils
import tracking as tracking
import experiment_main.data_disambiguator as corrector

from common_util_script import ArgumentParser as argumentParsar

import evaluation_error_categorization as python_execution_helper
import data_and_plotting_agents as AGENTS

PROJECT_BASE_DIRECTORY = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'

def receive_data_path_user_input_generate_data_des_insert_full_datasets_path_generate_prompt(user_input_dir, common_directory, data_subdirectories, extensions, output_dir, model):
    """
    This function searches for files with specified extensions in a common directory and predefined subdirectories,
    summarizes and saves descriptions for each file in a new directory within the common directory.
    
    Args:
        common_directory (str): The common directory to search in.
        subdirectories (list): A list of subdirectories to search within the common directory.
        extensions (list): A list of file extensions to look for.
        output_subdir (str): The name of the subdirectory to save output files in.
    """
    # output_dir = os.path.join(common_directory, output_subdir)
    # print("output_dir", output_dir)
    
    for data_subdir in data_subdirectories:
        data_search_path = os.path.join(common_directory, data_subdir, '*')
        for ext in extensions:
            data_files = glob.glob(f"{data_search_path}.{ext}")
            for data_file_path in data_files:
                print(f"\n\nProcessing file: {data_file_path}")
                # get the input data
                data_basename_with_extension = os.path.basename(data_file_path)
                # if tracking.check_string_status(data_basename_with_extension):
                #     continue
                
                # Remove the extension of input data file
                data_basename_without_extension = os.path.splitext(data_basename_with_extension)[0]
                # print("data_basename_without_extension: ", data_basename_without_extension)

                # user input directory and list all files
                user_input_files_in_directory = os.listdir(user_input_dir)
    
                # save user input file data as user_input_content
                
                # step 1: find the code description as user input
                user_input_content = ""
                # Find the file that starts with the provided filename and has an extension
                for user_input_file in user_input_files_in_directory:
                    user_input_base_name, ext = os.path.splitext(user_input_file)                    
                    # also remove the data type extention
                    user_input_base_name =  utils.get_base_filename(user_input_base_name)                    
                    
                    # print("user_input_base_name: ", user_input_base_name)
                    user_input_file_path = ''
                    if user_input_base_name == data_basename_without_extension:
                        user_input_file_path = os.path.join(user_input_dir, user_input_file)
                        # print(data_basename_with_extension)
                        
                        
                        # Read the file (as text here; change for binary or specific format)
                        with open(user_input_file_path, 'r') as f:
                            content = f.read()
                            user_input_content = content
                            # print("user input content: ", user_input_content)
                        # replace the file name by whole path
                        user_input_content = utils.replace_string(user_input_content, data_basename_with_extension, data_file_path )
                

                    #version 4: current testing: tokenizing the user input text getting the paths and data sets based on some priority words
                    print("\nRaw user input: \n", user_input_content)  
                    
                    clened_user_input_content=user_input_content.replace('\n', ' ')
                    clened_user_input_content=clened_user_input_content.replace('(', '')
                    clened_user_input_content=clened_user_input_content.replace(')', '')
                    clened_user_input_content=clened_user_input_content.replace('\'', '')
                    clened_user_input_content=clened_user_input_content.replace('.', ' ')
                    clened_user_input_content=clened_user_input_content.replace('?', ' ')
                    clened_user_input_content=clened_user_input_content.replace('!', ' ')
                    clened_user_input_content=clened_user_input_content.replace(',', ' ')
                    clened_user_input_content=clened_user_input_content.replace('`', '')
                    clened_user_input_content=clened_user_input_content.replace('*', '')
                    clened_user_input_content=clened_user_input_content.replace(':', ' ')
                    clened_user_input_content=clened_user_input_content.replace('\"', '')
                    print("\nAfter replcaing some special characters from user input: \n", clened_user_input_content)  

                    dataset_attribute_list = utils.tokenize_with_space_and_sort_reversed(clened_user_input_content)
                    
                    print("\nTokenization output without LLM: \n", dataset_attribute_list) 

                    # print(f"\n\nAll matched paths: {len(matchingDatasets)}:\n", matchingDatasets)
                    exact_matched_datasets, exact_matched_datasets_by_name, exact_matched_group_subgroups, exact_matched_group_subgroups_by_name = dataSummarizer.match_exact_dataset_full_partial_match(data_file_path, dataset_attribute_list)
                    
                    all_paths = dataSummarizer.get_all_paths_from_data_file(data_file_path)
                    dataset_attribute_list = utils.extend_list_by_making_paths_into_single_words(dataset_attribute_list)
                    # print("\nTokenization output after making single words: \n", dataset_attribute_list) 
                    rapid_fuzz_best_matched_output, all_matched_paths, best_matched_by_extract, all_matched_paths_by_extract  = utils.find_common_strings(dataset_attribute_list, all_paths)
                    print(f"\n\nRapidFuzz best_matched paths: {len(rapid_fuzz_best_matched_output)}:\n", rapid_fuzz_best_matched_output)
        

                    result=""
                    if len(dataset_attribute_list)>0:
                        
                        # input raw dataset attribute list by llm, output: if any exact dataset path given and correct
                        exact_dataset_path = dataSummarizer.extract_exact_datasets_from_input_generated_by_llm(data_file_path, dataset_attribute_list)
                        # print(f"\n\n exact_dataset_path, size: {len(exact_dataset_path)}: \n", exact_dataset_path)

                        single_word_group_dataset_attribute_list = utils.split_and_extend_paths(dataset_attribute_list)
                        print(f"\n\n single_word_group_dataset_attribute_list, size: {len(single_word_group_dataset_attribute_list)}: \n", single_word_group_dataset_attribute_list) 

                        # version 3
                        real_groups, real_datasets, real_attributes = dataSummarizer.extract_real_datasets_and_attributes(data_file_path, single_word_group_dataset_attribute_list)
                        print(f"\n\n real_groups, size: {len(real_groups)}: \n", real_groups)
                        real_groups = utils.remove_redundant_paths(real_groups)
                        print(f"\n\n real_groups after removing redundant, size: {len(real_groups)}: \n", real_groups)
                        
                        print(f"\n\n real_datasets, size: {len(real_datasets)}: \n", real_datasets)
                        print(f"\n\n real_attributes, size: {len(real_attributes)}: \n", real_attributes)
                        

                        # if exact dataset path given then need to filter the real datasets paths using that
                        filtered_real_datasets = []
                        if len(exact_dataset_path)>0:
                            
                            for dataset in real_datasets:
                                if dataset in exact_dataset_path:
                                    filtered_real_datasets.append(dataset)
                            # print(f"\n\n filtered_real_datasets from exact user input, size: {len(filtered_real_datasets)}: \n", filtered_real_datasets)
                        # let's make a score based paths where we will select top five scored path based on real datasets and tokens from user input
                        else:
                            filtered_real_datasets = utils.make_dictionary_of_score(dataset_attribute_list, real_datasets)
                            # print(f"\n\n filtered_real_datasets from scores, size: {len(filtered_real_datasets)}: \n", filtered_real_datasets)   

                        # this is the current testing final user prompt making
                        final_dataset_list = utils.decision_maker_about_the_final_list_of_datasets(exact_matched_datasets, exact_matched_datasets_by_name, exact_matched_group_subgroups, exact_matched_group_subgroups_by_name, rapid_fuzz_best_matched_output)
                        print(f"\n\n final_dataset_list, size: {len(final_dataset_list)}: \n", final_dataset_list)
                        
                        longitude_latitude_list, final_dataset_list_without_lat_lon = dataSummarizer.find_latitude_longditude_information_for_given_dataset_list(data_file_path, final_dataset_list)
                        print(f"\n\n longitude_latitude_list, size: {len(longitude_latitude_list)}: \n", longitude_latitude_list)
                        
                        
                        result = dataSummarizer.format_datasets_from_final_set_and_latitude_longitude_list(data_file_path, final_dataset_list_without_lat_lon, longitude_latitude_list)
                        print("\n\n Final Result: \n", result)
                    
                    llmRequester.generate_code_and_save_with_data_rule_based_reasoning(user_input_file_path=user_input_file_path, user_input_description=user_input_content, data_structure_information=result, full_data_path=data_file_path, target_dir=output_dir, model=model, URL=URL)


#development is in progress, it is implemented in a separate file, need to incorporate this
# mat plot agent csv to converted h5 datasets
#                                       user_input_dir, JSON_FILE_PATH, common_base_directory+"/"+data_dir, subdirectories, extensions, output_dir, output_subdir, model
def zero_shot_COT_csv_to_converted_h5_DATASETS(user_input_dir, JSON_FILE_PATH, common_directory, data_dir, data_subdirectories, extensions, output_dir, output_subdir, with_corrector, model):
    print(f'Processing directory {user_input_dir}')
    
    print(f'\nInside zero_shot_COT_csv_to_h5_DATASETS...')
    print(f'JSON_FILE_PATH: {JSON_FILE_PATH}')
    print(f'user_input_dir: {user_input_dir}')
    print(f'common_directory: {common_directory}')
    print(f'common_directory/data_dir/data_subdir: ', common_directory+'/'+data_dir)
    
    try:
        for data_subdir in data_subdirectories:
            data_search_path = os.path.join(common_directory+'/'+data_dir, data_subdir, '*')
            print(f'Processing data search directory {data_search_path}')

            for ext in extensions:
                data_files = glob.glob(f"{data_search_path}.{ext}")
                for data_file_path in data_files:
                    print(f"\n\nProcessing file: {data_file_path}")
                    # get the input data
                    data_basename_with_extension = os.path.basename(data_file_path)
                    # if tracking.check_string_status(data_basename_with_extension):
                    #     continue

                    # common_base_directory, JSON_FILE_PATH, directory_file_name, key
                    if tracking.check_tracking_status_is_done(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension):
                        continue
                    else:
                        tracking.insert_or_update_key(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension, 'started')
                        # tracking.insert_string_started(data_basename_with_extension)

                    # Remove the extension of input data file
                    data_basename_without_extension = os.path.splitext(data_basename_with_extension)[0]
                    # print("data_basename_without_extension: ", data_basename_without_extension)

                    # user input directory and list all files
                    user_input_files_in_directory = os.listdir(user_input_dir)
        
                    # save user input file data as user_input_content
                    
                    # step 1: find the code description as user input
                    user_input_content = ""
                    # Find the file that starts with the provided filename and has an extension
                    for user_input_file in user_input_files_in_directory:
                        user_input_base_name, ext = os.path.splitext(user_input_file)
                        
                        # also remove the data type extention
                        user_input_base_name =  utils.get_base_filename(user_input_base_name)                        
                        
                        # print("user_input_base_name: ", user_input_base_name)
                        if user_input_base_name == data_basename_without_extension:
                            user_input_file_path = os.path.join(user_input_dir, user_input_file)
                            print(data_basename_with_extension)                            
                            
                            # Read the file (as text here; change for binary or specific format)
                            with open(user_input_file_path, 'r') as f:
                                content = f.read()
                                user_input_content = content
                                print("user input content: ", user_input_content)
                            
                            # replace the file name by whole path
                            user_input_content = utils.replace_string(user_input_content, data_basename_with_extension, data_file_path )
                            if with_corrector == True:
                                print('\n------------Inside with corrector...')
                                # current with corrector
                                result, attribute_present, updated_text = corrector.corrector_function_main(user_input_content, data_file_path, is_memory)
                                print('Passed corrector_function_main function')                           
                            
                                # with updated text
                                user_input_content=updated_text                            
                            
                                # current with corrector
                                llmRequester.generate_code_and_save_with_data_zero_shot_CoT(user_input_file_path, user_input_content, result, data_file_path, output_dir+'/'+output_subdir, attribute_present, model, is_memory, URL, dataset)
                            else:
                                print('\n------------Inside without corrector...')
                                # current generating code without correcotrs
                                llmRequester.generate_code_and_save_without_data_zero_shot_CoT(user_input_file_path=user_input_file_path, user_input_description=user_input_content, full_data_path=data_file_path, target_dir=output_dir+'/'+output_subdir, model=model, python_script='', error_message='', iteration=0, URL=URL, dataset=dataset, dataset_attrubute_fullpath_list_result='')
                            
                            
                            # assuming code generating completed here
                            tracking.insert_or_update_key(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension, 'done')
                            # tracking.insert_string_done(data_basename_with_extension)
                        else:
                            print('No Match!')
    except Exception as e:
        print('Exception occurred in zero_shot_COT_csv_to_converted_h5_DATASETS, error message: ', e)


#                                       user_input_dir, JSON_FILE_PATH, common_base_directory+"/"+data_dir, subdirectories, extensions, output_dir, output_subdir, model
def zero_shot_COT_NASA_CLIMATE_DATASETS(user_input_dir, JSON_FILE_PATH, common_directory, data_dir, data_subdirectories, extensions, output_dir, output_subdir, with_corrector, model, is_memory, URL, dataset):
    print(f'Processing directory {user_input_dir}')
    
    print(f'\nInside zero_shot_COT_NASA_CLIMATE_DATASETS...')
    print(f'JSON_FILE_PATH: {JSON_FILE_PATH}')
    print(f'user_input_dir: {user_input_dir}')
    print(f'common_directory: {common_directory}')
    print(f'common_directory/data_dir/data_subdir: ', common_directory+'/'+data_dir)
    
    try:
        for data_subdir in data_subdirectories:
            data_search_path = os.path.join(common_directory+'/'+data_dir, data_subdir, '*')
            print(f'Processing data search directory {data_search_path}')

            for ext in extensions:
                data_files = glob.glob(f"{data_search_path}.{ext}")
                for data_file_path in data_files:
                    print(f"\n\nProcessing file: {data_file_path}")
                    # get the input data
                    data_basename_with_extension = os.path.basename(data_file_path)
                    # if tracking.check_string_status(data_basename_with_extension):
                    #     continue

                    # common_base_directory, JSON_FILE_PATH, directory_file_name, key
                    if tracking.check_tracking_status_is_done(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension):
                        continue
                    else:
                        tracking.insert_or_update_key(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension, 'started')
                        # tracking.insert_string_started(data_basename_with_extension)

                    # Remove the extension of input data file
                    data_basename_without_extension = os.path.splitext(data_basename_with_extension)[0]
                    # print("data_basename_without_extension: ", data_basename_without_extension)

                    # user input directory and list all files
                    user_input_files_in_directory = os.listdir(user_input_dir)

                    # save user input file data as user_input_content                    
                    # step 1: find the code description as user input
                    user_input_content = ""
                    # Find the file that starts with the provided filename and has an extension
                    for user_input_file in user_input_files_in_directory:
                        user_input_base_name, ext = os.path.splitext(user_input_file)
                        
                        # also remove the data type extention
                        user_input_base_name =  utils.get_base_filename(user_input_base_name)                        
                        
                        # print("user_input_base_name: ", user_input_base_name)
                        if user_input_base_name == data_basename_without_extension:
                            user_input_file_path = os.path.join(user_input_dir, user_input_file)
                            print(data_basename_with_extension)
                            
                            
                            # Read the file (as text here; change for binary or specific format)
                            with open(user_input_file_path, 'r') as f:
                                content = f.read()
                                user_input_content = content
                                print("user input content: ", user_input_content)
                            
                            # return content, user_input_file_path

                            # replace the file name by whole path
                            user_input_content = utils.replace_string(user_input_content, data_basename_with_extension, data_file_path )
                            if with_corrector == True:
                                print('\n------------Inside with corrector...')
                                # current with corrector
                                result, attribute_present, updated_text = corrector.corrector_function_main(user_input_content, data_file_path, is_memory)
                                print('Passed corrector_function_main function')
                                # without updated text
                         
                                # with updated text
                                user_input_content=updated_text
                            
                                # with updated text such as replacing bigram or monogram by acutual dataset paths and attribute names
                            
                                # current with corrector
                                llmRequester.generate_code_and_save_with_data_zero_shot_CoT(user_input_file_path, user_input_content, result, data_file_path, output_dir+'/'+output_subdir, attribute_present, model, is_memory, URL, dataset)
                            else:
                                print('\n------------Inside without corrector...')
                                # current generating code without correcotrs

                                llmRequester.generate_code_and_save_without_data_zero_shot_CoT(user_input_file_path=user_input_file_path, user_input_description=user_input_content, full_data_path=data_file_path, target_dir=output_dir+'/'+output_subdir, model=model, python_script='', error_message='', iteration=0, URL=URL, dataset=dataset, dataset_attrubute_fullpath_list_result='')
                            
                            
                            # assuming code generating completed here
                            tracking.insert_or_update_key(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension, 'done')
                            # tracking.insert_string_done(data_basename_with_extension)
                        else:
                            print('No Match!')
    except Exception as e:
        print('Exception occurred in zero_shot_COT_NASA_CLIMATE_DATASETS, error message: ', e)

# created on February 13, 2025
# to check if we can solve errors by giving error messages and generated code to LLM and ask to resolve
#                                       user_input_dir, JSON_FILE_PATH, common_base_directory+"/"+data_dir, subdirectories, extensions, output_dir, output_subdir, model
def zero_shot_COT_NASA_CLIMATE_DATASETS_ITERATIVE_ERROR_RESOLVE(user_input_dir, JSON_FILE_PATH, common_directory, data_dir, data_subdirectories, extensions, output_dir, output_subdir, with_corrector, model, is_memory, URL):
    print(f'Processing directory {user_input_dir}')
    print(f'\nsize of the data_subdirectories: {len(data_subdirectories)}')
    print(f'\nInside zero_shot_COT_NASA_CLIMATE_DATASETS...')
    print(f'JSON_FILE_PATH: {JSON_FILE_PATH}')
    print(f'user_input_dir: {user_input_dir}')
    print(f'common_directory: {common_directory}')
    print(f'common_directory/data_dir/data_subdir: ', common_directory+'/'+data_dir)
    
    try:
        for data_subdir in data_subdirectories:
            data_search_path = os.path.join(common_directory+'/'+data_dir, data_subdir, '*')
            print(f'Processing data search directory {data_search_path}')

            for ext in extensions:
                data_files = glob.glob(f"{data_search_path}.{ext}")
                for data_file_path in data_files:
                    try:
                        print(f"\n\nProcessing file: {data_file_path}")
                        # get the input data
                        data_basename_with_extension = os.path.basename(data_file_path)
                        # if tracking.check_string_status(data_basename_with_extension):
                        #     continue

                        # common_base_directory, JSON_FILE_PATH, directory_file_name, key
                        if tracking.check_tracking_status_is_done(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension):
                            continue
                        else:
                            tracking.insert_or_update_key(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension, 'started')
                            # tracking.insert_string_started(data_basename_with_extension)

                        # Remove the extension of input data file
                        data_basename_without_extension = os.path.splitext(data_basename_with_extension)[0]
                        # print("data_basename_without_extension: ", data_basename_without_extension)

                        # user input directory and list all files
                        user_input_files_in_directory = os.listdir(user_input_dir)
                        
                        result = ''
                        attribute_present = ''
                        # save user input file data as user_input_content                    
                        # step 1: find the code description as user input
                        user_input_content = ""
                        # Find the file that starts with the provided filename and has an extension
                        for user_input_file in user_input_files_in_directory:
                            user_input_base_name, ext = os.path.splitext(user_input_file)
                            
                            # also remove the data type extention
                            user_input_base_name =  utils.get_base_filename(user_input_base_name)                        
                            
                            # print("user_input_base_name: ", user_input_base_name)
                            if user_input_base_name == data_basename_without_extension:
                                user_input_file_path = os.path.join(user_input_dir, user_input_file)
                                print(data_basename_with_extension)
                                
                                
                                # Read the file (as text here; change for binary or specific format)
                                with open(user_input_file_path, 'r') as f:
                                    content = f.read()
                                    user_input_content = content
                                    print("user input content: ", user_input_content)
                                
                                # return content, user_input_file_path
                                #newly generated python script path
                                new_python_script_path = ''
                                generated_python_script = '' 


                                # replace the file name by whole path
                                user_input_content = utils.replace_string(user_input_content, data_basename_with_extension, data_file_path )
                                if with_corrector == True:
                                    print('\n------------Inside with corrector...')
                                    # current with corrector
                                    result, attribute_present, updated_text = corrector.corrector_function_main(user_input_content, data_file_path, is_memory)
                                    print('Passed corrector_function_main function')
                                    # without updated text
                                    # llmRequester.generate_code_and_save_with_data_zero_shot_CoT(user_input_file_path, user_input_content, result, data_file_path, output_dir, attribute_present, model)

                                    # with updated text
                                    user_input_content=updated_text
                                
                                    # with updated text such as replacing bigram or monogram by acutual dataset paths and attribute names
                                
                                    # current with corrector
                                    #                                                                                                            user_input_file_path, user_input_content, result, data_file_path, output_dir+'/'+output_subdir, attribute_present, model, is_memory, python_script, error_message 
                                    new_python_script_path, generated_python_script = llmRequester.generate_code_and_save_with_data_zero_shot_CoT_iterative_error_resolve(user_input_file_path, user_input_content, result, data_file_path, output_dir+'/'+output_subdir, attribute_present, model, is_memory, '', '', 0, URL)
                                else:
                                    print('\n------------Inside without corrector...')
                                    # current generating code without correcotrs
                                    # user_input_file_path, user_input_description, full_data_path, target_dir, model, old_ext='.txt'
                                    #                                                           user_input_file_path, user_input_description, full_data_path, target_dir, model, python_script, error_message, iteration, URL, dataset, dataset_attrubute_fullpath_list_result
                                    new_python_script_path, generated_python_script = llmRequester.generate_code_and_save_without_data_zero_shot_CoT(user_input_file_path, user_input_content, data_file_path, output_dir+'/'+output_subdir, model, python_script='', error_message='', iteration=0, URL=URL, dataset=dataset, dataset_attrubute_fullpath_list_result='')
                                
                                
                                # for iterative error resolving, don't save the file in the first generation and pass it for another generation
                                number_of_iteration = 4
                                # execute the code and check if is there any errors
                                # if error then get the get the generated code and error message together and regenerate the code
                                for iteration in range(1, number_of_iteration):
                                    print('Current iteration: ', iteration)
                                    # if the newly generated python script path has been returned 
                                    if len(new_python_script_path) > 0: 
                                            # Run the script and capture errors
                                        status, stderr = python_execution_helper.run_python_script(new_python_script_path, output_subdir, 'CLIMATE')
                                        if status=='Pass':
                                            print('Pass')
                                            break
                                        else:
                                            print('Fail')
                                            # Parse errors and categorize
                                            if stderr:
                                                print('There is an error: \n', stderr)
                                                if with_corrector == True:
                                                    print('iterative error resolving with corrector')
                                                                                                                                                                                                                                                                                                                                                                                                                    # python_script, error_message, iteration, URL
                                                    new_python_script_path, generated_python_script = llmRequester.generate_code_and_save_with_data_zero_shot_CoT_iterative_error_resolve(user_input_file_path=user_input_file_path, user_input_description=user_input_content, data_structure_information=result, full_data_path=data_file_path, target_dir=output_dir+'/'+output_subdir, attribute_present=attribute_present, model=model, is_memory=is_memory, python_script=generated_python_script, error_message=stderr, iteration=iteration, URL=URL)
                                                else:
                                                    # iteration error resolve without corrector
                                                    print('iterative error resolving without corrector')
                                                    #                                                                                                           user_input_file_path, user_input_description, full_data_path, target_dir, model, python_script, error_message, iteration, URL, dataset, dataset_attrubute_fullpath_list_result
                                                    new_python_script_path, generated_python_script = llmRequester.generate_code_and_save_without_data_zero_shot_CoT(user_input_file_path, user_input_content, data_file_path, output_dir+'/'+output_subdir, model, python_script=generated_python_script, error_message=stderr, iteration=iteration, URL=URL, dataset=dataset, dataset_attrubute_fullpath_list_result='')

                                # assuming code generating completed here
                                tracking.insert_or_update_key(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension, 'done')
                                # tracking.insert_string_done(data_basename_with_extension)
                            else:
                                print('No Match!')
                    except Exception as e:
                        print(f'Exception occurred at zero_shot_COT_NASA_CLIMATE_DATASETS_ITERATIVE_ERROR_RESOLVE:\n    while traversing through data file path: {data_file_path}, error: {e}')
    except Exception as e:
        print('Exception occurred in zero_shot_COT_NASA_CLIMATE_DATASETS_ITERATIVE_ERROR_RESOLVE, error message: ', e)
import traceback
import time
# created on June 29, 2025
# to check if we can solve errors by giving error messages and generated code to LLM and ask to resolve
#                                       user_input_dir, JSON_FILE_PATH, common_base_directory+"/"+data_dir, subdirectories, extensions, output_dir, output_subdir, model
def ITERATIVE_ERROR_RESOLVE_NASA_CLIMATE_DATASETS_WITH_RAG_CORRECTOR_ONLINE_SEARCH(user_input_dir, JSON_FILE_PATH, common_directory, data_dir, data_subdirectories, extensions, output_dir, output_subdir, with_corrector, model, URL, temperature):
    print(f'Processing directory {user_input_dir}')
    print(f'\nsize of the data_subdirectories: {len(data_subdirectories)}')
    print(f'\nInside zero_shot_COT_NASA_CLIMATE_DATASETS...')
    print(f'JSON_FILE_PATH: {JSON_FILE_PATH}')
    print(f'user_input_dir: {user_input_dir}')
    print(f'common_directory: {common_directory}')
    print(f'common_directory/data_dir/data_subdir: ', common_directory+'/'+data_dir)
    
    try:
        for data_subdir in data_subdirectories:
            data_search_path = os.path.join(common_directory+'/'+data_dir, data_subdir, '*')
            print(f'Processing data search directory {data_search_path}')

            for ext in extensions:
                data_files = glob.glob(f"{data_search_path}.{ext}")
                for data_file_path in data_files:
                    try:
                        print(f"\n\nProcessing file: {data_file_path}")
                        # get the input data
                        data_basename_with_extension = os.path.basename(data_file_path)
                        # if tracking.check_string_status(data_basename_with_extension):
                        #     continue

                        # common_base_directory, JSON_FILE_PATH, directory_file_name, key
                        if tracking.check_tracking_status_is_done(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension):
                            continue
                        else:
                            tracking.insert_or_update_key(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension, 'started')
                            # #tracking.insert_string_started(data_basename_with_extension)
                        # record keeping parameters
                        corrector_run_time = 0
                        rag_run_time = 0
                        llm_run_time = 0
                        

                        # Remove the extension of input data file
                        data_basename_without_extension = os.path.splitext(data_basename_with_extension)[0]
                        # print("data_basename_without_extension: ", data_basename_without_extension)

                        # user input directory and list all files
                        user_input_files_in_directory = os.listdir(user_input_dir)

                        # save user input file data as user_input_content                    
                        # step 1: find the code description as user input
                        user_input_content = ""
                        # Find the file that starts with the provided filename and has an extension
                        for user_input_file in user_input_files_in_directory:
                            user_input_base_name, ext = os.path.splitext(user_input_file)
                            
                            # also remove the data type extention
                            user_input_base_name =  utils.get_base_filename(user_input_base_name)                        
                            
                            # print("user_input_base_name: ", user_input_base_name)
                            if user_input_base_name == data_basename_without_extension:
                                user_input_file_path = os.path.join(user_input_dir, user_input_file)
                                print(data_basename_with_extension)                                
                                
                                # Read the file (as text here; change for binary or specific format)
                                with open(user_input_file_path, 'r') as f:
                                    content = f.read()
                                    user_input_content = content
                                    # print("user input content: ", user_input_content)
                                
                                # return content, user_input_file_path
                                #newly generated python script path
                                new_python_script_path = ''
                                generated_python_script = ''

                                # replace the file name by whole path
                                user_input_content = utils.replace_string(user_input_content, data_basename_with_extension, data_file_path )
                                query_augmentation = ''
                                # examples_codes_for_query_augmentation=''
                                if is_with_rag == True:
                                    rag_start_time = time.time()
                                    examples_codes_for_query_augmentation = AGENTS.get_augmented_query(data_basename_with_extension+'.txt', model_name, is_errors, 'CLIMATE', temperature)
                                    rag_end_time = time.time()
                                    rag_run_time = rag_end_time - rag_start_time
                                    print(f'Inside sci data prompting main:: examples code for query augmentation: \n{examples_codes_for_query_augmentation}')
                                    query_augmentation = examples_codes_for_query_augmentation

                                dataset_attrubute_fullpath_list_result = ''
                                if with_corrector == True:
                                    print('\n------------Inside with corrector...')
                                    # current with corrector
                                    corrector_start_time = time.time()
                                    result, attribute_present, updated_text = corrector.corrector_function_main(user_input_content, data_file_path, is_memory)
                                    corrector_end_time = time.time()
                                    corrector_run_time = corrector_end_time - corrector_start_time
                                    print('Passed corrector_function_main function')
                                    dataset_attrubute_fullpath_list_result = result
                                    # with updated text
                                    # user_input_content=updated_text                  
                                   
                                
                                    # current with corrector
                                    #
                                #    user_input_file_path, user_input_description, dataset_attrubute_fullpath_list_result, full_data_path, target_dir, model, python_script, error_message, iteration, URL, examples_for_query_augmentation
                                llm_start_time = time.time()
                                new_python_script_path, generated_python_script= llmRequester.generate_code_and_save_code_with_RAG_iterative_error_resolve(user_input_file_path, user_input_content, dataset_attrubute_fullpath_list_result, data_file_path, output_dir+'/'+output_subdir, model, '', '', 0, URL, query_augmentation, temperature)
                                llm_end_time = time.time()
                                llm_run_time = llm_end_time - llm_start_time
                                utils.track_and_log_runtimes(output_dir+'/'+output_subdir+'.csv', model_name, corrector_run_time, rag_run_time, llm_run_time)    
                                print(f'CSV file saved to the directory:\n{output_dir}'+f'/{output_subdir}'+'.csv')
                                # print('ITERATIVE_ERROR_RESOLVE_NASA_CLIMATE_DATASETS_WITH_RAG_CORRECTOR_ONLINE_SEARCH new_python_script_path:\n', new_python_script_path)
                                # print('ITERATIVE_ERROR_RESOLVE_NASA_CLIMATE_DATASETS_WITH_RAG_CORRECTOR_ONLINE_SEARCH generated_python_script:\n', generated_python_script)
                                
                                # number_of_iteration = 7
                                number_of_iteration = 1
                                
                                # execute the code and check if is there any errors
                                # if error then get the get the generated code and error message together and regenerate the code
                                for iteration in range(1, number_of_iteration):
                                    print('Current iteration: ', iteration)
                                    # if the newly generated python script path has been returned 
                                    if new_python_script_path is not None and len(new_python_script_path) > 0: 
                                            # Run the script and capture errors
                                        status, stderr = python_execution_helper.run_python_script(new_python_script_path, output_subdir, 'CLIMATE')
                                        print(f'During iteration: {iteration}, status: {status}, stderr: {stderr}')

                                        if status=='Pass':
                                            print('Pass')
                                            break
                                        else:
                                            print('Fail')
                                            # Parse errors and categorize
                                            if stderr is not None:
                                                print('There is an error: \n', stderr)
                                                query_augmentation = ''
                                                # if with_corrector == True or is_with_rag == True:
                                                formatted_error_message, last_line_of_error = utils.extract_key_lines_from_chained_exceptions(stderr)
                                                stderr = formatted_error_message
                                                    
                                                    
                                                print('iterative error resolving with corrector')
                                                    #                                                                                                                           user_input_file_path, user_input_content, result, data_file_path, output_dir+'/'+output_subdir, attribute_present, model, is_memory, '', '', 0, URL
                                                new_python_script_path, generated_python_script = llmRequester.generate_code_and_save_code_with_RAG_iterative_error_resolve(user_input_file_path, user_input_content, dataset_attrubute_fullpath_list_result, data_file_path, output_dir+'/'+output_subdir, model, generated_python_script, stderr, iteration, URL, query_augmentation, temperature)
                                                print('ITERATIVE_ERROR_RESOLVE_NASA_CLIMATE_DATASETS_WITH_RAG_CORRECTOR_ONLINE_SEARCH new_python_script_path:\n', new_python_script_path)
                                                print('ITERATIVE_ERROR_RESOLVE_NASA_CLIMATE_DATASETS_WITH_RAG_CORRECTOR_ONLINE_SEARCH generated_python_script:\n', generated_python_script)
                       
                                            else:
                                                print('ITERATIVE_ERROR_RESOLVE_NASA_CLIMATE_DATASETS_WITH_RAG_CORRECTOR:: Error is None')
                                # assuming code generating completed here
                                tracking.insert_or_update_key(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension, 'done')
                                # tracking.insert_string_done(data_basename_with_extension)
                            else:
                                print('No Match!')
                    except Exception as e:
                        print(f'Exception occurred at ITERATIVE_ERROR_RESOLVE_NASA_CLIMATE_DATASETS_WITH_RAG_CORRECTOR:\n   while traversing through data file path: {data_file_path}, error: {e}')
                        traceback.print_exc()
    except Exception as e:
        print('Exception occurred in ITERATIVE_ERROR_RESOLVE_NASA_CLIMATE_DATASETS_WITH_RAG_CORRECTOR, error message: ', e)



# DCM TO H5 FAST MRI BRAIN DATASETS 
def zero_shot_COT_FAST_MRI_BRAIN_DCM_TO_H5_DATASETS(user_input_dir, common_base_directory, data_file_base_name, data_file_full_path, output_dir, output_subdir, model, JSON_FILE_PATH, is_with_corrector, URL):
    
   
    print(f'Processing directory {user_input_dir}')

    all_user_queries_directory_full_path = os.path.join(common_base_directory, user_input_dir)
    print('all_user_queries_directory_full_path: ', all_user_queries_directory_full_path)
    
    user_query_files_in_directory = os.listdir(all_user_queries_directory_full_path)
    print('user_query_files_in_directory: \n', user_query_files_in_directory)

    user_input_content = ""
            # Find the file that starts with the provided filename and has an extension
    for user_input_file in user_query_files_in_directory:
        user_input_base_name, ext = os.path.splitext(user_input_file)
        
        # also remove the data type extention
        user_input_base_name =  utils.get_base_filename(user_input_base_name)

           
        user_input_file_full_path = os.path.join(all_user_queries_directory_full_path, user_input_file)
        # Read the file (as text here; change for binary or specific format)
        with open(user_input_file_full_path, 'r') as f:
            content = f.read()
            user_input_content = content
            print("\nuser input content: ", user_input_content)

        # Remove the extension of input data file
        data_basename_without_extension = os.path.splitext(data_file_full_path)[0]
        print("data_basename_without_extension: ", data_basename_without_extension)
        
        # replace the file name by whole path
        print('\ndata_file_base_name: ', data_file_base_name)
        print('\nData file full path: \n', data_file_full_path)

        user_input_content = utils.replace_string(user_input_content, data_file_base_name, data_file_full_path )
        
        print('\n\n---------------------------------------------------------')
        print('user_input_content: \n', user_input_content)

        if is_with_corrector == True:
            print('Inside with corrector ...')
            # current with corrector
            result, attribute_present, updated_text = corrector.corrector_function_main(user_input_content, data_file_full_path, is_memory)
            print('Passed corrector_function_main function')
            
            # without updated text
            # llmRequester.generate_code_and_save_with_data_zero_shot_CoT(user_input_file_path, user_input_content, result, data_file_path, output_dir, attribute_present, model)

            # with updated text
            user_input_content=updated_text
            # current with corrector
            llmRequester.generate_code_and_save_with_data_zero_shot_CoT(user_input_file_full_path, user_input_content, result, data_file_full_path, output_dir+'/'+output_subdir, attribute_present, model, is_memory, URL, dataset)
        else:
            print('Inside without corrector ...')
            # current generating code without correcotrs
            # user_input_file_path, user_input_description, full_data_path, target_dir, model, old_ext='.txt'
            #                                                              user_input_file_path, user_input_description, full_data_path, target_dir, model, python_script, error_message, iteration, URL, dataset, dataset_attrubute_fullpath_list_result
            llmRequester.generate_code_and_save_without_data_zero_shot_CoT(user_input_file_full_path, user_input_content, data_file_full_path, output_dir+'/'+output_subdir, model, python_script='', error_message='', iteration=0, URL=URL, dataset=dataset, dataset_attrubute_fullpath_list_result='')
        
        
        # assuming code generating completed here
        # common_base_directory, JSON_FILE_PATH, directory_file_name, key, value
        tracking.insert_or_update_key(common_base_directory, JSON_FILE_PATH, output_subdir, user_input_base_name, 'done')
        # tracking.insert_string_done(data_basename_with_extension)


# here this is a two steps process, at first it is generating user intent from the user query then using that information to form the query further
# DCM TO H5 FAST MRI BRAIN DATASETS 
def zero_shot_COT_FAST_MRI_BRAIN_DCM_TO_H5_DATASETS_WITH_USER_INTENT(user_input_dir, common_base_directory, data_file_base_name, data_file_full_path, output_dir, output_subdir, model, JSON_FILE_PATH, is_with_corrector, URL):
    
    print(f'Processing directory {user_input_dir}')

    all_user_queries_directory_full_path = os.path.join(PROJECT_BASE_DIRECTORY, user_input_dir)
    print('all_user_queries_directory_full_path: ', all_user_queries_directory_full_path)
    
    user_query_files_in_directory = os.listdir(all_user_queries_directory_full_path)
    print('user_query_files_in_directory: \n', user_query_files_in_directory)

    user_input_content = ""
            # Find the file that starts with the provided filename and has an extension
    for user_input_file in user_query_files_in_directory:
        user_input_base_name, ext = os.path.splitext(user_input_file)
        
        # also remove the data type extention
        user_input_base_name =  utils.get_base_filename(user_input_base_name)

       
        
        user_input_file_full_path = os.path.join(all_user_queries_directory_full_path, user_input_file)
        # Read the file (as text here; change for binary or specific format)
        with open(user_input_file_full_path, 'r') as f:
            content = f.read()
            user_input_content = content
            print("\nuser input content: ", user_input_content)


        # get the user intent and process
        user_intent = intent_generation_from_user_input_zero_shot_prompt(user_input_dir, data_file_base_name, data_file_full_path, output_dir, output_subdir, model, URL)
        attribute_name, condition, condition_value = utils.get_attribute_name_condition_condition_value(user_intent)
        print(f"attribute_name: {attribute_name}, condition: {condition}, condition_value: {condition_value}")


        # Remove the extension of input data file
        data_basename_without_extension = os.path.splitext(data_file_full_path)[0]
        print("data_basename_without_extension: ", data_basename_without_extension)
        
        # replace the file name by whole path
        print('\ndata_file_base_name: ', data_file_base_name)
        print('\nData file full path: \n', data_file_full_path)

        user_input_content = utils.replace_string(user_input_content, data_file_base_name, data_file_full_path )
        
        print('\n\n---------------------------------------------------------')
        print('user_input_content: \n', user_input_content)
               
        # without updated text
        # llmRequester.generate_code_and_save_with_data_zero_shot_CoT(user_input_file_path, user_input_content, result, data_file_path, output_dir, attribute_present, model)

        if  is_with_corrector == True:
            print('With corrector ...')

            # attribute_name, condition, condition_value,  

            # current with corrector
            result, attribute_present, updated_text = corrector.corrector_function_main(user_input_content, data_file_full_path, is_memory, attribute_name, condition, condition_value)
            if len(condition) > 0:
                print('result: ', result)
            else:
                print('Intent not found')

            # with updated text
            user_input_content = updated_text
            # current with corrector
            #                                                           user_input_file_path, user_input_description, data_structure_information, full_data_path, target_dir, attribute_present, model, is_memory, URL, dataset, old_ext='.txt'
            llmRequester.generate_code_and_save_with_data_zero_shot_CoT(user_input_file_full_path, user_input_content, result, data_file_full_path, output_dir+'/'+output_subdir, attribute_present, model, is_memory, URL, dataset=dataset)
        else:
            print('Without corrector ...')
            # current generating code without correcotrs
            #                                                              user_input_file_path, user_input_description, full_data_path, target_dir,                     model, python_script, error_message, iteration, URL, dataset, dataset_attrubute_fullpath_list_result, old_ext='.txt'
            llmRequester.generate_code_and_save_without_data_zero_shot_CoT(user_input_file_full_path, user_input_content, data_file_full_path, output_dir+'/'+output_subdir, model, python_script='', error_message='', iteration=0, URL=URL, dataset=dataset, dataset_attrubute_fullpath_list_result='')
        
        
        # assuming code generating completed here
        # common_base_directory, JSON_FILE_PATH, directory_file_name, key, value
        tracking.insert_or_update_key(common_base_directory, JSON_FILE_PATH, output_subdir, user_input_base_name, 'done')
        # tracking.insert_string_done(data_basename_with_extension)


# DCM TO H5 FAST MRI BRAIN DATASETS
# Intent generation from user queries 
def intent_generation_from_user_input_zero_shot_prompt(user_input_dir, data_file_base_name, data_file_full_path, output_dir, output_subdir, model, URL):
    print(f'Processing directory {user_input_dir}')

    all_user_queries_directory_full_path = os.path.join(PROJECT_BASE_DIRECTORY, user_input_dir)
    print('All_user_queries_directory_full_path: ', all_user_queries_directory_full_path)
    
    user_query_files_in_directory = os.listdir(all_user_queries_directory_full_path)
    print('User_query_files_in_directory: \n', user_query_files_in_directory)

    user_input_content = ""
    
    # Find the file that starts with the provided filename and has an extension
    for user_input_file in user_query_files_in_directory:
        user_input_base_name, ext = os.path.splitext(user_input_file)
        
        # also remove the data type extention
        user_input_base_name =  utils.get_base_filename(user_input_base_name)

        user_input_file_full_path = os.path.join(all_user_queries_directory_full_path, user_input_file)
        # Read the file (as text here; change for binary or specific format)
        with open(user_input_file_full_path, 'r') as f:
            content = f.read()
            user_input_content = content
            print("\nUser input content: ", user_input_content)

        # Remove the extension of input data file
        data_basename_without_extension = os.path.splitext(data_file_full_path)[0]
        print("Data_basename_without_extension: ", data_basename_without_extension)
        
        # replace the file name by whole path
        print('\ndata_file_base_name: ', data_file_base_name)
        print('\nData file full path: \n', data_file_full_path)

        # user_input_content = utils.replace_string(user_input_content, data_file_base_name, data_file_full_path )
        
        print('\n\n---------------------------------------------------------')
        print('user_input_content: \n', user_input_content)

        # intent generation from user input
        #                                                                                     user_input_file_full_path, user_input_content, target_dir, model, URL, old_ext='.txt'
        return llmRequester.zero_shot_CoT_generate_request_for_generating_intent_attribute_condition(user_input_file_full_path, user_input_content, output_dir+'/'+output_subdir, model, URL)
                    


# Intent generation from user queries 
def user_sub_queries_generation_from_user_input_for_CLIMATE_datasets(user_input_dir, common_base_directory, data_file_base_name, data_file_full_path, output_dir, output_subdir, model, URL, temperature):
    print(f'Processing directory {user_input_dir}')

    all_user_queries_directory_full_path = os.path.join(common_base_directory, user_input_dir)
    print('All_user_queries_directory_full_path: ', all_user_queries_directory_full_path)
    
    user_query_files_in_directory = os.listdir(all_user_queries_directory_full_path)
    print('User_query_files_in_directory: \n', user_query_files_in_directory)

    user_input_content = ""
    
    # Find the file that starts with the provided filename and has an extension
    for user_input_file in user_query_files_in_directory:
        user_input_base_name, ext = os.path.splitext(user_input_file)
        
        # also remove the data type extention
        user_input_base_name =  utils.get_base_filename(user_input_base_name)

        user_input_file_full_path = os.path.join(all_user_queries_directory_full_path, user_input_file)
        # Read the file (as text here; change for binary or specific format)
        with open(user_input_file_full_path, 'r') as f:
            content = f.read()
            user_input_content = content
            print("\nUser input content: ", user_input_content)

        # Remove the extension of input data file
        data_basename_without_extension = os.path.splitext(data_file_full_path)[0]
        print("Data_basename_without_extension: ", data_basename_without_extension)
        
        # replace the file name by whole path
        print('\ndata_file_base_name: ', data_file_base_name)
        print('\nData file full path: \n', data_file_full_path)

        
        print('\n\n---------------------------------------------------------')
        print('user_input_content: \n', user_input_content)

        #                                                                                     user_input_file_full_path, user_input_content, target_dir, model, old_ext='.txt'
        llmRequester.generate_multi_agents_request_for_sub_query_generation(user_input_file_full_path, user_input_content, output_dir+'/'+output_subdir, model, URL, temperature)


# Intent generation from user queries 
def user_sub_queries_generation_from_user_input_for_MATPLOTAGENT_datasets(user_input_dir, common_base_directory, data_file_base_name, data_file_full_path, output_dir, output_subdir, model, URL, temperature):
    print(f'Processing directory {user_input_dir}')

    all_user_queries_directory_full_path = os.path.join(common_base_directory, user_input_dir)
    print('All_user_queries_directory_full_path: ', all_user_queries_directory_full_path)
    
    user_query_files_in_directory = os.listdir(all_user_queries_directory_full_path)
    print('User_query_files_in_directory: \n', user_query_files_in_directory)

    user_input_content = ""
    
    # Find the file that starts with the provided filename and has an extension
    for user_input_file in user_query_files_in_directory:
        user_input_base_name, ext = os.path.splitext(user_input_file)
        
        # also remove the data type extention
        user_input_base_name =  utils.get_base_filename(user_input_base_name)

        user_input_file_full_path = os.path.join(all_user_queries_directory_full_path, user_input_file)
        # Read the file (as text here; change for binary or specific format)
        with open(user_input_file_full_path, 'r') as f:
            content = f.read()
            user_input_content = content
            print("\nUser input content: ", user_input_content)

        # Remove the extension of input data file
        data_basename_without_extension = os.path.splitext(data_file_full_path)[0]
        print("Data_basename_without_extension: ", data_basename_without_extension)
        
        # replace the file name by whole path
        print('\ndata_file_base_name: ', data_file_base_name)
        print('\nData file full path: \n', data_file_full_path)

        
        print('\n\n---------------------------------------------------------')
        print('user_input_content: \n', user_input_content)

        #                                                                                     user_input_file_full_path, user_input_content, target_dir, model, old_ext='.txt'
        llmRequester.generate_multi_agents_request_for_sub_query_generation(user_input_file_full_path, user_input_content, output_dir+'/'+output_subdir, model, URL, temperature)


# Intent generation from user queries 
def user_sub_queries_generation_from_user_input_for_FASTMRIBRAIN_datasets(user_input_dir, common_base_directory, data_file_base_name, data_file_full_path, output_dir, output_subdir, model, URL, temperature):
    print(f'Processing directory {user_input_dir}')

    all_user_queries_directory_full_path = os.path.join(common_base_directory, user_input_dir)
    print('All_user_queries_directory_full_path: ', all_user_queries_directory_full_path)
    
    user_query_files_in_directory = os.listdir(all_user_queries_directory_full_path)
    print('User_query_files_in_directory: \n', user_query_files_in_directory)

    user_input_content = ""
    
    # Find the file that starts with the provided filename and has an extension
    for user_input_file in user_query_files_in_directory:
        user_input_base_name, ext = os.path.splitext(user_input_file)
        
        # also remove the data type extention
        user_input_base_name =  utils.get_base_filename(user_input_base_name)

        user_input_file_full_path = os.path.join(all_user_queries_directory_full_path, user_input_file)
        # Read the file (as text here; change for binary or specific format)
        with open(user_input_file_full_path, 'r') as f:
            content = f.read()
            user_input_content = content
            print("\nUser input content: ", user_input_content)

        # Remove the extension of input data file
        data_basename_without_extension = os.path.splitext(data_file_full_path)[0]
        print("Data_basename_without_extension: ", data_basename_without_extension)
        
        # replace the file name by whole path
        print('\ndata_file_base_name: ', data_file_base_name)
        print('\nData file full path: \n', data_file_full_path)

        
        print('\n\n---------------------------------------------------------')
        print('user_input_content: \n', user_input_content)

        #                                                                                     user_input_file_full_path, user_input_content, target_dir, model, old_ext='.txt'
        llmRequester.generate_multi_agents_request_for_sub_query_generation(user_input_file_full_path, user_input_content, output_dir+'/'+output_subdir, model, URL, temperature)




#                                       user_input_dir, JSON_FILE_PATH, common_base_directory+"/"+data_dir, subdirectories, extensions, output_dir, output_subdir, model
def RAG_NASA_CLIMATE_DATASETS(user_input_dir, JSON_FILE_PATH, common_directory, data_dir, data_subdirectories, extensions, output_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector, temperature):
    print(f'Processing directory {user_input_dir}')
    
    print(f'\nInside RAG_NASA_CLIMATE_DATASETS ...')
    print(f'JSON_FILE_PATH: {JSON_FILE_PATH}')
    print(f'user_input_dir: {user_input_dir}')
    print(f'common_directory: {common_directory}')
    print(f'common_directory/data_dir/data_subdir: ', common_directory+'/'+data_dir)
    
    try:
        for data_subdir in data_subdirectories:
            data_search_path = os.path.join(common_directory+'/'+data_dir, data_subdir, '*')
            print(f'Processing data search directory {data_search_path}')

            for ext in extensions:
                data_files = glob.glob(f"{data_search_path}.{ext}")
                for data_file_path in data_files:
                    print(f"\n\nProcessing file: {data_file_path}")
                    # get the input data
                    data_basename_with_extension = os.path.basename(data_file_path)                   

                    # common_base_directory, JSON_FILE_PATH, directory_file_name, key
                    if tracking.check_tracking_status_is_done(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension):
                        continue
                    else:
                        tracking.insert_or_update_key(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension, 'started')

                    # Remove the extension of input data file
                    data_basename_without_extension = os.path.splitext(data_basename_with_extension)[0]

                    # user input directory and list all files
                    user_input_files_in_directory = os.listdir(user_input_dir)

                    # save user input file data as user_input_content                    
                    # step 1: find the code description as user input
                    user_input_content = ""
                    # Find the file that starts with the provided filename and has an extension
                    for user_input_file in user_input_files_in_directory:
                        user_input_base_name, ext = os.path.splitext(user_input_file)
                        
                        # also remove the data type extention
                        user_input_base_name =  utils.get_base_filename(user_input_base_name)                        
                        
                        # print("user_input_base_name: ", user_input_base_name)
                        if user_input_base_name == data_basename_without_extension:
                            user_input_file_path = os.path.join(user_input_dir, user_input_file)
                            print(data_basename_with_extension)
                            
                            # Read the file (as text here; change for binary or specific format)
                            with open(user_input_file_path, 'r') as f:
                                content = f.read()
                                user_input_content = content
                                print("user input content: ", user_input_content)

                            dataset_attrubute_fullpath_list_result = ''
                            # if is with corrector
                            if with_corrector == True:
                                    print('\n------------Inside with corrector...')
                                    # current with corrector
                                    dataset_attrubute_fullpath_list_result, attribute_present, updated_text = corrector.corrector_function_main(user_input_content, data_file_path, False)
                                    print('Passed corrector_function_main function')

                            # replace the file name by whole path
                            user_input_content = utils.replace_string(user_input_content, data_basename_with_extension, data_file_path )
                            if with_rag == True:
                                print('\n------------Inside with RAG ...')
                                
                                # with updated text
                                examples_codes_for_query_augmentation = AGENTS.get_augmented_query(data_basename_with_extension+'.txt', model_name, is_errors, 'CLIMATE', temperature)
                                print(f'Inside sci data prompting main:: examples code for query augmentation: \n{examples_codes_for_query_augmentation}')
                            
                                # current with corrector
                                llmRequester.generate_code_and_save_with_rag(user_input_file_path, user_input_content, examples_codes_for_query_augmentation, data_file_path, output_dir+'/'+output_subdir, model, URL, dataset_attrubute_fullpath_list_result, temperature)
                            else:
                                print('\n------------Inside without RAG ...')
                                # current generating code without correcotrs

                                llmRequester.generate_code_and_save_without_rag(user_input_file_path, user_input_content, data_file_path, output_dir+'/'+output_subdir, model, URL, dataset_attrubute_fullpath_list_result, temperature)
                            
                            # assuming code generating completed here
                            tracking.insert_or_update_key(common_directory, JSON_FILE_PATH, output_subdir, data_basename_with_extension, 'done')
                            # tracking.insert_string_done(data_basename_with_extension)
                        else:
                            print('No Match!')
    except Exception as e:
        print('Exception occurred in RAG_NASA_CLIMATE_DATASETS, error message: ', e)


# user_input_dir, common_base_directory, output_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector
def RAG_MATPLOTAGENT_DATASETS(user_input_dir, common_base_directory, output_or_target_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector, temperature):

    print(f'\nInside RAG_MATPLOTAGENT_DATASETS ...')
    print(f'Processing directory {user_input_dir}')   
    print(f'output_or_target_dir: {output_or_target_dir}')
    
    # user input directory and list all files
    user_input_files_in_directory = os.listdir(user_input_dir)

    # save user input file data as user_input_content                    
    # step 1: find the code description as user input
    user_input_content = ""
    # Find the file that starts with the provided filename and has an extension
    for user_input_file in user_input_files_in_directory:
        print(f'input_file: {user_input_file}')
        user_input_base_name, ext = os.path.splitext(user_input_file)
        
        # also remove the data type extention
        user_input_base_name =  utils.get_base_filename(user_input_base_name)
        user_input_file_path = os.path.join(user_input_dir, user_input_file)                        
            
        # Read the file (as text here; change for binary or specific format)
        with open(user_input_file_path, 'r') as f:
            content = f.read()
            user_input_content = content
            print("user input content: ", user_input_content)

        # set data file full path       
        # outside project directory
        full_data_path = PROJECT_BASE_DIRECTORY+'../data_files_llm_project/MatPlotAgent/csv_to_h5_data/*_h5_data.h5'
        
        splitted_name = user_input_base_name.split('_')
        if len(splitted_name)>0:
            full_data_path = full_data_path.replace('*', str(splitted_name[0]))
        data_file_path = full_data_path
        data_basename_with_extension = os.path.basename(data_file_path)
        
        dataset_attrubute_fullpath_list_result = ''
        # if is with corrector
        if with_corrector == True:
                print('\n------------Inside with corrector...')
                # current with corrector
                dataset_attrubute_fullpath_list_result, attribute_present, updated_text = corrector.corrector_function_main(user_input_content, data_file_path, False)
                print('Passed corrector_function_main function')

        # replace the file name by whole path
        user_input_content = utils.replace_string(user_input_content, data_basename_with_extension, data_file_path )
        if with_rag == True:
            print('\n------------Inside with RAG ...')
            examples_codes_for_query_augmentation = AGENTS.get_augmented_query(user_input_base_name+'.txt', model_name, is_errors, 'MATPLOTAGENT', temperature)
            print(f'Inside sci data prompting main:: examples code for query augmentation: \n{examples_codes_for_query_augmentation}')
        
            # current with corrector
            # generate_code_and_save_with_rag(user_input_file_path, user_input_description, examples_for_query_augmentation, full_data_path, target_dir, model, URL):
            llmRequester.generate_code_and_save_with_rag(user_input_file_path, user_input_content, examples_codes_for_query_augmentation, data_file_path, output_dir+'/'+output_subdir, model, URL, dataset_attrubute_fullpath_list_result, temperature)
        else:
            print('\n------------Inside without RAG ...')
            # current generating code without correcotrs

            # parameters: user_input_file_path, user_input_description, full_data_path, target_dir, model, URL, dataset_attrubute_fullpath_list_result
            llmRequester.generate_code_and_save_without_rag(user_input_file_path, user_input_content, data_file_path, output_dir+'/'+output_subdir, model, URL, dataset_attrubute_fullpath_list_result, temperature)


# user_input_dir, common_base_directory, output_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector
def ITERATIVE_ERROR_RESOLVE_RAG_MATPLOTAGENT_DATASETS(user_input_dir, output_or_target_dir, output_subdir, is_with_rag, model, URL, dataset, is_errors, with_corrector):

    print(f'\nInside RAG_MATPLOTAGENT_DATASETS ...')
    print(f'Processing directory {user_input_dir}')   
    print(f'output_or_target_dir: {output_or_target_dir}')
    
    # user input directory and list all files
    user_input_files_in_directory = os.listdir(user_input_dir)
    if len(user_input_files_in_directory)>0:
        print(f'Available User queries: " {len(user_input_files_in_directory)}')
        for user_input_file in user_input_files_in_directory:
            print(f'Script Name: {user_input_file}')

    # save user input file data as user_input_content                    
    # step 1: find the code description as user input
    user_input_content = ""
    # Find the file that starts with the provided filename and has an extension
    for user_input_file in user_input_files_in_directory:
        print(f'input_file: {user_input_file}')
        user_input_base_name, ext = os.path.splitext(user_input_file)
        
        # also remove the data type extention
        user_input_base_name =  utils.get_base_filename(user_input_base_name)

        user_input_file_path = os.path.join(user_input_dir, user_input_file)                        
            
        # Read the file (as text here; change for binary or specific format)
        with open(user_input_file_path, 'r') as f:
            content = f.read()
            user_input_content = content
            print("user input content: ", user_input_content)

        # set data file full path
        base_directory ='/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
        full_data_path = base_directory+'/matplot_agent_data/plot_generation/csv_to_h5_data/*_h5_data.h5'
        splitted_name = user_input_base_name.split('_')
        if len(splitted_name)>0:
            full_data_path = full_data_path.replace('*', str(splitted_name[0]))
        data_file_path = full_data_path
        data_basename_with_extension = os.path.basename(data_file_path)
        # initalyze time
        corrector_run_time = 0
        rag_run_time = 0
        llm_run_time = 0

        dataset_attrubute_fullpath_list_result = ''
        # if is with corrector
        if with_corrector == True:
                print('\n------------Inside with corrector...')
                # current with corrector
                
                corrector_start_time = time.time()
                dataset_attrubute_fullpath_list_result, attribute_present, updated_text = corrector.corrector_function_main(user_input_content, data_file_path, False)
                corrector_end_time = time.time()
                corrector_run_time = corrector_end_time - corrector_start_time
                
                print('Passed corrector_function_main function')

        # replace the file name by whole path
        user_input_content = utils.replace_string(user_input_content, data_basename_with_extension, data_file_path )
        
        generated_python_code = ''
        generated_python_code_path = ''
        if is_with_rag == True:
            print('\n------------Inside with RAG ...')
            # current with corrector
            # result, attribute_present, updated_text = corrector.corrector_function_main(user_input_content, data_file_path, is_memory)
            # print('Passed corrector_function_main function')
            
            # with updated text
            # user_input_content=updated_text
            rag_start_time = time.time()
            examples_codes_for_query_augmentation = AGENTS.get_augmented_query(user_input_base_name+'.txt', model_name, is_errors, 'MATPLOTAGENT', temperature)
            rag_end_time = time.time()
            rag_run_time = rag_end_time - rag_start_time
            print(f'Inside sci data prompting main:: examples code for query augmentation: \n{examples_codes_for_query_augmentation}')
        
            # current with corrector
            # generate_code_and_save_with_rag(user_input_file_path, user_input_description, examples_for_query_augmentation, full_data_path, target_dir, model, URL):
            llm_start_time = time.time()
            generated_python_code_path, generated_python_code = llmRequester.generate_code_and_save_with_rag(user_input_file_path, user_input_content, examples_codes_for_query_augmentation, data_file_path, output_dir+'/'+output_subdir, model, URL, dataset_attrubute_fullpath_list_result, temperature)
            llm_end_time = time.time()
            llm_run_time = llm_end_time - llm_start_time
            utils.track_and_log_runtimes(output_or_target_dir+'/'+output_subdir+'.csv', model_name, corrector_run_time, rag_run_time, llm_run_time)    
            print(f'CSV file saved to the directory:\n{output_or_target_dir}'+f'/{output_subdir}'+'.csv')
        else:
            print('\n------------Inside without RAG ...')
            # current generating code without correcotrs

            # parameters: user_input_file_path, user_input_description, full_data_path, target_dir, model, URL, dataset_attrubute_fullpath_list_result
            generated_python_code_path, generated_python_code = llmRequester.generate_code_and_save_without_rag(user_input_file_path, user_input_content, data_file_path, output_dir+'/'+output_subdir, model, URL, dataset_attrubute_fullpath_list_result, temperature)


        # number_of_iteration = 6
        number_of_iteration = 0
                                
        # execute the code and check if is there any errors
        # if error then get the get the generated code and error message together and regenerate the code
        for iteration in range(0, number_of_iteration):
            print('Current iteration: ', iteration)
            # if the newly generated python script path has been returned 
            if generated_python_code_path is not None and len(generated_python_code_path) > 0: 
                    # Run the script and capture errors
                status, stderr = python_execution_helper.run_python_script(generated_python_code_path, output_subdir, 'MATPLOTAGENT')
                print(f'During iteration: {iteration}, status: {status}, stderr: {stderr}')

                if status=='Pass':
                    print('Pass')
                    break
                else:
                    print('Fail')
                    # Parse errors and categorize
                    if stderr is not None:
                        print('There is an error: \n', stderr)
                        query_augmentation = ''
                        # if with_corrector == True or is_with_rag == True:
                        formatted_error_message, last_line_of_error = utils.extract_key_lines_from_chained_exceptions(stderr)
                        stderr = formatted_error_message
                        
                        print('iterative error resolving with corrector')
                        #                                                                                                                          user_input_file_path, user_input_description, dataset_attrubute_fullpath_list_result, full_data_path, target_dir, model, python_script, error_message, iteration, URL, examples_for_query_augmentation, temperature
                        generated_python_code_path, generated_python_code = llmRequester.generate_code_and_save_code_MATPLOTAGENT_RAG_iterative_error_resolve(user_input_file_path, user_input_content, dataset_attrubute_fullpath_list_result, data_file_path, output_dir+'/'+output_subdir, model, generated_python_code, stderr, iteration, URL, query_augmentation, temperature)
                        print('ITERATIVE_ERROR_RESOLVE_NASA_CLIMATE_DATASETS_WITH_RAG_CORRECTOR_ONLINE_SEARCH new_python_script_path:\n', generated_python_code_path)
                        print('ITERATIVE_ERROR_RESOLVE_NASA_CLIMATE_DATASETS_WITH_RAG_CORRECTOR_ONLINE_SEARCH generated_python_script:\n', generated_python_code)
                       
                    else:
                        print('ITERATIVE_ERROR_RESOLVE_NASA_CLIMATE_DATASETS_WITH_RAG_CORRECTOR:: Error is None')

# user_input_dir, common_base_directory, output_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector
def RAG_FASTMRIBRAIN_DATASETS(user_input_dir, output_or_target_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector, temperature):

    print(f'\nInside RAG_MATPLOTAGENT_DATASETS ...')
    print(f'Processing directory {user_input_dir}')   
    print(f'output_or_target_dir: {output_or_target_dir}')
    
    # user input directory and list all files
    user_input_files_in_directory = os.listdir(user_input_dir)

    # save user input file data as user_input_content                    
    # step 1: find the code description as user input
    user_input_content = ""
    # Find the file that starts with the provided filename and has an extension
    for user_input_file in user_input_files_in_directory:
        print(f'input_file: {user_input_file}')
        user_input_base_name, ext = os.path.splitext(user_input_file)
        
        # also remove the data type extention
        user_input_base_name =  utils.get_base_filename(user_input_base_name)

        user_input_file_path = os.path.join(user_input_dir, user_input_file)                        
            
        # Read the file (as text here; change for binary or specific format)
        with open(user_input_file_path, 'r') as f:
            content = f.read()
            user_input_content = content
            print("user input content: ", user_input_content)

        # fetching the id
        user_input_prefix_id = user_input_base_name.split('_')[0]

        # set data file full path
       
        # inside project
        # full_data_path = base_directory+'/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/**_fastMRI_brain_first_10_dcm_to_h5.h5'
        # outside project
        full_data_path = PROJECT_BASE_DIRECTORY+'../data_files_llm_project/fastMri/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/**_fastMRI_brain_first_10_dcm_to_h5.h5'
        full_data_path = full_data_path.replace('**', user_input_prefix_id)
        # splitted_name = user_input_base_name.split('_')
        # if len(splitted_name)>0:
            # full_data_path = full_data_path.replace('*', str(splitted_name[0]))
        data_file_path = full_data_path
        data_basename_with_extension = os.path.basename(data_file_path)
        
        dataset_attrubute_fullpath_list_result = ''
        # if is with corrector
        if with_corrector == True:
                print('\n------------Inside with corrector...')
                # current with corrector
                dataset_attrubute_fullpath_list_result, attribute_present, updated_text = corrector.corrector_function_main(user_input_content, data_file_path, False)
                print('Passed corrector_function_main function')

        # replace the file name by whole path
        user_input_content = utils.replace_string(user_input_content, data_basename_with_extension, data_file_path )
        if with_rag == True:
            print('\n------------Inside with RAG ...')
            examples_codes_for_query_augmentation = AGENTS.get_augmented_query(user_input_base_name+'.txt', model_name, is_errors, 'FASTMRIBRAIN', temperature)
            print(f'Inside sci data prompting main:: examples code for query augmentation: \n{examples_codes_for_query_augmentation}')
        
            llmRequester.generate_code_and_save_with_rag(user_input_file_path, user_input_content, examples_codes_for_query_augmentation, data_file_path, output_dir+'/'+output_subdir, model, URL, dataset_attrubute_fullpath_list_result, temperature)
        else:
            print('\n------------Inside without RAG ...')
       
            llmRequester.generate_code_and_save_without_rag(user_input_file_path, user_input_content, data_file_path, output_dir+'/'+output_subdir, model, URL, dataset_attrubute_fullpath_list_result, temperature)

def ITERATIVE_ERROR_RESOLVE_RAG_FASTMRIBRAIN_DATASETS(user_input_dir, output_or_target_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector, temperature):

    print(f'\nInside ITERATIVE_ERROR_RESOLVE_RAG_FASTMRIBRAIN_DATASETS ...')
    print(f'Processing directory {user_input_dir}')   
    print(f'output_or_target_dir: {output_or_target_dir}')
    
    # user input directory and list all files
    user_input_files_in_directory = os.listdir(user_input_dir)

    # save user input file data as user_input_content                    
    # step 1: find the code description as user input
    user_input_content = ""
    # Find the file that starts with the provided filename and has an extension
    for user_input_file in user_input_files_in_directory:
        print(f'input_file: {user_input_file}')
        user_input_base_name, ext = os.path.splitext(user_input_file)
        
        # also remove the data type extention
        user_input_base_name =  utils.get_base_filename(user_input_base_name)

        user_input_file_path = os.path.join(user_input_dir, user_input_file)                        
            
        # Read the file (as text here; change for binary or specific format)
        with open(user_input_file_path, 'r') as f:
            content = f.read()
            user_input_content = content
            print("user input content: ", user_input_content)

        # fetching the id
        user_input_prefix_id = user_input_base_name.split('_')[0]

        # set data file full path
        base_directory ='/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
        full_data_path = base_directory+'/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5/**_fastMRI_brain_first_10_dcm_to_h5.h5'
        full_data_path = full_data_path.replace('**', user_input_prefix_id)
        # splitted_name = user_input_base_name.split('_')
        # if len(splitted_name)>0:
            # full_data_path = full_data_path.replace('*', str(splitted_name[0]))
        data_file_path = full_data_path
        data_basename_with_extension = os.path.basename(data_file_path)
        # initialyze time
        corrector_run_time = 0
        rag_run_time = 0
        llm_run_time = 0

        dataset_attrubute_fullpath_list_result = ''
        # if is with corrector
        if with_corrector == True:
                print('\n------------Inside with corrector...')
                # current with corrector
                corrector_start_time = time.time()
                dataset_attrubute_fullpath_list_result, attribute_present, updated_text = corrector.corrector_function_main(user_input_content, data_file_path, False)
                corrector_end_time = time.time()
                corrector_run_time = corrector_end_time - corrector_start_time
                
                print('Passed corrector_function_main function')

        # replace the file name by whole path
        user_input_content = utils.replace_string(user_input_content, data_basename_with_extension, data_file_path )
        examples_codes_for_query_augmentation = ''
        if with_rag == True:
            print('\n------------Inside with RAG ...')
            # current with corrector
            
            # with updated text
            # user_input_content=updated_text
            rag_start_time = time.time()
            examples_codes_for_query_augmentation = AGENTS.get_augmented_query(user_input_base_name+'.txt', model_name, is_errors, 'FASTMRIBRAIN', temperature)
            rag_end_time = time.time()
            rag_run_time = rag_end_time - rag_start_time
            print(f'Inside sci data prompting main:: examples code for query augmentation: \n{examples_codes_for_query_augmentation}')
        
            # current with corrector
        llm_start_time = time.time()
        generated_python_script_path, generated_python_script = llmRequester.generate_code_and_save_with_rag(user_input_file_path, user_input_content, examples_codes_for_query_augmentation, data_file_path, output_dir+'/'+output_subdir, model, URL, dataset_attrubute_fullpath_list_result, temperature)
        llm_end_time = time.time()
        llm_run_time = llm_end_time - llm_start_time

        utils.track_and_log_runtimes(output_or_target_dir+'/'+output_subdir+'.csv', model_name, corrector_run_time, rag_run_time, llm_run_time)    
        print(f'CSV file saved to the directory:\n{output_or_target_dir}'+f'/{output_subdir}'+'.csv')
        # number_of_iteration = 6
        # for time record with single iteration
        number_of_iteration = 0

        # if error then get the get the generated code and error message together and regenerate the code
        for iteration in range(0, number_of_iteration):
            print('Current iteration: ', iteration)
            # if the newly generated python script path has been returned 
            if generated_python_script_path is not None and len(generated_python_script_path) > 0: 
                    # Run the script and capture errors
                status, stderr = python_execution_helper.run_python_script(generated_python_script_path, output_subdir, 'FASTMRIBRAIN')
                print(f'During iteration: {iteration}, status: {status}, stderr: {stderr}')

                if status=='Pass':
                    print('Pass')
                    break
                else:
                    print('Fail')
                    # Parse errors and categorize
                    if stderr is not None:
                        print('There is an error: \n', stderr)
                        query_augmentation = ''
                        # if with_corrector == True or is_with_rag == True:
                        formatted_error_message, last_line_of_error = utils.extract_key_lines_from_chained_exceptions(stderr)
                        stderr = formatted_error_message
                        
                        print('iterative error resolving with corrector')
                        
                        generated_python_script_path, generated_python_script = llmRequester.generate_code_and_save_code_FASTMRIBRAIN_RAG_iterative_error_resolve(
                                            user_input_file_path=user_input_file_path, 
                                            user_input_description=user_input_content, 
                                            dataset_attrubute_fullpath_list_result=dataset_attrubute_fullpath_list_result, 
                                            full_data_path=data_file_path, 
                                            target_dir=output_dir+'/'+output_subdir, 
                                            model=model, 
                                            python_script=generated_python_script, 
                                            error_message=stderr, 
                                            iteration=iteration, 
                                            URL=URL, 
                                            examples_for_query_augmentation=query_augmentation, 
                                            temperature=temperature)
                        print('generate_code_and_save_code_FASTMRIBRAIN_RAG_iterative_error_resolve generated_python_script_path:\n', generated_python_script_path)
                        print('generate_code_and_save_code_FASTMRIBRAIN_RAG_iterative_error_resolve generated_python_script:\n', generated_python_script)
                       
                    else:
                        print('ITERATIVE_ERROR_RESOLVE_NASA_CLIMATE_DATASETS_WITH_RAG_CORRECTOR:: Error is None')


# user_input_dir, common_base_directory, output_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector
def RAG_VTK_DATASETS(user_input_dir, output_or_target_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector):

    print(f'\nInside RAG_VTK_DATASETS ...')
    print(f'Processing directory {user_input_dir}')   
    print(f'output_or_target_dir: {output_or_target_dir}')
    
    # user input directory and list all files
    user_input_files_in_directory = os.listdir(user_input_dir)

    # save user input file data as user_input_content                    
    # step 1: find the code description as user input
    user_input_content = ""
    # Find the file that starts with the provided filename and has an extension
    for user_input_file in user_input_files_in_directory:
        print(f'input_file: {user_input_file}')
        user_input_base_name, ext = os.path.splitext(user_input_file)
        
        # also remove the data type extention
        user_input_base_name =  utils.get_base_filename(user_input_base_name)

        user_input_file_path = os.path.join(user_input_dir, user_input_file)                        
            
        # Read the file (as text here; change for binary or specific format)
        with open(user_input_file_path, 'r') as f:
            content = f.read()
            user_input_content = content
            print("user input content: ", user_input_content)

        # fetching the id
        user_input_prefix_id = user_input_base_name.split('_')[0]
        full_data_path = ''
       
        data_file_path = full_data_path
        data_basename_with_extension = os.path.basename(data_file_path)
        
        dataset_attrubute_fullpath_list_result = ''
        # if is with corrector
        if with_corrector == True:
                print('\n------------Inside with corrector...')               
                print('Passed corrector_function_main function')

        # replace the file name by whole path
        user_input_content = utils.replace_string(user_input_content, data_basename_with_extension, data_file_path )
        if with_rag == True:
            print('\n------------Inside with RAG ...')
            # with updated text
            # user_input_content=updated_text
            examples_codes_for_query_augmentation = AGENTS.get_augmented_query(user_input_base_name+'.txt', model_name, is_errors, 'FASTMRIBRAIN', temperature)
            print(f'Inside sci data prompting main:: examples code for query augmentation: \n{examples_codes_for_query_augmentation}')
        
        else:
            print('\n------------Inside without RAG ...')
            # current generating code without correcotrs
            llmRequester.generate_code_and_save_VTK_related_python_scripts_without_rag(user_input_file_path=user_input_file_path, 
                                                                                       user_input_description=user_input_content, 
                                                                                       full_data_path=data_file_path, 
                                                                                       target_dir=output_or_target_dir+'/'+output_subdir, 
                                                                                       model=model, URL=URL, dataset_attrubute_fullpath_list_result=dataset_attrubute_fullpath_list_result)

# user_input_dir, common_base_directory, output_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector
def ITERATIVE_ERROR_RESOLVE_RAG_VTK_DATASETS(user_input_dir, output_or_target_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector):

    print(f'\nInside RAG_VTK_DATASETS ...')
    print(f'Processing directory {user_input_dir}')   
    print(f'output_or_target_dir: {output_or_target_dir}')

    # for the vtk user queries a first transfer all data files to the current directory
    #at first move all data files to the generated script directory
    extensions = ['.txt', '.pgm', '.3ds', '.vtk', '.vtp', '.mhd', '.zraw', '.raw', '.mha', '.tri']      
    # utils.move_files_by_extension(all_files_source_directory, python_script_dir, extensions)
    target_base_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data'
    all_files_source_directory = f'{target_base_dir}/vtk_data'

    program_execution_base_directory = PROJECT_BASE_DIRECTORY
    utils.move_files_by_extension(all_files_source_directory, program_execution_base_directory, extensions)
    
    # user input directory and list all files
    user_input_files_in_directory = os.listdir(user_input_dir)

    # save user input file data as user_input_content                    
    # step 1: find the code description as user input
    user_input_content = ""
    # Find the file that starts with the provided filename and has an extension
    for user_input_file in user_input_files_in_directory:
        print(f'input_file: {user_input_file}')
        user_input_base_name, ext = os.path.splitext(user_input_file)
        
        # also remove the data type extention
        user_input_base_name =  utils.get_base_filename(user_input_base_name)

        user_input_file_path = os.path.join(user_input_dir, user_input_file)                        
            
        # Read the file (as text here; change for binary or specific format)
        with open(user_input_file_path, 'r') as f:
            content = f.read()
            user_input_content = content
            print("user input content: ", user_input_content)

        # fetching the id
        user_input_prefix_id = user_input_base_name.split('_')[0]

        # set data file full path
        full_data_path = ''
        # splitted_name = user_input_base_name.split('_')
        # if len(splitted_name)>0:
            # full_data_path = full_data_path.replace('*', str(splitted_name[0]))
        data_file_path = full_data_path
        data_basename_with_extension = os.path.basename(data_file_path)
        
        dataset_attrubute_fullpath_list_result = ''
        # if is with corrector
        if with_corrector == True:
                print('\n------------Inside with corrector...')
                # current with corrector
                print('Passed corrector_function_main function')

        # replace the file name by whole path
        user_input_content = utils.replace_string(user_input_content, data_basename_with_extension, data_file_path )
        examples_codes_for_query_augmentation = ''
        if with_rag == True:
            print('\n------------Inside with RAG ...')
            
            # with updated text
            # user_input_content=updated_text
            examples_codes_for_query_augmentation = AGENTS.get_augmented_query(user_input_base_name+'.txt', model_name, is_errors, 'VTK', temperature)
            print(f'Inside sci data prompting main:: examples code for query augmentation: \n{examples_codes_for_query_augmentation}')
        
        # , , , , model, URL, dataset_attrubute_fullpath_list_result
        generated_python_script_path, generated_python_script = llmRequester.generate_code_and_save_VTK_related_python_scripts_without_rag(
                    user_input_file_path=user_input_file_path, 
                    user_input_description=user_input_content, 
                    full_data_path=data_file_path, 
                    target_dir=output_or_target_dir+'/'+output_subdir, 
                    model=model, URL=URL, dataset_attrubute_fullpath_list_result=dataset_attrubute_fullpath_list_result)
        number_of_iteration = 1

        # execute the code and check if is there any errors
        # if error then get the get the generated code and error message together and regenerate the code
        for iteration in range(1, number_of_iteration):
            print('Current iteration: ', iteration)
            # if the newly generated python script path has been returned 
            if generated_python_script_path is not None and len(generated_python_script_path) > 0: 
                    # Run the script and capture errors
                status, stderr = python_execution_helper.run_python_script(generated_python_script_path, output_subdir, 'VTK')
                print(f'During iteration: {iteration}, status: {status}, stderr: {stderr}')

                if status=='Pass':
                    print('Pass')
                    break
                else:
                    print('Fail')
                    # Parse errors and categorize
                    if stderr is not None:
                        print('There is an error: \n', stderr)
                        query_augmentation = ''
                        # if with_corrector == True or is_with_rag == True:
                        formatted_error_message, last_line_of_error = utils.extract_key_lines_from_chained_exceptions(stderr)
                        stderr = formatted_error_message
                        
                        print('iterative error resolving with corrector')
                        # for the VTK related user queries there is no data file path
                        data_file_path = ''
                        #                                                                                                                           user_input_file_path, user_input_content, result, data_file_path, output_dir+'/'+output_subdir, attribute_present, model, is_memory, '', '', 0, URL
                        generated_python_script_path, generated_python_script = llmRequester.generate_code_and_save_code_VTK_RAG_iterative_error_resolve(user_input_file_path, user_input_content, dataset_attrubute_fullpath_list_result, data_file_path, output_dir+'/'+output_subdir, model, generated_python_script, stderr, iteration, URL, query_augmentation)
                        print('generate_code_and_save_code_FASTMRIBRAIN_RAG_iterative_error_resolve generated_python_script_path:\n', generated_python_script_path)
                        print('generate_code_and_save_code_FASTMRIBRAIN_RAG_iterative_error_resolve generated_python_script:\n', generated_python_script)
                       
                    else:
                        print('ITERATIVE_ERROR_RESOLVE_NASA_CLIMATE_DATASETS_WITH_RAG_CORRECTOR:: Error is None')

    #At the end move all data files to the generated script directory 
    utils.move_files_by_extension(program_execution_base_directory, all_files_source_directory, extensions)

# USER queries generation from VTK related python scripts
def user_queries_generation_from_vtk_related_python_scripts_for_VTK_datasets(user_input_dir, data_file_base_name, data_file_full_path, output_dir, output_subdir, model, URL):
    print(f'Processing directory {user_input_dir}')

    all_user_queries_directory_full_path = os.path.join(PROJECT_BASE_DIRECTORY, user_input_dir)
    print('All_user_queries_directory_full_path: ', all_user_queries_directory_full_path)
    
    user_query_files_in_directory = os.listdir(all_user_queries_directory_full_path)
    print('User_query_files_in_directory: \n', user_query_files_in_directory)

    user_input_content = ""
    
    # Find the file that starts with the provided filename and has an extension
    for user_input_file in user_query_files_in_directory:
        user_input_base_name, ext = os.path.splitext(user_input_file)
        
        # also remove the data type extention
        user_input_base_name =  utils.get_base_filename(user_input_base_name)

        user_input_file_full_path = os.path.join(all_user_queries_directory_full_path, user_input_file)
        # Read the file (as text here; change for binary or specific format)
        with open(user_input_file_full_path, 'r') as f:
            content = f.read()
            user_input_content = content
            print("\nUser input content: ", user_input_content)

        # Remove the extension of input data file
        data_basename_without_extension = os.path.splitext(data_file_full_path)[0]
        print("Data_basename_without_extension: ", data_basename_without_extension)
        
        # replace the file name by whole path
        print('\ndata_file_base_name: ', data_file_base_name)
        print('\nData file full path: \n', data_file_full_path)

        
        print('\n\n---------------------------------------------------------')
        print('user_input_content: \n', user_input_content)

        llmRequester.generate_request_for_VTK_related_user_query_generation(user_input_file_full_path=user_input_file_full_path, 
                                                                            user_input_content=user_input_content, 
                                                                            target_dir=output_dir+'/'+output_subdir, model=model, URL=URL, is_errors=is_errors)





if __name__ == '__main__':    
    # this is for the GSU sci-data virtual machine
    extensions = ['hdf5', 'he5', 'h5', 'HDF5', 'H5', 'HE5']
       
    # Create the argument parser
    parser = argparse.ArgumentParser(description = "Select models to use correct LLM model")   
    
    model, model_name, dataset, is_with_rag, URL, is_errors, with_corrector, is_online_search, temperature = argumentParsar.parse_argument(parser)  
    output_directory_prefix = model_name
    
    output_subdir =''
    user_input_dir = ''
    is_memory = False
    # create a tracking file with same name as output_subdir
    # def initialize_json(PROJECT_BASE_DIRECTORY, JSON_FILE_PATH, directory_file_name):
    JSON_FILE_PATH = 'experiment_main/tracking_file'
    temp = str(temperature).replace('.', '_')

    # model_name = "gpt_oss_20b"
    prefix = "single_phase"
    
    # created May 18, 2025
    #user sub queries generation
    if dataset == 'USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS':
        
        extensions = ['hdf5', 'he5', 'h5', 'HDF5', 'H5', 'HE5']
        output_dir = PROJECT_BASE_DIRECTORY+'/user_queries/generated_user_sub_queries'
             
        # without errors
        if is_errors==False:
            # output_directory_prefix=model_name
            output_subdir = f'{output_directory_prefix}_temp_{temp}_generated_user_sub_queries_from_expert_user_queries_final'
            user_input_dir = PROJECT_BASE_DIRECTORY +f'/user_queries/generated_user_queries/deepseek_r1_70b_generated_expert_queries_from_human_expert_queries_final_manually_corrected'
        # with errors
        else:
            output_subdir = f'{output_directory_prefix}_temp_{temp}_generated_user_sub_queries_from_expert_user_queries_final_with_errors'
            # queries with errors
            user_input_dir = PROJECT_BASE_DIRECTORY +f'/user_queries/generated_user_queries/deepseek_r1_70b_generated_expert_queries_from_human_expert_queries_final_manually_corrected_with_errors'

        print('Inside USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS ...')
        data_file_base_name = ''
        data_file_full_path = ''

        user_sub_queries_generation_from_user_input_for_CLIMATE_datasets(user_input_dir, PROJECT_BASE_DIRECTORY, data_file_base_name, data_file_full_path, output_dir, output_subdir, model, URL, temperature)
        

    # created Jun 10, 2025
    #user sub queries generation
    elif dataset == 'USER_SUB_QUERY_GENERATION_MATPLOTAGENT_DATASETS':
        # file_list = ['76', '77', '78', '79', '83', '84', '87', '95', '96', '97', '99', '100']
        extensions = ['hdf5', 'he5', 'h5', 'HDF5', 'H5', 'HE5']
        output_dir = PROJECT_BASE_DIRECTORY+'/user_queries/generated_user_sub_queries/matplotagent'
        
        # without errors
        if is_errors==False:
            output_subdir = f'{output_directory_prefix}_matplotagent_generated_user_sub_queries_from_expert_user_queries_final'
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/generated_user_queries/matplotagent/expert_queries'
        # with errors
        else:
            output_subdir = f'{output_directory_prefix}_matplotagent_generated_user_sub_queries_from_expert_user_queries_final_with_errors'
            # queries with errors
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/generated_user_queries/matplotagent/simple_queries'

        print('Inside USER_SUB_QUERY_GENERATION_MATPLOT_DATASETS ...')
        data_file_base_name = ''
        data_file_full_path = ''

        user_sub_queries_generation_from_user_input_for_MATPLOTAGENT_datasets(user_input_dir, PROJECT_BASE_DIRECTORY, data_file_base_name, data_file_full_path, output_dir, output_subdir, model, URL, temperature)
       
    
    # created May 18, 2025
    #user sub queries generation
    elif dataset == 'USER_SUB_QUERY_GENERATION_FASTMRIBRAIN_DATASETS':
        # extensions = ['hdf5', 'he5', 'h5', 'HDF5', 'H5', 'HE5']
        output_dir = PROJECT_BASE_DIRECTORY+'/user_queries/generated_user_sub_queries/fastmri_brain'
        
        
        # without errors
        if is_errors==False:
            output_subdir = f'{output_directory_prefix}_fastmribrain_generated_user_sub_queries_from_expert_user_queries_final'
             
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/manually_edited_user_queries/fast_mri_brain_datasets/user_queries_generated_by_10_percent_reduc_final_with_attributes'
        # with errors
        else:
            output_subdir = f'{output_directory_prefix}_fastmribrain_generated_user_sub_queries_from_expert_user_queries_final_with_errors'
            # queries with errors
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/manually_edited_user_queries/fast_mri_brain_datasets/user_queries_generated_by_10_percent_reduc_then_human_modified_error_insertion'

        print('Inside USER_SUB_QUERY_GENERATION_FASTMRIBRAIN_DATASETS ...')
        data_file_base_name = ''
        data_file_full_path = ''

        user_sub_queries_generation_from_user_input_for_FASTMRIBRAIN_datasets(user_input_dir, PROJECT_BASE_DIRECTORY, data_file_base_name, data_file_full_path, output_dir, output_subdir, model, URL, temperature)
      

    elif dataset == 'CLIMATE_RAG':
        output_dir = PROJECT_BASE_DIRECTORY+'/NASA_EOS/llm_rag_generated_python_scripts/non_iterative'
        with_rag = is_with_rag
        
        print('Inside Climate datasets')
        
        data_dir = 'ACL_DIRS'  # Replace with your common directory path        
        # Replace with your predefined subdirectory names
        subdirectories = ['ASF', 'GES_DISC', 'GHRC', 'ICESat_2', 'LAADS', 'LaRC', 'LP_DAAC', 'NSIDC', 'Ocen_Biology', 'PO_DAAC', 'AURA_DATA_VC']
        
        # user queries input directory
        input_sub_directories = 'user_queries/generated_user_queries'
        
        
        # without errors
        if is_errors==False:
            user_input_dir = PROJECT_BASE_DIRECTORY +'/'+input_sub_directories+'/deepseek_r1_70b_generated_expert_queries_from_human_expert_queries_final_manually_corrected'
        
        # with errors
        else:       
            user_input_dir = PROJECT_BASE_DIRECTORY +'/'+input_sub_directories+'/deepseek_r1_70b_generated_expert_queries_from_human_expert_queries_final_manually_corrected_with_errors'

        # python script output directory
        if with_rag == True:
            # with rag
            # without error
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_{temp}_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_{temp}_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector'

            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_{temp}_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_{temp}_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector'
        else:
            # without rag
            # without errors
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_{temp}_python_scripts_without_rag_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_{temp}_python_scripts_without_rag_with_corrector'
            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_{temp}_python_scripts_without_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_{temp}_python_scripts_without_rag_with_errors_with_corrector'

        tracking.initialize_json(PROJECT_BASE_DIRECTORY, JSON_FILE_PATH, output_subdir)

        #                         user_input_dir, JSON_FILE_PATH, common_directory,      data_dir, data_subdirectories, extensions, output_dir, output_subdir, model
        RAG_NASA_CLIMATE_DATASETS(user_input_dir, JSON_FILE_PATH, PROJECT_BASE_DIRECTORY, data_dir, subdirectories, extensions, output_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector, temperature)

    elif dataset == 'ITERATIVE_ERROR_RESOLVE_CLIMATE':
        print('Inside ITERATIVE_ERROR_RESOLVE_CLIMATE ...')
        output_dir = PROJECT_BASE_DIRECTORY+'/NASA_EOS/llm_rag_generated_python_scripts/iterative_error_resolve'
        
        input_sub_directories = 'user_queries/generated_user_queries'

        # without errors
        if is_errors==False:
            # newly created expert level queries``
            user_input_dir = PROJECT_BASE_DIRECTORY +'/'+input_sub_directories+'/deepseek_r1_70b_generated_expert_queries_from_human_expert_queries_final_manually_corrected'        
        # with errors
        else:       
            user_input_dir = PROJECT_BASE_DIRECTORY +'/'+input_sub_directories+'/deepseek_r1_70b_generated_expert_queries_from_human_expert_queries_final_manually_corrected_with_errors'

        data_dir = 'ACL_DIRS'  # Replace with your common directory path        
        # Replace with your predefined subdirectory names
        subdirectories = ['NSIDC', 'PO_DAAC', 'ASF', 'GES_DISC', 'GHRC', 'ICESat_2', 'LAADS', 'LaRC', 'LP_DAAC',  'Ocen_Biology', 'AURA_DATA_VC']
        
        # python script output directory
        if is_with_rag == True:
            # with rag
            # without error
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_climate_iterative_error_resolve_python_scripts_with_rag_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_climate_iterative_error_resolve_python_scripts_with_rag_with_corrector'

            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_with_corrector'
        else:
            # without rag
            # without errors
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_climate_iterative_error_resolve_python_scripts_without_rag_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_climate_iterative_error_resolve_python_scripts_without_rag_with_corrector'
            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_with_corrector'

        tracking.initialize_json(PROJECT_BASE_DIRECTORY, JSON_FILE_PATH, output_subdir)

        ITERATIVE_ERROR_RESOLVE_NASA_CLIMATE_DATASETS_WITH_RAG_CORRECTOR_ONLINE_SEARCH(user_input_dir, JSON_FILE_PATH, PROJECT_BASE_DIRECTORY, data_dir, subdirectories, extensions, output_dir, output_subdir, with_corrector, model, URL, temperature)
        # collect all images and store them into a new directory
        source_dirs = subdirectories  # List of source directories
        source_dirs.append('../prompting_techniques/zero_shot_sci_data_prompting')
        new_dir_name = output_subdir
        # data_dir = 'ACL_DIRS'
        
        utils.collect_and_store_png(source_dirs, new_dir_name, data_dir)
    
   

    elif dataset == 'MATPLOTAGENT_RAG':
        print('Inside Matplotagent datasets ...')
        output_dir = PROJECT_BASE_DIRECTORY+'/MatPlotAgent/llm_rag_generated_python_scripts/non_iterative'
        with_rag = is_with_rag        
                
        # without errors
        if is_errors==False:
            # newly created expert level queries
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/generated_user_queries/matplotagent/expert_queries'
        # with errors
        else:       
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/generated_user_queries/matplotagent/simple_queries'

        # python script output directory
        if with_rag == True:
            # with rag
            # without error
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_{temp}_matplotagent_python_scripts_with_rag_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_{temp}_matplotagent_python_scripts_with_rag_with_corrector'

            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_{temp}_matplotagent_python_scripts_with_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_{temp}_matplotagent_python_scripts_with_rag_with_errors_with_corrector'
        else:
            # without rag
            # without errors
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_{temp}_matplotagent_python_scripts_without_rag_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_{temp}_matplotagent_python_scripts_without_rag_with_corrector'
            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_{temp}_matplotagent_python_scripts_without_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_{temp}_matplotagent_python_scripts_without_rag_with_errors_with_corrector'

   
        RAG_MATPLOTAGENT_DATASETS(user_input_dir, PROJECT_BASE_DIRECTORY, output_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector, temperature)
    
    
    elif dataset == 'ITERATIVE_ERROR_RESOLVE_MATPLOTAGENT_RAG':
        print('Inside Matplotagent datasets ...')
        output_dir = PROJECT_BASE_DIRECTORY+'/MatPlotAgent/llm_rag_generated_python_scripts/iterative_error_resolve'
        with_rag = is_with_rag        
                
        # without errors
        if is_errors==False:
            # newly created expert level queries
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/generated_user_queries/matplotagent/expert_queries'
        # with errors
        else:       
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/generated_user_queries/matplotagent/simple_queries'

        # python script output directory
        if with_rag == True:
            # with rag
            # without error
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_matplotagent_iterative_python_scripts_with_rag_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_matplotagent_iterative_python_scripts_with_rag_with_corrector_time_record'
            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_matplotagent_iterative_python_scripts_with_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_matplotagent_iterative_python_scripts_with_rag_with_errors_with_corrector'
        else:
            # without rag
            # without errors
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_matplotagent_iterative_python_scripts_without_rag_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_matplotagent_iterative_python_scripts_without_rag_with_corrector'
            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_matplotagent_iterative_python_scripts_without_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_matplotagent_iterative_python_scripts_without_rag_with_errors_with_corrector'

        # tracking.initialize_json(PROJECT_BASE_DIRECTORY, JSON_FILE_PATH, output_subdir)
        ITERATIVE_ERROR_RESOLVE_RAG_MATPLOTAGENT_DATASETS(user_input_dir=user_input_dir, output_or_target_dir=output_dir, output_subdir=output_subdir, is_with_rag=with_rag, 
                                                          model=model, URL=URL, dataset=dataset, is_errors=is_errors, with_corrector=with_corrector)

    elif dataset == 'FASTMRIBRAIN_RAG':
        print('Inside FASTMRIBRAIN_RAG datasets ...')
        output_dir = PROJECT_BASE_DIRECTORY+'/fastMri/llm_rag_generated_python_scripts/non_iterative'
        with_rag = is_with_rag        
                
        # without errors
        if is_errors==False:
            # newly created expert level queries
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/manually_edited_user_queries/fast_mri_brain_datasets/user_queries_generated_by_10_percent_reduc_final_with_attributes'
        # with errors
        else:       
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/manually_edited_user_queries/fast_mri_brain_datasets/user_queries_generated_by_10_percent_reduc_then_human_modified_error_insertion'

        # python script output directory
        if with_rag == True:
            # with rag
            # without error
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_{temp}_fastmribrain_python_scripts_with_rag_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_{temp}_fastmribrain_python_scripts_with_rag_with_corrector'

            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_{temp}_fastmribrain_python_scripts_with_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_{temp}_fastmribrain_python_scripts_with_rag_with_errors_with_corrector'
        else:
            # without rag
            # without errors
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_{temp}_fastmribrain_python_scripts_without_rag_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_{temp}_fastmribrain_python_scripts_without_rag_with_corrector'
            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_{temp}_fastmribrain_python_scripts_without_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_{temp}_fastmribrain_python_scripts_without_rag_with_errors_with_corrector'

        # tracking.initialize_json(PROJECT_BASE_DIRECTORY, JSON_FILE_PATH, output_subdir)

        RAG_FASTMRIBRAIN_DATASETS(user_input_dir, output_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector, temperature)
    elif dataset == 'ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG':
        print('Inside FASTMRIBRAIN_RAG datasets ...')
        output_dir = PROJECT_BASE_DIRECTORY+'/fastMri/llm_rag_generated_python_scripts/iterative_error_resolve'
        with_rag = is_with_rag        
                
        # without errors
        if is_errors==False:
            # newly created expert level queries
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/manually_edited_user_queries/fast_mri_brain_datasets/user_queries_generated_by_10_percent_reduc_final_with_attributes'
        # with errors
        else:       
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/manually_edited_user_queries/fast_mri_brain_datasets/user_queries_generated_by_10_percent_reduc_then_human_modified_error_insertion'

        # python script output directory
        if with_rag == True:
            # with rag
            # without error
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_fastmribrain_iterative_python_scripts_with_rag_without_corrector'
                if with_corrector == True:
                    # output_subdir = f'{output_directory_prefix}_fastmribrain_iterative_python_scripts_with_rag_with_corrector'
                    output_subdir = f'{output_directory_prefix}_fastmribrain_iterative_python_scripts_with_rag_with_corrector_time_record'

            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_fastmribrain_iterative_python_scripts_with_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_fastmribrain_iterative_python_scripts_with_rag_with_errors_with_corrector'
        else:
            # without rag
            # without errors
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_fastmribrain_iterative_python_scripts_without_rag_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_fastmribrain_iterative_python_scripts_without_rag_with_corrector'
            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_fastmribrain_iterative_python_scripts_without_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_fastmribrain_iterative_python_scripts_without_rag_with_errors_with_corrector'

        # tracking.initialize_json(PROJECT_BASE_DIRECTORY, JSON_FILE_PATH, output_subdir)

        ITERATIVE_ERROR_RESOLVE_RAG_FASTMRIBRAIN_DATASETS(user_input_dir, output_dir, output_subdir, with_rag, model, URL, dataset, is_errors, with_corrector, temperature)
    
    elif dataset == 'VTK_RAG':
        print('Inside VTK_RAG datasets ...')
        output_dir = PROJECT_BASE_DIRECTORY+'/VTK/llm_rag_generated_python_scripts/non_iterative'
                
        # without errors: expert queries
        if is_errors==False:
            # newly created expert level queries
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/generated_user_queries/vtk/deepseek_r1_70b_generated_user_queries_from_vtk_python_scripts_human_reviewed'
        # with errors
        else:       
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/generated_user_queries/vtk/devstral_24b_generated_user_queries_from_vtk_python_scripts_with_errors'

        # python script output directory
        if is_with_rag == True:
            # with rag
            # without error
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_vtk_python_scripts_with_rag_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_vtk_python_scripts_with_rag_with_corrector'

            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_vtk_python_scripts_with_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_vtk_python_scripts_with_rag_with_errors_with_corrector'
        else:
            # without rag
            # without errors
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_vtk_python_scripts_without_rag_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_vtk_python_scripts_without_rag_with_corrector'
            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_vtk_python_scripts_without_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_vtk_python_scripts_without_rag_with_errors_with_corrector'

        # tracking.initialize_json(PROJECT_BASE_DIRECTORY, JSON_FILE_PATH, output_subdir)
        RAG_VTK_DATASETS(user_input_dir=user_input_dir, output_or_target_dir=output_dir, output_subdir=output_subdir, with_rag=is_with_rag, model=model, URL=URL, dataset=dataset, is_errors=is_errors, with_corrector=with_corrector)
    
    elif dataset == 'ITERATIVE_ERROR_RESOLVE_VTK_RAG':
        print('Inside VTK_RAG datasets ...')
        output_dir = PROJECT_BASE_DIRECTORY+'/VTK/llm_rag_generated_python_scripts/iterative_error_resolve'
        # with_rag = is_with_rag        
                
        # without errors: expert queries
        if is_errors==False:
            # newly created expert level queries
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/generated_user_queries/vtk/deepseek_r1_70b_generated_user_queries_from_vtk_python_scripts_human_reviewed'
        # with errors
        else:       
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/generated_user_queries/vtk/devstral_24b_generated_user_queries_from_vtk_python_scripts_with_errors'

        # python script output directory
        if is_with_rag == True:
            # with rag
            # without error
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_vtk_iterative_python_scripts_with_rag_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_vtk_iterative_python_scripts_with_rag_with_corrector'

            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_vtk_iterative_python_scripts_with_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_vtk_iterative_python_scripts_with_rag_with_errors_with_corrector'
        else:
            # without rag
            # without errors
            if is_errors==False:
                output_subdir = f'{output_directory_prefix}_vtk_iterative_python_scripts_without_rag_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_vtk_iterative_python_scripts_without_rag_with_corrector'
            # with errors
            else:
                output_subdir = f'{output_directory_prefix}_vtk_iterative_python_scripts_without_rag_with_errors_without_corrector'
                if with_corrector == True:
                    output_subdir = f'{output_directory_prefix}_vtk_iterative_python_scripts_without_rag_with_errors_with_corrector'

        # tracking.initialize_json(PROJECT_BASE_DIRECTORY, JSON_FILE_PATH, output_subdir)

        ITERATIVE_ERROR_RESOLVE_RAG_VTK_DATASETS(user_input_dir, output_dir, output_subdir, is_with_rag, model, URL, dataset, is_errors, with_corrector)
    
    #user queries generation for the vtk related python scripts
    elif dataset == 'VTK_USER_QUERY_GENERATION_VTK_DATASETS':
        print('Inside VTK_USER_QUERY_GENERATION_VTK_DATASETS ...')
               
        output_dir = PROJECT_BASE_DIRECTORY+'/user_queries/generated_user_queries/vtk'        
               
        # without errors
        if is_errors==False:
            output_subdir = f'{output_directory_prefix}_generated_user_queries_from_vtk_python_scripts'
            
            user_input_dir = PROJECT_BASE_DIRECTORY +'/vtk_example_python_scripts_with_data'
        # with errors
        else:
            
            output_subdir = f'{output_directory_prefix}_generated_user_queries_from_vtk_expert_queries_with_errors'
            user_input_dir = PROJECT_BASE_DIRECTORY +'/user_queries/generated_user_queries/vtk/deepseek_r1_70b_generated_user_queries_from_vtk_python_scripts_human_reviewed'       
        data_file_base_name = ''
        data_file_full_path = ''

        user_queries_generation_from_vtk_related_python_scripts_for_VTK_datasets(user_input_dir, data_file_base_name, data_file_full_path, output_dir, output_subdir, model, URL)
    
    
     # this is under planning, not implemented yet
    elif dataset == 'USER_INTENT_GENERATION_FROM_CLIMATE_RELATED_QUERIES':
        output_dir = PROJECT_BASE_DIRECTORY+'/prompting_techniques/zero_shot_sci_data_prompting/python-script-output/fastMRI_brain'
        print('Inside USER_INTENT_GENERATION_FROM_CLIMATE_RELATED_QUERIES ...')
        user_input_dir = PROJECT_BASE_DIRECTORY+'/user_queries/manually_edited_user_queries/generated_user_queries_with_manually_modifying_for_resolving_errors'
        data_file_base_name = ''
        data_file_full_path = ''

        output_dir = PROJECT_BASE_DIRECTORY+'/prompting_techniques/zero_shot_sci_data_prompting/generated_user_intent'
        intent_generation_from_user_input_zero_shot_prompt(user_input_dir, data_file_base_name, data_file_full_path, output_dir, output_subdir, model, URL)

    # for the fast mmri brain image data we have to generate user intent from the user queries first, then it need to processed for final python code generation
    elif dataset == 'USER_INTENT_GENERATION_FROM_FAST_MRI_BRAIN_RELATED_QUERIES':
        output_dir = PROJECT_BASE_DIRECTORY+'/mri_nyu_data/generated_python_script_llm'
        user_input_dir = PROJECT_BASE_DIRECTORY+'/mri_nyu_data/user_queries_generated_human_modified_error_insertion_with_search_queries'
        data_file_base_name = ''
        data_file_full_path = ''

        output_dir = PROJECT_BASE_DIRECTORY+'/prompting_techniques/zero_shot_sci_data_prompting/generated_user_intent'
        intent_generation_from_user_input_zero_shot_prompt(user_input_dir, data_file_base_name, data_file_full_path, output_dir, output_subdir, model, URL)
    
    elif dataset == 'FAST_MRI_BRAIN_WITH_USER_INTENT':
        output_dir = PROJECT_BASE_DIRECTORY+'/mri_nyu_data/generated_python_script_llm_user_intent' 
        output_subdir = f'{output_directory_prefix}_zero_shot_CoT_with_corrector_fastMRI_brain_with_path_errors_with_corrector_search_queries'
        user_input_dir = PROJECT_BASE_DIRECTORY+'/mri_nyu_data/user_queries_generated_human_modified_error_insertion_with_search_queries'

        data_file_directory_full_path = f'{PROJECT_BASE_DIRECTORY}/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_dcm_to_h5'
        data_file_base_name = 'fastMRI_brain_200_dcm_to_h5.h5'

        tracking.initialize_json(PROJECT_BASE_DIRECTORY, JSON_FILE_PATH, output_subdir)
        
        zero_shot_COT_FAST_MRI_BRAIN_DCM_TO_H5_DATASETS_WITH_USER_INTENT(user_input_dir, PROJECT_BASE_DIRECTORY, data_file_base_name, data_file_directory_full_path+'/'+data_file_base_name, output_dir, output_subdir, model, JSON_FILE_PATH, with_corrector, URL)
    