#!/bin/bash

# Define your screen session names and associated commands

declare -A jobs=(
  [job41]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model qwen3-coder:30b --temp 0.8 --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/qwen3_coder_30b_temp_08_user_sub_queries_generation.log 2>&1"
  [job42]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model qwen3-coder:30b --temp 0.8 --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/qwen3_coder_30b_temp_08_user_sub_queries_generation_with_errors.log 2>&1"
  
  [job43]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model qwen3-coder:30b --temp 0.6 --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/qwen3_coder_30b_temp_06_user_sub_queries_generation.log 2>&1"
  [job44]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model qwen3-coder:30b --temp 0.6 --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/qwen3_coder_30b_temp_06_user_sub_queries_generation_with_errors.log 2>&1"
  
  [job45]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model qwen3-coder:30b --temp 0.4 --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/qwen3_coder_30b_temp_04_user_sub_queries_generation.log 2>&1"
  [job46]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model qwen3-coder:30b --temp 0.4 --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/qwen3_coder_30b_temp_04_user_sub_queries_generation_with_errors.log 2>&1"
  
  [job47]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model qwen3-coder:30b --temp 0.2 --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/qwen3_coder_30b_temp_02_user_sub_queries_generation.log 2>&1"
  [job48]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model qwen3-coder:30b --temp 0.2 --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/qwen3_coder_30b_temp_02_user_sub_queries_generation_with_errors.log 2>&1"
  
  [job49]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model qwen3-coder:30b --temp 0.0 --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/qwen3_coder_30b_temp_00_user_sub_queries_generation.log 2>&1"
  [job50]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model qwen3-coder:30b --temp 0.0 --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/qwen3_coder_30b_temp_00_user_sub_queries_generation_with_errors.log 2>&1"
 
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


echo "Starting Python scripts generation screen"
screen -dmS ai_qwen3_coder bash -c './running_experiments_scripts/climate/single/run_screens_qwen3_coder.sh'

# Wait for Python screen to finish
while screen -ls | grep -q "\.ai_qwen3_coder"; do
    sleep 5
done

echo "Python scripts generation job completed."
