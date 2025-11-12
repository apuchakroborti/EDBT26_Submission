import pydicom
import h5py
import numpy as np
import os

specific_folders = ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010']

def construct_group_and_datasets(dicom_root_folder, output_h5_file):
    all_subdirectories = os.listdir(dicom_root_folder)
    # print('All subdirectories: ', all_subdirectories)
    # all_subdirectories = all_subdirectories.remove('.DS_Store')    
    # Initialize an HDF5 file
    with h5py.File(output_h5_file, "w") as h5_file:
        # create the root group
        group_name = 'MRI_ROOT'  # Use file name as group name
        root_group = h5_file.create_group(group_name)
        print('Root Group: ', root_group)
        
        for folders_root_directory in all_subdirectories:
            if folders_root_directory in specific_folders and folders_root_directory!='.DS_Store':
                root_sub_group = root_group.create_group(folders_root_directory)
                print('Root Sub Group: ', root_sub_group)

                folders_root_directory_full_path = os.path.join(dicom_root_folder, folders_root_directory)
                
                all_directories_under_root = os.listdir(folders_root_directory_full_path)
                # print('Sub directories under root: ', all_directories_under_root)
                for immediate_parent_group in all_directories_under_root:
                    if immediate_parent_group!='.DS_Store':
                        immediate_parent_sub_group = root_sub_group.create_group(immediate_parent_group)
                        print('Immediate Parent Group: ', immediate_parent_sub_group)
                        
                        immediate_parent_group_full_path = os.path.join(folders_root_directory_full_path, immediate_parent_group)
                        all_directories_under_immediate_parent_group = os.listdir(immediate_parent_group_full_path)
                        # print('All directories under immediate parent group: ', all_directories_under_immediate_parent_group)
                        
                        for dicom_file in all_directories_under_immediate_parent_group:
                            if dicom_file!='.DS_Store':
                                file_name = dicom_file.split('.')[0]
                                parent_group = immediate_parent_sub_group.create_group(file_name)
                                print('Parent Group: ', parent_group)

                                print('Processing file: ', dicom_file)
                                if dicom_file.endswith(".dcm"):
                                    file_path = os.path.join(immediate_parent_group_full_path, dicom_file)

                                    # Read DICOM file
                                    dicom_data = pydicom.dcmread(file_path)
                                    # print(dicom_data)
                                    # print('dicom_data.fileobj_type: ', dicom_data.fileobj_type)
                                    # print('dicom_data.elements: ', dicom_data.elements)
                                    # print('dicom_data.data_element: ', dicom_data.data_element)
                                    # print('dicom_data.filename: ', dicom_data.filename)
                                    # print('dicom_data.keys: ', dicom_data.keys)
                                    
                                    # Extract pixel data and metadata
                                    pixel_data = dicom_data.pixel_array
                                    metadata = {tag: dicom_data[tag].value for tag in dicom_data.dir() if tag in dicom_data}
                                    # metadata = {tag: dicom_data[tag].value for tag in dicom_data.dir() if tag in dicom_data and tag !='PixelData'}
                                    # print('Metadata: ', metadata)

                                    # Create a group in HDF5 for this DICOM file
                                    # group_name = os.path.splitext(dicom_file)[0]  # Use file name as group name
                                    # group = h5_file.create_group(group_name)

                                    # Store pixel data
                                    # datasets = parent_group.create_dataset("pixel_data", data=pixel_data, compression="gzip")
                                    
                                    # without compression
                                    datasets = parent_group.create_dataset("pixel_data", data=pixel_data)
                                    print('Datasets: ', datasets)

                                    # Store metadata
                                    metadata_group = parent_group.create_group("metadata")
                                    # metadata_datasets = group.create_dataset("metadata")
                                    for key, value in metadata.items():
                                        # print('Key: ', key, end=': ')
                                        # print('Value: ', value)
                                        # Handle non-serializable metadata values
                                        try:
                                            metadata_group.attrs[key] = str(value)
                                            # metadata_datasets.attrs[key] = str(value)
                                            # print('metadata_group.attrs[key]', metadata_group.attrs[key])
                                        except Exception:
                                            metadata_group.attrs[key] = "Not serializable"
                                            # metadata_datasets.attrs[key] = "Not serializable"


