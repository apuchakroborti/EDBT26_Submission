#!/bin/bash

# Define your screen session names and associated commands

declare -A jobs=(
  # only simple
  [job21]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.8 --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_08_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # simple with only corrector
  [job22]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.8 --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_08_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # simpl with both corrector and RAG
  [job23]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.8 --errors True --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_08_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # only detailed
  [job24]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.8 --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_08_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  
  
  # [job4]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --errors True --rag True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # [job7]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --rag True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  # [job8]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.8 -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_08_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1"
  # [job9]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1"

  # only simple
  [job25]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.6 --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_06_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # simple with only corrector
  [job26]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.6 --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_06_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # simpl with both corrector and RAG
  [job27]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.6 --errors True --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_06_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # only detailed
  [job28]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.6 --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_06_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  
  # only simple
  [job29]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.4 --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_04_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # simple with only corrector
  [job30]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.4 --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_04_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # simpl with both corrector and RAG
  [job31]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.4 --errors True --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_04_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # only detailed
  [job32]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.4 --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_04_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  
  # only simple
  [job33]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.2 --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_02_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # simple with only corrector
  [job34]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.2 --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_02_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # simpl with both corrector and RAG
  [job35]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.2 --errors True --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_02_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # only detailed
  [job36]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.2 --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_02_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  
  # only simple
  [job37]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.0 --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_00_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  # simple with only corrector
  [job38]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.0 --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_00_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # simpl with both corrector and RAG
  [job39]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.0 --errors True --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_00_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  # only detailed
  [job40]="python3 ./experiment_main/llm_code_generation_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model gemma3:27b --temp 0.0 --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/gemma3_27b_temp_00_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  

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
screen -dmS final_python bash -c "python3 ./experiment_main/data_moving_for_each_single_phase_run.py --model gemma3_27b --dataset climate"

# Wait for Python screen to finish
while screen -ls | grep -q "\.final_python"; do
    sleep 5
done

echo "Final Python job completed."