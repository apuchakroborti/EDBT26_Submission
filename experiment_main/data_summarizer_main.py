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


def receive_data_path_print_data_summary(data_files_common_directory, data_subdirectories, extensions, output_directory):
    try:
        for data_subdir in data_subdirectories:
            data_search_path = os.path.join(data_files_common_directory, data_subdir, '*')
            
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
                    if datasets_attributes is not None:
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
                    else:
                        print(f'No data found!')
                    
                    # create the data subdirectory if not exists
                    if not os.path.exists(output_directory+'/'+data_subdir):
                        os.makedirs(output_directory+'/'+data_subdir)

                    output_file_path = os.path.join(output_directory+'/'+data_subdir, f'{file_base_name}.txt')
                    
                    print('output_file_path: ', output_file_path)
                    utils.save_file(output_file_path, data_summaries)
    except Exception as e:
        print('Exception message is: ', e)
        return None


if __name__ == '__main__':
    
    # common data paths
    PROJECT_BASE_DIRECTORY = '/Users/apukumarchakroborti/gsu_research/llam_test'
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
        print('Data full directory: ', PROJECT_BASE_DIRECTORY+'/'+data_dir)
        receive_data_path_print_data_summary(PROJECT_BASE_DIRECTORY+"/"+data_dir, subdirectories, extensions, output_directory)
    
    elif dataset == 'CLIMATE':
        data_dir = 'ACL_DIRS'
        # for the fast MRI datasets
        
        subdirectories = ['ASF', 'GES_DISC', 'GHRC', 'ICESat_2', 'LAADS', 'LaRC', 'LP_DAAC', 'NSIDC', 'Ocen_Biology', 'PO_DAAC', 'AURA_DATA_VC']  # Replace with your predefined subdirectory names

        
        output_directory = f'{PROJECT_BASE_DIRECTORY}/NASA_EOS/data_summaries/CLIMATE_DATA_METADATA_DESCRIPTIONS'
        
       
        # NASA climate datsets
        # data_dir = 'ACL_DIRS'  # Replace with your common directory path
        # subdirectories = ['ASF', 'GES_DISC', 'GHRC', 'ICESat_2', 'LAADS', 'LaRC', 'LP_DAAC', 'NSIDC', 'Ocen_Biology', 'PO_DAAC', 'AURA_DATA_VC']  # Replace with your predefined subdirectory names
       
        # this part is for reading data and make summaries along with the example data
        receive_data_path_print_data_summary(data_files_common_directory=PROJECT_BASE_DIRECTORY+"/"+data_dir, data_subdirectories=subdirectories, extensions=extensions, output_directory=output_directory)