def convert_fastMRI_brain_DICOM_whole_dcm_to_hdf5(dicom_root_folder, output_h5_file):
    all_subdirectories = os.listdir(dicom_root_folder)
    # print('All fastMRI_brain DICOM subdirectories: ', all_subdirectories)
    # all_subdirectories = all_subdirectories.remove('.DS_Store')    
    # Initialize an HDF5 file
    max_count = 200

    root_group = ''
    group_name = ''
    with h5py.File(output_h5_file, "w") as h5_file:
        # create the root group
        group_name = 'FAST_MRI_BRAIN_ROOT'  # Use file name as group name
        root_group = h5_file.create_group(group_name)
        print('Root Group: ', root_group)
    
        for sub_directory in all_subdirectories:
            if max_count < 0:
                break

            max_count-=1
            if sub_directory == '.DS_Store':
                continue

            print('root group: ', root_group)
            print('sub_directory: ', sub_directory)
            
            immediate_parent_group_full_path=''
            try:
                
                immediate_parent_sub_group = root_group.create_group(sub_directory)
                print('immediate_parent_sub_group: ', immediate_parent_sub_group)

                immediate_parent_group_full_path = dicom_root_folder+'/'+sub_directory
                print('immediate_parent_group_full_path: ', immediate_parent_group_full_path)

            except Exception as e:
                print('Error: ', e)
                            
            all_directories_under_immediate_parent_group = os.listdir(immediate_parent_group_full_path)
            # all_directories_under_immediate_parent_group = ['abc']
            print('All directories: ', all_directories_under_immediate_parent_group)
            
            for dicom_file in all_directories_under_immediate_parent_group:
                if dicom_file!='.DS_Store':
                    file_name = dicom_file.split('.')[0]
                    parent_group = immediate_parent_sub_group.create_group(file_name)
                    print('Parent Group: ', parent_group)

                    print('Processing file: ', dicom_file)
                    if dicom_file.endswith(".dcm"):
                        file_path = os.path.join(immediate_parent_group_full_path, dicom_file)

                        # Read DICOM file
                        dicom_data = pydicom.dcmread(file_path)
                        # print(dicom_data)
                        # print('dicom_data.fileobj_type: ', dicom_data.fileobj_type)
                        # print('dicom_data.elements: ', dicom_data.elements)
                        # print('dicom_data.data_element: ', dicom_data.data_element)
                        # print('dicom_data.filename: ', dicom_data.filename)
                        # print('dicom_data.keys: ', dicom_data.keys)
                        
                        # Extract pixel data and metadata
                        pixel_data = dicom_data.pixel_array
                        # metadata = {tag: dicom_data[tag].value for tag in dicom_data.dir() if tag in dicom_data}
                        metadata = {tag: dicom_data[tag].value for tag in dicom_data.dir() if tag in dicom_data and tag !='PixelData'}
                        # print('Metadata: ', metadata)

                        # Create a group in HDF5 for this DICOM file
                        # group_name = os.path.splitext(dicom_file)[0]  # Use file name as group name
                        # group = h5_file.create_group(group_name)

                        # Store pixel data
                        # datasets = parent_group.create_dataset("pixel_data", data=pixel_data, compression="gzip")
                        
                        # without compression
                        # datasets = parent_group.create_dataset("pixel_data", data=pixel_data)
                        datasets = parent_group.create_dataset("fastMRI_brain_data", data=pixel_data)
                        print('Datasets: ', datasets)

                        # Store metadata
                        metadata_group = parent_group.create_group("metadata")
                        # metadata_datasets = group.create_dataset("metadata")
                        for key, value in metadata.items():
                            # print('Key: ', key, end=': ')
                            # print('Value: ', value)
                            # Handle non-serializable metadata values
                            try:
                                metadata_group.attrs[key] = str(value)
                                # metadata_datasets.attrs[key] = str(value)
                                # print('metadata_group.attrs[key]', metadata_group.attrs[key])
                            except Exception:
                                metadata_group.attrs[key] = "Not serializable"
                                # metadata_datasets.attrs[key] = "Not serializable"


