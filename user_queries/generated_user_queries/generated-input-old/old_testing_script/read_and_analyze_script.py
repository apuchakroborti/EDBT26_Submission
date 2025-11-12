import requests
import json
import os
import glob
import random

URL = 'http://ai-lab2.dyn.gsu.edu:11434/api/generate'

def generate_request_for_describing_source_code(sample, seed, model="llama3:70b"):
    s = "Explain the following python code step-by-step: \n" + sample + "\n Include as many implementation details as possible. \n Keep names of all parent groups of each dataset so that each dataset can be identified within the HDF5 hierarchy."
    data = {
        "model": model,
        "prompt": s,
        "stream": False,
        "options": {
            "seed": seed,
            "temperature": 0.5
        }
    }
    return data

def generate_request_for_condensing_description_20_percent(sample, seed, model="llama3:70b"):
    s = "Reduce 20% of the text in the following description while keeping as many implementation details as possible: \n" + sample + "\n Keep names of all parent groups of each dataset so that each dataset can be identified within the HDF5 hierarchy."
    data = {
        "model": model,
        "prompt": s,
        "stream": False,
        "options": {
            "seed": seed,
            "temperature": 0.5
        }
    }
    return data

# input_directory = '/Users/lwan/Research/data/hdf-eos/ges-disc/scripts'
#input_directory = '/Users/lwan/Research/data/hdf-eos/ges-disc/scripts/tmp'
# Question: scripts means referring this same file or not?
# input_directory = 'C:\\Users\\apuhu\\research\\data_llm'
# input_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/LaRC'
input_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/ASF'

input_file_pattern = '*.py'
input_file_path_pattern = os.path.join(input_directory, input_file_pattern)
input_file_paths = glob.glob(input_file_path_pattern)


# output_directory = '/Users/lwan/Research/data/hdf-eos/ges-disc/llm_gen_description/multi-runs'
# output_directory ='/Users/apukumarchakroborti/gsu_research/server/llam_test_output'
output_directory ='/Users/apukumarchakroborti/gsu_research/llam_test/llam_test_output'
# output_file_path = output_directory+"/output.txt"
output_file_path = output_directory
print("APU: start")
for input_file_path in input_file_paths:

    with open(input_file_path, "r") as f:
        original_source_code = f.read()
    print(original_source_code)
    
    file_name = os.path.basename(input_file_path)
    for run in range(10):
        
        seed = random.randint(1, 20000)
        code_description_gen = generate_request_for_describing_source_code(original_source_code, seed, "llama3:70b")
        code_description_gen = json.dumps(code_description_gen).encode("utf-8")
        code_description = requests.post(URL, data=code_description_gen)
        code_description  = code_description.json()
        
        seed = random.randint(1, 20000)
        condensed_code_description_gen = generate_request_for_condensing_description_20_percent(code_description['response'], seed, "llama3:70b")
        condensed_code_description_gen = json.dumps(condensed_code_description_gen).encode("utf-8")
        condensed_code_description = requests.post(URL, data=condensed_code_description_gen)
        condensed_code_description  = condensed_code_description.json()
    
        with open(output_file_path+f"/{file_name}_output.txt", 'w') as f:
            f.write(str(condensed_code_description['response']) + '\n')