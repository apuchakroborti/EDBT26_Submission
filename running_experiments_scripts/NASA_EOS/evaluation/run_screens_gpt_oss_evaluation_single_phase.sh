#!/bin/bash

# Define your screen session names and associated commands
declare -A jobs=(
  [job2]="python3 ./experiment_main/evaluation_error_categorization.py --model  gpt-oss:20b  --dataset CLIMATE_RAG_IMAGE_WITH_TEMP > ./NASA_EOS/evaluation_logs/non_iterative/gpt_oss_20b_climate_evaluation_logs.log 2>&1"
 
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
