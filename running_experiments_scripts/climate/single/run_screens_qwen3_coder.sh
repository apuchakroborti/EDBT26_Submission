#!/bin/bash

# Define your screen session names and associated commands

declare -A jobs=(
  # only simple
  [job1]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.8 --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_08_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # simple with only corrector
  [job2]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.8 --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_08_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # simpl with both corrector and RAG
  [job3]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.8 --errors True --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_08_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # only detailed
  [job4]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.8 --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_08_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  
  
  # [job4]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --errors True --rag True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/deepseek_r1_32b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # [job7]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --rag True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/deepseek_r1_32b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  # [job8]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.8 -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_08_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1"
  # [job9]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model deepseek-r1:32b --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/deepseek_r1_32b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1"

  # only simple
  [job5]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.6 --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_06_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # simple with only corrector
  [job6]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.6 --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_06_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # simpl with both corrector and RAG
  [job7]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.6 --errors True --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_06_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # only detailed
  [job8]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.6 --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_06_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  
  # only simple
  [job9]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.4 --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_04_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # simple with only corrector
  [job0]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.4 --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_04_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # simpl with both corrector and RAG
  [job1]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.4 --errors True --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_04_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # only detailed
  [job2]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.4 --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_04_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  
  # only simple
  [job3]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.2 --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_02_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # simple with only corrector
  [job4]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.2 --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_02_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # simpl with both corrector and RAG
  [job5]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.2 --errors True --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_02_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # only detailed
  [job6]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.2 --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_02_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  
  # only simple
  [job7]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.0 --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_00_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # simple with only corrector
  [job8]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.0 --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_00_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # simpl with both corrector and RAG
  [job9]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.0 --errors True --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_00_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # only detailed
  [job0]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://localhost:11434/api/generate --model qwen3-coder:30b --temp 0.0 --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/qwen3_coder_30b_temp_00_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  

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

echo "Starting final Python screen session..."
screen -dmS final_python_ bash -c "python3 ./prompting_techniques/zero_shot_sci_data_prompting/data_moving_for_each_single_phase_run.py --model qwen3_coder_30b --dataset climate"

# Wait for Python screen to finish
while screen -ls | grep -q "\.final_python_"; do
    sleep 5
done

echo "Final Python job completed."