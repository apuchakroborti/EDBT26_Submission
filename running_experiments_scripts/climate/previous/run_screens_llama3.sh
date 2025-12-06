#!/bin/bash

# Define your screen session names and associated commands

declare -A jobs=(
  [job2]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model llama3:70b  --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/llama3_70b_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  [job3]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model llama3:70b  --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/llama3_70b_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  [job4]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model llama3:70b  --errors True --rag True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/llama3_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  [job5]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model llama3:70b  --errors True --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/llama3_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  [job6]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model llama3:70b  --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/llama3_70b_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  [job7]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model llama3:70b --rag True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/llama3_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  [job8]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model llama3:70b -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/llama3_70b_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1"
  [job9]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model llama3:70b --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/llama3_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1"
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
