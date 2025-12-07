#!/bin/bash

# Define your screen session names and associated commands

declare -A jobs=(
  # [job2]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/evaluation_csv_to_h5_logs/devstral_24b_matplotagent_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # [job3]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True -c True --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/evaluation_csv_to_h5_logs/devstral_24b_matplotagent_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # [job4]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --rag True --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/evaluation_csv_to_h5_logs/devstral_24b_matplotagent_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # [job5]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --rag True -c True --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/evaluation_csv_to_h5_logs/devstral_24b_matplotagent_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  [job6]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model devstral:24b --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/evaluation_csv_to_h5_logs/devstral_24b_matplotagent_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  [job7]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/evaluation_csv_to_h5_logs/devstral_24b_matplotagent_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  [job8]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model devstral:24b -c True --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/evaluation_csv_to_h5_logs/devstral_24b_matplotagent_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1"
  [job9]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True -c True --dataset MATPLOTAGENT_RAG > ./matplot_agent_data/plot_generation/evaluation_csv_to_h5_logs/devstral_24b_matplotagent_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1"
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