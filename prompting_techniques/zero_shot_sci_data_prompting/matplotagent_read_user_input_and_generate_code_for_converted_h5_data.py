import json
import requests
import os
import argparse
from common_util_script import ArgumentParser as argumentParsar

URL = 'http://ai-lab2.dyn.gsu.edu:11434/api/generate'
# model = 'llama3:latest'
# model = 'deepseek-coder-v2'
# model = 'llama3:70b'
# model = 'magicoder'

# Later the below path will be used: Sigma0_Data/cell_sigma0_hh_fore
# import JsonInputProcessingLLMRequester as requestor

from common_util_script import LLMRequester as llmRequester
# Function to read, process, and save the JSON file
from common_util_script import Utils as utils
import evaluation_error_categorization as python_execution_helper



file_list = ['76', '77', '78', '79', '83', '84', '87', '95', '96', '97', '99', '100']

def process_json(input_file, target_dir, model):
    # Read the JSON file
    with open(input_file, 'r') as infile:
        data = json.load(infile)  # Load the JSON data

    # Process the data (example: convert all strings to uppercase)
    processed_data = []
    for item in data:
        if isinstance(item, dict):  # If the item is a dictionary
            print('Processing file: ', item['id'])
            if str(item['id']) not in file_list:
                continue           
           
            # base_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'
            base_directory ='/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data'
            common_data_path = base_directory+'/matplot_agent_data/plot_generation/csv_to_h5_data/*_h5_data.h5'
            # common_data_path = '/Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/plot_generation/csv_to_h5_data/*_h5_data.h5'
            common_data_path = common_data_path.replace('*', str(item['id']))
            
            users_simple_instruction=item['simple_instruction']
            users_simple_instruction = users_simple_instruction.replace('data.csv', common_data_path)
            users_simple_instruction = users_simple_instruction.replace('CSV', 'hdf5')
            users_simple_instruction = users_simple_instruction.replace('columns', 'datasets')
            users_simple_instruction = users_simple_instruction.replace('column', 'dataset')
            print('\n\nRaw Simple Instruction: \n',  users_simple_instruction)

            
            # simple_instruction_converter = requestor.generate_request_convert_text_input_to_human_generated_and_add_external_data_path(item['simple_instruction'], model)
            # simple_instruction_converter = requestor.form_request_to_generate_code_from_text(users_simple_instruction, model)
            # simple_instruction_converter = requestor.generate_request_for_generating_source_code_with_zero_shot_CoT_without_corrector(users_simple_instruction, common_data_path, model)
            
            simple_instruction_converter = llmRequester.generate_request_for_generating_source_code_with_zero_shot_CoT_without_corrector_step_by_step(users_simple_instruction, common_data_path, model)
            # generate_request_for_generating_source_code_with_zero_shot_CoT_without_corrector_step_by_step(user_input, full_data_path, model)
            # source_code_gen = json.dumps(simple_instruction_converter).encode("utf-8")
            # llm_gen_source_code = requests.post(URL, data=source_code_gen)
            #print(llm_gen_source_code)
            # llm_gen_source_code  = llm_gen_source_code.json()
            # print('Raw output: \n',llm_gen_source_code)


            simple_instruction_converter = json.dumps(simple_instruction_converter).encode("utf-8")
            simple_instruction_converter = requests.post(URL, data=simple_instruction_converter)
            converted_simple_instruction  = simple_instruction_converter.json()
            print('Processed Simple instruction Raw output: \n',converted_simple_instruction)
            print('\nResponse from model for Processed Simple Instruction: \n', converted_simple_instruction['response'])

            si_response_code = utils.extract_python_code_from_response(converted_simple_instruction['response'])
            print("\n\nFirst Generated code: \n", si_response_code)
        
        
            if si_response_code is not None:
                regen_response_code = si_response_code
                if regen_response_code is not None:
                    id=item['id']
                    output_file_path = os.path.join(target_dir, f'si_python_script_{id}.py')
                    utils.save_file(output_file_path, si_response_code)


            users_expert_instruction=item['expert_instruction']
            users_expert_instruction = users_expert_instruction.replace('data.csv', common_data_path)
            users_expert_instruction = users_expert_instruction.replace('CSV', 'hdf5')
            users_expert_instruction = users_expert_instruction.replace('columns', 'datasets')
            users_expert_instruction = users_expert_instruction.replace('column', 'dataset')
            
            print('\n\n\nRaw Expert Instruction: \n', item['expert_instruction'])
            # expert_instruction_converter = requestor.form_request_to_generate_code_from_text(users_expert_instruction, model)
            # expert_instruction_converter = requestor.generate_request_for_generating_source_code_with_zero_shot_CoT_without_corrector(users_expert_instruction, common_data_path, model)
            
            expert_instruction_converter = llmRequester.generate_request_for_generating_source_code_with_zero_shot_CoT_without_corrector_step_by_step(users_expert_instruction, common_data_path, model)


            expert_instruction_converter = json.dumps(expert_instruction_converter).encode("utf-8")
            expert_instruction_converter = requests.post(URL, data=expert_instruction_converter)
            converted_expert_instruction  = expert_instruction_converter.json()
            print('Processed Expert instruction Raw output: \n',converted_expert_instruction)
            print('Response from model for Processed Expert Instruction: \n',converted_expert_instruction['response'])

            ei_response_code = utils.extract_python_code_from_response(converted_expert_instruction['response'])
            print("\n\nFirst Generated code: \n", ei_response_code)
            if ei_response_code is not None:
                regen_response_code = ei_response_code
                if regen_response_code is not None:
                    id=item['id']
                    output_file_path = os.path.join(target_dir, f'ei_python_script_{id}.py')
                    utils.save_file(output_file_path, ei_response_code)


            # processed_data.append({k: v.upper() if isinstance(v, str) else v for k, v in item.items()})
        # else:
            # processed_data.append(item)  # No modification for non-dict items
    
    # Save the processed data into another JSON file
    # with open(output_file, 'w') as outfile:
        # json.dump(processed_data, outfile, indent=4)  # Write the processed data with indent for readability



