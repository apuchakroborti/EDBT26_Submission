Python scripts that have subarray access
/ACL_DIRS/GES_DISC/python_script/acos_L2s_110101_02_Production_v201201_L2Sub7309_r01_PolB_161206183303.h5.py
/ACL_DIRS/GES_DISC/python_script/BUV_Nimbus04_L3zm_v01_00_2012m0203t144121_h5.py
/ACL_DIRS/GES_DISC/python_script/GSSTF_3_2008_12_31.py
/ACL_DIRS/GES_DISC/python_script/GSSTF_NCEP_3_2008_12_31.py
/ACL_DIRS/GES_DISC/python_script/GSSTFYC_3_Year_1998_2008.py
/ACL_DIRS/GES_DISC/python_script/HIRDLS-Aura_L2_v07-00-20-c01_2008d077.he5.py
/ACL_DIRS/GES_DISC/python_script/HIRDLS-Aura_L3ZFCNO2_v07-00-20-c01_2005d022-2008d077.he5.py
/ACL_DIRS/GES_DISC/python_script/MLS-Aura_L2GP-BrO_v04-23-c03_2016d302.he5.py
/ACL_DIRS/GES_DISC/python_script/MLS-Aura_L2GP-O3_v04-23-c02_2019d001.he5.py
/ACL_DIRS/GES_DISC/python_script/oco2_L2StdND_03949a_150330_B8100r_170916014809.h5.py
/ACL_DIRS/LaRC/python_script/CAL_LID_L2_BlowingSnow_Antarctica-Standard-V2-00.2023-06.hdf5.py
/ACL_DIRS/LaRC/python_script/CATS-ISS_L2O_D-M7.2-V2-01_05kmLay.2017-05-01T00-47-40T01-28-41UTC.hdf5.py
/ACL_DIRS/LaRC/python_script/MOP02J-20131129-L2V19.9.3.he5.py
code-generation-by-llm-for-scientific-data/ACL_DIRS/LaRC/python_script/MOP02N-20180311-L2V19.9.2.he5.py
code-generation-by-llm-for-scientific-data/ACL_DIRS/LaRC/python_script/TES-Aura_L2-O3-Nadir_r0000002433_F08_12.he5.py
code-generation-by-llm-for-scientific-data/ACL_DIRS/LP_DAAC/python_script/AG100.v003.64.-089.0001.h5.py


To run a model
---------------------
$ ollama run llama3:70
$ ollama run magicoder
$ ollama run deepseek-r1:70b
$ ollama run deepseek-coder-v2

To stop a model
---------------
$ ollama stop llama3:70
$ ollama stop magicoder
$ ollama stop deepseek-r1:70b
$ ollama stop deepseek-coder-v2

Generate User queries:
$ python3 generate_human_like_description_from_py_script.py > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/utility_related_python_scripts/human_like_text_generation_from_python_script/output_logs/generated_expert_user_queries_from_deepseek_r1_70b.log

$ python3 generate_human_like_description_from_py_script.py > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/utility_related_python_scripts/human_like_text_generation_from_python_script/output_logs/generated_expert_user_queries_from_llama3_70b.log

MATPLOTAGENT datasets: To run the function to generate python code with corrector function for the csv to converted h5 data
$ cd /Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/zero_shot_sci_data_prompting

$ python3 read_user_input_and_generate_code_for_converted_h5_data_with_corrector.py --dataset MATPLOTAGENT --model magicoder > /Users/apukumarchakroborti/gsu_research/llam_test/matplot_agent_data/plot_generation/output_logs/magicoder_final_with_corrector.log

$ python3 read_user_input_and_generate_code_for_converted_h5_data_with_corrector.py --dataset MATPLOTAGENT --model llama3:70b > /Users/apukumarchakroborti/gsu_research/llam_test/matplot_agent_data/plot_generation/output_logs/llama3_70b_final_with_corrector.log

$ python3 read_user_input_and_generate_code_for_converted_h5_data_with_corrector.py --dataset MATPLOTAGENT --model deepseek-coder-v2 > /Users/apukumarchakroborti/gsu_research/llam_test/matplot_agent_data/plot_generation/output_logs/deepseek_coder_v2_final_with_corrector.log

$ python3 read_user_input_and_generate_code_for_converted_h5_data_with_corrector.py --dataset MATPLOTAGENT --model deepseek-r1:70b > /Users/apukumarchakroborti/gsu_research/llam_test/matplot_agent_data/plot_generation/output_logs/deepseek_r1_70b_final_with_corrector.log

MATPLOTAGENT datasets: To run the function to generate python code without corrector function for the csv to converted h5 data
$ cd /Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/zero_shot_sci_data_prompting

