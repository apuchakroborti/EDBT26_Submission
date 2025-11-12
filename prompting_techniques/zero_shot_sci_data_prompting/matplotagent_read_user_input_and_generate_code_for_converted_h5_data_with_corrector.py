import json
import requests
import os
URL = 'http://ai-lab2.dyn.gsu.edu:11434/api/generate'
import argparse
from common_util_script import ArgumentParser as argumentParsar
import os

from common_util_script import LLMRequester as llmRequester
# Function to read, process, and save the JSON file
from common_util_script import Utils as utils
import sci_data_prompting_corrector as corrector
import evaluation_error_categorization as python_execution_helper

file_list = ['76', '77', '78', '79', '83', '84', '87', '95', '96', '97', '99', '100']

def process_json(input_file, target_dir):
    # Read the JSON file
    with open(input_file, 'r') as infile:
        data = json.load(infile)  # Load the JSON data

    # Process the data (example: convert all strings to uppercase)
    processed_data = []
    for item in data:
        if isinstance(item, dict):  # If the item is a dictionary
            print('Processing file: ', item['id'])
            ID = str(item['id'])
            if ID not in file_list:
                continue            
           
            try:
                print(f'\n\n-----------------------------------------------------------------------------')                
                print(f'Processing file: si_python_script_{ID}.py\n\n')
                # common_data_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/*_h5_data.h5'
                # common_data_path = '/Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/plot_generation/csv_to_h5_data/*_h5_data.h5'
                
                # this is for macbook Me pro
                # base_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'
                
                # this is for gsu server
                base_directory ='/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data'
                common_data_path = base_directory+'/matplot_agent_data/plot_generation/csv_to_h5_data/*_h5_data.h5'
                common_data_path = common_data_path.replace('*', str(item['id']))
                
                try:
                    users_simple_instruction = ''
                    users_simple_instruction=item['simple_instruction']
                    users_simple_instruction = users_simple_instruction.replace('data.csv', common_data_path)
                    users_simple_instruction = users_simple_instruction.replace('CSV', 'hdf5')
                    users_simple_instruction = users_simple_instruction.replace('columns', 'datasets')
                    users_simple_instruction = users_simple_instruction.replace('column', 'dataset')
                    print('\n\nRaw Simple Instruction: \n',  users_simple_instruction)
                    # function returns result, attribute_present, updated_text
                    data_structure_information, attribute_present, updated_text = corrector.corrector_function_main(users_simple_instruction, common_data_path)
                    
                    print('Data structure information for simple instruction:\n', data_structure_information)
                    # simple_instruction_converter = requestor.generate_request_convert_text_input_to_human_generated_and_add_external_data_path(item['simple_instruction'], model)
                    # simple_instruction_converter = requestor.form_request_to_generate_code_from_text(users_simple_instruction, model)
                    # parameters: user_input, data_structure_information, full_data_path, model)
                    # simple_instruction_converter = requestor.generate_request_for_generating_source_code_with_data_rule_base_reasoning_copied(users_simple_instruction, data_structure_information, common_data_path, model)
                    
                    # zero-shot CoT
                    # def generate_request_for_generating_source_code_with_zero_shot_CoT_best_success(user_input, data_structure_information, full_data_path, attribute_present):
                    # simple_instruction_converter = requestor.generate_request_for_generating_source_code_with_zero_shot_CoT_with_corrector(users_simple_instruction, data_structure_information, common_data_path, attribute_present, model)
                    
                    # without using updated text
                    # simple_instruction_converter = llmRequester.generate_request_for_generating_source_code_separate_prompt_method_with_zero_shot_CoT_with_corrector_step_by_step(users_simple_instruction, data_structure_information, common_data_path, attribute_present, model)
                    
                    # with updated user quries
                    users_simple_instruction = updated_text
                    simple_instruction_converter = llmRequester.generate_request_for_generating_source_code_separate_prompt_method_with_zero_shot_CoT_with_corrector_step_by_step(users_simple_instruction, data_structure_information, common_data_path, attribute_present, model)

                    # source_code_gen = json.dumps(simple_instruction_converter).encode("utf-8")
                    # llm_gen_source_code = requests.post(URL, data=source_code_gen)
                    #print(llm_gen_source_code)
                    # llm_gen_source_code  = llm_gen_source_code.json()
                    # print('Raw output: \n',llm_gen_source_code)


                    simple_instruction_converter = json.dumps(simple_instruction_converter).encode("utf-8")
                    simple_instruction_converter = requests.post(URL, data=simple_instruction_converter)
                    converted_simple_instruction  = simple_instruction_converter.json()
                    print('Processed Simple instruction Raw output: \n',converted_simple_instruction)
                    print('\nProcessed Simple Instruction: \n', converted_simple_instruction['response'])

                    si_response_code = utils.extract_python_code_from_response(converted_simple_instruction['response'])
                    print("\n\nFirst Generated code: \n", si_response_code)
                
                
                    if si_response_code is not None:
                        regen_response_code = si_response_code
                        if regen_response_code is not None:
                            id=item['id']
                            output_file_path = os.path.join(target_dir, f'si_python_script_{id}.py')
                            utils.save_file(output_file_path, si_response_code)
                except Exception as e:
                    print('\n\nCode generation failed for simple instruction, path of the file:\n', common_data_path)
                    print("Error message: \n", e)

                try:
                    print(f'Processing file: ei_python_script_{ID}.py')
                    users_expert_instruction = ''
                    users_expert_instruction = item['expert_instruction']
                    users_expert_instruction = users_expert_instruction.replace('data.csv', common_data_path)
                    users_expert_instruction = users_expert_instruction.replace('CSV', 'hdf5')
                    users_expert_instruction = users_expert_instruction.replace('columns', 'datasets')
                    users_expert_instruction = users_expert_instruction.replace('column', 'dataset')
                    
                    print('\n\n\nRaw Expert Instruction: \n', item['expert_instruction'])
                    # expert_instruction_converter = requestor.form_request_to_generate_code_from_text(users_expert_instruction, model)
                    data_structure_information, attribute_present, updated_text = corrector.corrector_function_main(users_expert_instruction, common_data_path)
                    print('Data structure information for expert instruction:\n', data_structure_information)
                    # rule based reasoning
                    # expert_instruction_converter = requestor.generate_request_for_generating_source_code_with_data_rule_base_reasoning_copied(users_expert_instruction, data_structure_information, common_data_path, model)
                    
                    # zero-shot COT
                    # expert_instruction_converter = requestor.generate_request_for_generating_source_code_with_zero_shot_CoT_with_corrector(users_expert_instruction, data_structure_information, common_data_path, attribute_present, model)
                    # with updated user quries
                    users_expert_instruction = updated_text

                    expert_instruction_converter = llmRequester.generate_request_for_generating_source_code_separate_prompt_method_with_zero_shot_CoT_with_corrector_step_by_step(users_expert_instruction, data_structure_information, common_data_path, attribute_present, model)
                                            
                    expert_instruction_converter = json.dumps(expert_instruction_converter).encode("utf-8")
                    expert_instruction_converter = requests.post(URL, data=expert_instruction_converter)
                    converted_expert_instruction  = expert_instruction_converter.json()
                    print('Processed Expert instruction Raw output: \n',converted_expert_instruction)
                    print('Processed Expert Instruction: \n',converted_expert_instruction['response'])

                    ei_response_code = utils.extract_python_code_from_response(converted_expert_instruction['response'])
                    print("\n\nFirst Generated code: \n", ei_response_code)
                    if ei_response_code is not None:
                        regen_response_code = ei_response_code
                        if regen_response_code is not None:
                            id=item['id']
                            output_file_path = os.path.join(target_dir, f'ei_python_script_{id}.py')
                            utils.save_file(output_file_path, ei_response_code)
                except Exception as e:
                    print('\n\nCode generation failed for expert instruction, path of the file:\n', common_data_path)
                    print("Error message: \n", e)
                    
            except Exception as e:
                print('\n\nCode generation failed for the file:\n', common_data_path)
                print('Error message: \n', e)