def process_json_iteratively(input_file, target_dir, model, iteration):
    # Read the JSON file
    with open(input_file, 'r') as infile:
        data = json.load(infile)  # Load the JSON data

    # Process the data (example: convert all strings to uppercase)
    processed_data = []
    for item in data:
        if isinstance(item, dict):  # If the item is a dictionary
            print('Processing file: ', item['id'])
            if str(item['id']) not in file_list:
                continue           
           
            # base_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'
            base_directory ='/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data'
            common_data_path = base_directory+'/matplot_agent_data/plot_generation/csv_to_h5_data/*_h5_data.h5'
            # common_data_path = '/Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/plot_generation/csv_to_h5_data/*_h5_data.h5'
            common_data_path = common_data_path.replace('*', str(item['id']))
            
            users_simple_instruction=item['simple_instruction']
            users_simple_instruction = users_simple_instruction.replace('data.csv', common_data_path)
            users_simple_instruction = users_simple_instruction.replace('CSV', 'hdf5')
            users_simple_instruction = users_simple_instruction.replace('columns', 'datasets')
            users_simple_instruction = users_simple_instruction.replace('column', 'dataset')
            print('\n\nRaw Simple Instruction: \n',  users_simple_instruction)

            
            # simple_instruction_converter = requestor.generate_request_convert_text_input_to_human_generated_and_add_external_data_path(item['simple_instruction'], model)
            # simple_instruction_converter = requestor.form_request_to_generate_code_from_text(users_simple_instruction, model)
            # simple_instruction_converter = requestor.generate_request_for_generating_source_code_with_zero_shot_CoT_without_corrector(users_simple_instruction, common_data_path, model)
            python_script = ''
            error_message = ''
            for iteration in range(1, iteration):
                simple_instruction_converter = llmRequester.generate_request_for_generating_source_code_with_zero_shot_CoT_without_corrector_step_by_step(users_simple_instruction, common_data_path, model)
            # generate_request_for_generating_source_code_with_zero_shot_CoT_without_corrector_step_by_step(user_input, full_data_path, model)
            # source_code_gen = json.dumps(simple_instruction_converter).encode("utf-8")
            # llm_gen_source_code = requests.post(URL, data=source_code_gen)
            #print(llm_gen_source_code)
            # llm_gen_source_code  = llm_gen_source_code.json()
            # print('Raw output: \n',llm_gen_source_code)


                simple_instruction_converter = json.dumps(simple_instruction_converter).encode("utf-8")
                simple_instruction_converter = requests.post(URL, data=simple_instruction_converter)
                converted_simple_instruction  = simple_instruction_converter.json()
                print('Processed Simple instruction Raw output: \n',converted_simple_instruction)
                print('\nResponse from model for Processed Simple Instruction: \n', converted_simple_instruction['response'])

                si_response_code = utils.extract_python_code_from_response(converted_simple_instruction['response'])
                print("\n\nFirst Generated code: \n", si_response_code)
        
        
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


            users_expert_instruction=item['expert_instruction']
            users_expert_instruction = users_expert_instruction.replace('data.csv', common_data_path)
            users_expert_instruction = users_expert_instruction.replace('CSV', 'hdf5')
            users_expert_instruction = users_expert_instruction.replace('columns', 'datasets')
            users_expert_instruction = users_expert_instruction.replace('column', 'dataset')
            
            print('\n\n\nRaw Expert Instruction: \n', item['expert_instruction'])
            # expert_instruction_converter = requestor.form_request_to_generate_code_from_text(users_expert_instruction, model)
            # expert_instruction_converter = requestor.generate_request_for_generating_source_code_with_zero_shot_CoT_without_corrector(users_expert_instruction, common_data_path, model)
            
            expert_instruction_converter = llmRequester.generate_request_for_generating_source_code_with_zero_shot_CoT_without_corrector_step_by_step(users_expert_instruction, common_data_path, model)


            expert_instruction_converter = json.dumps(expert_instruction_converter).encode("utf-8")
            expert_instruction_converter = requests.post(URL, data=expert_instruction_converter)
            converted_expert_instruction  = expert_instruction_converter.json()
            print('Processed Expert instruction Raw output: \n',converted_expert_instruction)
            print('Response from model for Processed Expert Instruction: \n',converted_expert_instruction['response'])

            ei_response_code = utils.extract_python_code_from_response(converted_expert_instruction['response'])
            print("\n\nFirst Generated code: \n", ei_response_code)
            if ei_response_code is not None:
                regen_response_code = ei_response_code
                if regen_response_code is not None:
                    id=item['id']
                    output_file_path = os.path.join(target_dir, f'ei_python_script_{id}.py')
                    utils.save_file(output_file_path, ei_response_code)
