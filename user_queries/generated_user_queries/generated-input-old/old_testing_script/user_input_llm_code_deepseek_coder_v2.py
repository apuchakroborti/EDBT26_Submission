import requests
import json
import os
# import glob

URL = 'http://ai-lab2.dyn.gsu.edu:11434/api/generate'

def extract_substring(text, start_delim, end_delim):
    start_idx = text.find(start_delim)
    if start_idx == -1:
        return None
    
    start_idx += len(start_delim)
    end_idx = text.find(end_delim, start_idx)
    if end_idx == -1:
        return None
    
    return text[start_idx:end_idx]

def generate_request_for_generating_source_code(sample, model="deepseek-coder-v2"):
    s = "Generate the python code based on the following description: \n" + sample + "\n Make sure the input file can be specified as a command line parameter by importing and utilizing the sys module."
    data = {
        "model": model,
        "prompt": s,
        "stream": False,
        "options": {
            "seed": 12344,
            "temperature": 0.0
        }
    }
    return data

#input_directory = '/Users/lwan/Research/data/hdf-eos/ges-disc/llm_gen_description'
# input_directory = '/Users/lwan/Research/data/hdf-eos/ges-disc/llm_gen_description/multi-runs'
input_directory = '/Users/apukumarchakroborti/gsu_research/llam_test'
# input_file_pattern = '*.txt'
# input_file_pattern = 'TES-Aura_L2-O3-Nadir_r0000002433_F08_12.he5.py_output.txt'
# input_file_pattern = 'TES-Aura_L2-O3-Nadir_r0000002433_F08_12.he5.py_output_with_path.txt'
# input_file_path_pattern = os.path.join(input_directory, input_file_pattern)
# input_file_paths = glob.glob(input_file_path_pattern)

#output_directory = '/Users/lwan/Research/data/hdf-eos/ges-disc/llm_gen_scripts'
# output_directory = '/Users/lwan/Research/data/hdf-eos/ges-disc/llm_gen_scripts/multi-runs-llama3'
output_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/des_to_code_by_deek_seek_code_v2'


# Open the file in read mode
with open(f'{input_directory}/input_examples_deek_seek_coder_v2.txt', 'r') as file:
    # Read each line from the file
    file_num=1
    for line in file:
        # Print the line, strip() removes any leading/trailing whitespaces or newline characters
        print(line.strip())
        
        source_code_gen = generate_request_for_generating_source_code(line, "deepseek-coder-v2")
        source_code_gen = json.dumps(source_code_gen).encode("utf-8")
        llm_gen_source_code = requests.post(URL, data=source_code_gen)
        #print(llm_gen_source_code)
        llm_gen_source_code  = llm_gen_source_code.json()
        print('Raw output ', llm_gen_source_code)
        #print(llm_gen_source_code)
        print(llm_gen_source_code['response'])
        
        start_delim_1 = "```python\n"
        start_delim_2 = "```Python\n"
        start_delim_3 = "```\n"
        end_delim = "```"

        result_1 = extract_substring(llm_gen_source_code['response'], start_delim_1, end_delim)
        result_2 = extract_substring(llm_gen_source_code['response'], start_delim_2, end_delim)
        result_3 = extract_substring(llm_gen_source_code['response'], start_delim_3, end_delim)
        
        
        output_file_path = os.path.join(output_directory, f'code_deep_seek_coder_v2_{file_num}.py')
        file_num+=1
        
        if result_1:
            #print(result)
            with open(output_file_path, 'w') as f:
                f.write(result_1)
        elif result_2:
            with open(output_file_path, 'w') as f:
                f.write(result_2)
        elif result_3:
            with open(output_file_path, 'w') as f:
                f.write(result_3)
        else:
            print("source code not found")