def process_json_iteratively(input_file, target_dir, iteration):
    # Read the JSON file
    with open(input_file, 'r') as infile:
        data = json.load(infile)  # Load the JSON data

    # Process the data (example: convert all strings to uppercase)
    processed_data = []
    for item in data:
        if isinstance(item, dict):  # If the item is a dictionary
            print('Processing file: ', item['id'])
            ID = str(item['id'])
            if ID not in file_list:
                continue            
           
            try:
                print(f'\n\n-----------------------------------------------------------------------------')                
                print(f'Processing file: si_python_script_{ID}.py\n\n')
                # common_data_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/*_h5_data.h5'
                # common_data_path = '/Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/plot_generation/csv_to_h5_data/*_h5_data.h5'
                
                # this is for macbook Me pro
                # base_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'
                
                # this is for gsu server
                base_directory ='/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data'
                common_data_path = base_directory+'/matplot_agent_data/plot_generation/csv_to_h5_data/*_h5_data.h5'
                common_data_path = common_data_path.replace('*', str(item['id']))
                
                try:
                    users_simple_instruction = ''
                    users_simple_instruction=item['simple_instruction']
                    users_simple_instruction = users_simple_instruction.replace('data.csv', common_data_path)
                    users_simple_instruction = users_simple_instruction.replace('CSV', 'hdf5')
                    users_simple_instruction = users_simple_instruction.replace('columns', 'datasets')
                    users_simple_instruction = users_simple_instruction.replace('column', 'dataset')
                    print('\n\nRaw Simple Instruction: \n',  users_simple_instruction)
                    # function returns result, attribute_present, updated_text
                    data_structure_information, attribute_present, updated_text = corrector.corrector_function_main(users_simple_instruction, common_data_path)
                    
                    print('Data structure information for simple instruction:\n', data_structure_information)
                    # simple_instruction_converter = requestor.generate_request_convert_text_input_to_human_generated_and_add_external_data_path(item['simple_instruction'], model)
                    # simple_instruction_converter = requestor.form_request_to_generate_code_from_text(users_simple_instruction, model)
                    # parameters: user_input, data_structure_information, full_data_path, model)
                    # simple_instruction_converter = requestor.generate_request_for_generating_source_code_with_data_rule_base_reasoning_copied(users_simple_instruction, data_structure_information, common_data_path, model)
                    
                    # zero-shot CoT
                    # def generate_request_for_generating_source_code_with_zero_shot_CoT_best_success(user_input, data_structure_information, full_data_path, attribute_present):
                    # simple_instruction_converter = requestor.generate_request_for_generating_source_code_with_zero_shot_CoT_with_corrector(users_simple_instruction, data_structure_information, common_data_path, attribute_present, model)
                    
                    # without using updated text
                    # simple_instruction_converter = llmRequester.generate_request_for_generating_source_code_separate_prompt_method_with_zero_shot_CoT_with_corrector_step_by_step(users_simple_instruction, data_structure_information, common_data_path, attribute_present, model)
                    
                    python_script = ''
                    error_message = ''
                    for iteration in range(1, iteration):
                        # with updated user quries
                        users_simple_instruction = updated_text
                        simple_instruction_converter = llmRequester.generate_request_for_generating_source_code_separate_prompt_method_with_zero_shot_CoT_with_corrector_step_by_step(users_simple_instruction, data_structure_information, common_data_path, attribute_present, model, python_script, error_message)

                        
                        simple_instruction_converter = json.dumps(simple_instruction_converter).encode("utf-8")
                        simple_instruction_converter = requests.post(URL, data=simple_instruction_converter)
                        converted_simple_instruction  = simple_instruction_converter.json()
                        print('Processed Simple instruction Raw output: \n',converted_simple_instruction)
                        print('\nProcessed Simple Instruction: \n', converted_simple_instruction['response'])

                        si_response_code = utils.extract_python_code_from_response(converted_simple_instruction['response'])
                        print("\n\nFirst Generated code: \n", si_response_code)
                        
                        # execute the code if there is no error then break
                        if si_response_code is not None:
                            regen_response_code = si_response_code
                            if regen_response_code is not None:
                                id=item['id']
                                output_file_path = os.path.join(target_dir, f'si_python_script_{id}.py')
                                utils.save_file(output_file_path, si_response_code)
                                
                                # iterative file saving
                                file_name_end = iteration - 1
                                output_file_path_iterative = os.path.join(target_dir, f'si_python_script_{id}_iteration_{file_name_end}.py')
                                utils.save_file(output_file_path_iterative, si_response_code)

                                # now execute the code
                                # need to call the excute result
                                # if no error then break
                                # if error store the error message and read the python_script that should be sent next
                                python_script=si_response_code
                                status, stderr = python_execution_helper.run_python_script_for_evaluation_for_matplot_agent_fastmri_brain(output_file_path)
                                if status=='Pass':
                                    print('Pass')
                                    break
                                else:
                                    print('Fail')
                                    # Parse errors and categorize
                                    if stderr:
                                        print('There is an error: \n', stderr)
                                        print('iterative error resolving with corrector')
                                        error_message=stderr



                except Exception as e:
                    print('\n\nCode generation failed for simple instruction, path of the file:\n', common_data_path)
                    print("Error message: \n", e)

                try:
                    print(f'Processing file: ei_python_script_{ID}.py')
                    users_expert_instruction = ''
                    users_expert_instruction = item['expert_instruction']
                    users_expert_instruction = users_expert_instruction.replace('data.csv', common_data_path)
                    users_expert_instruction = users_expert_instruction.replace('CSV', 'hdf5')
                    users_expert_instruction = users_expert_instruction.replace('columns', 'datasets')
                    users_expert_instruction = users_expert_instruction.replace('column', 'dataset')
                    
                    print('\n\n\nRaw Expert Instruction: \n', item['expert_instruction'])
                    # expert_instruction_converter = requestor.form_request_to_generate_code_from_text(users_expert_instruction, model)
                    data_structure_information, attribute_present, updated_text = corrector.corrector_function_main(users_expert_instruction, common_data_path)
                    print('Data structure information for expert instruction:\n', data_structure_information)
                    # rule based reasoning
                    # expert_instruction_converter = requestor.generate_request_for_generating_source_code_with_data_rule_base_reasoning_copied(users_expert_instruction, data_structure_information, common_data_path, model)
                    
                    # zero-shot COT
                    # expert_instruction_converter = requestor.generate_request_for_generating_source_code_with_zero_shot_CoT_with_corrector(users_expert_instruction, data_structure_information, common_data_path, attribute_present, model)
                    # with updated user quries

                    expert_python_script = ''
                    expert_error_message = ''
                    for step in range(1, iteration):
                        users_expert_instruction = updated_text

                        expert_instruction_converter = llmRequester.generate_request_for_generating_source_code_separate_prompt_method_with_zero_shot_CoT_with_corrector_step_by_step(users_expert_instruction, data_structure_information, common_data_path, attribute_present, model, expert_python_script, expert_error_message)
                                            
                        expert_instruction_converter = json.dumps(expert_instruction_converter).encode("utf-8")
                        expert_instruction_converter = requests.post(URL, data=expert_instruction_converter)
                        converted_expert_instruction  = expert_instruction_converter.json()
                        print('Processed Expert instruction Raw output: \n',converted_expert_instruction)
                        print('Processed Expert Instruction: \n',converted_expert_instruction['response'])

                        ei_response_code = utils.extract_python_code_from_response(converted_expert_instruction['response'])
                        print("\n\nFirst Generated code: \n", ei_response_code)
                        if ei_response_code is not None:
                            regen_response_code = ei_response_code
                            if regen_response_code is not None:
                                id=item['id']
                                output_file_path = os.path.join(target_dir, f'ei_python_script_{id}.py')
                                utils.save_file(output_file_path, ei_response_code)

                                # iterative file saving
                                file_name_end = step - 1
                                output_file_path_iterative = os.path.join(target_dir, f'ei_python_script_{id}_iteration_{file_name_end}.py')
                                utils.save_file(output_file_path_iterative, ei_response_code)

                                expert_python_script=ei_response_code
                                status, stderr = python_execution_helper.run_python_script_for_evaluation_for_matplot_agent_fastmri_brain(output_file_path)
                                if status=='Pass':
                                    print('Pass')
                                    break
                                else:
                                    print('Fail')
                                    # Parse errors and categorize
                                    if stderr:
                                        print('There is an error: \n', stderr)
                                        print('iterative error resolving with corrector')
                                        expert_error_message=stderr
                except Exception as e:
                    print('\n\nCode generation failed for expert instruction, path of the file:\n', common_data_path)
                    print("Error message: \n", e)
                    
            except Exception as e:
                print('\n\nCode generation failed for the file:\n', common_data_path)
                print('Error message: \n', e)
                    
