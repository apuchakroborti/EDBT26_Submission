import argparse

def parse_argument(parser):
    print('Inside argument parsar function ...')
    allowed_model_list = ["gpt-oss:20b", "qwen3-coder:30b", "deepseek-r1:32b", "devstral:24b", "gemma3:27b", "llama3:70b", "magicoder"]
    
    # Add arguments
    
    parser.add_argument(
        "--url", "-u",
        choices=["http://ai-lab2.dyn.gsu.edu:8081/api/generate", "http://localhost:11434/api/generate", 
                 "http://10.51.197.174:8080/api/generate", "http://10.51.197.174:11434/api/generate", "http://ai-lab2.dyn.gsu.edu:11434/api/generate"],
        required=False,
        default= "http://localhost:11434/api/generate",
        help="URL of the server"
    )
    
    parser.add_argument(
        "--model", "-m",
        # choices=["devstral:24b",  "gemma3:27b", "magicoder", "deepseek-r1:32b", "llama3:70b", "deepseek-coder-v2", "deepseek-r1:latest", "deepseek-r1:70b",  "qwen3:32b"],
        choices=allowed_model_list,
        required=True,
        help="Request to send into LLM model"
    )

    parser.add_argument(
        "--dataset", "-d",
        choices=[ "MATPLOTAGENT", "FASTMRIBRAIN", "CLIMATE", 
                "ITERATIVE_ERROR_RESOLVE_CLIMATE",
                "ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN_RAG",
                "ITERATIVE_ERROR_RESOLVE_MATPLOTAGENT_RAG",
                "ITERATIVE_ERROR_RESOLVE_VTK_RAG_IMAGE",

                "ITERATIVE_ERROR_RESOLVE_MATPLOTAGENT", "ITERATIVE_ERROR_RESOLVE_FASTMRIBRAIN", 
                 "FAST_MRI_BRAIN_WITH_USER_INTENT", 
                 "USER_INTENT_GENERATION_FROM_CLIMATE_RELATED_QUERIES", 
                 "USER_INTENT_GENERATION_FROM_FAST_MRI_BRAIN_RELATED_QUERIES", 
                #  sub query generation from user queries
                 "USER_SUB_QUERY_GENERATION_CLIMATE_DATASETS", "USER_SUB_QUERY_GENERATION_MATPLOTAGENT_DATASETS", "USER_SUB_QUERY_GENERATION_FASTMRIBRAIN_DATASETS",
                 
                #  python code generation
                 "CLIMATE_RAG",
                 "MATPLOTAGENT_RAG",
                 "FASTMRIBRAIN_RAG",
                 "VTK_RAG", 
                 
                #  evaluation
                 "CLIMATE_RAG_IMAGE",
                 "CLIMATE_RAG_IMAGE_WITH_TEMP",
                 "MATPLOTAGENT_RAG_IMAGE",
                 "FASTMRIBRAIN_RAG_IMAGE",
                 "VTK_RAG_IMAGE",

                 "ITERATIVE_CLIMATE_RAG_IMAGE",
                 "ITERATIVE_MATPLOTAGENT_RAG_IMAGE",
                 "ITERATIVE_FASTMRIBRAIN_RAG_IMAGE",
                 "ITERATIVE_ERROR_RESOLVE_VTK_RAG",
                                  

                 "VTK_USER_QUERY_GENERATION_VTK_DATASETS" 
                 ],
        required=True,
        help="Required for selecting datasets"
    )
    
    parser.add_argument(
        "--corrector", "-c",
        choices=[ 'True', 'False' ],
        required=False,
        help="Required for selecting corrector or not"
    )

    parser.add_argument(
        "--onlinesearch", "-os",
        choices=[ 'True', 'False' ],
        required=False,
        help="Required for searching online or not"
    )

    parser.add_argument(
        "--rag", "-r",
        choices=[ 'True', 'False' ],
        required=False,
        help="Required for selecting corrector or not"
    )

    # parser.add_argument(
    #     "--memory", "-mem",
    #     choices=[ 'True', 'False' ],
    #     required=False,
    #     help="Required for using LLM memory or not"
    # )
    parser.add_argument(
        "--errors", "-e",
        choices=[ 'True', 'False' ],
        required=False,
        help="Required for selecting user input queries"
    )

    parser.add_argument(
        "--temp", "-t",
        required=False,
        help="temperature value range 0.0(determinstic) to 2.0(non-determinstic)"
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    URL = 'http://localhost:11434/api/generate'
    if args.url and len(args.url)>0:
        URL = args.url
    
    model = ''
    model_name = ''
    if args.model and args.model in allowed_model_list:
        model = args.model

  
        
    model_name = model.replace('-', '_')
    model_name = model_name.replace(':', '_')
        
            
    dataset = ''
    if args.dataset and len(args.dataset)>0:
        dataset = args.dataset

   
    with_corrector = False
    if args.corrector == 'True':
        with_corrector = True
    
    is_rag = False
    if args.rag == 'True':
        is_rag = True

    # is_memory = False
    # if args.memory == 'True':
    #     is_memory = True

    is_errors = False
    if args.errors == 'True':
        is_errors = True

    is_online_search = False
    if args.onlinesearch == 'True':
        is_online_search = True

    temperature = 0.0
    if args.temp:
        temperature = float(args.temp)
    
    print(f'model: {model}')
    print(f'model_name: {model_name}')
    print(f'dataset: {dataset}')
    print(f'is_rag: {is_rag}')
    print(f'is_errors: {is_errors}')
    print(f'with_corrector: {with_corrector}')
    print(f'is_online_search: {is_online_search}')
    print(f'temperature: {temperature}')    

    return model, model_name, dataset, is_rag, URL, is_errors, with_corrector, is_online_search, temperature