if __name__  == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Select models to use correct LLM model")
    
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
    # input_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/benchmark_instructions.json'
    # input_file = '/Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/plot_generation/benchmark_instructions.json'
    # mackbook pro M3
    # input_file = '/Users/apukumarchakroborti/gsu_research/llam_test/user_queries/manually_edited_user_queries/matplot_agent_datasets/benchmark_instructions.json'

    # gsu server
    # input_file = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/user_queries/manually_edited_user_queries/matplot_agent_datasets/benchmark_instructions.json'
    input_file = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/user_queries/manually_edited_user_queries/matplot_agent_datasets/benchmark_instructions_modified.json'
    # target_dir = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/generated_python_script_replaced_colums_by_datasets'
    # target_dir = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/python_script_llm/deepseek_coder_v2_generated_python_script_for_hdf5'
    # output_file = 'processed_benchmark_instructions.json'

    # target_dir = '/Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/plot_generation/python_script_llm/llama_70b_zero_shot_CoT_csv_to_h5_without_corrector'
    # target_dir = '/Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/plot_generation/python_script_llm/magicoder_zero_shot_CoT_csv_to_h5_without_corrector'
    # target_dir = '/Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/plot_generation/python_script_llm/deepseek_coder_v2_zero_shot_CoT_csv_to_h5_without_corrector'
    # target_dir = f'/Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/plot_generation/python_script_llm/{model_name}_zero_shot_CoT_csv_to_h5_without_corrector'
    
    # target_dir = f'/Users/apukumarchakroborti/gsu_research/llam_test/matplot_agent_data/plot_generation/python_script_llm/{model_name}_zero_shot_CoT_csv_to_h5_without_corrector'
    target_dir = f'/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/matplot_agent_data/plot_generation/python_script_llm/{model_name}_zero_shot_CoT_csv_to_h5_without_corrector_modified'
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if dataset=='MATPLOTAGENT':
        process_json(input_file, target_dir, model)
    elif dataset=='ITERATIVE_ERROR_RESOLVE_MATPLOTAGENT':
        iteration = 4
        process_json_iteratively(input_file, target_dir, model, iteration)

# magicoder_zero_shot_CoT_csv_to_h5_without_corrector
# llama3_70b_zero_shot_CoT_csv_to_h5_without_corrector
# deepseek_coder_v2_zero_shot_CoT_csv_to_h5_without_corrector
# deepseek_r1_70b_zero_shot_CoT_csv_to_h5_without_corrector