$ python3 read_user_input_and_generate_code_for_converted_h5_data.py --dataset MATPLOTAGENT --model magicoder > /Users/apukumarchakroborti/gsu_research/llam_test/matplot_agent_data/plot_generation/output_logs/magicoder_final_without_corrector.log

$ python3 read_user_input_and_generate_code_for_converted_h5_data.py --dataset MATPLOTAGENT --model llama3:70b > /Users/apukumarchakroborti/gsu_research/llam_test/matplot_agent_data/plot_generation/output_logs/llama3_70b_final_without_corrector.log

$ python3 read_user_input_and_generate_code_for_converted_h5_data.py --dataset MATPLOTAGENT --model deepseek-coder-v2 > /Users/apukumarchakroborti/gsu_research/llam_test/matplot_agent_data/plot_generation/output_logs/deepseek_coder_v2_without_corrector.log

$ python3 read_user_input_and_generate_code_for_converted_h5_data.py --dataset MATPLOTAGENT --model deepseek-r1:70b > /Users/apukumarchakroborti/gsu_research/llam_test/matplot_agent_data/plot_generation/output_logs/deepseek_r1_70b_final_with_corrector.log

FASTMRIBRAIN datasets: code generation:
Normal queries without intent generation

With corrector $ python3 sci_data_prompting_main.py --model magicoder --d FASTMRIBRAIN -c True > /Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/output_logs/magicoder_fast_mri_final_code_generation.log

$ python3 sci_data_prompting_main.py --model deepseek-coder-v2 --d FASTMRIBRAIN -c True > /Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/output_logs/deepseek_coder_v2_fast_mri_final_code_generation.log

$ python3 sci_data_prompting_main.py --model llama3:70b --dataset FASTMRIBRAIN -c True > /Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/output_logs/llama3_70b_fast_mri_final_code_generation.log

$ python3 sci_data_prompting_main.py --model deepseek-r1:70b --dataset FASTMRIBRAIN -c True > /Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/output_logs/deepseek_r1_70b_final_code_generation.log

Without corrector
$ python3 sci_data_prompting_main.py --model magicoder --dataset FASTMRIBRAIN > /Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/output_logs/magicoder_fast_mri_normal_code_generation_without_corrector.log

$ python3 sci_data_prompting_main.py --model deepseek-coder-v2 --dataset FASTMRIBRAIN > /Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/output_logs/deepseek_coder_v2_fast_mri_normal_code_generation_without_corrector.log

$ python3 sci_data_prompting_main.py --model llama3:70b --dataset FASTMRIBRAIN > /Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/output_logs/llama3_70b_fast_mri_normal_code_generation_without_corrector.log

$ python3 sci_data_prompting_main.py --model deepseek-r1:70b --dataset FASTMRIBRAIN > /Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/output_logs/deepseek_r1_70b_final_code_generation.log

CLIMATE datasets: code generation:
Normal queries without intent generation With corrector

$ python3 sci_data_prompting_main.py --model magicoder --d CLIMATE -c True > /Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/zero_shot_sci_data_prompting/output_logs/magicoder_climate_final_code_generation.log

$ python3 sci_data_prompting_main.py --model deepseek-coder-v2 --d CLIMATE -c True > /Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/zero_shot_sci_data_prompting/output_logs/deepseek_coder_v2_climate_final_code_generation.log

$ python3 sci_data_prompting_main.py --model llama3:70b --dataset CLIMATE -c True > /Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/zero_shot_sci_data_prompting/output_logs/llama3_70b_climate_final_code_generation.log

$ python3 sci_data_prompting_main.py --model deepseek-r1:70b --dataset CLIMATE -c True > /Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/zero_shot_sci_data_prompting/output_logs/deepseek_r1_70b_final_code_generation.log

With memory
$ python3 sci_data_prompting_main.py --model deepseek-r1:70b --dataset CLIMATE -c True -mem True > /Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/zero_shot_sci_data_prompting/output_logs/deepseek_r1_70b_zero_shot_CoT_with_corrector_final_with_memory_dataset_attribute_shape.log

For VM, with memory
------------------------
$ python3 sci_data_prompting_main.py --model deepseek-r1:70b --dataset CLIMATE -c True -mem True > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs/deepseek_r1_70b_zero_shot_CoT_with_corrector_final_with_memory_dataset_attribute_shape.log

$ python3 sci_data_prompting_main.py --model magicoder --dataset CLIMATE -c True -mem True > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs/magicoder_zero_shot_CoT_with_corrector_final_with_memory_dataset_attribute_shape.log

