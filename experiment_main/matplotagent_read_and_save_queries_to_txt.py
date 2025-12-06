import json
import os
from common_util_script import Utils as utils

file_list = ['76', '77', '78', '79', '83', '84', '87', '95', '96', '97', '99', '100']

input_file = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/user_queries/manually_edited_user_queries/matplot_agent_datasets/benchmark_instructions_modified.json'

with open(input_file, 'r') as infile:
    data = json.load(infile)  # Load the JSON data


for item in data:
    if isinstance(item, dict):  # If the item is a dictionary
        print('\n\nProcessing file: ', item['id'])
        ID = str(item['id'])
        if ID not in file_list:
            continue

        # save simple instructions
        users_simple_instruction = item['simple_instruction']
        print(f'Simple queries: {users_simple_instruction}')
        target_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/user_queries/generated_user_queries/matplotagent/simple_queries'
        output_file_path = os.path.join(target_dir, f'{ID}_simple_instruction.txt')
        utils.save_file(output_file_path, users_simple_instruction) 

        # save expert instructions
        users_simple_instruction = item['expert_instruction']
        print(f'Expert queries: {users_simple_instruction}')
        target_dir = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/user_queries/generated_user_queries/matplotagent/expert_queries'
        output_file_path = os.path.join(target_dir, f'{ID}_expert_instruction.txt')
        utils.save_file(output_file_path, users_simple_instruction) 