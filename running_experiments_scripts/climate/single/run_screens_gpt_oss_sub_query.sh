#!/bin/bash

# Define your screen session names and associated commands

declare -A jobs=(
  [job1]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gpt-oss:20b --temp 0.8 --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/gpt_oss_20b_temp_08_user_sub_queries_generation.log 2>&1"
  [job2]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gpt-oss:20b --temp 0.8 --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/gpt_oss_20b_temp_08_user_sub_queries_generation_with_errors.log 2>&1"
  
  [job3]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gpt-oss:20b --temp 0.6 --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/gpt_oss_20b_temp_06_user_sub_queries_generation.log 2>&1"
  [job4]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gpt-oss:20b --temp 0.6 --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/gpt_oss_20b_temp_06_user_sub_queries_generation_with_errors.log 2>&1"
  
  [job5]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gpt-oss:20b --temp 0.4 --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/gpt_oss_20b_temp_04_user_sub_queries_generation.log 2>&1"
  [job6]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gpt-oss:20b --temp 0.4 --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/gpt_oss_20b_temp_04_user_sub_queries_generation_with_errors.log 2>&1"
  
  [job7]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gpt-oss:20b --temp 0.2 --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/gpt_oss_20b_temp_02_user_sub_queries_generation.log 2>&1"
  [job8]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gpt-oss:20b --temp 0.2 --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/gpt_oss_20b_temp_02_user_sub_queries_generation_with_errors.log 2>&1"
  
  [job9]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gpt-oss:20b --temp 0.0 --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/gpt_oss_20b_temp_00_user_sub_queries_generation.log 2>&1"
  [job10]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model gpt-oss:20b --temp 0.0 --errors True --dataset USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS > ./user_sub_query_generation_logs/gpt_oss_20b_temp_00_user_sub_queries_generation_with_errors.log 2>&1"
 
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
