#!/bin/bash

# Define your screen session names and associated commands

declare -A jobs=(
  [job2]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --dataset ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG > ./mri_nyu_data/iterative_python_scripts_generation_logs/devstral_24b_fastmribrain_iterative_python_scripts_without_rag__with_errors_without_corrector.log 2>&1"
  # [job3]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True -c True --dataset ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG > ./mri_nyu_data/iterative_python_scripts_generation_logs/devstral_24b_fastmribrain_iterative_python_scripts_without_rag__with_errors_with_corrector.log 2>&1"
  # [job4]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --rag True --dataset ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG > ./mri_nyu_data/iterative_python_scripts_generation_logs/devstral_24b_fastmribrain_iterative_python_scripts_with_rag__with_errors_without_corrector.log 2>&1"
  # [job5]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --errors True --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG > ./mri_nyu_data/iterative_python_scripts_generation_logs/devstral_24b_fastmribrain_iterative_python_scripts_with_rag__with_errors_with_corrector.log 2>&1"
  # [job6]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --dataset ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG > ./mri_nyu_data/iterative_python_scripts_generation_logs/devstral_24b_fastmribrain_iterative_python_scripts_without_rag_without_corrector.log 2>&1"
  # [job7]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True --dataset ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG > ./mri_nyu_data/iterative_python_scripts_generation_logs/devstral_24b_fastmribrain_iterative_python_scripts_with_rag__without_corrector.log 2>&1"
  # [job8]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b -c True --dataset ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG > ./mri_nyu_data/iterative_python_scripts_generation_logs/devstral_24b_fastmribrain_iterative_python_scripts_without_rag__with_corrector.log 2>&1"
  # [job9]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model devstral:24b --rag True -c True --dataset ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG > ./mri_nyu_data/iterative_python_scripts_generation_logs/devstral_24b_fastmribrain_iterative_python_scripts_with_rag__with_corrector.log 2>&1"
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
