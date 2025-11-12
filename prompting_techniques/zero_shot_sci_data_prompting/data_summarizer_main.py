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


def receive_data_path_print_data_summary(common_directory, data_subdirectories, extensions, output_directory):
    try:
        for data_subdir in data_subdirectories:
            data_search_path = os.path.join(common_directory, data_subdir, '*')
            
            print('Data search path: ', data_search_path)
            
            for ext in extensions:
                data_files = glob.glob(f"{data_search_path}.{ext}")
                print('data_files: ', data_files)

                for data_file_path in data_files:
                    print(f"\n\nProcessing file: {data_file_path}")
                    file_base_name = os.path.basename(data_file_path)
                    # structure: datasets_attributes = {'attributes': {}, 'description': {'shape': obj.shape, 'dtype': str(obj.dtype),}}
                    # datasets_attributes = dataSummarizer.summarize_hdf5_print_dataset_paths_attribute(data_file_path)
                    
                    # for MRI dataset
                    datasets_attributes = dataSummarizer.summarize_hdf5_print_dataset_paths_attribute_and_attribute_from_groups(data_file_path)

                    # for climate datasets
                    # datasets_attributes = dataSummarizer.summarize_hdf5_print_dataset_metadata_information(data_file_path)
                

                    data_summaries = ''
                    # for key in datasets_attributes['attributes']:
                    for key in datasets_attributes:
                        if key == 'description':
                            data_summaries+='\n\n'

                            print('Inside description key, datasets_attributes[key]: ', datasets_attributes[key])
                            
                            for dataset_key in datasets_attributes[key]:
                                # print(f'Dataset: ', key, f' Description:\n Shape: {datasets_attributes['description'][key]['shape']} ---dtype: {datasets_attributes['description'][key]['dtype']}')
                                # print('dataset_key: ', dataset_key)
                                dataset = f'\nDataset: {dataset_key}'
                                # print('dataset: '+dataset)
                                data_summaries+=dataset+'\n'
                            
                                # description  = f'Description: \n'+{datasets_attributes['description'][key]}
                                dataset_description = datasets_attributes[key][dataset_key]
                                shape = datasets_attributes[key][dataset_key]['shape']
                                # print('Shape: ', shape)
                                
                                data_type = datasets_attributes[key][dataset_key]['dtype']
                                # print('data_type: ', data_type)
                                
                                # data = datasets_attributes[key][dataset_key]['data']
                                # print('data: ', data)

                                description  = f'Description:\n\t\t {dataset_description}'
                                description  = f'\n\tShape:\n\t\t {shape}'
                                description  = f'\n\tdtype:\n\t\t {data_type}'
                                # description  = f'\n\tdata:\n\t\t {data}'
                                # print(description)
                                data_summaries+=description+'\n'
                        
                        elif key == 'attributes':
                            data_summaries+='\n\n'
                            print('Inside attribute key, datasets_attributes[key]: ', datasets_attributes[key])

                            for attribute_key in datasets_attributes[key]:    
                                attributes_description = datasets_attributes[key][attribute_key]
                                # attributes = f'Attributes: \n'+{datasets_attributes[key][attribute_key]}
                                description = ''
                                
                                for attribute in attributes_description:
                                    description+=attribute+', '
                                
                                attributes = f'Attributes in {attribute_key}: \n'+description
                                # print(attributes)
                                data_summaries+=attributes+'\n'
                            # print(f' Description:\n Shape: {datasets_attributes['description'][key]['shape']} ---dtype: {datasets_attributes['description'][key]['dtype']}')

                        # print(f'\nDataset: ', key, '\nAttributes:\n ', value)
                    print('Final datasummaries: ', data_summaries)
                    
                    # create the data subdirectory if not exists
                    if not os.path.exists(output_directory+'/'+data_subdir):
                        os.makedirs(output_directory+'/'+data_subdir)

                    output_file_path = os.path.join(output_directory+'/'+data_subdir, f'{file_base_name}.txt')
                    
                    print('output_file_path: ', output_file_path)
                    utils.save_file(output_file_path, data_summaries)
    except Exception as e:
        print('Exception message is: ', e)


