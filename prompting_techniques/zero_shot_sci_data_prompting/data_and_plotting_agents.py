import search_query_from_faiss_index as SEARCH_QUERY_AGENTS

def extract_second_subquery_blocks(file_path):
    """
    Extracts content for each of the three sub-query headers from their second occurrence in the file.

    Parameters:
        file_path (str): Path to the .txt file.

    Returns:
        dict: Dictionary with headers as keys and their associated block text as values.
    """
    headers = [
        "HDF5 Dataset Access Sub-query:",
        "NumPy Data Preprocessing Sub-query:",
        "Plotting and Visualization Sub-query:"
    ]

    with open(file_path, 'r') as file:
        content = file.read()

    result = {}
    # Store the second occurrence positions
    positions = []

    for header in headers:
        # Find all occurrences
        occurrences = [i for i in range(len(content)) if content.startswith(header, i)]
        if len(occurrences) < 2:
            raise ValueError(f"Header '{header}' occurs less than twice.")
        second_occurrence = occurrences[1]
        positions.append((header.rstrip(":"), second_occurrence))

    # Sort headers based on position in the text
    positions.sort(key=lambda x: x[1])

    for i, (header, start_idx) in enumerate(positions):
        end_idx = len(content)
        if i + 1 < len(positions):
            end_idx = positions[i + 1][1]
        # Slice text between current and next header
        section_text = content[start_idx + len(header) + 1:end_idx].strip()  # +1 for the colon
        result[header] = section_text
    print(f'Sub query_results: {result}')
    return result

# created May 18, 2025
def get_user_sub_query_by_file_name_and_sub_query_header(sub_query_base_name, sub_query_header, model_name, is_errors, dataset_name):
    try:
        project_base_path = "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data"
        print('Inside data and plotting agent:: get_user_sub_query_by_file_name_and_sub_query_header')
        print(f'sub query file base name: {sub_query_base_name}')
        print(f'sub query header name: {sub_query_header}')
        print(f'Dataset name: {dataset_name}')

        # sub_query_path = "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/user_queries/generated_user_sub_queries/llama3_70b_generated_user_sub_queries_from_expert_user_queries_final"
        sub_query_path = ''
        if is_errors == False:
            
            if dataset_name=="MATPLOTAGENT":
                sub_query_path = f"{project_base_path}/user_queries/generated_user_sub_queries/matplotagent/{model_name}_matplotagent_generated_user_sub_queries_from_expert_user_queries_final"
            elif dataset_name == "FASTMRIBRAIN":
                sub_query_path = f"{project_base_path}/user_queries/generated_user_sub_queries/fastmri_brain/{model_name}_fastmribrain_generated_user_sub_queries_from_expert_user_queries_final"
            # default CLIMATE
            else:
                sub_query_path = f"{project_base_path}/user_queries/generated_user_sub_queries/{model_name}_generated_user_sub_queries_from_expert_user_queries_final"

        else:
            if dataset_name == "MATPLOTAGENT":
                sub_query_path = f"{project_base_path}/user_queries/generated_user_sub_queries/matplotagent/{model_name}_matplotagent_generated_user_sub_queries_from_expert_user_queries_final_with_errors"
            elif dataset_name == "FASTMRIBRAIN":
                sub_query_path = f"{project_base_path}/user_queries/generated_user_sub_queries/fastmri_brain/{model_name}_fastmribrain_generated_user_sub_queries_from_expert_user_queries_final_with_errors"
            # default CLIMATE
            else:
                sub_query_path = f"{project_base_path}/user_queries/generated_user_sub_queries/{model_name}_generated_user_sub_queries_from_expert_user_queries_final_with_errors" 

        result_dic = extract_second_subquery_blocks(sub_query_path+'/'+sub_query_base_name)
        if len(result_dic)>0 and result_dic[sub_query_header]:
            print(f'Key: {sub_query_header}, Value:\n{result_dic[sub_query_header]}')
            return result_dic[sub_query_header]
        else:
            print('Result is empty for the below information:\n')
            print(f'Model name: {model_name}')
            print(f'sub query file base name: {sub_query_base_name}')
            print(f'sub query header name: {sub_query_header}')
    except Exception as e:
        print(f'Exception occurred while fetching sub queries, error message: {e}')
        raise Exception('No message for query Augmentation!')
