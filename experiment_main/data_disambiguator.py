import os
import glob
import re
import requests
import json
import os
import sys


from common_util_script import DataSummarizer as dataSummarizer
from common_util_script import LLMRequester as llmRequester
from common_util_script import Utils as utils


# Define the list of keywords
priority_words = ['read data', 'dataset', 'paths', 'plot', 'graph', 'access', 'path', 'attribute', 'group', 'from source', 'draw', 'source', 'directory']


def get_data_paths_based_on_conditions(data_file_path, attribute_name='', condition='', condition_value=''):
    print(f'get_data_paths_based_on_conditions(data_file_path, attribute_name='', condition='', condition_value='')')
    dataset = dataSummarizer.list_all_dataset_and_attribute_name_based_on_conditions(data_file_path, attribute_name, condition, condition_value)
    dataset = f'Based on the user intent and condition the below path retrieve so use the below path and ignore the condition mentioned for the dataset: \n{dataset}'
    return dataset


def corrector_function_main(user_input_content, data_file_path, is_memory=False, attribute_name='', condition='', condition_value=''):
    # if condition present then get data paths based on that
    if len(attribute_name)>0 and len(condition)>0 and len(condition_value)>0:
        dataset_path_result = get_data_paths_based_on_conditions(data_file_path, attribute_name, condition, condition_value)
        print('dataset_path_result: ', dataset_path_result)
        return dataset_path_result, False, user_input_content

    """
    
    Path related Problems we are going to resolve:
    -----------------------------------------------------------------------------------------------------------------
    1. incorrect whole path such as any group or sub-group name is absent
        such as in the VNP46A1.A2020302.h07v07.001.2020303075447.h5 file
        available whole path is 'HDFEOS/GRIDS/VNP_Grid_DNB/Data Fields/BrightnessTemperature_M12'
        but give user input path is 'HDFEOS/SWATHS/BrightnessTemperature/M12/BrightnessTemperature_M12'
    2. mentioning group, sub-group, or dataset name separately and LLM struggle to form the full path
        such as read data from 'abc' dataset, 'bcd' group, and 'def' sub-group
    3. sometimes only root group and dataset names are mentioned not the sub groups name
    4. sometimes case is mismatched
    5. sometimes typo error in the paths (not handled yet)
    6. only datasets name mentioned but no group name or sub group name 
        (if the unique number of datasets is small then it will work, otherwise too much information for LLM)
    7. Dataset path names containing spaces (not tested if LLM fails to set the paths correctly or not)

    
    Latitude and Longitude providing related problems for the map projections:
    --------------------------------------------------------------------------------------------------------------------
    1. sometimes no latitude and longitude present in the datasets then LLM need to assume the paths but will face error
        solution: need to tell LLM that you need to create a demo latitude and longitude
    2. Sometimes either latitude and longitude is mentioned but no the both
        solution: we may need to check if the same group/sub-groups contains the latitude or longitude present
    3. No full path of latitude and longitude mentioned but need to construct by combining with the main dataset paths
        3.1: for multiple dataset it is a problem if both datasets contains the latitude and longitude
    4.      
    
    Problem with accessing attributes from the datasets:
    -----------------------------------------------------------------------------------------------------------------------
    1. can't access the attributes properly
        solution: need to provide example how to access attributes


    Problem with shape while mapping with the projection function:
    -----------------------------------------------------------------------------------------------------------------------
    1. sometimes it fails to do some calculation related to projection functions due to shape mismatch
        solution: may be need to give extra information related to shape but not handled yet (complex)    
        
    
    Algorithm of finding close matching datasets based on the input hdf5 file and user input prompt:
    ------------------------------------------------------------------------------------------------------------------------
    Step 1. At first replace all newlines by a singl espace
    Step 2. then remove all of the punctuations
    Step 3. create monograms and sort reversely based on words length
    Step 4. create bigrams from the cleaned user input
    Step 5. based on the monograms and bigrams create the following list:
        1. check the dataset exact path name match or starts with any of bigrams
        2. check the dataset exact name only match or ends with any of bigrams
        3. check the dataset exact path name match with any of monograms
        4. check the dataset exact name only match with any of monograms
    
    """

    # get list of all datasets and attributes
    all_dataset_attribute_list = dataSummarizer.list_all_dataset_and_attribute_name(data_file_path)

    # take all of the dataset and attributes information to save into memory
    all_dataset_paths_attributes = ''
    if is_memory:
        all_dataset_paths_attributes = dataSummarizer.collect_all_paths_to_store_memory(data_file_path)

    print(f'\n\nall_dataset_attribute_list size: {len(all_dataset_attribute_list)}\n')
    if len(all_dataset_attribute_list)<100:
        print(all_dataset_attribute_list)

    updated_text = utils.tokenize_and_replace(user_input_content, all_dataset_attribute_list)
    print("Updated Text without Levenshtein:", updated_text)

    
    updated_text = utils.tokenize_and_replace_with_Levenshtein(user_input_content, all_dataset_attribute_list)
    print("Updated Text with Levenshtein:", updated_text)
    
    # replace the incorrect datastes and attributes by correct datasets and attributes
    # corrected_user_input = utils.replace_user_input_attributes_with_origial_attributes(sequential_tokens, all_dataset_attribute_list)
    # print("\n\n Corrected user input: \n", corrected_user_input) 
    user_input_content = updated_text
    # end



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

    monogram_dataset_attribute_list = utils.tokenize_with_space_and_sort_reversed(clened_user_input_content)
    
    print("\nTokenization output without LLM: \n", monogram_dataset_attribute_list)

    # newly added bigram creation
    # date: 02 Nov 2024
    bigram_dataset_attribute_list = utils.generate_2grams(clened_user_input_content)
    print("\nTokenization bigram output without LLM: \n", bigram_dataset_attribute_list)

    
    # make the tokens more smaller such as paths into single words
    single_word_tokenization_from_user_input_paths = utils.extend_list_by_making_paths_into_single_words(monogram_dataset_attribute_list)


    # current test
    dataset_group_response = dataSummarizer.match_exact_dataset_full_partial_match_upto_bigram(data_file_path, monogram_dataset_attribute_list, bigram_dataset_attribute_list, single_word_tokenization_from_user_input_paths)
    exact_datasets_matched_by_whole_path = dataset_group_response[0]
    exact_datasets_matched_by_name_only = dataset_group_response[1] 
    exact_immediate_group_subgroup_match_by_name_only = dataset_group_response[2] 
    exact_matched_group_subgroups = dataset_group_response[3] 
    exact_matched_group_subgroups_by_name = dataset_group_response[4]
    all_paths = dataset_group_response[5]
    root_groups = dataset_group_response[6]
    
    
    
    rapid_fuzz_best_matched_output, all_matched_paths, best_matched_by_extract, all_matched_paths_by_extract  = utils.find_common_strings(single_word_tokenization_from_user_input_paths, all_paths)
    print(f"\n\nRapidFuzz best_matched paths: {len(rapid_fuzz_best_matched_output)}:\n", rapid_fuzz_best_matched_output)

    result=""
   

    single_word_group_dataset_attribute_list = utils.split_and_extend_paths(single_word_tokenization_from_user_input_paths)
    print(f"\n\n single_word_group_dataset_attribute_list, size: {len(single_word_group_dataset_attribute_list)}: \n", single_word_group_dataset_attribute_list)

    # version 3
    real_groups, real_datasets, real_attributes = dataSummarizer.extract_real_datasets_and_attributes(data_file_path, single_word_group_dataset_attribute_list)
    print(f"\n\n real_groups, size: {len(real_groups)}: \n", real_groups)
    real_groups = utils.remove_redundant_paths(real_groups)
    print(f"\n\n real_groups after removing redundant, size: {len(real_groups)}: \n", real_groups)
    
    print(f"\n\n real_datasets, size: {len(real_datasets)}: \n", real_datasets)
    print(f"\n\n real_attributes, size: {len(real_attributes)}: \n", real_attributes)
    

    final_dataset_list = utils.decision_maker_about_the_final_list_of_datasets(exact_datasets_matched_by_whole_path, exact_datasets_matched_by_name_only, 
                                                                                exact_matched_group_subgroups, exact_matched_group_subgroups_by_name, rapid_fuzz_best_matched_output)
    print(f"\n\n final_dataset_list, size: {len(final_dataset_list)}: \n", final_dataset_list)
    
     
    # created Nov 02 2024
    # data_file_path, 
    result, attribute_present = dataSummarizer.format_datasets_from_final_dataset_list(data_file_path=data_file_path, final_dataset_list=final_dataset_list)
    if result is not None:
        print("\n\n Final Result: \n", result)
    else:
        print(f'result is None')
    if attribute_present is not None:
        print('\nAttribute present: ', attribute_present)
    else:
        print(f'Attribute is None')

    if is_memory:
        result = all_dataset_paths_attributes

    return result, attribute_present, updated_text


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
                
                        # step 2: ask LLM to generate required dataset and groups and receive the datasets name
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

                        # dataset_attribute_list = utils.tokenize_with_priority(clened_user_input_content, priority_words)
                        dataset_attribute_list = utils.tokenize_with_space_and_sort_reversed(clened_user_input_content)
                        
                        print("\nTokenization output without LLM: \n", dataset_attribute_list) 

                        # print(f"\n\nAll matched paths: {len(matchingDatasets)}:\n", matchingDatasets)
                        exact_matched_datasets, exact_matched_datasets_by_name, exact_matched_group_subgroups, exact_matched_group_subgroups_by_name = dataSummarizer.match_exact_dataset_full_partial_match(data_file_path, dataset_attribute_list)
                            
                        all_paths = dataSummarizer.get_all_paths_from_data_file(data_file_path)
                        dataset_attribute_list = utils.extend_list_by_making_paths_into_single_words(dataset_attribute_list)
                        # print("\nTokenization output after making single words: \n", dataset_attribute_list) 
                        rapid_fuzz_best_matched_output, all_matched_paths, best_matched_by_extract, all_matched_paths_by_extract  = utils.find_common_strings(dataset_attribute_list, all_paths)
                        print(f"\n\nRapidFuzz best_matched paths: {len(rapid_fuzz_best_matched_output)}:\n", rapid_fuzz_best_matched_output)
                        # print(f"\n\nRapidFuzz All matched paths: {len(all_matched_paths)}:\n", all_matched_paths)
                        

                        comma_separated_data_list=""
                        # if len(group_dataset_attribute_list)>0:
                        result=""
                        if len(dataset_attribute_list)>0:
                            
                            # input raw dataset attribute list by llm, output: if any exact dataset path given and correct
                            exact_dataset_path = dataSummarizer.extract_exact_datasets_from_input_generated_by_llm(data_file_path, dataset_attribute_list)
                            # print(f"\n\n exact_dataset_path, size: {len(exact_dataset_path)}: \n", exact_dataset_path)

            
                            single_word_group_dataset_attribute_list = utils.split_and_extend_paths(dataset_attribute_list)
                            print(f"\n\n single_word_group_dataset_attribute_list, size: {len(single_word_group_dataset_attribute_list)}: \n", single_word_group_dataset_attribute_list)

            
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
                            # let's make a score based paths where we will select top five scored path based on real datasets and tokens from user input
                            else:
                                filtered_real_datasets = utils.make_dictionary_of_score(dataset_attribute_list, real_datasets)
                                # print(f"\n\n filtered_real_datasets from scores, size: {len(filtered_real_datasets)}: \n", filtered_real_datasets)

                            # this is the current testing final user prompt making
                            # def decision_maker_about_the_final_list_of_datasets(exact_matched_datasets, exact_matched_datasets_by_name, exact_matched_group_subgroups, exact_matched_group_subgroups_by_name, rapid_fuzz_best_matched_output):
                            final_dataset_list = utils.decision_maker_about_the_final_list_of_datasets(exact_matched_datasets, exact_matched_datasets_by_name, exact_matched_group_subgroups, exact_matched_group_subgroups_by_name, rapid_fuzz_best_matched_output)
                            print(f"\n\n final_dataset_list, size: {len(final_dataset_list)}: \n", final_dataset_list)
                            
                            longitude_latitude_list, final_dataset_list_without_lat_lon = dataSummarizer.find_latitude_longditude_information_for_given_dataset_list(data_file_path, final_dataset_list)
                            print(f"\n\n longitude_latitude_list, size: {len(longitude_latitude_list)}: \n", longitude_latitude_list)
                            
                            
                            # result = dataSummarizer.format_datasets_from_final_set_add_example_prompt_if_latitude_longtitude_not_present(data_file_path, final_dataset_list)
                            result = dataSummarizer.format_datasets_from_final_set_and_latitude_longitude_list(data_file_path, final_dataset_list_without_lat_lon, longitude_latitude_list)
                            # dataSummarizer.find_latitudes_and_longditudes_based_on_final_dataset(data_file_path, final_dataset_list)
                            print("\n\n Final Result: \n", result)

                        # step 5: call the llm again the generate the python code
                        old_ext = ".txt"
                    
                    
                        llmRequester.generate_code_and_save_with_data_rule_based_reasoning(user_input_file_path, user_input_content, result, data_file_path, output_dir, model, old_ext)

if __name__ == '__main__':
   
    common_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'
    data_dir = 'ACL_DIRS'  # Replace with your common directory path
    subdirectories = ['ASF', 'GES_DISC', 'GHRC', 'ICESat_2', 'LAADS', 'LaRC', 'LP_DAAC', 'NSIDC', 'Ocen_Biology', 'PO_DAAC', 'AURA_DATA_VC']  # Replace with your predefined subdirectory names
    extensions = ['hdf5', 'he5', 'h5', 'HDF5', 'H5', 'HE5']
    
    output_dir = common_directory+'/sci_data_prompting/python-script-output'
    
    output_subdir = 'llama3_70b_latest_alogo'

    model = ['llama3:latest', 'deepseek-coder-v2', 'codellama', 'codellama:7b-python', 'llama3:70b']
    user_input_dir = common_directory+'/generated_user_input_human_like_text_directly_remove_library_names'
    receive_data_path_user_input_generate_data_des_insert_full_datasets_path_generate_prompt(user_input_dir, common_directory+"/"+data_dir, subdirectories, extensions, output_dir+'/'+output_subdir, model[4])
