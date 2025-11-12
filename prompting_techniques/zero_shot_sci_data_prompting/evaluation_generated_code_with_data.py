import os
import subprocess
import pandas as pd



def find_python_scripts(script_dir):
    """
    Search for Python scripts in a specified directory.
    
    Args:
        script_dir (str): Directory where Python scripts are located.
    
    Returns:
        dict: Dictionary where keys are base filenames (without extension), and values are the full paths to Python scripts.
    """
    py_scripts = {}
    for root, _, files in os.walk(script_dir):
        for file in files:
            if file.endswith('.py'):
                base_name = os.path.splitext(file)[0]  # Get base filename without extension
                py_scripts[base_name] = os.path.join(root, file)
    return py_scripts

def run_python_script(script_path):
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
        return 'Pass', None  # If it runs successfully, return 'Pass'
    except subprocess.CalledProcessError as e:
        return 'Fail', e.stderr  # If an error occurs, return 'Fail' and the error message

def create_xlsx_report(results, output_file):
    """
    Creates an Excel file with the results.
    
    Args:
        results (list): List of dictionaries containing script name, status, and error (if any).
        output_file (str): Path to save the Excel file.
    """
    df = pd.DataFrame(results)
    # df.to_excel(output_file, index=False)
    df.to_csv(output_file, index=False)
    print(f"Report saved to {output_file}")

def process_scripts(script_dir, output_file):
    """
    Main function to process HDF5 files and Python scripts, run the scripts, and generate the report.
    
    Args:
        sub_dirs (list): List of directories containing HDF5 files.
        script_dir (str): Directory containing Python scripts.
        output_file (str): Path to save the Excel report.
    """
    # Step 1: Find all HDF5 files in the subdirectories
 
    # Step 2: Find all Python scripts in the script directory
    py_scripts = find_python_scripts(script_dir)

    results = []  # To store results

    # Step 3: Match HDF5 files with Python scripts (based on base filename) and run the script
        # cleaned_py_base_name = clean_filename(base_name)  # Remove unwanted substrings

        # if base_name == cleaned_py_base_name:
        # if base_name in py_scripts:
    for py_script in py_scripts:
    
        script_path = py_scripts[py_script]
        print(f"Running script {script_path}...")
        
        # Run the Python script and capture pass/fail status and any errors
        status, error = run_python_script(script_path)
        
        code =''
        with open(script_path, 'r') as f:
            code = f.read()

        # Add result to the list
        results.append({
            'Code: ': code,
            'Python Script': os.path.basename(script_path),
            'Status': status,
            'Error': error
        })
      

    # Step 4: Create the Excel report
    create_xlsx_report(results, output_file)



