URLS Used for the RAG source
Basemap:
1. https://matplotlib.org/basemap/stable/users/mapsetup.html
2. https://matplotlib.org/basemap/stable/users/examples.html

Cartopy:
1. https://cartopy-pelson.readthedocs.io/en/readthedocs/matplotlib/intro.html
2. https://cartopy-pelson.readthedocs.io/en/readthedocs/crs/projections.html#cartopy-projections


<!-- To run an ollama model -->
$ ollama run llama3:70 
$ ollama run magicoder 
$ ollama run deepseek-r1:70b 
$ ollama run deepseek-coder-v2
$ ollama run gemma3:27b
$ ollama run devstral:24b

<!-- To stop an ollama model -->
$ ollama stop llama3:70 
$ ollama stop magicoder 
$ ollama stop deepseek-r1:70b 
$ ollama stop deepseek-coder-v2
$ ollama stop gemma3:27b
$ ollama stop devstral:24b
<!-- with time recording -->
<!-- expert queries:: devstral:24b with corrector and with rag: done  -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/devstral_24b_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'

% <!-- expert queries:: deepseek-r1:32b with corrector and with rag: done  -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/deepseek_32b_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'

<!-- expert queries:: llama3:70b with corrector and with rag: done -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model llama3:70b --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/llama3_70b_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'

% <!-- expert queries:: magicoder with corrector and with rag: done -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model magicoder --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/magicoder_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'

<!-- expert queries:: gemma3:27b with corrector and with rag: done-->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gemma3:27b --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/gemma3_27b_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'


<!-- ITERATIVE_ERROR_RESOLVE_CLIMATE -->
% devstral:24b done
<!-- expert queries:: with corrector and with rag: done -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True -os True -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/devstral_24b_user_iterative_error_resolve_python_script_generation.log 2>&1'

% expert queries:: without rag and without corrector: done
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/devstral_24b_user_iterative_error_resolve_python_script_generation_expert_without_rag_without_corrector.log 2>&1'

<!-- expert queries:: without rag and with corrector: done -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/devstral_24b_user_iterative_error_resolve_python_script_generation_without_rag_with_corrector.log 2>&1'

<!-- expert queries:: with rag and without corrector: done -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/devstral_24b_user_iterative_error_resolve_python_script_generation_with_rag_without_corrector.log 2>&1'

% SIMPLE QUERIES
% simple queries:: with rag and with corrector--> done
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True --errors True -os True -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/devstral_24b_user_iterative_error_resolve_python_script_generation_with_errors.log 2>&1'

<!-- % simple queries:: without corrector and without rag: done--> 
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True  -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/devstral_24b_user_iterative_error_resolve_python_script_generation_with_error_without_corrector_without_rag.log 2>&1'

% simple queries:: with rag and without corrector: done-->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True --errors True -os True -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/devstral_24b_user_iterative_error_resolve_python_script_generation_with_errors.log 2>&1'

<!-- % simple queries:: with rag and without corrector: done--> -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --rag True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/devstral_24b_user_iterative_error_resolve_python_script_generation_with_errors_rag_true_without_corrector.log 2>&1'

% MATPLOTAGENT ITERATIVE TIME RECORD
<!-- with time recording -->
<!-- expert queries:: devstral:24b with corrector and with rag: done  -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/iterative_python_scripts_generation_logs/devstral_24b_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'

<!-- deepseek-r1:32b IP-->
$ screen -dmS deepseek-r1:32b bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/iterative_python_scripts_generation_logs/deepseek_r1_32b_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'

% magicoder done
$ screen -dmS magicoder bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model magicoder --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/iterative_python_scripts_generation_logs/magicoder_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'

<!-- gemma3:27b done-->
$ screen -dmS gemma3_27b bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gemma3:27b --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/iterative_python_scripts_generation_logs/gemma3_27b_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'

% llama3:70b IP
$ screen -dmS llama3:70b bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model llama3:70b --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/iterative_python_scripts_generation_logs/llama3_70b_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'

<!-- % FASTMRIBRAIN ITERATIVE TIME RECORD -->
<!-- with time recording -->
<!-- expert queries:: devstral:24b with corrector and with rag: done  -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG > ./mri_nyu_data/iterative_python_scripts_generation_logs/devstral_24b_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'

% deepseek-r1:32b IP
$ screen -dmS deepseek-r1:32b bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG > ./mri_nyu_data/iterative_python_scripts_generation_logs/deepseek_r1_32b_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'
<!-- magicoder done-->
$ screen -dmS magicoder bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model magicoder --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG > ./mri_nyu_data/iterative_python_scripts_generation_logs/magicoder_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'
% gemma3:27b IP
$ screen -dmS gemma3:27b bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gemma3:27b --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG > ./mri_nyu_data/iterative_python_scripts_generation_logs/gemma3_27b_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'
<!-- llama3:70b -->
$ screen -dmS llama3:70b bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model llama3:70b --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG > ./mri_nyu_data/iterative_python_scripts_generation_logs/llama3_70b_user_iterative_error_resolve_python_script_generation_with_time.log 2>&1'

<!-- DEEPSEEK-R1:32B -->
<!-- deepseek-r1:32b -->
<!-- expert queries:: with corrector and with rag: done -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/deeepseek_r1_32b_user_iterative_error_resolve_python_script_generation_with_rag_with_corrector.log 2>&1'

% expert queries:: without rag and without corrector: 
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/deeepseek_r1_32b_user_iterative_error_resolve_python_script_generation_expert_without_rag_without_corrector.log 2>&1'

<!-- expert queries:: without rag and with corrector:  -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/deeepseek_r1_32b_user_iterative_error_resolve_python_script_generation_without_rag_with_corrector.log 2>&1'

<!-- expert queries:: with rag and without corrector:  -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --rag True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/deeepseek_r1_32b_user_iterative_error_resolve_python_script_generation_with_rag_without_corrector.log 2>&1'

% SIMPLE QUERIES
% simple queries:: with rag and with corrector: in progress--> 
$ screen -dmS deepseek bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --rag True --errors True -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/deeepseek_r1_32b_user_iterative_error_resolve_python_script_generation_with_errors.log 2>&1'

<!-- % simple queries:: without corrector and without rag: --> 
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --errors True  -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/deeepseek_r1_32b_user_iterative_error_resolve_python_script_generation_with_error_without_corrector_without_rag.log 2>&1'

% simple queries:: with rag and without corrector: -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --rag True --errors True -os True -c True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/deeepseek_r1_32b_user_iterative_error_resolve_python_script_generation_with_errors.log 2>&1'