if __name__ == '__main__':
    
    # Create the argument parser
    parser = argparse.ArgumentParser(description = "Select models to use correct LLM model")   

    model, model_name, dataset, is_with_corrector, is_memory, URL = argumentParsar.parse_argument(parser)  
    # Add arguments
    # parser.add_argument("num1", type=float, help="First number")
    # parser.add_argument("num2", type=float, help="Second number")
    # parser.add_argument(
    #     "--model", "-m",
    #     choices=["deepseek-coder-v2", "llama3:70b", "magicoder", "deepseek-r1:latest"],
    #     required=True,
    #     help="Request to send into LLM model"
    # )
    
    # # Parse the arguments
    # args = parser.parse_args()
    # model = ''
    # model_name = ''
    # if args.model == "deepseek-coder-v2":
    #     model = 'deepseek-coder-v2'
    #     model_name = model.replace('-', '_')
        
    # elif args.model == "llama3:70b":
    #     model = 'llama3:70b'
    #     model_name = model.replace(':', '_')
    
    # elif args.model == "magicoder":
    #     model = 'magicoder'
    #     model_name = model
    
    # elif args.model == "deepseek-r1:latest":
    #     model = 'deepseek-r1:latest'
    #     model_name = model.replace('-', '_')
        

    # Usage Example:
    # input_file = '/Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/plot_generation/benchmark_instructions.json'
    
    # this is for macbook pro M3
    # input_file = '/Users/apukumarchakroborti/gsu_research/llam_test/user_queries/manually_edited_user_queries/matplot_agent_datasets/benchmark_instructions.json'
    
    # gsu server path
    # input_file = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/user_queries/manually_edited_user_queries/matplot_agent_datasets/benchmark_instructions.json'
    input_file = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/user_queries/manually_edited_user_queries/matplot_agent_datasets/benchmark_instructions_modified.json'
    # target_dir = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/generated_python_script_replaced_colums_by_datasets'
    # output_file = 'processed_benchmark_instructions.json'
    
    # target_dir = '/Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/plot_generation/python_script_llm/magicoder_zero_shot_CoT_csv_to_h5_with_corrector'
    # target_dir = '/Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/plot_generation/python_script_llm/deepseek_coder_v2_zero_shot_CoT_csv_to_h5_with_corrector'
    # target_dir = '/Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/plot_generation/python_script_llm/llama3_70b_zero_shot_CoT_csv_to_h5_with_corrector'
    # target_dir = f'/Users/apukumarchakroborti/gsu_research/llam_test/matplot_agent_data/plot_generation/python_script_llm/{model_name}_zero_shot_CoT_csv_to_h5_with_corrector'
    
    # This is for the Macbook Pro M3 path
    # target_dir = f'/Users/apukumarchakroborti/gsu_research/llam_test/matplot_agent_data/plot_generation/python_script_llm/{model_name}_zero_shot_CoT_csv_to_h5_with_corrector'

    # GSU server path
    target_dir = f'/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/python_script_llm/{model_name}_zero_shot_CoT_csv_to_h5_with_corrector_modified'
    
    # Create directory if it does not exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if dataset=='MATPLOTAGENT':
        process_json(input_file, target_dir)
    elif dataset=='ITERATIVE_ERROR_RESOLVE_MATPLOTAGENT':
        iteration = 4
        process_json_iteratively(input_file, target_dir, iteration)