$ python3 sci_data_prompting_main.py --model llama3:70b --dataset CLIMATE -c True -mem True > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs/llama3_70b_zero_shot_CoT_with_corrector_final_with_memory_dataset_attribute_shape.log

$ python3 sci_data_prompting_main.py --model deepseek-coder-v2 --dataset CLIMATE -c True -mem True > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs/deepseek_coder_v2_zero_shot_CoT_with_corrector_final_with_memory_dataset_attribute_shape.log



Without corrector
$ python3 sci_data_prompting_main.py --model magicoder --dataset CLIMATE > /Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/zero_shot_sci_data_prompting/output_logs/magicoder_climate_final_code_generation_without_corrector.log

$ python3 sci_data_prompting_main.py --model deepseek-coder-v2 --dataset CLIMATE > /Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/zero_shot_sci_data_prompting/output_logs/deepseek_coder_v2_climate_final_code_generation_without_corrector.log

$ python3 sci_data_prompting_main.py --model llama3:70b --dataset CLIMATE > /Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/zero_shot_sci_data_prompting/output_logs/llama3_70b_climate_final_code_generation_without_corrector.log

$ python3 sci_data_prompting_main.py --model deepseek-r1:70b --dataset CLIMATE > /Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/zero_shot_sci_data_prompting/output_logs/deepseek_r1_70b_climate_final_code_generation_without_corrector.log

Bargraph generation:
$ cd /Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/graph_generation_with_label_mapping

$ python3 deepseek_coder_v2_climate_datasets_bargraph_generation.py $ python3 deepseek_coder_v2_csv_to_h5_datasets_bargraph_generation.py $ python3 deepseek_coder_v2_fast_mri_datasets_bargraph_generation.py

$ python3 llama3_70b_climate_datasets_bargraph_generation.py $ python3 llama3_70b_csv_to_h5_datasets_bargraph_generation.py $ python3 llama3_70b_fast_mri_datasets_bargraph_generation.py

$ python3 magicoder_climate_datasets_bargraph_generation.py $ python3 magicoder_csv_to_h5_datasets_bargraph_generation.py $ python3 magicoder_fast_mri_brain_datasets_bargraph_generation.py

--------------------Error categorization------------------------------------- With corrector 
$ python3 evaluation_error_categorization.py --model deepseek-r1:70b --dataset CLIMATE -c True -mem True > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs/deepseek_r1_70b_error_categorization_with_corrector_final_with_memory_dataset_attribute_shape.log

$ python3 evaluation_error_categorization.py --model magicoder --dataset CLIMATE -c True -mem True > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs/magicoder_error_categorization_with_corrector_final_with_memory_dataset_attribute_shape.log

$ python3 evaluation_error_categorization.py --model llama3:70b --dataset CLIMATE -c True -mem True > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs/llama3_70b_error_categorization_with_corrector_final_with_memory_dataset_attribute_shape.log



$ python3 evaluation_error_categorization.py --model magicoder --dataset FAST_MRI_BRAIN -c True > ./fast_mri_brain_error_categorization_report/magicoder_fast_mri_normal_error_categorization_with_corrector.log 

$ python3 evaluation_error_categorization.py --model deepseek-coder-v2 --dataset FAST_MRI_BRAIN -c True > ./fast_mri_brain_error_categorization_report/deepseek_coder_v2_fast_mri_normal_error_categorization_with_corrector.log $ python3 evaluation_error_categorization.py --model llama3:70b --dataset FAST_MRI_BRAIN -c True > ./fast_mri_brain_error_categorization_report/llama3_70b_fast_mri_normal_error_categorization_with_corrector.log 

$ python3 evaluation_error_categorization.py --model deepseek-r1:70b --dataset CLIMATE > /Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/zero_shot_sci_data_prompting/output_logs/deepseek_r1_70b_error_categorization_with_corrector.log

Without corrector $ python3 evaluation_error_categorization.py --model magicoder --dataset FAST_MRI_BRAIN > ./fast_mri_brain_error_categorization_report/magicoder_fast_mri_normal_error_categorization_without_corrector.log $ python3 evaluation_error_categorization.py --model deepseek-coder-v2 --dataset FAST_MRI_BRAIN > ./fast_mri_brain_error_categorization_report/deepseek_coder_v2_fast_mri_normal_error_categorization_without_corrector.log $ python3 evaluation_error_categorization.py --model llama3:70b --dataset FAST_MRI_BRAIN > ./fast_mri_brain_error_categorization_report/llama3_70b_fast_mri_normal_error_categorization_without_corrector.log