<!-- % simple queries:: with rag and without corrector: --> -->
$ screen -dmS devstral bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --errors True --rag True --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE > ./prompting_techniques/iterative_python_code_generation_logs/deeepseek_r1_32b_user_iterative_error_resolve_python_script_generation_with_errors_rag_true_without_corrector.log 2>&1'



<!-- RAG: USER SUB QUERY GENERATION -->
% main server
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model magicoder --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/magicoder_user_sub_queries_generation.log

<!-- temporary server -->
% magicoder
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model magicoder --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/magicoder_user_sub_queries_generation.log

<!-- magicoder without errors -->
$ screen -dmS sci_magicoder_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model magicoder --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/magicoder_user_sub_queries_generation_without_errors.log 2>&1'

% <!-- magicoder with errors -->
$ screen -dmS sci_magicoder_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model magicoder --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/magicoder_user_sub_queries_generation_with_errors.log 2>&1'

<!-- llama3:70b -->
<!-- without errors/ expert queries -->
$ screen -dmS llama3_sub_query bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model llama3:70b --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/llama3_70b_user_sub_queries_generation.log 2>&1'

% with errors
$ screen -dmS llama3_sub_query bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model llama3:70b --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/llama3_70b_user_sub_queries_generation_with_errors.log 2>&1'

% deepseek-r1:70b
% without errors
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:70b --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/deepseek_r1_70b_user_sub_queries_generation.log

<!-- with errors -->
$ screen -dmS deepseek_sub_query bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:70b --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/deepseek_r1_70b_user_sub_queries_generation_with_errors.log 2>&1'

<!-- MATPLOTAGENT -->
% without errors: done
$ screen -dmS deepseek_sub_query bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --dataset USER_SUB_QUERY_GENERATION_MATPLOTAGENT_DATASETS > ./user_sub_query_generation_logs/deepseek_r1_32b_matplotagent_user_sub_queries_generation.log 2>&1'

<!-- with errors: done -->
$ screen -dmS deepseek_sub_query bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --errors True --dataset USER_SUB_QUERY_GENERATION_MATPLOTAGENT_DATASETS > ./user_sub_query_generation_logs/deepseek_r1_32b_matplotagent_user_sub_queries_generation_with_errors.log 2>&1'

<!-- FASTMRIBRAIN -->
% without errors: done
$ screen -dmS deepseek_sub_query bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --dataset USER_SUB_QUERY_GENERATION_FASTMRIBRAIN_DATASETS > ./user_sub_query_generation_logs/deepseek_r1_32b_fastmribrain_user_sub_queries_generation.log 2>&1'

<!-- with errors: done -->
$ screen -dmS deepseek_sub_query bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --errors True --dataset USER_SUB_QUERY_GENERATION_FASTMRIBRAIN_DATASETS > ./user_sub_query_generation_logs/deepseek_r1_32b_fastmribrain_user_sub_queries_generation_with_errors.log 2>&1'

<!-- gemma3:27b done--> 
$ screen -dmS sci_gemma_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gemma3:27b --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/gemma3_270b_user_sub_queries_generation.log 2>&1'
% with errors
$ screen -dmS sci_gemma_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gemma3:27b --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/gemma3_27b_user_sub_queries_generation_with_errors.log 2>&1'

% devstral:24b done
$ screen -dmS sci_devstral_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/devstral_24b_user_sub_queries_generation.log 2>&1'

% with errors
$ screen -dmS sci_devstral_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/devstral_24b_user_sub_queries_generation_with_errors.log 2>&1'



% GENERATE PYTHON CODE WITH RAG <!-- with screen -->
<!-- magicoder -->
$ screen -dmS sci_magicoder_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model magicoder --rag True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/magicoder_python_scripts_with_rag_multi_agents_and_sub_query_decomposition.log 2>&1'

% <!-- llama3:70b -->
$ screen -dmS sci_llama3_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model llama3:70b --rag True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/llama3_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition.log 2>&1'

<!-- with rag and with errors and with corrector -->
$ screen -dmS sci_llama3_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model llama3:70b --rag True --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/llama3_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1'

% without rag and with errors and with corrector
$ screen -dmS sci_llama3_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model llama3:70b  --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/llama3_70b_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1'


<!-- deepseek-r1:70b -->
% <!-- with rag and without error and with corrector -->
$ screen -dmS sci_deepseek_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:70b --rag True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/deepseek_r1_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition.log 2>&1'

<!-- with rag and with error and with corrector -->
$ screen -dmS sci_deepseek_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:70b --rag True --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/deepseek_r1_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1'

% without rag and with errors and with corrector
$ screen -dmS sci_deepseek_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:70b --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/deepseek_r1_70b_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1'

% gemma3:27b done
% with rag and without error and without corrector
$ screen -dmS sci_gemma_code_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gemma3:27b --rag True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition.log 2>&1'
<!-- with rag and with errors and without corrector -->
$ screen -dmS sci_gemma_code_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gemma3:27b --rag True --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors.log 2>&1'

% with rag and with errors and with corrector
$ screen -dmS sci_gemma_code_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gemma3:27b -c True --rag True --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1'

<!-- devstral:24b -->
<!-- Non Expert Queries -->
<!--Step1: with errors and without rag and without corrector: done-->
$ screen -dmS sci_devstral_code_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b  --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/devstral_24b_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1'

% Step2: with errors and without rag and with corrector: done
$ screen -dmS sci_devstral_code_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b  --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/devstral_24b_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1'

<!-- Step3: with errors and with rag and without corrector: done -->
$ screen -dmS sci_devstral_code_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b  --errors True --rag True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/devstral_24b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1'

% <!-- Step4: with errors and with rag and with corrector: done-->
$ screen -dmS sci_devstral_code_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b  --errors True --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/devstral_24b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1'

<!-- % Expert Queries -->
<!-- Step5: without errors and without rag and without corrector: done -->
$ screen -dmS sci_devstral_code_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b  --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/devstral_24b_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1'

% <!-- Step6: without errors and with rag and without corrector: done -->
$ screen -dmS sci_devstral_code_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/devstral_24b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1'

% <!-- Step7: without errors and without rag and with corrector: done -->
$ screen -dmS sci_devstral_code_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/devstral_24b_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1'

% <!-- Step8: without errors and with rag and with corrector: in progress -->
$ screen -dmS sci_devstral_code_rag_log bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/devstral_24b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1'


<!-- % VTK_USER_QUERY_GENERATION_VTK_DATASETS -->
<!-- % USER queries generation from vtk related python scripts -->
<!-- without errors -->
<!-- devstral -->
$ screen -dmS sci_devstral_vtk bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --dataset VTK_USER_QUERY_GENERATION_VTK_DATASETS > ./vtk_python_scripts_experiment/logs/deepseek_r1_70b_user_query_generation_from_vtk_related_python_scripts.log 2>&1'

