#!/bin/bash

# Define your screen session names and associated commands

declare -A jobs=(
  [job2]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model gemma3:27b --dataset USER_SUB_QUERY_GENERATION_MATPLOTAGENT_DATASETS > ./user_sub_query_generation_logs/gemma3_27b_matplotagent_user_sub_queries_generation.log 2>&1"
  # [job3]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model gemma3:27b --errors True --dataset USER_SUB_QUERY_GENERATION_MATPLOTAGENT_DATASETS > ./user_sub_query_generation_logs/gemma3_27b_matplotagent_user_sub_queries_generation_with_errors.log 2>&1"
 
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
