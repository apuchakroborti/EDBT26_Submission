# Project Setup Instructions

## 1. Environment Setup

```bash
pip3 install -r requirements.txt
```

When installing the `sentence-transformers` library using the command:

```bash
pip3 install -U sentence-transformers
```

The model `all-MiniLM-L6-v2` will be automatically downloaded and cached in your local system. To ensure the model is accessible for offline use, you can manually place it in a dedicated `models/` directory.
or
```bash
git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
mv all-MiniLM-L6-v2 target_directory/models
```

## 2. Data Collection and Preparation

### NASA EOS

1. Go to the [NASA HDF-EOS Examples Website](https://hdfeos.org/zoo/index_openGESDISC_Examples.php#AIRS).
2. Download datasets with any of the following extensions: `.h5`, `.H5`, `.he5`, `.HE5`, `.HDF5`, `.hdf5`.
3. Organize the data into directories using:

```bash
cd /path/to/this/project
mkdir ACL_DIR
mkdir -p ACL_DIR/ASF ACL_DIR/GES_DISC ACL_DIR/GHRC ACL_DIR/ICESat_2 ACL_DIR/LAADS ACL_DIR/LaRC ACL_DIR/LP_DAAC ACL_DIR/NSIDC ACL_DIR/Ocen_Biology ACL_DIR/PO_DAAC ACL_DIR/AURA_DATA_VC
```

4. Download associated Python scripts for ground truth generation and place them in the same directory (or update script paths accordingly).


### MatPlotAgent

1. Visit the [MatPlotAgent GitHub repo](https://github.com/thunlp/MatPlotAgent).
2. Download CSV files from the [`benchmark_data/data`](https://github.com/thunlp/MatPlotAgent/tree/main/benchmark_data/data) directory.
3. Create the data directory:

```bash
mkdir -p MatPlotAgent/benchmark_data/data
```

4. Convert the CSVs (12 files) to HDF5 format using:

```bash
python3 experiment_main/matplotagent_convert_csv_to_h5_data.py
```

5. Converted `.h5` files will be saved in:
   `MatPlotAgent/data_files`


### fastMRI

1. Go to the [fastMRI site](https://fastmri.med.nyu.edu/) and register with your email to receive dataset links.
2. Download the **Brain DICOM dataset** (\~38.8 GB).
3. Create a directory for the data:

```bash
mkdir -p fastMri/data_files/fastMRI_brain_DICOM
```

4. Move the downloaded DICOM files into that directory.
5. Convert DICOM to HDF5 using:

```bash
python3 fastMri/convert_dcm_to_h5.py
```

6. You’ll find `fastMRI_brain_first_10_dcm_to_h5.h5` in `fastMri/data_files`.

7. Duplicate the converted file to simulate per-query inputs:

```bash
cd fastMri/data_files
for i in {0..10}; do cp fastMRI_brain_first_10_dcm_to_h5.h5 ${i}_fastMRI_brain_first_10_dcm_to_h5.h5; done
```


## 3. LLM Installation with Ollama

1. Install [Ollama](https://ollama.com):

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. Install the required models:

```bash
ollama run devstral:24b
ollama run magicoder
ollama run llama3:70b
ollama run deepseek-r1:32b
ollama run gemma3:27b
```


## 4. Generate Sub-Queries from User Queries

### NASA EOS

```bash
bash ./running_experiments_scripts/NASA_EOS/run_screens_deepseek_r1_sub_query.sh
bash ./running_experiments_scripts/NASA_EOS/run_screens_devstral_sub_query.sh
bash ./running_experiments_scripts/NASA_EOS/run_screens_gemma3_sub_query.sh
bash ./running_experiments_scripts/NASA_EOS/run_screens_llama3_sub_query.sh
bash ./running_experiments_scripts/NASA_EOS/run_screens_magicoder_sub_query.sh
```

### MatPlotAgent

```bash
bash ./running_experiments_scripts/matplotagent/run_screens_deepseek_r1_matplotagent_sub_query.sh
bash ./running_experiments_scripts/matplotagent/run_screens_gemma3_matplotagent_sub_query.sh  
bash ./running_experiments_scripts/matplotagent/run_screens_devstral_matplotagent_sub_query.sh  
bash ./running_experiments_scripts/matplotagent/run_screens_magicoder_matplotagent_sub_query.sh
bash ./running_experiments_scripts/matplotagent/run_screens_llama3_matplotagent_sub_query.sh
```

### fastMRI

```bash
bash ./running_experiments_scripts/fastmribrain/run_screens_gemma3_fastmribrain_sub_query.sh
bash ./running_experiments_scripts/fastmribrain/run_screens_deepseek_r1_fastmribrain_sub_query.sh  
bash ./running_experiments_scripts/fastmribrain/run_screens_devstral_fastmribrain_sub_query.sh  
bash ./running_experiments_scripts/fastmribrain/run_screens_magicoder_fastmribrain_sub_query.sh
bash ./running_experiments_scripts/fastmribrain/run_screens_llama3_fastmribrain_sub_query.sh
```

## 5. Generate Python Scripts

### NASA EOS (Single Iteration)

```bash
bash ./running_experiments_scripts/NASA_EOS/run_screens_deepseek_r1.sh            
bash ./running_experiments_scripts/NASA_EOS/run_screens_devstral.sh            
bash ./running_experiments_scripts/NASA_EOS/run_screens_gemma3.sh            
bash ./running_experiments_scripts/NASA_EOS/run_screens_llama3.sh            
bash ./running_experiments_scripts/NASA_EOS/run_screens_magicoder.sh 
```

### NASA EOS (Iterative Error Resolution)

```bash
bash ./running_experiments_scripts/NASA_EOS/run_screens_devstral_iterative_code_generation.sh  
```

### MatPlotAgent (Single Iteration)

```bash
bash ./running_experiments_scripts/matplotagent/run_screens_deepseek_r1_matplotagent.sh            
bash ./running_experiments_scripts/matplotagent/run_screens_devstral_matplotagent.sh            
bash ./running_experiments_scripts/matplotagent/run_screens_magicoder_matplotagent.sh
bash ./running_experiments_scripts/matplotagent/run_screens_llama3_matplotagent.sh            
bash ./running_experiments_scripts/matplotagent/run_screens_gemma3_matplotagent.sh
```

### MatPlotAgent (Iterative Error Resolution)

```bash
bash ./running_experiments_scripts/matplotagent/run_screens_devstral_matplotagent_iterative.sh     
```

### fastMRI (Single Iteration)

```bash
bash ./running_experiments_scripts/fastmribrain/run_screens_deepseek_r1_fastmribrain.sh            
bash ./running_experiments_scripts/fastmribrain/run_screens_devstral_fastmribrain.sh
bash ./running_experiments_scripts/fastmribrain/run_screens_magicoder_fastmribrain.sh
bash ./running_experiments_scripts/fastmribrain/run_screens_llama3_fastmribrain.sh           
bash ./running_experiments_scripts/fastmribrain/run_screens_gemma3_fastmribrain.sh
```

### fastMRI (Iterative Error Resolution)

```bash
bash ./running_experiments_scripts/fastmribrain/run_screens_devstral_fastmribrain_iterative.sh     
```


## 6. Evaluation

### NASA EOS

* **Single Iteration Evaluation**

```bash
bash ./running_experiments_scripts/NASA_EOS/run_screens_devstral_single_iteration_code_evaluation.sh
```

* **Iterative Evaluation**

```bash
bash ./running_experiments_scripts/NASA_EOS/run_screens_devstral_iterative_code_evaluation.sh 
```

### MatPlotAgent

* **Single Iteration Evaluation**

```bash
bash ./running_experiments_scripts/matplotagent/run_screens_devstral_single_iteration_code_evaluation.sh
```

* **Iterative Evaluation**

```bash
bash ./running_experiments_scripts/matplotagent/run_screens_devstral_iterative_code_evaluation.sh 
```


### fastMRI

* **Single Iteration Evaluation**

```bash
bash ./running_experiments_scripts/fastmribrain/run_screens_devstral_single_iteration_code_evaluation.sh
```

* **Iterative Evaluation**

```bash
bash ./running_experiments_scripts/fastmribrain/run_screens_devstral_iterative_code_evaluation.sh 
```


## Evaluation Results

After running evaluations, results will be found in:

1. `NASA_EOS/evaluation_results`
2. `MatPlotAgent/error_categorization_evaluation_result`
3. `fastMri/error_categorization_evaluation_result`

## Similarity Score Generation By Comparing Extracted Images from the LLM-Generated Python Scripts and Ground Truth Images::

```bash
bash python3 ./experiment_main/evaluation_similarity_score_encoded_image_comparison.py
```

## Graph Generation
Figure 1: Execution results of data analysis/visualization codes generated by different LLMs using simple and de- tailed prompts (M1: Devstral-24B, M2: Magicoder-7B, M3: Llama3-70B, M4: Gemma3-27B, M5: DeepSeek-R1-70B).

```bash
bash python3 ./graph_generation/combined_3_datasets_simple_vs_expert.py
```

Figure 2: Execution results of data analysis/visualization codes generated by different LLMs using simple prompts without and with data-aware prompt disambiguation en- abled (M1: Devstral-24B, M2: Magicoder-7B, M3: Llama3- 70B, M4: Gemma3-27B, M5: DeepSeek-R1-70B).
```bash
bash python3 ./graph_generation/simple_query_combined_3_datasets_wc_vs_wo_c.py
```

Figure 3: Execution results of data analysis/visualization codes generated by different LLMs using simple prompts (data-aware prompt disambiguation is enabled by default) without and with retrieval-augmented prompt enhance- ment enabled (M1: Devstral-24B, M2: Magicoder-7B, M3: Llama3-70B, M4: Gemma3-27B, M5: DeepSeek-R1-32B).
```bash
bash python3 ./graph_generation/simple_query_combined_3_datasets_w_rag_vs_wo_rag.py
```

Figure 4: Execution results of data analysis/visualization codes generated by Devstral-24B using simple prompts (both data-aware prompt disambiguation and retrieval- augmented prompt enhancement are enabled by default) with different number of iterations.

```bash
bash python3 ./graph_generation/simple_query_combined_3_datasets_iterative_error_resolve.py
```