% deepseep=r1:70b
$ screen -dmS sci_devstral_vtk bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:70b --dataset VTK_USER_QUERY_GENERATION_VTK_DATASETS > ./vtk_python_scripts_experiment/logs/deepseek_r1_70b_user_query_generation_from_vtk_related_python_scripts.log 2>&1'


% with errors
$ screen -dmS sci_devstral_vtk bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --dataset VTK_USER_QUERY_GENERATION_VTK_DATASETS > ./vtk_python_scripts_experiment/logs/devstral_24b_user_query_generation_from_vtk_related_python_scripts_with_errors.log 2>&1'
<!-- simple query generation from expert queries: IP -->
$ screen -dmS sci_devstral_vtk bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:70b --errors True --dataset VTK_USER_QUERY_GENERATION_VTK_DATASETS > ./vtk_python_scripts_experiment/logs/deepseek_r1_70b_user_query_generation_from_vtk_related_expert_queries_with_errors.log 2>&1'


<!-- % VTK_RAG generate python scripts -->
% expert queries without rag: done
$ screen -dmS sci_devstral_vtk bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag False --dataset VTK_RAG > ./vtk_python_scripts_experiment/logs/devstral_24b_vtk_python_scripts_generation_from_vtk_related_user_queries_v3.log 2>&1'

<!-- expert queries with -->
$ screen -dmS sci_devstral_vtk bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:70b --rag False --dataset VTK_RAG > ./vtk_python_scripts_experiment/logs/deepseek_r1_70b_vtk_python_scripts_generation_from_vtk_related_user_queries_v2.log 2>&1'

% <!-- simple queries without rag -->
$ screen -dmS sci_devstral_vtk bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag False --errors True --dataset VTK_RAG > ./vtk_python_scripts_experiment/logs/devstral_24b_vtk_python_scripts_generation_from_vtk_related_user_queries_with_errors_v2.log 2>&1'

% ITERATIVE_ERROR_RESOLVE_VTK_RAG 
<!-- % expert queries devstral:24b done -->
$ screen -dmS sci_devstral_vtk bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag False --dataset ITERATIVE_ERROR_RESOLVE_VTK_RAG > ./vtk_python_scripts_experiment/logs/devstral_24b_vtk_iterative_python_scripts_generation_from_vtk_related_user_queries.log 2>&1'

% expert queries deepseek-r1:24b:: done
$ screen -dmS sci_deepseek_vtk bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --rag False --dataset ITERATIVE_ERROR_RESOLVE_VTK_RAG > ./vtk_python_scripts_experiment/logs/deepseek_r1_32b_vtk_iterative_python_scripts_generation_from_vtk_related_expert_user_queries.log 2>&1'

<!-- expert queries llama3:70b: done -->
$ screen -dmS sci_deepseek_vtk bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model llama3:70b --rag False --dataset ITERATIVE_ERROR_RESOLVE_VTK_RAG > ./vtk_python_scripts_experiment/logs/llama3_70b_vtk_iterative_python_scripts_generation_from_vtk_related_expert_user_queries.log 2>&1'

% gemma3:27b:: done
$ screen -dmS sci_deepseek_vtk bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gemma3:27b --rag False --dataset ITERATIVE_ERROR_RESOLVE_VTK_RAG > ./vtk_python_scripts_experiment/logs/gemma3_27b_vtk_iterative_python_scripts_generation_from_vtk_related_expert_user_queries.log 2>&1'

% magicoder:: 
$ screen -dmS sci_magicoder_vtk bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model magicoder --rag False --dataset ITERATIVE_ERROR_RESOLVE_VTK_RAG > ./vtk_python_scripts_experiment/logs/magicoder_vtk_iterative_python_scripts_generation_from_vtk_related_expert_user_queries.log 2>&1'

<!-- simple queries -->
$ screen -dmS sci_devstral_vtk bash -c 'python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --dataset ITERATIVE_ERROR_RESOLVE_VTK_RAG > ./vtk_python_scripts_experiment/logs/devstral_24b_vtk_iterative_python_scripts_generation_from_vtk_related_user_queries_simple_queries_v2.log 2>&1'


<!-- % EVALUATION -->
% this model does not matter, internally there is an array
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  gemma3:27b  --rag True --dataset CLIMATE_RAG_IMAGE > ./llm_rag_python_scripts_evaluation_logs/devstral_24b_evaluation_error_categorization_with_rag_multi_agents_and_sub_query_decomposition_image_0_8.log

% MATPLOTAGENT
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate -m devstral:24b --dataset MATPLOTAGENT_RAG_IMAGE > ./matplot_agent_data/plot_generation/evaluation_csv_to_h5_logs/llama3_without_errors_matplotagent_error_categorization_with_rag_multi_agents_and_sub_query_decomposition_image.log

<!-- FASTMRIBRAIN -->
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  gemma3:27b  --rag True --dataset FASTMRIBRAIN_RAG_IMAGE > ./mri_nyu_data/evaluation_logs/all_fastmribrain_evaluation_error_categorization_image.log

% VTK
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True --dataset VTK_RAG_IMAGE > ./vtk_python_scripts_experiment/logs/deepseek_vtk_evaluation_error_categorization_image_v6.log

% ITERATIVE VTK
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True --dataset ITERATIVE_ERROR_RESOLVE_VTK_RAG_IMAGE > ./vtk_python_scripts_experiment/logs/deepseek_vtk_iterative_evaluation_error_categorization_image_with_errors.log

% ite 0 to 6
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True --dataset ITERATIVE_ERROR_RESOLVE_VTK_RAG_IMAGE > ./vtk_python_scripts_experiment/logs/devstral_24b_vtk_iterative_0_6_evaluation_error_categorization_image.log

<!-- VTK ALL -->
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True --dataset ITERATIVE_ERROR_RESOLVE_VTK_RAG_IMAGE > ./vtk_python_scripts_experiment/logs/magicoder_deepseek_gemma3_llama3_vtk_iterative_evaluation_error_categorization_image_all.log


<!-- % ITERATIVE ERROR resolve -->
<!-- ITERATIVE_CLIMATE_RAG_IMAGE -->
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True -c True --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_corrector.log

$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True -c True --errors True--dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_with_corrector.log

$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True --errors True --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_without_corrector.log

$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_without_corrector.log

$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  -c True --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_corrector.log

$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  -c True --errors True --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_with_corrector.log

$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --errors True --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_without_corrector.log

