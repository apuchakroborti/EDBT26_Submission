#!/bin/bash

# Define your screen session names and associated commands
declare -A jobs=(
  [job2]="python3 ./experiment_main/evaluation_error_categorization.py --model  devstral:24b  --dataset CLIMATE_RAG_IMAGE_WITH_TEMP > ./prompting_techniques/llm_rag_generated_python_scripts_evaluation_logs/devstral_24b_climate_evaluation_logs.log 2>&1"
 
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
