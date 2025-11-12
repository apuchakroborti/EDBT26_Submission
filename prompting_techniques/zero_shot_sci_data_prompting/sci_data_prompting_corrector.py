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
# from . import tracking as tracking
# from common_util_script.DataSummarizer import DataSummarizer as dataSummarizer
# from common_util_script.LLMRequester import LLMRequester as llmRequester
# from common_util_script.Utils import Utils as utils

# from common_util_script import DataSummarizer
# from common_util_script import LLMRequester
# from common_util_script import Utils


# sys.path.append(os.path.abspath('../common-util-script'))
# import DataSummarizer as dataSummarizer
# import LLMRequester as llmRequester
# import Utils as utils


# Define the list of keywords
priority_words = ['read data', 'dataset', 'paths', 'plot', 'graph', 'access', 'path', 'attribute', 'group', 'from source', 'draw', 'source', 'directory']


def get_data_paths_based_on_conditions(data_file_path, attribute_name='', condition='', condition_value=''):
    print(f'get_data_paths_based_on_conditions(data_file_path, attribute_name='', condition='', condition_value='')')
    dataset = dataSummarizer.list_all_dataset_and_attribute_name_based_on_conditions(data_file_path, attribute_name, condition, condition_value)
    dataset = 'Based on the user intent and condition the below path retrieve so use the below path and ignore the condition mentioned for the dataset: \n'+dataset
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

    # these steps for replacing single or double words from the user input direct to replace incorrect dataset and attributes 
    # start
    
    # test manual tokenization
    # Process tokens and updated text
    # single_tokens, double_tokens, updated_text = utils.tokenize_and_process(user_input_content)
    # single_tokens, double_tokens= utils.tokenize_and_process(user_input_content)
    # print("Single Tokens:", single_tokens)
    # print("Double Tokens:", double_tokens)
    # print("Updated Text:", updated_text)


    #convert user input into space and punctuations separated sequential tokens 
    # sequential_tokens = utils.split_text_based_on_space_and_punctuations(user_input_content)
    # print(f'\n\nsequential_tokens size and tokens: {len(sequential_tokens)}\n', sequential_tokens)
    
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

    # Last use 02 Nov 2024
    # exact_matched_datasets, exact_matched_datasets_by_name, exact_matched_group_subgroups, exact_matched_group_subgroups_by_name = dataSummarizer.match_exact_dataset_full_partial_match(data_file_path, monogram_dataset_attribute_list, bigram_dataset_attribute_list)
    
    # make the tokens more smaller such as paths into single words
    single_word_tokenization_from_user_input_paths = utils.extend_list_by_making_paths_into_single_words(monogram_dataset_attribute_list)


    # current test
    # first use 02 Nov 2024
    # exact_datasets_matched_by_whole_path, exact_datasets_matched_by_name_only, exact_immediate_group_subgroup_match_by_name_only, exact_matched_group_subgroups, exact_matched_group_subgroups_by_name 
    dataset_group_response = dataSummarizer.match_exact_dataset_full_partial_match_upto_bigram(data_file_path, monogram_dataset_attribute_list, bigram_dataset_attribute_list, single_word_tokenization_from_user_input_paths)
    exact_datasets_matched_by_whole_path = dataset_group_response[0]
    exact_datasets_matched_by_name_only = dataset_group_response[1] 
    exact_immediate_group_subgroup_match_by_name_only = dataset_group_response[2] 
    exact_matched_group_subgroups = dataset_group_response[3] 
    exact_matched_group_subgroups_by_name = dataset_group_response[4]
    all_paths = dataset_group_response[5]
    root_groups = dataset_group_response[6]
    
    
    # test string rapidFuzz fuzzy matching library
    # get the user in put tokens
    # get all the paths
    # all_paths = dataSummarizer.get_all_paths_from_data_file(data_file_path)
    
    rapid_fuzz_best_matched_output, all_matched_paths, best_matched_by_extract, all_matched_paths_by_extract  = utils.find_common_strings(single_word_tokenization_from_user_input_paths, all_paths)
    print(f"\n\nRapidFuzz best_matched paths: {len(rapid_fuzz_best_matched_output)}:\n", rapid_fuzz_best_matched_output)

    result=""
    # if len(dataset_attribute_list)>0:
        
    # input raw dataset attribute list by llm, output: if any exact dataset path given and correct
    # exact_dataset_path = dataSummarizer.extract_exact_datasets_from_input_generated_by_llm(data_file_path, single_word_tokenization_from_user_input_paths)
    # print(f"\n\n exact_dataset_path, size: {len(exact_dataset_path)}: \n", exact_dataset_path)


    single_word_group_dataset_attribute_list = utils.split_and_extend_paths(single_word_tokenization_from_user_input_paths)
    print(f"\n\n single_word_group_dataset_attribute_list, size: {len(single_word_group_dataset_attribute_list)}: \n", single_word_group_dataset_attribute_list)

    # version 3
    real_groups, real_datasets, real_attributes = dataSummarizer.extract_real_datasets_and_attributes(data_file_path, single_word_group_dataset_attribute_list)
    print(f"\n\n real_groups, size: {len(real_groups)}: \n", real_groups)
    real_groups = utils.remove_redundant_paths(real_groups)
    print(f"\n\n real_groups after removing redundant, size: {len(real_groups)}: \n", real_groups)
    
    print(f"\n\n real_datasets, size: {len(real_datasets)}: \n", real_datasets)
    print(f"\n\n real_attributes, size: {len(real_attributes)}: \n", real_attributes)
    
    """
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
    """
    

    # this is the current testing final user prompt making
    # def decision_maker_about_the_final_list_of_datasets(exact_matched_datasets, exact_matched_datasets_by_name, exact_matched_group_subgroups, exact_matched_group_subgroups_by_name, rapid_fuzz_best_matched_output):
    final_dataset_list = utils.decision_maker_about_the_final_list_of_datasets(exact_datasets_matched_by_whole_path, exact_datasets_matched_by_name_only, 
                                                                                exact_matched_group_subgroups, exact_matched_group_subgroups_by_name, rapid_fuzz_best_matched_output)
    print(f"\n\n final_dataset_list, size: {len(final_dataset_list)}: \n", final_dataset_list)
    

    # this should be move to the next module to resolve latitude and longitude path and configuraion related problems
    # longitude_latitude_list, final_dataset_list_without_lat_lon = dataSummarizer.find_latitude_longditude_information_for_given_dataset_list(data_file_path, final_dataset_list)
    # print(f"\n\n longitude_latitude_list, size: {len(longitude_latitude_list)}: \n", longitude_latitude_list)
    
    
    # result = dataSummarizer.format_datasets_from_final_set_add_example_prompt_if_latitude_longtitude_not_present(data_file_path, final_dataset_list)
    # result = dataSummarizer.format_datasets_from_final_set_and_latitude_longitude_list(data_file_path, final_dataset_list_without_lat_lon, longitude_latitude_list)
    
    # current developing function
    # result = dataSummarizer.format_datasets_from_final_set_and_latitude_longitude_list_without_latitude_longitude(data_file_path, final_dataset_list_without_lat_lon, longitude_latitude_list)

    # new testing function
    # last used Nov 02
    # result, attribute_present = dataSummarizer.format_datasets_from_final_dataset_list(data_file_path, final_dataset_list_without_lat_lon)
    # dataSummarizer.find_latitudes_and_longditudes_based_on_final_dataset(data_file_path, final_dataset_list)
    
    # created Nov 02 2024
    result, attribute_present = dataSummarizer.format_datasets_from_final_dataset_list(data_file_path, final_dataset_list)
    print('\nAttribute present: ', attribute_present)
    print("\n\n Final Result: \n", result)

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
                        
                        # return content, user_input_file_path

                        # replace the file name by whole path
                        user_input_content = utils.replace_string(user_input_content, data_basename_with_extension, data_file_path )
                
                # step 2: ask LLM to generate required dataset and groups and receive the datasets name
                # call LLMRequestor
                
                #version 2: this is for getting group, dataset, and attributes names from user input
                # group_dataset_attribute_list = llmRequester.get_group_dataset_and_attribute_name(user_input_content, model)
                
                # version 1
                # group_dataset_attribute_json_list = utils.get_list_from_json(group_dataset_attribute_list)
                
                #version 3: current testing: this is for getting only dataset and attributes name list from user input 
                # getting path and datasets list not working properly, LLM failes to extract those list
                # dataset_attribute_list=llmRequester.get_dataset_and_attribute_name(user_input_content, model)

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

                # dataset_attribute_list = utils.tokenize_with_priority(clened_user_input_content, priority_words)
                dataset_attribute_list = utils.tokenize_with_space_and_sort_reversed(clened_user_input_content, priority_words)
                
                print("\nTokenization output without LLM: \n", dataset_attribute_list) 

                # check paths of exact or partial match
                # matchingDatasets = dataSummarizer.match_exact_dataset_full_partial_match(data_file_path, dataset_attribute_list)
                # print(f"\n\nAll matched paths: {len(matchingDatasets)}:\n", matchingDatasets)
                exact_matched_datasets, exact_matched_datasets_by_name, exact_matched_group_subgroups, exact_matched_group_subgroups_by_name = dataSummarizer.match_exact_dataset_full_partial_match(data_file_path, dataset_attribute_list)
                
                """ 
                Does not work well
                # test sequence matcher calling
                # get the user in put tokens
                # get all the paths
                all_paths = dataSummarizer.get_all_paths_from_data_file(data_file_path)
                dataset_attribute_list = utils.extend_list_by_making_paths_into_single_words(dataset_attribute_list)
                print("\nTokenization output after making single words: \n", dataset_attribute_list) 
                all_matched_paths  = utils.get_all_closed_paths_sn_matcher(dataset_attribute_list, all_paths)
                print(f"\n\nAll matched paths: {len(all_matched_paths)}:\n", all_matched_paths)
                """
                
               
                # test string rapidFuzz fuzzy matching library
                # get the user in put tokens
                # get all the paths
                all_paths = dataSummarizer.get_all_paths_from_data_file(data_file_path)
                dataset_attribute_list = utils.extend_list_by_making_paths_into_single_words(dataset_attribute_list)
                # print("\nTokenization output after making single words: \n", dataset_attribute_list) 
                rapid_fuzz_best_matched_output, all_matched_paths, best_matched_by_extract, all_matched_paths_by_extract  = utils.find_common_strings(dataset_attribute_list, all_paths)
                print(f"\n\nRapidFuzz best_matched paths: {len(rapid_fuzz_best_matched_output)}:\n", rapid_fuzz_best_matched_output)
                # print(f"\n\nRapidFuzz All matched paths: {len(all_matched_paths)}:\n", all_matched_paths)
                # print(f"\n\nRapidFuzz best_matched_by_extract paths: {len(best_matched_by_extract)}:\n", best_matched_by_extract)
                # print(f"\n\nRapidFuzz All matched all_matched_paths_by_extract paths: {len(all_matched_paths_by_extract)}:\n", all_matched_paths_by_extract)




                
                # group_dataset_attribute_list=[]
                
                # if group_dataset_attribute_json_list:
                    # print(dataset_json_list['datasets'])
                    # group_dataset_attribute_list = group_dataset_attribute_json_list['datasets']
                comma_separated_data_list=""
                # if len(group_dataset_attribute_list)>0:
                result=""
                if len(dataset_attribute_list)>0:
                    
                    # input raw dataset attribute list by llm, output: if any exact dataset path given and correct
                    exact_dataset_path = dataSummarizer.extract_exact_datasets_from_input_generated_by_llm(data_file_path, dataset_attribute_list)
                    # print(f"\n\n exact_dataset_path, size: {len(exact_dataset_path)}: \n", exact_dataset_path)

                    
                    
                    # block to classify input token into different categories like; groups, subgroups, datasets, and attributes
                    # convert the paths into single word to further classification as groups, subgroups, datasets, and attributes
                    # single_word_group_dataset_attribute_list = utils.split_and_extend_paths(group_dataset_attribute_list)
                    # print(f"\n\n single_word_group_dataset_attribute_list, size: {len(single_word_group_dataset_attribute_list)}: \n", single_word_group_dataset_attribute_list)

                    single_word_group_dataset_attribute_list = utils.split_and_extend_paths(dataset_attribute_list)
                    print(f"\n\n single_word_group_dataset_attribute_list, size: {len(single_word_group_dataset_attribute_list)}: \n", single_word_group_dataset_attribute_list)

                    # Now get the 4 list of outputs
                    # version 1
                    # real_groups, real_attributes = dataSummarizer.extract_real_groups_and_attributes(data_file_path, single_word_group_dataset_attribute_list)
                    # print(f"\n\n real_groups, size: {len(real_groups)}: \n", real_groups)
                    # print(f"\n\n real_attributes, size: {len(real_attributes)}: \n", real_attributes)
                    
                    # verion 2
                    # real_groups, real_attributes = dataSummarizer.extract_real_groups_and_attributes(data_file_path, dataset_attribute_list)
                    # print(f"\n\n real_groups, size: {len(real_groups)}: \n", real_groups)
                    # print(f"\n\n real_attributes, size: {len(real_attributes)}: \n", real_attributes)

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
                    

                    # this passes both group and datasets
                    # matching_dataset_list = dataSummarizer.match_rightmost_paths(data_file_path, group_dataset_attribute_list)
                    
                    # this is only passing dataset
                    # version 1
                    # matching_dataset_list =  dataSummarizer.match_rightmost_paths_only_dataset_match(data_file_path, group_dataset_attribute_list)

                    # version 2
                    # matching_dataset_list =  dataSummarizer.match_rightmost_paths_only_dataset_match(data_file_path, dataset_attribute_list)

                    # version 3: here matching only dataset name: return dataset list
                    
                    # this is the current algorithm for making final input result
                    """
                    matching_dataset_list, matching_dataset_path_attributes_dic =  dataSummarizer.match_dataset_and_get_full_path_with_attribute(data_file_path, real_datasets, real_attributes)


                    print(f"\n\n Matching dataset_list, size: {len(matching_dataset_list)}: \n", matching_dataset_list)

                    # if exact dataset path given by user then the matching dataset should be filtered by that
                    if len(exact_dataset_path)>0:
                        matching_dataset_path_attributes_dic_new = {}
                        for exat in exact_dataset_path:
                            for key, value in matching_dataset_path_attributes_dic.items():
                                if exat in key:
                                    matching_dataset_path_attributes_dic_new[key]=value
                        
                        # update the previous dictionary
                        matching_dataset_path_attributes_dic=matching_dataset_path_attributes_dic_new
                    
                    print("\n Final dataset and attribute list:")
                    # result = dataSummarizer.format_datasets_and_attributes(matching_dataset_path_attributes_dic)
                    result = dataSummarizer.format_datasets_and_attributes_and_add_example_prompt_if_latitude_longtitude_not_present(matching_dataset_path_attributes_dic)
                    """

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
                    

                    """ 
                    if len(matching_dataset_list) <1:
                        print("\nNo correct dataset name provided\n")
                        continue
                    """
                    
                    """ # input_group = set()
                    input_attribute = set()
                    for path in matching_dataset_list:
                        for check_attribute in real_attributes:
                            if path.endswith(check_attribute):
                                input_attribute.add(path)
                    
                    
                    # print(f"\n\n input_group, size: {len(input_group)}: \n", input_group)    
                    print(f"\n\n input_attribute, size: {len(input_attribute)}: \n", input_attribute)    
                    result = []"""
                    
                    """ if len(input_group)>0 and len(input_attribute)>0:
                        result = list(input_group.intersection(input_attribute))
                    elif len(input_group)>0:
                        result = list(input_group)
                    else:
                        result = list(input_attribute)"""
                    
                    # result = list(input_group.union(input_attribute))
                    # version 1
                    """
                    input_attribute = list(input_attribute)
                    for check_group in real_groups:
                        for attribute in input_attribute:
                            if attribute.startswith(check_group):
                                # input_group.add(path)
                                result.append(attribute)

                    print(f"\n\n result, size: {len(result)}: \n", result)
                    """ 
                    
                    """# version 2
                    input_attribute = list(input_attribute)
                    for check_dataset in real_datasets:
                        for attribute in input_attribute:
                            if attribute.startswith(check_dataset):
                                # input_group.add(path)
                                result.append(attribute)

                    print(f"\n\n result, size: {len(result)}: \n", result)   """
                    # print(result)
                    #

                    # there are too many all possible matching: now going to take those which has at least one matching
                    """matching_only_set = set()
                    for attribute in single_word_group_dataset_attribute_list:
                        for path in matching_dataset_list:
                            if attribute in path:
                                matching_only_set.add(path)
                    
                    matching_only = []
                    if len(matching_only_set)>0:
                        matching_only = list(matching_only_set)
                    print(f"\n\n Matching only paths, size: {len(matching_only)} \n", matching_only)"""




                    # unique_matching_dataset_list = utils.remove_redundant_paths(matching_dataset_list)
                    
                    # taking only matching paths
                    # unique_matching_dataset_list = utils.remove_redundant_paths(matching_only)
                    # print(f"\n\nunique_matching_dataset_list, size: {len(unique_matching_dataset_list)}:\n", unique_matching_dataset_list)  

                    # unique_matching_dataset_with_separate_attribute_list = utils.extract_paths_with_attributes(unique_matching_dataset_list)
                    # print(f"\n\nunique_matching_dataset_with_separate_attribute_list, size: {len(unique_matching_dataset_with_separate_attribute_list)}: \n", unique_matching_dataset_with_separate_attribute_list)  
                    
                    # comma_separated_data_list = utils.make_list_comma_separated_item(matching_dataset_list)
                    # comma_separated_data_list = utils.make_list_comma_separated_item(unique_matching_dataset_list)
                    # comma_separated_data_list = utils.make_list_comma_separated_item(unique_matching_dataset_with_separate_attribute_list)
                    
                    # unique_matching_dataset_list = utils.remove_redundant_paths(result)
                    # print(f"\n\nunique_matching_dataset_list, size: {len(unique_matching_dataset_list)}:\n", unique_matching_dataset_list)  


                    # comma_separated_data_list = utils.make_list_comma_separated_item(result)
                    # comma_separated_data_list = utils.make_list_comma_separated_item(unique_matching_dataset_list)
                    # print("\n\ncomma_separated_data_list:\n", comma_separated_data_list)

                    # check if the paths are correct
                    # result = dataSummarizer.verify_and_correct_paths_v2(data_file_path, dataset_list)
                      
                        # Print the verification result
                    # for path, status in result.items():
                        # print(f"Path: {path} - Status: {status}")


                # print(extract_datasets(extract_datasets_from_string(datasets_from_user_response['response'])))
                # print(extract_datasets_from_string(datasets_from_user_response['response']))
                # print(extract_xml_from_llm_response(datasets_from_user_response['response']))
        
                # step 3: read data and get the group and dataset list
                # step 4: find the full path of the data set paths and make a description string based on the datasets 
                # data_summary = dataSummarizer.summarize_hdf5(data_file_path)
                # print(data_summary)

                # print all attributes paths for checking
                # attribute_paths = dataSummarizer.list_all_attribute_paths(data_file_path)
                # print(f"\n\nattribute_paths, size: {len(attribute_paths)}: \n", attribute_paths)
                
                
                # datasets_with_attributes = dataSummarizer.collect_datasets_with_attributes(data_file_path)
                # dataSummarizer.print_datasets_with_attributes(datasets_with_attributes)

                # Example usage
                # file_path = 'your_file.h5'  # Replace with your HDF5, H5, HE5 file path
                # dataset_filter_list = ['/Sigma0_Data/cell_sigma0_hh_fore', '/another/dataset']  # Datasets you want to filter

                # Get the filtered datasets in JSON format
                # filtered_datasets_json = dataSummarizer.extract_filtered_datasets_and_attributes(data_file_path, dataset_list)

                # Print the JSON output
                # print("Json: ")
                # print(filtered_datasets_json)
                # Example usage
                # file_path = 'your_file.h5'  # Replace with your HDF5, H5, HE5 file path

                # List of dataset names to filter (case-insensitive)
                # dataset_names_to_filter = ['dataset1', 'dataset2']  # Add your dataset names here

                # Get the list of all filtered attribute paths
                """
                dataset_names_to_filter = utils.split_and_combine(dataset_list)
                if dataset_names_to_filter:
                    filtered_attribute_path_list = dataSummarizer.list_filtered_attribute_paths(data_file_path, dataset_names_to_filter)
                if filtered_attribute_path_list:
                    # Print each path
                    clean_path_list = []
                    for path in filtered_attribute_path_list:
                        clean_path = path.strip('/')
                        clean_path_list.append(clean_path)
                        # print(clean_path)
                   
                    commasepated_path_structure_list = utils.make_list_comma_separated_item(clean_path_list) 
                """
                # Optionally, convert the path list to JSON format
                # attribute_path_list_json = json.dumps(filtered_attribute_path_list, indent=4)
                # print(attribute_path_list_json)
                
                # step 5: call the llm again the generate the python code
                old_ext = ".txt"
                # llmRequester.generate_code_and_save_with_data_information(user_input_file_path, comma_separated_data_list, data_file_path, output_dir, old_ext)
                # llmRequester.generate_code_and_save_with_data_structure_information(user_input_file_path, comma_separated_data_list, commasepated_path_structure_list, data_file_path, output_dir, old_ext)
                # llmRequester.generate_code_and_save_with_data_structure_information_with_repair(user_input_file_path, comma_separated_data_list, commasepated_path_structure_list, data_file_path, output_dir, old_ext)
                
                # user_input_file_path, dataset_information, data_structure_information, full_data_path, target_dir, model, old_ext='.txt'
                
                # current best performer around 25%
                # testing turning off this only for checking 
                # llmRequester.generate_code_and_save_with_data_structure_information_with_repair(user_input_file_path, user_input_content, comma_separated_data_list, comma_separated_data_list, data_file_path, output_dir, model, old_ext)


                # just for testing not calling for generating code:
                # continue
                # example test rule base reasoning
                # llmRequester.generate_code_and_save_with_data_rule_based_reasoning(user_input_file_path, user_input_content, comma_separated_data_list, comma_separated_data_list, data_file_path, output_dir, model, old_ext)
                llmRequester.generate_code_and_save_with_data_rule_based_reasoning(user_input_file_path, user_input_content, result, data_file_path, output_dir, model, old_ext)
                
                
                # step 6: get the substructure of the data based on the path example
                # then call LLM
                
                # summary = summarize_hdf5(file_path)
                # description = describe_summary(summary)
                # save_description_with_out_dir(file_path, description, output_dir)



