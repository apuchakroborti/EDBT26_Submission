#!/bin/bash

# Define your screen session names and associated commands

declare -A jobs=(
  # with rag
  [job4]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --rag True --dataset FASTMRIBRAIN_RAG > ./mri_nyu_data/llm_rag_python_scripts_generation_logs/devstral_24b_fastmribrain_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  [job5]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --rag True -c True --dataset FASTMRIBRAIN_RAG > ./mri_nyu_data/llm_rag_python_scripts_generation_logs/devstral_24b_fastmribrain_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  [job7]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True --dataset FASTMRIBRAIN_RAG > ./mri_nyu_data/llm_rag_python_scripts_generation_logs/devstral_24b_fastmribrain_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  [job9]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True -c True --dataset FASTMRIBRAIN_RAG > ./mri_nyu_data/llm_rag_python_scripts_generation_logs/devstral_24b_fastmribrain_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1"

  # without rag
  # [job2]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --dataset FASTMRIBRAIN_RAG > ./mri_nyu_data/llm_rag_python_scripts_generation_logs/devstral_24b_fastmribrain_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # [job3]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True -c True --dataset FASTMRIBRAIN_RAG > ./mri_nyu_data/llm_rag_python_scripts_generation_logs/devstral_24b_fastmribrain_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # [job6]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --dataset FASTMRIBRAIN_RAG > ./mri_nyu_data/llm_rag_python_scripts_generation_logs/devstral_24b_fastmribrain_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  # [job8]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b -c True --dataset FASTMRIBRAIN_RAG > ./mri_nyu_data/llm_rag_python_scripts_generation_logs/devstral_24b_fastmribrain_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1"
  
  # [job10]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/llm_rag_python_scripts_generation_logs/devstral_24b_matplotagent_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # [job11]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True -c True --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/llm_rag_python_scripts_generation_logs/devstral_24b_matplotagent_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  [job12]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --rag True --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/llm_rag_python_scripts_generation_logs/devstral_24b_matplotagent_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  [job13]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --rag True -c True --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/llm_rag_python_scripts_generation_logs/devstral_24b_matplotagent_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # [job14]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/llm_rag_python_scripts_generation_logs/devstral_24b_matplotagent_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  [job15]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/llm_rag_python_scripts_generation_logs/devstral_24b_matplotagent_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  # [job16]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b -c True --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/llm_rag_python_scripts_generation_logs/devstral_24b_matplotagent_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1"
  [job17]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True -c True --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/llm_rag_python_scripts_generation_logs/devstral_24b_matplotagent_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1"

)

for job in "${!jobs[@]}"; do
  echo "Starting $job..."
  screen -dmS "$job" bash -c "${jobs[$job]}"
  
  # Wait until the screen session ends
  while screen -ls | grep -q "$job"; do
    sleep 5
  done

  echo "$job finished."
done

echo "All jobs completed."