$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_without_corrector.log

<!-- expert queries:: with rag and with corrector: done -->
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./llm_rag_python_scripts_evaluation_logs/devstral_24b_iterative_evaluation_error_categorization_image.log

% simple queries:: with rag and with corrector: done
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./llm_rag_python_scripts_evaluation_logs/devstral_24b_iterative_evaluation_error_categorization_with_rag_multi_agents_and_sub_query_decomposition_image_with_errors.log

<!-- simple queries:: without corrector and without rag: done -->
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./llm_rag_python_scripts_evaluation_logs/devstral_24b_iterative_evaluation_error_categorization_simple_queries_without_corrector_without_rag_part1.log

<!-- simple queries:: without corrector and without rag: inprogress -->
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./llm_rag_python_scripts_evaluation_logs/devstral_24b_iterative_evaluation_error_categorization_simple_queries_with_corrector_without_rag.log

<!-- % ITERATIVE_MATPLOTAGENT_RAG_IMAGE -->
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True --dataset ITERATIVE_MATPLOTAGENT_RAG_IMAGE > ./matplot_agent_data/plot_generation/iterative_evaluation_logs/devstral_24b_iterative_evaluation_error_categorization_all_v3.log


% <!-- ITERATIVE_FASTMRIBRAIN_RAG_IMAGE -->
$ python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True --dataset ITERATIVE_FASTMRIBRAIN_RAG_IMAGE > ./mri_nyu_data/iterative_evaluation_logs/devstral_24b_iterative_evaluation_error_categorization_all_v5.log

% To quit screen
$ screen -X -S screen_name  quit
% single turn iteration1
% gpt-oss
$ screen -dmS gpt_oss_sub bash -c './running_experiments_scripts/climate/single/run_screens_gpt_oss_sub_query.sh'

$ screen -dmS gpt_oss bash -c './running_experiments_scripts/climate/single/run_screens_gpt_oss.sh'



% climate
<!-- iterative error resolving -->
$ screen -dmS devstral bash -c './running_experiments_scripts/climate/run_screens_devstral_iterative_code_generation.sh' 
$ screen -dmS devstral bash -c './running_experiments_scripts/climate/run_screens_devstral_iterative_code_evaluation.sh' 

% devstral: done 
$ screen -dmS devstral_sub bash -c './run_screens_devstral_sub_query.sh'
$ screen -dmS devstral bash -c './running_experiments_scripts/climate/run_screens_devstral.sh'

% gemma3: done 
$ screen -dmS screen_runner bash -c './run_screens_gemma3_sub_query.sh'
$ screen -dmS screen_runner bash -c './run_screens_gemma3.sh'

% magicoder: done 
$ screen -dmS screen_runner bash -c './run_screens_magicoder.sh'
$ screen -dmS screen_runner bash -c './run_screens_magicoder_sub_query.sh'

% llama3:70b -- done
$ screen -dmS llama3_sub bash -c './run_screens_llama3_sub_query.sh'
$ screen -dmS llama3 bash -c './run_screens_llama3.sh'

% deepseek-r1:32b
$ screen -dmS deepseek_sub bash -c './run_screens_deepseek_r1_sub_query.sh'
$ screen -dmS deepseek bash -c './running_experiments_scripts/climate/run_screens_deepseek_r1.sh'

% matplotagent
% Run scripts inside screens
% devstral:  done
$ screen -dmS devstrals bash -c './running_experiments_scripts/matplotagent/run_screens_devstral_matplotagent_sub_query.sh'
$ screen -dmS devstral bash -c './running_experiments_scripts/matplotagent/run_screens_devstral_matplotagent.sh'

% gemma3: done
$ screen -dmS screen_runner bash -c './running_experiments_scripts/matplotagent/run_screens_gemma3_matplotagent_sub_query.sh'
$ screen -dmS screen_runner bash -c './running_experiments_scripts/matplotagent/run_screens_gemma3_matplotagent.sh'

% magicoder:  done
$ screen -dmS magicoders bash -c './running_experiments_scripts/matplotagent/run_screens_magicoder_matplotagent_sub_query.sh'
$ screen -dmS magicoder bash -c './running_experiments_scripts/matplotagent/run_screens_magicoder_matplotagent.sh'


% llama3:70b: ip
$ screen -dmS llama3s bash -c './running_experiments_scripts/matplotagent/run_screens_llama3_matplotagent_sub_query.sh'
$ screen -dmS llama3 bash -c './running_experiments_scripts/matplotagent/run_screens_llama3_matplotagent.sh'

% deepseek-r1:32b --> done
$ screen -dmS deepseeks bash -c './running_experiments_scripts/matplotagent/run_screens_deepseek_r1_matplotagent_sub_query.sh'
$ screen -dmS deepseek bash -c './running_experiments_scripts/matplotagent/run_screens_deepseek_r1_matplotagent.sh'


% fastmribrain
% Run scripts inside screens
% devstral:  done
$ screen -dmS devstrals bash -c './running_experiments_scripts/fastmribrain/run_screens_devstral_fastmribrain_sub_query.sh'
$ screen -dmS devstral bash -c './running_experiments_scripts/fastmribrain/run_screens_devstral_fastmribrain.sh'

% gemma3: done
$ screen -dmS gemma3s bash -c './running_experiments_scripts/fastmribrain/run_screens_gemma3_fastmribrain_sub_query.sh'
$ screen -dmS gemma3 bash -c './running_experiments_scripts/fastmribrain/run_screens_gemma3_fastmribrain.sh'

% magicoder: done
$ screen -dmS magicoders bash -c './running_experiments_scripts/fastmribrain/run_screens_magicoder_fastmribrain_sub_query.sh'
$ screen -dmS magicoder bash -c './running_experiments_scripts/fastmribrain/run_screens_magicoder_fastmribrain.sh'


% llama3:70b: done
$ screen -dmS llama3s bash -c './running_experiments_scripts/fastmribrain/run_screens_llama3_fastmribrain_sub_query.sh'
$ screen -dmS llama3 bash -c './running_experiments_scripts/fastmribrain/run_screens_llama3_fastmribrain.sh'

% deepseek-r1:32b --> done
$ screen -dmS deepseeks bash -c './running_experiments_scripts/fastmribrain/run_screens_deepseek_r1_fastmribrain_sub_query.sh'
$ screen -dmS deepseek bash -c './running_experiments_scripts/fastmribrain/run_screens_deepseek_r1_fastmribrain.sh'


% matplotlib and fastmribrain
% Run scripts inside screens
% devstral:  
$ screen -dmS screen_runner bash -c './run_screens_devstral_fastmribrain_sub_query.sh'
$ screen -dmS screen_runner bash -c './run_screens_devstral_fastmribrain.sh'

