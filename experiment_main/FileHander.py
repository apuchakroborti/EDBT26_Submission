import os
import glob

from common_util_script import Utils as utils

from common_util_script import DataSummarizer as dataSummarizer

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
    dir2_dict = {utils.get_base_filename(os.path.basename(f)): f for f in files_dir2}
    # print('dir2_dict', dir2_dict)

    for file1 in files_dir1:
        # print(file1)
        base_name1 = utils.get_base_filename(os.path.basename(file1))
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



common_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'
data_dir = 'ACL_DIRS'  # Replace with your common directory path
subdirectories = ['ASF', 'GES_DISC', 'GHRC', 'ICESat_2', 'LAADS', 'LaRC', 'LP_DAAC', 'NSIDC', 'Ocen_Biology', 'PO_DAAC', 'AURA_DATA_VC']  # Replace with your predefined subdirectory names
extensions = ['hdf5', 'he5', 'h5', 'HDF5', 'H5', 'HE5']

# output_dir = common_directory+'/sci_data_prompting/python-script-output'
print("FileHandler")
for data_subdir in subdirectories:
    data_search_path = os.path.join(common_directory+"/"+data_dir, data_subdir, '*')
    for ext in extensions:
        data_files = glob.glob(f"{data_search_path}.{ext}")
        for data_file_path in data_files:
            print(f"\n\nProcessing file: {data_file_path}")
            # dataSummarizer.summarize_hdf5_and_print(data_file_path)
            # break
            dataSummarizer.summarize_latitude_longditude_information_and_print(data_file_path)
            