#!/bin/bash

# Define your screen session names and associated commands
declare -A jobs=(
  [job2]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True -c True --errors False --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_corrector.log 2>&1"
  [job3]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True -c True --errors True --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_with_corrector.log 2>&1"
  # done
  # [job4]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True -c False --errors True --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_without_corrector.log 2>&1"
  [job5]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag True -c False --errors False --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_without_corrector.log 2>&1"
  [job6]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag False -c True --errors False --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_corrector.log 2>&1"
  # done
  # [job7]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag False -c False --errors True --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_without_corrector.log 2>&1"
  [job8]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag False -c False --errors False --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_without_corrector.log 2>&1"
  [job9]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/evaluation_error_categorization.py --url http://localhost:11434/api/generate --model  devstral:24b  --rag False -c True --errors True --dataset ITERATIVE_CLIMATE_RAG_IMAGE > ./prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_without_rag_with_errors_with_corrector.log 2>&1"
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