% gemma3:  
$ screen -dmS screen_runner bash -c './run_screens_gemma3_fastmribrain_sub_query.sh'
$ screen -dmS screen_runner bash -c './run_screens_gemma3_fastmribrain.sh'

% magicoder:  
$ screen -dmS screen_runner bash -c './run_screens_magicoder_fastmribrain.sh'
$ screen -dmS screen_runner bash -c './run_screens_magicoder_fastmribrain_sub_query.sh'

% llama3:70b: 
$ screen -dmS screen_runner bash -c './run_screens_llama3_fastmribrain_sub_query.sh'
$ screen -dmS screen_runner bash -c './run_screens_llama3_fastmribrain.sh'

% deepseek-r1:32b --> in progress
$ screen -dmS screen_runner bash -c './run_screens_deepseek_r1_fastmribrain_sub_query.sh'
$ screen -dmS screen_runner bash -c './run_screens_deepseek_r1_fastmribrain.sh'


<!-- ITERATIVE ERROR RESOLVE_CLIMATE -->
<!-- $ python3 evaluation_error_categorization.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model llama3:70b --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE -c True > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs_error_categorization/llama3_70b_error_categorization_with_corrector_expert_level_queries_human_error_insertions_remove_image_from_query_v2.log -->

<!-- $ python3 evaluation_error_categorization.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model llama3:70b --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE -c False > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs_error_categorization/llama3_70b_error_categorization_without_corrector_expert_level_queries_human_error_insertions_remove_image_from_query_v2.log -->


<!-- $ python3 evaluation_error_categorization.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model deepseek-r1:70b --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE -c False > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs_error_categorization/deepseek_r1_70b_error_categorization_without_corrector_expert_level_queries_human_error_insertions_remove_image_from_query_v2.log -->

<!-- $ python3 evaluation_error_categorization.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model deepseek-r1:70b --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE -c True > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs_error_categorization/deepseek_r1_70b_error_categorization_with_corrector_expert_level_queries_human_error_insertions_remove_image_from_query_v2.log -->

<!-- $ python3 evaluation_error_categorization.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model magicoder --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE -c False > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs_error_categorization/magicoder_error_categorization_without_corrector_expert_level_queries_human_error_insertions_remove_image_from_query_v2.log -->

<!-- $ python3 evaluation_error_categorization.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model magicoder --dataset ITERATIVE_ERROR_RESOLVE_CLIMATE -c True > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs_error_categorization/magicoder_error_categorization_with_corrector_expert_level_queries_human_error_insertions_remove_image_from_query_v2.log -->

<!-- FOR CLIMATE -->
<!-- $ python3 evaluation_error_categorization.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model llama3:70b --dataset CLIMATE -c True > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs_error_categorization/llama3_70b_zero_shot_error_categorization_with_corrector_expert_level_queries_human_error_insertions_remove_image_from_query_v2.log -->

<!-- $ python3 evaluation_error_categorization.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model llama3:70b --dataset CLIMATE -c False > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs_error_categorization/llama3_70b_zero_shot_error_categorization_without_corrector_expert_level_queries_human_error_insertions_remove_image_from_query_v2.log -->


<!-- $ python3 evaluation_error_categorization.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model deepseek-r1:70b --dataset CLIMATE -c False > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs_error_categorization/deepseek_r1_70b_zero_shot_error_categorization_without_corrector_expert_level_queries_human_error_insertions_remove_image_from_query_v2.log -->

<!-- $ python3 evaluation_error_categorization.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model deepseek-r1:70b --dataset CLIMATE -c True > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs_error_categorization/deepseek_r1_70b_zero_shot_error_categorization_with_corrector_expert_level_queries_human_error_insertions_remove_image_from_query_v2.log -->

<!-- $ python3 evaluation_error_categorization.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model magicoder --dataset CLIMATE -c False > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs_error_categorization/magicoder_zero_shot_error_categorization_without_corrector_expert_level_queries_human_error_insertions_remove_image_from_query_v2.log -->

<!-- $ python3 evaluation_error_categorization.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model magicoder --dataset CLIMATE -c True > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs_error_categorization/magicoder_zero_shot_error_categorization_with_corrector_expert_level_queries_human_error_insertions_remove_image_from_query_v2.log -->

<!-- CLIMATE: WITHOUT CORRECTOR EXPERT QUERIES -->
<!-- $ python3 evaluation_error_categorization.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model magicoder --dataset CLIMATE -c False > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs_error_categorization/magicoder_zero_shot_error_categorization_without_corrector_expert_human_modified_queries_with_accurate_information_based_on_original_scripts.log -->

<!-- $ python3 evaluation_error_categorization.py --url http://ai-lab2.dyn.gsu.edu:8080/api/generate --model llama3:70b --dataset CLIMATE -c False > /home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/output_logs_error_categorization/llama3_70b_zero_shot_error_categorization_without_corrector_expert_level_queries_human_modified_queries_with_accurate_information_based_on_original_scripts.log -->



Future Work Let's imagine we have a lot of hdf5, h5, or he5 data and based on the data we have to generate some python codes that will read data from the scientific data file and visualize the data automatically.

Specific Task: For example we have: A scientifica data file --> read the data file and store the metadata and dataset's paths and attributes into a text file And User query --> based on the user query data we have to fetch the paths and attribute's paths as data that are described in the user query as a free text

Challenges to the LLM:

LLM can't read the tokens beyond it's limit, so passing all paths from the data file won't produce any good result: Need to find the research paper where described the updated version of input tokens to LLMs, where LLMs can read much words without hallucinations Research problems: Need to find an algorithm by using that we can form the dataset paths specifically to pass it to the LLM model

Existing methods:
How to select existing methods:

Choosing the Right Algorithm Simple typos or short strings: Levenshtein, Damerau-Levenshtein. Names or records: Soundex, Metaphone, Jaro-Winkler. Text comparison: TF-IDF + Cosine Similarity, BERT embeddings. Large datasets or near-duplicates: SimHash, MinHash. Ordered sequences: Longest Common Subsequence.