if __name__ == '__main__':
    
    # common data paths
    common_base_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'
    extensions = ['hdf5', 'he5', 'h5', 'HDF5', 'H5', 'HE5']

    dataset_list = ['MATPLOT_AGENT', 'FAST_MRI_BRAIN', 'CLIMATE']
    
    # mat plot agent
    dataset = dataset_list[0]
    
    # fast mri brain
    dataset = dataset_list[1]

    # climate
    # dataset = dataset_list[2]

    if dataset == 'MATPLOT_AGENT':
        print('This module is for the matplot agent csv dataset')
    elif dataset == 'FAST_MRI_BRAIN':
        print('Inside fast MRI brain data...')
        
        data_dir = 'mri_nyu_data/data_files/dcm_to_h5_converted_data_files'  # Replace with your common directory path
        # subdirectories = ['singlecoil_test', 'multicoil_test']  # Replace with your predefined subdirectory names
        # subdirectories = ['singlecoil_val']  # Replace with your predefined subdirectory names
        # subdirectories = ['dcm_to_h5']
        subdirectories = [
            # 'all_dicom_to_single_h5',
            'fastMRI_brain_dcm_to_h5'
        ]

        output_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/data_summaries/FAST_MRI_BRAIN_DICOM_TO_H5_DATASETS'
        # output_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data'

         # for fast MRI datasets
        print('Data full directory: ', common_base_directory+'/'+data_dir)
        receive_data_path_print_data_summary(common_base_directory+"/"+data_dir, subdirectories, extensions, output_directory)
    
    elif dataset == 'CLIMATE':
        data_dir = 'ACL_DIRS'
        # for the fast MRI datasets
        
        subdirectories = ['ASF', 'GES_DISC', 'GHRC', 'ICESat_2', 'LAADS', 'LaRC', 'LP_DAAC', 'NSIDC', 'Ocen_Biology', 'PO_DAAC', 'AURA_DATA_VC']  # Replace with your predefined subdirectory names

        
        output_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/data_summaries/CLIMATE_DATA_METADATA_DESCRIPTIONS'
        
        # source_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/chain_of_repair_input_llama3_latest'
        # target_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/output_chain_of_repair'

        # generate_code_and_save(source_directory, target_directory, old_ext='.txt')


        # NASA climate datsets
        # data_dir = 'ACL_DIRS'  # Replace with your common directory path
        # subdirectories = ['ASF', 'GES_DISC', 'GHRC', 'ICESat_2', 'LAADS', 'LaRC', 'LP_DAAC', 'NSIDC', 'Ocen_Biology', 'PO_DAAC', 'AURA_DATA_VC']  # Replace with your predefined subdirectory names
        
        # output_subdir = '/zero_shot_output/summaries'  # The name of the directory to save output files
        # output_subdir = 'chain_of_repair_with_data_structure_output_llama3_latest'  # The name of the directory to save output files

        # output_dir = common_directory+'/sci_data_prompting/python-script-output'
        # output_subdir = 'deepseek_coder_v2_with_data_separate_attribute'  # The name of the directory to save output files
        # output_subdir = 'deepseek_coder_v2_with_data_rule_base_reasoning-exact-dataset-path-matching'  # The name of the directory to save output files


        # model = ['llama3:latest', 'deepseek-coder-v2']
        # this part is for reading data and make summaries along with the example data
        # remove the example data part
        # find_and_process_files(common_directory, subdirectories, extensions)
        # user_input_dir = common_directory+"/original_python_script_description_with_20_p_reduc"
        # user_input_dir = common_directory+"/generated_user_input_local_llama3"
        receive_data_path_print_data_summary(common_base_directory+"/"+data_dir, subdirectories, extensions)