if __name__ == '__main__':
    model_list = ['llama3:latest', 'deepseek-coder-v2', 'codellama', 'codellama:7b-python', 'llama3:70b', 'magicoder']
    # magicoder
    # model = model_list[5]

    # deepseek-coder-v2
    # model = model_list[1]
    
    
    # llama3:70b
    model = model_list[4]
    
    model_name = model.replace('-', '_')
    model_name = model_name.replace(':', '_')

    # corrector = 'with'
    corrector = 'without'
    

    common_base_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'
    # output_file ='/Users/apukumarchakroborti/gsu_research/llam_test/sci_data_prompting/evaluation-result/magicoder_zero_shot_CoT_without_corrector_path_variations.csv'
    output_file =f'{common_base_directory}/prompting_techniques/zero_shot_sci_data_prompting/evaluation-result/{model_name}_zero_shot_CoT_{corrector}_corrector_resolving_errors.csv'

    # python_script_dir = common_directory+"/sci_data_prompting/python-script-output/magicoder_zero_shot_CoT_without_corrector_path_variations"
    python_script_dir = f"{common_base_directory}/prompting_techniques/zero_shot_sci_data_prompting/python-script-output/fastMRI_brain/{model_name}_zero_shot_CoT_{corrector}_corrector_resolving_errors"

    process_scripts(python_script_dir, output_file)

    
    # Example usage
    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/sci_data_prompting/evaluation-result/deepseek_coder_v2_zero_shot_CoT_with_corrector.csv'
    # output_file = "/Users/apukumarchakroborti/gsu_research/llam_test/sci_data_prompting/evaluation-result/deepseek_coder_v2_zero_shot_CoT_with_corrector_v3.csv"

    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/evaluation-result/deepseek_coder_v2_generated_python_script_for_hdf5_with_corrector.csv'
    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/evaluation-result/magicoder_zero_shot_CoT_generated_python_script_for_hdf5_with_corrector.csv'  
    # output_file = "/Users/apukumarchakroborti/gsu_research/llam_test/sci_data_prompting/evaluation-result/magicoder_zero_shot_CoT_with_corrector_root_and_immediate_group.csv"
    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/sci_data_prompting/evaluation-result/magicoder_zero_shot_CoT_with_corrector_replace_incorrect_datasets_attributes_test.csv'
    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/evaluation-result/llama3_70b_generated_python_script_for_hdf5_with_corrector.csv'  
    # output_file ='/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/evaluation-result/magicoder_zero_shot_CoT_with_corrector_replace_incorrect_datasets_attributes_lavenshtein.csv'
    # output_file ='/Users/apukumarchakroborti/gsu_research/llam_test/sci_data_prompting/evaluation-result/magicoder_zero_shot_CoT_with_corrector_user_prompt_words_correction_lavenshtein'
    # output_file ='/Users/apukumarchakroborti/gsu_research/llam_test/sci_data_prompting/evaluation-result/magicoder_zero_shot_CoT_with_corrector_v1.csv'
    # output_file ='/Users/apukumarchakroborti/gsu_research/llam_test/sci_data_prompting/evaluation-result/magicoder_zero_shot_CoT_with_corrector_asked_llm_step_by_step'
    # output_file ='/Users/apukumarchakroborti/gsu_research/llam_test/sci_data_prompting/evaluation-result/magicoder_zero_shot_CoT_with_corrector_with_slicing.csv'
    # output_file ='/Users/apukumarchakroborti/gsu_research/llam_test/sci_data_prompting/evaluation-result/deepseek_coder_v2_zero_shot_CoT_with_corrector_with_slicing.csv'
    # output_file ='/Users/apukumarchakroborti/gsu_research/llam_test/sci_data_prompting/evaluation-result/llama3_70b_zero_shot_CoT_with_corrector_with_slicing.csv'
    # output_file ='/Users/apukumarchakroborti/gsu_research/llam_test/sci_data_prompting/evaluation-result/llama3_70b_zero_shot_CoT_without_corrector.csv'
    # output_file ='/Users/apukumarchakroborti/gsu_research/llam_test/sci_data_prompting/evaluation-result/deepseek_coder_v2_zero_shot_CoT_without_corrector_path_variations.csv'


    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/evaluation-result/deepseek_coder_v2_generated_python_script_for_hdf5_zero_shot_CoT.csv'  # Path to save the Excel report
    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/evaluation-result/magicoder_generated_python_script_for_hdf5_zero_shot_CoT.csv'  # Path to save the Excel report
    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/evaluation-result/llama_70b_generated_python_script_for_hdf5_zero_shot_CoT.csv'  # Path to save the Excel report

    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/evaluation-result/llama3_70b_generated_python_script_for_csv.csv'  # Path to save the Excel report

    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/evaluation-result/llama3_70b_generated_python_script_for_csv.csv'  # Path to save the Excel report
    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/evaluation-result/llama3_70b_generated_python_script_for_csv.csv'  # Path to save the Excel report
    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/evaluation-result/llama3_70b_generated_python_script_for_csv.csv'  # Path to save the Excel report

    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/evaluation-result/magicoder_generated_python_script_for_hdf5.csv'  # Path to save the Excel report
    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/evaluation-result/llama3_70b_generated_python_script_for_csv.csv'  # Path to save the Excel report
    # output_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/evaluation-result/llama3_70b_generated_python_script_for_csv.csv'  # Path to save the Excel report

    # script_dir=common_directory+"/"+"chain_of_repair_output_llama3_latest"
    # script_dir=common_directory+"/"+"chain_of_repair_with_data_deep_seek_coder_v2"
    # script_dir = common_directory+"/cor_with_data_deepseek_coder_v2_with_data_extensions"
    # script_dir = common_directory+"/cor_with_data_deepseek_coder_v2_with_data_ext_path"
    # script_dir = common_directory+"/cor_with_data_deepseek_coder_v2_with_data_replaced_base_name_by_path"
    # script_dir = common_directory+"/cor_with_data_deepseek_coder_v2_with_data_getting_dataset_only"
    # script_dir = common_directory+"/cor_with_data_deepseek_coder_v2_with_data_all_possible_combination"
    # script_dir = common_directory+"/cor_with_data_deepseek_coder_v2_with_data_separate_dataset_attribute_v2"

    # script_dir = common_directory+"/sci_data_prompting/python-script-output/deepseek_coder_v2_with_data_rule_base_reasoning"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output-sepeate-group-attribute/deepseek_coder_v2_with_data_rule_base_reasoning"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/deepseek_coder_v2_with_data_rule_base_reasoning-exact-dataset-path-matching"

    # script_dir = common_directory+"/sci_data_prompting/python-script-output/deepseek_coder_v2_with_data_rbs_example_latitude_longtidue_code"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/deepseek_coder_v2_with_data_rbs_with_restrictions"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/deepseek_coder_v2_with_data_rbs_path_import_restrictions"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/llama3_latest_with_data_rbs_path_import_restrictions"
    # script_dir = common_directory+'/sci_data_prompting/python-script-output/deepseek_coder_v2_final_set_with_fuzzy'
    # script_dir = common_directory+'/sci_data_prompting/python-script-output/deepseek_coder_v2_spearate_dataset_latitude_and_longitude'
    # script_dir = common_directory+'/sci_data_prompting/python-script-output/generated_user_input_human_like_text_directly_remove_library_names'
    # script_dir = common_directory+'/sci_data_prompting/python-script-output/generated_user_input_human_like_text_directly_remove_library_names_added_paths'
    # script_dir = common_directory+'/plot_generation/generated_python_script_replaced_colums_by_datasets'
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/deepseek_coder_v2_zero_shot_CoT_with_corrector"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/deepseek_coder_v2_zero_shot_CoT_with_corrector_v3"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/magicoder_zero_shot_CoT_with_corrector_root_and_immediate_group"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/magicoder_zero_shot_CoT_with_corrector_replace_incorrect_datasets_attributes_test"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/magicoder_zero_shot_CoT_with_corrector_replace_incorrect_datasets_attributes_lavenshtein"

    # script_dir = common_directory+"/sci_data_prompting/python-script-output/magicoder_zero_shot_CoT_with_corrector_user_prompt_words_correction_lavenshtein"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/magicoder_zero_shot_CoT_with_corrector_v1"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/magicoder_zero_shot_CoT_with_corrector_asked_llm_step_by_step"

    # script_dir = common_directory+"/sci_data_prompting/python-script-output/magicoder_zero_shot_CoT_with_corrector_with_function"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/magicoder_zero_shot_CoT_with_corrector_with_slicing"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/deepseek_coder_v2_zero_shot_CoT_with_corrector_with_slicing"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/llama3_70b_zero_shot_CoT_with_corrector_with_slicing"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/llama3_70b_zero_shot_CoT_without_corrector"
    # script_dir = common_directory+"/sci_data_prompting/python-script-output/deepseek_coder_v2_zero_shot_CoT_without_corrector_path_variations"

    # These are for the MatPlotAgent
    # script_dir = common_directory+'/plot_generation/python_script_llm/deepseek_coder_v2_generated_python_script_for_csv'
    # script_dir = common_directory+'/plot_generation/python_script_llm/magicoder_generated_python_script_for_csv'
    # script_dir = common_directory+'/plot_generation/python_script_llm/llama3_70b_generated_python_script_for_csv'

    # script_dir = common_directory+'/plot_generation/python_script_llm/magicoder_zero_shot_CoT_generated_python_script_for_hdf5_with_corrector'
    # script_dir = common_directory+'/plot_generation/python_script_llm/deepseek_coder_v2_generated_python_script_for_hdf5_with_corrector'
    # script_dir = common_directory+'/plot_generation/python_script_llm/llama3_70b_generated_python_script_for_hdf5_with_corrector'

    # script_dir = common_directory+'/plot_generation/python_script_llm/magicoder_generated_python_script_for_hdf5_zero_shot_CoT'
    # script_dir = common_directory+'/plot_generation/python_script_llm/deepseek_coder_v2_generated_python_script_for_hdf5_zero_shot_CoT'
    # script_dir = common_directory+'/plot_generation/python_script_llm/llama_70b_generated_python_script_for_hdf5_zero_shot_CoT'

   