Python scripts that have subarray access /ACL_DIRS/GES_DISC/python_script/acos_L2s_110101_02_Production_v201201_L2Sub7309_r01_PolB_161206183303.h5.py /ACL_DIRS/GES_DISC/python_script/BUV_Nimbus04_L3zm_v01_00_2012m0203t144121_h5.py /ACL_DIRS/GES_DISC/python_script/GSSTF_3_2008_12_31.py /ACL_DIRS/GES_DISC/python_script/GSSTF_NCEP_3_2008_12_31.py /ACL_DIRS/GES_DISC/python_script/GSSTFYC_3_Year_1998_2008.py /ACL_DIRS/GES_DISC/python_script/HIRDLS-Aura_L2_v07-00-20-c01_2008d077.he5.py /ACL_DIRS/GES_DISC/python_script/HIRDLS-Aura_L3ZFCNO2_v07-00-20-c01_2005d022-2008d077.he5.py /ACL_DIRS/GES_DISC/python_script/MLS-Aura_L2GP-BrO_v04-23-c03_2016d302.he5.py /ACL_DIRS/GES_DISC/python_script/MLS-Aura_L2GP-O3_v04-23-c02_2019d001.he5.py /ACL_DIRS/GES_DISC/python_script/oco2_L2StdND_03949a_150330_B8100r_170916014809.h5.py /ACL_DIRS/LaRC/python_script/CAL_LID_L2_BlowingSnow_Antarctica-Standard-V2-00.2023-06.hdf5.py /ACL_DIRS/LaRC/python_script/CATS-ISS_L2O_D-M7.2-V2-01_05kmLay.2017-05-01T00-47-40T01-28-41UTC.hdf5.py /ACL_DIRS/LaRC/python_script/MOP02J-20131129-L2V19.9.3.he5.py /ACL_DIRS/LaRC/python_script/MOP02N-20180311-L2V19.9.2.he5.py /ACL_DIRS/LaRC/python_script/TES-Aura_L2-O3-Nadir_r0000002433_F08_12.he5.py /ACL_DIRS/LP_DAAC/python_script/AG100.v003.64.-089.0001.h5.py


<!-- copy files from M3 pro to gsu server -->
$ scp MOP02J-20131129-L2V19.9.3.he5 achakroborti1@rapids.cs.gsu.edu:/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/ACL_DIRS/LaRC
$ scp MOP02N-20180311-L2V19.9.2.he5 achakroborti1@rapids.cs.gsu.edu:/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/ACL_DIRS/LaRC
$ scp MOP03T-20131129-L3V5.9.1.he5 achakroborti1@rapids.cs.gsu.edu:/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/ACL_DIRS/LaRC
$ scp MOP03TM-201802-L3V95.9.1.he5 achakroborti1@rapids.cs.gsu.edu:/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/ACL_DIRS/LaRC
$ scp TES-Aura_L2-O3-Nadir_r0000002433_F08_12.he5 achakroborti1@rapids.cs.gsu.edu:/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/ACL_DIRS/LaRC
$ scp TES-Aura_L3-CH4_r0000033028_C01_F01_12.he5 achakroborti1@rapids.cs.gsu.edu:/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/ACL_DIRS/LaRC
$ scp CAL_LID_L2_BlowingSnow_Antarctica-Standard-V2-00.2023-06.hdf5 achakroborti1@rapids.cs.gsu.edu:/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/ACL_DIRS/LaRC
$ scp DSCOVR_EPIC_L2_TO3_03_20210301005516_03.h5 achakroborti1@rapids.cs.gsu.edu:/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/ACL_DIRS/LaRC
$ scp CATS-ISS_L2O_D-M7.2-V2-01_05kmLay.2017-05-01T00-47-40T01-28-41UTC.hdf5 achakroborti1@rapids.cs.gsu.edu:/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/ACL_DIRS/LaRC

$ scp Q2011280003000.L2_SCI_V5.0.h5 achakroborti1@rapids.cs.gsu.edu:/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/ACL_DIRS/PO_DAAC
$ scp Q2012034.L3m_DAY_SCI_V5.0_SSS_1deg.h5 achakroborti1@rapids.cs.gsu.edu:/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/ACL_DIRS/PO_DAAC

$ scp SMAP_L2B_SSS_32221_20210211T162812_R17000_V5.0.h5 achakroborti1@rapids.cs.gsu.edu:/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/ACL_DIRS/PO_DAAC

neuroimaging data
$ scp Task* achakroborti1@rapids.cs.gsu.edu:/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/mri_nyu_data/neuroimaging_python_scripts/data

