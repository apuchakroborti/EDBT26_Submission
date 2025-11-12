import json
import requests
URL = 'http://ai-lab2.dyn.gsu.edu:11434/api/generate'
model = 'llama3:latest'
# Later the below path will be used: Sigma0_Data/cell_sigma0_hh_fore
import sci_data_prompting.JsonInputProcessingLLMRequester as requestor
# Function to read, process, and save the JSON file
def process_json(input_file, output_file):
    # Read the JSON file
    with open(input_file, 'r') as infile:
        data = json.load(infile)  # Load the JSON data

    # Process the data (example: convert all strings to uppercase)
    processed_data = []
    for item in data:
        if isinstance(item, dict):  # If the item is a dictionary
            print('\n\nRaw Simple Instruction: \n', item['simple_instruction'])
            simple_instruction_converter = requestor.generate_request_convert_text_input_to_human_generated_and_add_external_data_path(item['simple_instruction'], model)
            
            simple_instruction_converter = json.dumps(simple_instruction_converter).encode("utf-8")
            simple_instruction_converter = requests.post(URL, data=simple_instruction_converter)
            converted_simple_instruction  = simple_instruction_converter.json()
            print('Processed Simple instruction Raw output: \n',converted_simple_instruction)
            print('\nProcessed Simple Instruction: \n', converted_simple_instruction['response'])


            print('\n\n\nRaw Expert Instruction: \n', item['expert_instruction'])
            expert_instruction_converter = requestor.generate_request_convert_text_input_to_human_generated_and_add_external_data_path(item['expert_instruction'], model)
            expert_instruction_converter = json.dumps(expert_instruction_converter).encode("utf-8")
            expert_instruction_converter = requests.post(URL, data=expert_instruction_converter)
            converted_expert_instruction  = expert_instruction_converter.json()
            print('Processed Expert instruction Raw output: \n',converted_expert_instruction)
            print('Processed Expert Instruction: \n',converted_expert_instruction['response'])


            # processed_data.append({k: v.upper() if isinstance(v, str) else v for k, v in item.items()})
        # else:
            # processed_data.append(item)  # No modification for non-dict items
    
    # Save the processed data into another JSON file
    # with open(output_file, 'w') as outfile:
        # json.dump(processed_data, outfile, indent=4)  # Write the processed data with indent for readability

# Usage Example:
input_file = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/benchmark_instructions.json'
output_file = 'processed_benchmark_instructions.json'
process_json(input_file, output_file)
