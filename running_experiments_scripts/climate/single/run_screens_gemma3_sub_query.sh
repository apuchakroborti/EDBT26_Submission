#!/bin/bash

# Define your screen session names and associated commands

declare -A jobs=(
  [job2]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model magicoder  --errors True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/magicoder_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  [job3]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model magicoder  --errors True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/magicoder_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  [job4]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model magicoder  --errors True --rag True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/magicoder_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_without_corrector.log 2>&1"
  [job5]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model magicoder  --errors True --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/magicoder_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector.log 2>&1"
  [job6]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model magicoder  --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/magicoder_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  [job7]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model magicoder --rag True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/magicoder_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_without_corrector.log 2>&1"
  [job8]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model magicoder -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/magicoder_python_scripts_without_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1"
  [job9]="python3 ./prompting_techniques/zero_shot_sci_data_prompting/sci_data_prompting_main.py --url http://ai-lab2.dyn.gsu.edu:8081/api/generate --model magicoder --rag True -c True --dataset CLIMATE_RAG > ./llm_rag_python_scripts_generation_logs/magicoder_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_corrector.log 2>&1"
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
