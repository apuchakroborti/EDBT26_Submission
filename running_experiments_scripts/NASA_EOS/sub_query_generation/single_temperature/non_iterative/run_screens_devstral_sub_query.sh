#!/bin/bash

# Define your screen session names and associated commands

declare -A jobs=(
  [job49]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model devstral:24b --temp 0.0 --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/devstral_24b_temp_00_user_sub_queries_generation.log 2>&1"
  [job50]="python3 ./experiment_main/llm_code_generation_main.py --url http://localhost:11434/api/generate --model devstral:24b --temp 0.0 --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/devstral_24b_temp_00_user_sub_queries_generation_with_errors.log 2>&1"
 
)

# Run the entire model 4 times
for run in {1..4}; do
  echo "==============================="
  echo "   Starting FULL RUN $run"
  echo "==============================="

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


  echo "Starting Python scripts generation screen"
  screen -dmS ai_devstral bash -c './running_experiments_scripts/climate/single/run_screens_devstral.sh'

  # Wait for Python screen to finish
  while screen -ls | grep -q "\.ai_devstral"; do
      sleep 5
  done

  echo "Python scripts generation job completed."

done
echo "Python scripts generation for the devstral completed."