76
headers:  ['Womans millions of dollars', 'Mens millions of dollars']
Saved /home/achakroborti1/related_work/MatPlotAgent/benchmark_data/data/76/data.csv as <Closed HDF5 file>
77
headers:  ['Country', 'Red Meat', 'White Meat', 'Eggs', 'Milk', 'Fish', 'Cereals', 'Starch', 'Nuts', 'Fruits and Vegetables']
Saved /home/achakroborti1/related_work/MatPlotAgent/benchmark_data/data/77/data.csv as <Closed HDF5 file>
78
headers:  ['0-60 mph(sec)', 'Gas Mileage(mpg)', 'Power(kW)', 'Weight(kg)', 'Engine Displacement(cc)']
Saved /home/achakroborti1/related_work/MatPlotAgent/benchmark_data/data/78/data.csv as <Closed HDF5 file>
79
headers:  ['Petal Length(cm)', 'Petal Width(cm)', 'Sepal Length(cm)', 'Sepal Width(cm)', 'Species']
Saved /home/achakroborti1/related_work/MatPlotAgent/benchmark_data/data/79/data.csv as <Closed HDF5 file>
83
headers:  ['date', 'Dow Jones Industrial Average', '1 year moving average']
Saved /home/achakroborti1/related_work/MatPlotAgent/benchmark_data/data/83/data.csv as <Closed HDF5 file>
84
headers:  ['Temperature(K)', 'Pressure(Liquid)', 'Temperature(K).1', 'Pressure(Gas)']
Saved /home/achakroborti1/related_work/MatPlotAgent/benchmark_data/data/84/data.csv as <Closed HDF5 file>
87
headers:  ['SL_NO', 'country', 'continent', 'year', 'lifeExp', 'pop', 'gdpPercap', 'iso_alpha', 'iso_num']
Saved /home/achakroborti1/related_work/MatPlotAgent/benchmark_data/data/87/data.csv as <Closed HDF5 file>
95
headers:  ['Year', 'Date', 'Temperature']
Saved /home/achakroborti1/related_work/MatPlotAgent/benchmark_data/data/95/data.csv as <Closed HDF5 file>
96
headers:  ['Quarter', 'Samsung', 'Nokia/Microsoft', 'Apple', 'LG', 'ZTE', 'Huawei']
Saved /home/achakroborti1/related_work/MatPlotAgent/benchmark_data/data/96/data.csv as <Closed HDF5 file>
97
headers:  ['SL_NO', 'IL (25°C)', 'toluene (25°C)', 'n-heptane (25°C)']
Saved /home/achakroborti1/related_work/MatPlotAgent/benchmark_data/data/97/data.csv as <Closed HDF5 file>
99
headers:  ['SL_NO', 'total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'size']
Saved /home/achakroborti1/related_work/MatPlotAgent/benchmark_data/data/99/data.csv as <Closed HDF5 file>
100
headers:  ['Series', 'Wavelength', 'l position', 'p position']
Saved /home/achakroborti1/related_work/MatPlotAgent/benchmark_data/data/100/data.csv as <Closed HDF5 file>


TES-Aura_L2-O3-Nadir_r0000002433_F08_12.he5.txt --> TES-Aura_L2-O3-Nadir_r0000002433_F08_12.he5.py.png | Score: 0.91 | FOUND
ATL20-01_20181101001332_05100101_004_01.h5.txt --> ATL20-01_20181101001332_05100101_004_01.h5.py.png | Score: 0.91 | FOUND
BUV-Nimbus04_L3zm_v01-02-2013m0422t101810.h5.txt --> BUV-Nimbus04_L3zm_v01-02-2013m0422t101810.h5.py.png | Score: 0.91 | FOUND
MLS-Aura_L2GP-BrO_v04-23-c03_2016d302.he5.txt --> MLS-Aura_L2GP-BrO_v04-23-c03_2016d302.he5.py.png | Score: 0.90 | FOUND
DSCOVR_EPIC_L2_TO3_03_20210301005516_03.h5.txt --> DSCOVR_EPIC_L2_TO3_03_20210301005516_03.h5.py.png | Score: 0.91 | FOUND
ATL16_20210101010136_01231001_005_01.h5.txt --> ATL16_20210101010136_01231001_005_01.h5.py.png | Score: 0.90 | FOUND
CATS-ISS_L2O_D-M7.2-V2-01_05kmLay.2017-05-01T00-47-40T01-28-41UTC.hdf5.txt --> CATS-ISS_L2O_D-M7.2-V2-01_05kmLay.2017-05-01T00-47-40T01-28-41UTC.hdf5.py.png | Score: 0.94 | FOUND
ATL08_20210114234518_03361001_006_01.h5.txt --> ATL08_20210114234518_03361001_006_01.h5.py.png | Score: 0.90 | FOUND
MOP03TM-201802-L3V95.9.1.he5.txt --> MOP03TM-201802-L3V95.9.1.he5.py.png | Score: 0.87 | FOUND
SMAP_L1A_RADIOMETER_30031_A_20200914T223611_R17000_001.h5.txt --> SMAP_L1A_RADIOMETER_30031_A_20200914T223611_R17000_001.h5.py.png | Score: 0.93 | FOUND
SMAP_L1B_TB_50719_D_20240730T124417_R19240_001.h5.txt --> SMAP_L1B_TB_50719_D_20240730T124417_R19240_001.h5.py.png | Score: 0.92 | FOUND
ATL19_20181001010615_00370101_003_02.h5.txt --> ATL19_20181001010615_00370101_003_02.h5.py.png | Score: 0.90 | FOUND
ATL09_20181117090604_07600101_006_02.h5.txt --> ATL09_20181117090604_07600101_006_02.h5.py.png | Score: 0.90 | FOUND
MLS-Aura_L2GP-H2O_v04-20-c01_2013d003.he5.txt --> MLS-Aura_L2GP-H2O_v04-20-c01_2013d003.he5.py.png | Score: 0.90 | FOUND
DeepBlue-SeaWiFS_L2_20101210T135954Z_v004-20130525T172725Z.h5.txt --> DeepBlue-SeaWiFS_L2_20101210T135954Z_v004-20130525T172725Z.h5.py.png | Score: 0.93 | FOUND
ATL07-01_20210223204748_09451001_006_01.h5.txt --> ATL07-01_20210223204748_09451001_006_01.h5.py.png | Score: 0.91 | FOUND
OMI-Aura_L3-OMTO3e_2017m0105_v003-2017m0203t091906.he5.txt --> OMI-Aura_L3-OMTO3e_2017m0105_v003-2017m0203t091906.he5222.py.png | Score: 0.90 | FOUND
SMAP_L4_SM_gph_20200915T193000_Vv7032_001.h5.txt --> SMAP_L4_SM_gph_20200915T193000_Vv7032_001.h5.py.png | Score: 0.91 | FOUND
GLAH13_633_2103_001_1317_0_01_0001.h5.txt --> GLAH13_633_2103_001_1317_0_01_0001.h5.py.png | Score: 0.89 | FOUND
ATL22_20210712003905_02811201_003_01.h5.txt --> ATL22_20210712003905_02811201_003_01.h5.py.png | Score: 0.90 | FOUND
ATL13_20190330212241_00250301_006_01.h5.txt --> ATL13_20190330212241_00250301_006_01.h5.py.png | Score: 0.90 | FOUND
AMSR_U2_L3_SeaIce25km_B01_20181008.he5.txt --> AMSR_E_L2_Land_V11_201110031920_D.he5.py.png | Score: 0.51 | FOUND
1A.GPM.GMI.COUNT2021.20160105-S230545-E003816.010538.V07A.HDF5.txt --> 1A.GPM.GMI.COUNT2021.20160105-S230545-E003816.010538.V07A.HDF5.py.png | Score: 0.93 | FOUND
acos_L2s_110101_02_Production_v201201_L2Sub7309_r01_PolB_161206183303.h5.txt --> acos_L2s_110101_02_Production_v201201_L2Sub7309_r01_PolB_161206183303.h5.py.png | Score: 0.94 | FOUND
ATL11_051911_0321_006_06.h5.txt --> ATL11_051911_0321_006_06.h5.py.png | Score: 0.86 | FOUND
HIRDLS-Aura_L2_v07-00-20-c01_2008d077.he5.txt --> HIRDLS-Aura_L2_v07-00-20-c01_2008d077.he5.py.png | Score: 0.90 | FOUND
ATL02_20190520193327_08020311_006_01.h5.txt --> ATL02_20190520193327_08020311_006_01.h5.py.png | Score: 0.90 | FOUND
ATL06_20190223232535_08780212_006_02.h5.txt --> ATL06_20190223232535_08780212_006_02.h5.py.png | Score: 0.90 | FOUND
MLS-Aura_L2GP-O3_v04-23-c02_2019d001.he5.txt --> MLS-Aura_L2GP-O3_v04-23-c02_2019d001.he5.py.png | Score: 0.90 | FOUND
3A-MO.GPM.GMI.GRID2021R1.20140701-S000000-E235959.07.V07A.HDF5.txt --> 3A-MO.GPM.GMI.GRID2021R1.20140701-S000000-E235959.07.V07A.HDF5.py.png | Score: 0.93 | FOUND
2A.GPM.DPR.V9-20211125.20170704-S001905-E015140.019017.V07A.HDF5.txt --> 2A.GPM.DPR.V9-20211125.20170704-S001905-E015140.019017.V07A.HDF5.py.png | Score: 0.94 | FOUND
VNP46A1.A2020302.h07v07.001.2020303075447.h5.txt --> VNP46A1.A2020302.h07v07.001.2020303075447.h5.py.png | Score: 0.91 | FOUND
ATL04_20181117090604_07600101_006_02.h5.txt --> ATL04_20181117090604_07600101_006_02.h5.py.png | Score: 0.90 | FOUND
VNP09GA.A2020305.h30v07.001.2020306101330.h5.txt --> VNP09GA.A2020305.h30v07.001.2020306101330.h5.py.png | Score: 0.91 | FOUND
ATL10-02_20181227215113_13790101_006_02.h5.txt --> ATL10-02_20181227215113_13790101_006_02.h5.py.png | Score: 0.91 | FOUND
MOP03T-20131129-L3V5.9.1.he5.txt --> MOP03T-20131129-L3V5.9.1.he5.py.png | Score: 0.87 | FOUND
AMSR_E_L2_Land_V11_201110031920_D.he5.txt --> AMSR_E_L2_Land_V11_201110031920_D.he5.py.png | Score: 0.89 | FOUND
SBUV2-NOAA17_L2-SBUV2N17L2_2011m1231_v01-02-2013m0828t143157.h5.txt --> SBUV2-NOAA17_L2-SBUV2N17L2_2011m1231_v01-02-2013m0828t143157.h5.py.png | Score: 0.93 | FOUND
DeepBlue-SeaWiFS-1.0_L3_20100101_v004-20130604T131317Z.h5.txt --> DeepBlue-SeaWiFS-1.0_L3_20100101_v004-20130604T131317Z.h5.py.png | Score: 0.93 | FOUND
Q2011280003000.L2_SCI_V5.0.h5.txt --> Q2011280003000.L2_SCI_V5.0.h5Q2011280003000.L2_SCI_V5.0.h5.py.png | Score: 0.61 | FOUND
SMAP_L3_SM_P_20200916_R19240_001.h5.txt --> SMAP_L3_SM_P_20200916_R19240_001.h5.py.png | Score: 0.89 | FOUND
1B.GPM.GMI.TB2021.20160105-S230545-E003816.010538.V07A.HDF5.txt --> 1B.GPM.GMI.TB2021.20160105-S230545-E003816.010538.V07A.HDF5.py.png | Score: 0.93 | FOUND
SMAP_L2_SM_P_30058_D_20200916T194350_R19240_001.h5.txt --> SMAP_L2_SM_P_30058_D_20200916T194350_R19240_001.h5.py.png | Score: 0.92 | FOUND
SMAP_L1C_S0_HIRES_02298_A_20150707T160502_R13080_001.h5.txt --> SMAP_L1C_S0_HIRES_02298_A_20150707T160502_R13080_001.h5.py.png | Score: 0.93 | FOUND
GSSTF_3_2008_12_31.he5.txt     --> GSSTF_3_2008_12_31.he5.py.png  | Score: 0.84 | FOUND
OMI-Aura_L2-OMNO2_2008m0720t2016-o21357_v003-2016m0820t102252.he5.txt --> OMI-Aura_L2-OMNO2_2008m0720t2016-o21357_v003-2016m0820t102252.he5.py.png | Score: 0.94 | FOUND
ATL03_20181027235521_04480111_006_02.h5.txt --> ATL03_20181027235521_04480111_006_02.h5.py.png | Score: 0.90 | FOUND
GLAH10_633_2131_001_1317_0_01_0001.H5.txt --> GLAH10_633_2131_001_1317_0_01_0001.H5.py.png | Score: 0.89 | FOUND
ATL21-01_20210301005637_10241001_003_01.h5.txt --> ATL21-01_20210301005637_10241001_003_01.h5.py.png | Score: 0.91 | FOUND
SMAP_L2B_SSS_32221_20210211T162812_R17000_V5.0.h5.txt --> SMAP_L2B_SSS_32221_20210211T162812_R17000_V5.0.h5SMAP_L2B_SSS_32221_20210211T162812_R17000_V5.0.h5.py.png | Score: 0.63 | FOUND
ATL17_20201201000814_10360901_005_01.h5.txt --> ATL17_20201201000814_10360901_005_01.h5.py.png | Score: 0.90 | FOUND
1C.F19.SSMIS.XCAL2021-V.20160105-S214106-E232259.009078.V07A.HDF5.txt --> 1C.F19.SSMIS.XCAL2021-V.20160105-S214106-E232259.009078.V07A.HDF5.py.png | Score: 0.94 | FOUND
GEOLST4KHR_201612291600_002_20210714015139.h5.txt --> GEOLST4KHR_201612291600_002_20210714015139.h5.py.png | Score: 0.91 | FOUND
MOP02J-20131129-L2V19.9.3.he5.txt --> MOP02J-20131129-L2V19.9.3.he5.py.png | Score: 0.87 | FOUND
MOP02N-20180311-L2V19.9.2.he5.txt --> MOP02N-20180311-L2V19.9.2.he5.py.png | Score: 0.87 | FOUND
AG100.v003.64.-089.0001.h5.txt --> AG100.v003.64.-089.0001.h5.py.png | Score: 0.86 | FOUND
Q2012034.L3m_DAY_SCI_V5.0_SSS_1deg.h5.txt --> Q2012034.L3m_DAY_SCI_V5.0_SSS_1deg.h5Q2012034.L3m_DAY_SCI_V5.0_SSS_1deg.h5.py.png | Score: 0.62 | FOUND
TES-Aura_L3-CH4_r0000033028_C01_F01_12.he5.txt --> TES-Aura_L3-CH4_r0000033028_C01_F01_12.he5.py.png | Score: 0.91 | FOUND
SMAP_L1C_TB_50719_D_20240730T124417_R19240_001.h5.txt --> SMAP_L1C_TB_50719_D_20240730T124417_R19240_001.h5.py.png | Score: 0.92 | FOUND
oco2_L2StdND_03949a_150330_B8100r_170916014809.h5.txt --> oco2_L2StdND_03949a_150330_B8100r_170916014809.h5.py.png | Score: 0.92 | FOUND
ATL12_20190330212241_00250301_006_03.h5.txt --> ATL12_20190330212241_00250301_006_03.h5.py.png | Score: 0.90 | FOUND