# created May 18, 2025
# for query agmentation
def get_augmented_query(query_base_name, model_name, is_errors, dataset_name):
    print(f'data_and_plotting_agents::get_augmented_query, query_base_name: {query_base_name}')
    faiss_index_list = ['h5py', 'python3_numpy', 'matplotlib_basemap_cartopy']
    
    headers = [
        "HDF5 Dataset Access Sub-query",
        "NumPy Data Preprocessing Sub-query",
        "Plotting and Visualization Sub-query"
    ]
    augmented_query = ''
    
    for header in headers:
        if header in 'HDF5 Dataset Access Sub-query':
            print('Header for Augmented Query:\n', header)
            
            try:
                dataset_sub_query = get_user_sub_query_by_file_name_and_sub_query_header(query_base_name, header, model_name, is_errors, dataset_name)+'\n'
                examples = SEARCH_QUERY_AGENTS.get_top_k_matching_results(dataset_sub_query, faiss_index_list[0])
                augmented_query+='Dataset and attribute access related examples:\n'
                augmented_query+=examples+'\n'
            except Exception as e:
                print('Exception occurred while fecthing data related to HDF5 Dataset Access Sub-query!')
                continue
            
            
        elif header in 'NumPy Data Preprocessing Sub-query':
            print('Header for Augmented Query:\n', header)
            
            try:
                numpy_python3 = get_user_sub_query_by_file_name_and_sub_query_header(query_base_name, header, model_name, is_errors, dataset_name)+'\n'
                examples = SEARCH_QUERY_AGENTS.get_top_k_matching_results(numpy_python3, faiss_index_list[1])
                augmented_query+='Dataset masking related examples:\n'
                augmented_query+=examples+'\n'
            except Exception as e:
                print('Exception occurred while fecthing data related to NumPy Data Preprocessing Sub-query!')
                continue

        elif header in 'Plotting and Visualization Sub-query':
            print('Header for Augmented Query:\n', header)
            
            try:
                plotting_and_visualizations_sub_query = get_user_sub_query_by_file_name_and_sub_query_header(query_base_name, header, model_name, is_errors, dataset_name)+'\n'
                examples = SEARCH_QUERY_AGENTS.get_top_k_matching_results(plotting_and_visualizations_sub_query, faiss_index_list[2])
                
                augmented_query+='Plotting and Visualization related examples:\n'
                augmented_query+=examples+'\n'
            except Exception as e:
                print('Exception occurred while fecthing data related to Plotting and Visualization Sub-query!')
                continue           
    
    print('Augmented Query:\n', augmented_query)
    return augmented_query
    
def get_augmented_query_for_matplotagent(query_base_name, model_name, is_errors):
    print(f'MATPLOTAGENT::data_and_plotting_agents::get_augmented_query, query_base_name: {query_base_name}')
    faiss_index_list = ['h5py', 'python3_numpy', 'matplotlib_basemap_cartopy']
    
    headers = [
        "HDF5 Dataset Access Sub-query",
        "NumPy Data Preprocessing Sub-query",
        "Plotting and Visualization Sub-query"
    ]
    augmented_query = ''
    
    for header in headers:
        if header in 'HDF5 Dataset Access Sub-query':
            print('Header for Augmented Query:\n', header)
            
            try:
                dataset_sub_query = get_user_sub_query_by_file_name_and_sub_query_header(query_base_name, header, model_name, is_errors)+'\n'
                examples = SEARCH_QUERY_AGENTS.get_top_k_matching_results(dataset_sub_query, faiss_index_list[0])
                augmented_query+='Dataset and attribute access related examples:\n'
                augmented_query+=examples+'\n'
            except Exception as e:
                print('Exception occurred while fecthing data related to HDF5 Dataset Access Sub-query!')
                continue
            
            
        elif header in 'NumPy Data Preprocessing Sub-query':
            print('Header for Augmented Query:\n', header)
            
            try:
                numpy_python3 = get_user_sub_query_by_file_name_and_sub_query_header(query_base_name, header, model_name, is_errors)+'\n'
                examples = SEARCH_QUERY_AGENTS.get_top_k_matching_results(numpy_python3, faiss_index_list[1])
                augmented_query+='Dataset masking related examples:\n'
                augmented_query+=examples+'\n'
            except Exception as e:
                print('Exception occurred while fecthing data related to NumPy Data Preprocessing Sub-query!')
                continue

        elif header in 'Plotting and Visualization Sub-query':
            print('Header for Augmented Query:\n', header)
            
            try:
                plotting_and_visualizations_sub_query = get_user_sub_query_by_file_name_and_sub_query_header(query_base_name, header, model_name, is_errors)+'\n'
                examples = SEARCH_QUERY_AGENTS.get_top_k_matching_results(plotting_and_visualizations_sub_query, faiss_index_list[2])
                
                augmented_query+='Plotting and Visualization related examples:\n'
                augmented_query+=examples+'\n'
            except Exception as e:
                print('Exception occurred while fecthing data related to Plotting and Visualization Sub-query!')
                continue           
    
    print('Augmented Query:\n', augmented_query)
    return augmented_query


   
