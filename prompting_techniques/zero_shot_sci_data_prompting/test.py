import sci_data_prompting_main as sci_main

list_dirs = [
        "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/user_queries/generated_user_sub_queries",
        "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/user_sub_query_generation_logs",
        "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/llm_rag_generated_python_scripts",
        "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/llm_rag_python_scripts_generation_logs"
        ]
model_name = "gpt_oss_20b"
prefix = "single_phase"
sci_main.move_prefixed_items(list_dirs, model_name, prefix)