if __name__ == '__main__':
    # source_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/chain_of_repair_input_llama3_latest'
    # target_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/output_chain_of_repair'

    # generate_code_and_save(source_directory, target_directory, old_ext='.txt')

    # initialize the tracking csv file
    # tracking.initialize_csv()

    common_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'
    data_dir = 'ACL_DIRS'  # Replace with your common directory path
    subdirectories = ['ASF', 'GES_DISC', 'GHRC', 'ICESat_2', 'LAADS', 'LaRC', 'LP_DAAC', 'NSIDC', 'Ocen_Biology', 'PO_DAAC', 'AURA_DATA_VC']  # Replace with your predefined subdirectory names
    extensions = ['hdf5', 'he5', 'h5', 'HDF5', 'H5', 'HE5']
    # output_subdir = '/zero_shot_output/summaries'  # The name of the directory to save output files
    # output_subdir = 'chain_of_repair_with_data_structure_output_llama3_latest'  # The name of the directory to save output files

    output_dir = common_directory+'/sci_data_prompting/python-script-output'
    # output_subdir = 'deepseek_coder_v2_with_data_separate_attribute'  # The name of the directory to save output files
    # output_subdir = 'deepseek_coder_v2_with_data_rbs_example_latitude_longtidue_code'  # The name of the directory to save output files
    # output_subdir = 'deepseek_coder_v2_with_data_rbs_with_restrictions'  # The name of the directory to save output files

    # current deepseek-coder-v2 implementation
    # output_subdir = 'deepseek_coder_v2_with_data_rbs_path_import_restrictions'  # The name of the directory to save output files

    # llama3:latest output
    # output_subdir = 'llama3_latest_with_data_rbs_path_import_restrictions'  # The name of the directory to save output files
    # output_subdir = 'codellama_7b_python_with_data_rbs_path_import_restrictions'  # The name of the directory to save output files
    # output_subdir = 'deepseek_coder_v2_spearate_dataset_latitude_and_longitude'  # The name of the directory to save output files
    # output_subdir = 'generated_user_input_human_like_text_directly_remove_library_names_added_paths'
    output_subdir = 'llama3_70b_latest_alogo'



    # codellama does not produce runable codes
    # codellama:7b-python does not generate any code after wait a while
    model = ['llama3:latest', 'deepseek-coder-v2', 'codellama', 'codellama:7b-python', 'llama3:70b']
    # model suggested by Lipeng Wan
    # gpt4, magicoder and deepseek-coder-v2, and may be llama3:70b

    # this part is for reading data and make summaries along with the example data
    # remove the example data part
    # find_and_process_files(common_directory, subdirectories, extensions)
    # user_input_dir = common_directory+"/original_python_script_description_with_20_p_reduc"

    # these are the previously generated user input string
    # user_input_dir = common_directory+"/generated_user_input_local_llama3"

    # newly generated human like text without python codes
    # user_input_dir = common_directory+'/generated_user_input_human_like_text'
    # user_input_dir = common_directory+'/generated_user_input_human_like_text_edited'
    user_input_dir = common_directory+'/generated_user_input_human_like_text_directly_remove_library_names'
    receive_data_path_user_input_generate_data_des_insert_full_datasets_path_generate_prompt(user_input_dir, common_directory+"/"+data_dir, subdirectories, extensions, output_dir+'/'+output_subdir, model[4])