def get_augmented_query_for_fastmribrain(query_base_name, model_name, is_errors):
    print(f'FASTMRIBRAIN::data_and_plotting_agents::get_augmented_query, query_base_name: {query_base_name}')
    faiss_index_list = ['h5py', 'python3_numpy', 'matplotlib_basemap_cartopy']
    
    headers = [
        "HDF5 Dataset Access Sub-query",
        "NumPy Data Preprocessing Sub-query",
        "Plotting and Visualization Sub-query"
    ]
    augmented_query = ''
    
    for header in headers:
        if header in 'HDF5 Dataset Access Sub-query':
            print('Header for Augmented Query:\n', header)
            
            try:
                dataset_sub_query = get_user_sub_query_by_file_name_and_sub_query_header(query_base_name, header, model_name, is_errors)+'\n'
                examples = SEARCH_QUERY_AGENTS.get_top_k_matching_results(dataset_sub_query, faiss_index_list[0])
                augmented_query+='Dataset and attribute access related examples:\n'
                augmented_query+=examples+'\n'
            except Exception as e:
                print('Exception occurred while fecthing data related to HDF5 Dataset Access Sub-query!')
                continue
            
            
        elif header in 'NumPy Data Preprocessing Sub-query':
            print('Header for Augmented Query:\n', header)
            
            try:
                numpy_python3 = get_user_sub_query_by_file_name_and_sub_query_header(query_base_name, header, model_name, is_errors)+'\n'
                examples = SEARCH_QUERY_AGENTS.get_top_k_matching_results(numpy_python3, faiss_index_list[1])
                augmented_query+='Dataset masking related examples:\n'
                augmented_query+=examples+'\n'
            except Exception as e:
                print('Exception occurred while fecthing data related to NumPy Data Preprocessing Sub-query!')
                continue

        elif header in 'Plotting and Visualization Sub-query':
            print('Header for Augmented Query:\n', header)
            
            try:
                plotting_and_visualizations_sub_query = get_user_sub_query_by_file_name_and_sub_query_header(query_base_name, header, model_name, is_errors)+'\n'
                examples = SEARCH_QUERY_AGENTS.get_top_k_matching_results(plotting_and_visualizations_sub_query, faiss_index_list[2])
                
                augmented_query+='Plotting and Visualization related examples:\n'
                augmented_query+=examples+'\n'
            except Exception as e:
                print('Exception occurred while fecthing data related to Plotting and Visualization Sub-query!')
                continue           
    
    print('Augmented Query:\n', augmented_query)
    return augmented_query




if __name__ == '__main__':
    sub_query_path = "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/user_queries/generated_user_sub_queries/llama3_70b_generated_user_sub_queries_from_expert_user_queries_final/1A.GPM.GMI.COUNT2021.20160105-S230545-E003816.010538.V07A.HDF5.txt"
    title_keyword = "HDF5 Dataset Access Sub-query:"
    # print(extract_subquery_content(sub_query_path, title_keyword))
    result_dic = extract_second_subquery_blocks(sub_query_path)

    for key in result_dic.keys():
        # print(f'Data: Key: {key}, Value: {result_dic[key]}')
        print(f'\n\n{result_dic[key]}\n\n')
    
    # headers = [
    #     "HDF5 Dataset Access Sub-query",
    #     "NumPy Data Preprocessing Sub-query",
    #     "Plotting and Visualization Sub-query"
    # ]
    # for title_keyword in headers:
    #     print(f'\n\nTitle: {title_keyword}')
    #     print(extract_subquery_content(sub_query_path, title_keyword))