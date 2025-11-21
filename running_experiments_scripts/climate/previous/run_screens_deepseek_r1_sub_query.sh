#!/bin/bash

# Define your screen session names and associated commands

declare -A jobs=(
  [job2]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/deepseek_r1_32b_user_sub_queries_generation.log 2>&1"
  [job3]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/deepseek_r1_32b_user_sub_queries_generation_with_errors.log 2>&1"
 
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