With user intent generation $ python3 sci_data_prompting_main.py --model magicoder --dataset FAST_MRI_BRAIN_WITH_USER_INTENT > ./fast_mri_dataset_output_logs/magicoder_fast_mri_code_generation.log $ python3 sci_data_prompting_main.py --model deepseek-coder-v2 --dataset FAST_MRI_BRAIN_WITH_USER_INTENT > ./fast_mri_dataset_output_logs/deepseek_coder_v2_fast_mri_code_generation.log $ python3 sci_data_prompting_main.py --model llama3:70b --dataset FAST_MRI_BRAIN_WITH_USER_INTENT > ./fast_mri_dataset_output_logs/llama3_70b_fast_mri_code_generation.log

$ python3 sci_data_prompting_main.py --model magicoder --dataset USER_INTENT_GENERATION_FROM_FAST_MRI_BRAIN_RELATED_QUERIES > ./fast_mri_dataset_output_logs/magicoder_user_intent_generation.log $ python3 sci_data_prompting_main.py --model deepseek-coder-v2 --dataset USER_INTENT_GENERATION_FROM_FAST_MRI_BRAIN_RELATED_QUERIES > ./fast_mri_dataset_output_logs/magicoder_user_intent_generation.log $ python3 sci_data_prompting_main.py --model llama3:70b --dataset USER_INTENT_GENERATION_FROM_FAST_MRI_BRAIN_RELATED_QUERIES > ./fast_mri_dataset_output_logs/magicoder_user_intent_generation.log

Command for generation code: $ python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py > ./prompting_techniques/zero_shot_sci_data_prompting/output_logs/startcoder2_15b_zero_shot_CoT_without_corrector_resolving_errors.log

Error categorization $ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py > ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization_logs/codellama_34b_zero_shot_CoT_with_corrector_resolving_errors.log

Evaluation categorization
Without corrector -->

$ python3 evaluation_error_categorization.py --model magicoder --d MATPLOT_AGENT -c False > ../plot_generation/evaluation_csv_to_h5_logs/magicoder_zero_shot_CoT_csv_to_h5_without_corrector.log

$ python3 evaluation_error_categorization.py --model llama3:70b --d MATPLOT_AGENT -c False > ../plot_generation/evaluation_csv_to_h5_logs/llama3_70b_zero_shot_CoT_csv_to_h5_without_corrector.log

$ python3 evaluation_error_categorization.py --model deepseek-coder-v2 --d MATPLOT_AGENT -c False > ../plot_generation/evaluation_csv_to_h5_logs/deepseek_coder_v2_zero_shot_CoT_csv_to_h5_without_corrector.log

With corrector --> $ python3 evaluation_error_categorization.py --model magicoder --d MATPLOT_AGENT -c True > ../plot_generation/evaluation_csv_to_h5_logs/magicoder_zero_shot_CoT_csv_to_h5_without_corrector.log

$ python3 evaluation_error_categorization.py --model llama3:70b --d MATPLOT_AGENT -c True > ../plot_generation/evaluation_csv_to_h5_logs/llama3_70b_zero_shot_CoT_csv_to_h5_without_corrector.log

$ python3 evaluation_error_categorization.py --model deepseek-coder-v2 --d MATPLOT_AGENT -c True > ../plot_generation/evaluation_csv_to_h5_logs/deepseek_coder_v2_zero_shot_CoT_csv_to_h5_without_corrector.log

$ python3 evaluation_error_categorization.py > ../plot_generation/evaluation_csv_to_h5_logs/magicoder_zero_shot_CoT_csv_to_h5_with_corrector.log $ python3 evaluation_error_categorization.py > ../plot_generation/evaluation_csv_to_h5_logs/magicoder_zero_shot_CoT_csv_to_h5_without_corrector.log

Future Work
Let's imagine we have a lot of hdf5, h5, or he5 data and based on the data we have to generate some python codes that will read data from the scientific data file and visualize the data automatically.

Specific Task: For example we have: A scientifica data file --> read the data file and store the metadata and dataset's paths and attributes into a text file
And User query --> based on the user query data we have to fetch the paths and attribute's paths as data that are described in the user query as a free text

Challenges to the LLM:

LLM can't read the tokens beyond it's limit, so passing all paths from the data file won't produce any good result: Need to find the research paper where described the updated version of input tokens to LLMs, where LLMs can read much words without hallucinations
Research problems: Need to find an algorithm by using that we can form the dataset paths specifically to pass it to the LLM model

Existing methods:

How to select existing methods:

Choosing the Right Algorithm
Simple typos or short strings: Levenshtein, Damerau-Levenshtein.
Names or records: Soundex, Metaphone, Jaro-Winkler.
Text comparison: TF-IDF + Cosine Similarity, BERT embeddings.
Large datasets or near-duplicates: SimHash, MinHash.
Ordered sequences: Longest Common Subsequence.