fastMRI_brain_specific_folders = ['279.dcm', '280.dcm', '281.dcm', '282.dcm', '283.dcm', '283.dcm', '294.dcm', '295.dcm', '300.dcm', '301.dcm']
def convert_fastMRI_brain_DICOM_partial_dcm_to_hdf5(dicom_root_folder, output_h5_file):
    
    all_subdirectories = os.listdir(dicom_root_folder)
    # print('All fastMRI_brain DICOM subdirectories: ', all_subdirectories)
    # all_subdirectories = all_subdirectories.remove('.DS_Store')    
    # Initialize an HDF5 file
    with h5py.File(output_h5_file, "w") as h5_file:
        # create the root group
        group_name = 'FAST_MRI_BRAIN_ROOT'  # Use file name as group name
        root_group = h5_file.create_group(group_name)
        print('Root Group: ', root_group)
    
        immediate_parent_group_full_path=''
        try:
            immediate_parent_sub_group = root_group.create_group('100099070170')
            immediate_parent_group_full_path = dicom_root_folder+'/100099070170'
        except Exception as e:
            print('Error: ', e)
        # for folders_root_directory in all_subdirectories:
            # if folders_root_directory in specific_folders and folders_root_directory!='.DS_Store':
                # root_sub_group = root_group.create_group(folders_root_directory)
                # print('Root Sub Group: ', root_sub_group)

                # folders_root_directory_full_path = os.path.join(dicom_root_folder, folders_root_directory)
                
                # all_directories_under_root = os.listdir(folders_root_directory_full_path)
                # print('Sub directories under root: ', all_directories_under_root)
                # for immediate_parent_group in all_directories_under_root:
                    # if immediate_parent_group!='.DS_Store':
                        # immediate_parent_sub_group = root_sub_group.create_group(immediate_parent_group)
                        # print('Immediate Parent Group: ', immediate_parent_sub_group)
                        
                        # immediate_parent_group_full_path = os.path.join(folders_root_directory_full_path, immediate_parent_group)
                        # all_directories_under_immediate_parent_group = os.listdir(immediate_parent_group_full_path)
                        # print('All directories under immediate parent group: ', all_directories_under_immediate_parent_group)
                        
        all_directories_under_immediate_parent_group = os.listdir(immediate_parent_group_full_path)
        print('All directories: ', all_directories_under_immediate_parent_group)
        
        for dicom_file in all_directories_under_immediate_parent_group:
            if dicom_file!='.DS_Store' and dicom_file in fastMRI_brain_specific_folders:
                file_name = dicom_file.split('.')[0]
                parent_group = immediate_parent_sub_group.create_group(file_name)
                print('Parent Group: ', parent_group)

                print('Processing file: ', dicom_file)
                if dicom_file.endswith(".dcm"):
                    file_path = os.path.join(immediate_parent_group_full_path, dicom_file)

                    # Read DICOM file
                    dicom_data = pydicom.dcmread(file_path)
                    # print(dicom_data)
                    # print('dicom_data.fileobj_type: ', dicom_data.fileobj_type)
                    # print('dicom_data.elements: ', dicom_data.elements)
                    # print('dicom_data.data_element: ', dicom_data.data_element)
                    # print('dicom_data.filename: ', dicom_data.filename)
                    # print('dicom_data.keys: ', dicom_data.keys)
                    
                    # Extract pixel data and metadata
                    pixel_data = dicom_data.pixel_array
                    metadata = {tag: dicom_data[tag].value for tag in dicom_data.dir() if tag in dicom_data}
                    # metadata = {tag: dicom_data[tag].value for tag in dicom_data.dir() if tag in dicom_data and tag !='PixelData'}
                    # print('Metadata: ', metadata)

                    # Create a group in HDF5 for this DICOM file
                    # group_name = os.path.splitext(dicom_file)[0]  # Use file name as group name
                    # group = h5_file.create_group(group_name)

                    # Store pixel data
                    # datasets = parent_group.create_dataset("pixel_data", data=pixel_data, compression="gzip")
                    
                    # without compression
                    # datasets = parent_group.create_dataset("pixel_data", data=pixel_data)
                    datasets = parent_group.create_dataset("fastMRI_brain_data", data=pixel_data)
                    print('Datasets: ', datasets)

                    # Store metadata
                    metadata_group = parent_group.create_group("metadata")
                    # metadata_datasets = group.create_dataset("metadata")
                    for key, value in metadata.items():
                        # print('Key: ', key, end=': ')
                        # print('Value: ', value)
                        # Handle non-serializable metadata values
                        try:
                            metadata_group.attrs[key] = str(value)
                            # metadata_datasets.attrs[key] = str(value)
                            # print('metadata_group.attrs[key]', metadata_group.attrs[key])
                        except Exception:
                            metadata_group.attrs[key] = "Not serializable"
                            # metadata_datasets.attrs[key] = "Not serializable"

                


if __name__ == '__main__':
    # Input path
    # dicom_root_folder = "/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/DICOMS/001/AX_DIFFUSION_ADC"
    # dicom_root_folder = "/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/DICOMS"  # Folder containing .dcm files
    dicom_root_folder = "/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/data_files/original_data_files/fastMRI_brain_DICOM"
    
    # Output path
    # output_h5_file = "/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/output_dcm_96_data.h5"
    # output_h5_file = "/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/dcm_first_10_to_h5_without_compression.h5"
    # output_h5_file = "/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/fastMRI_brain_dcm_to_h5/fastMRI_brain_first_10_dcm_to_h5.h5"
    # output_h5_file = "/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_100_dcm_to_h5.h5"
    output_h5_file = "/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/data_files/dcm_to_h5_converted_data_files/fastMRI_brain_200_dcm_to_h5.h5"

    
    # this is for the partial fastMRI_brain_DICOM files
    # convert_fastMRI_brain_DICOM_partial_dcm_to_hdf5(dicom_root_folder, output_h5_file)

    # this is for the whole fastMRI_brain_DICOM files
    convert_fastMRI_brain_DICOM_whole_dcm_to_hdf5(dicom_root_folder, output_h5_file)

    # this is for the prostrate DICOM files
    # construct_group_and_datasets(dicom_root_folder, output_h5_file)