import requests
import json
import os
import glob

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

def generate_request_for_generating_source_code(sample, model="llama3:70b"):
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
input_directory = '/Users/lwan/Research/data/hdf-eos/ges-disc/llm_gen_description/multi-runs'
input_file_pattern = '*.txt'
input_file_path_pattern = os.path.join(input_directory, input_file_pattern)
input_file_paths = glob.glob(input_file_path_pattern)

#output_directory = '/Users/lwan/Research/data/hdf-eos/ges-disc/llm_gen_scripts'
output_directory = '/Users/lwan/Research/data/hdf-eos/ges-disc/llm_gen_scripts/multi-runs-llama3'

for input_file_path in input_file_paths:
    
    input_file_name = os.path.basename(input_file_path)
        
    print(input_file_name)
    
    output_file_path = os.path.join(output_directory, input_file_name+'_code_gen.py')
    
    #if file_name != "BUV_Nimbus04_L3zm_v01_00_2012m0203t144121_h5.py_code_description.txt":
    #    continue
    
    with open(input_file_path, "r") as f:
        llm_gen_description = f.read()
    print(llm_gen_description)
    
    source_code_gen = generate_request_for_generating_source_code(llm_gen_description, "llama3:70b")
    source_code_gen = json.dumps(source_code_gen).encode("utf-8")
    llm_gen_source_code = requests.post(URL, data=source_code_gen)
    #print(llm_gen_source_code)
    llm_gen_source_code  = llm_gen_source_code.json()
    #print(llm_gen_source_code)
    print(llm_gen_source_code['response'])
    
    start_delim_1 = "```python\n"
    start_delim_2 = "```Python\n"
    start_delim_3 = "```\n"
    end_delim = "```"

    result_1 = extract_substring(llm_gen_source_code['response'], start_delim_1, end_delim)
    result_2 = extract_substring(llm_gen_source_code['response'], start_delim_2, end_delim)
    result_3 = extract_substring(llm_gen_source_code['response'], start_delim_3, end_delim)
    
    
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
