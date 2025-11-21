import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def get_top_k_matching_results(query, index_name):
   try:
      print('Inside search query from faiss index::get_top_k_matching_results ...')
      PROJECT_BASE_PATH = "/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data" 
      
      faiss_index_path = ''
      faiss_metadata_path = ''
      if index_name in ['h5py', 'python3_numpy', 'matplotlib_basemap_cartopy']:   
         faiss_index_path = f"{PROJECT_BASE_PATH}/prompting_techniques/zero_shot_sci_data_prompting/faiss_index/{index_name}_projections_index.faiss"
         faiss_metadata_path = f"{PROJECT_BASE_PATH}/prompting_techniques/zero_shot_sci_data_prompting/faiss_metadata/{index_name}_projections_chunks_metadata.npy"
      else:
         print('Index name not matched!')
         return ''
      # Load index and metadata
      index = faiss.read_index(faiss_index_path)
      chunks = np.load(faiss_metadata_path, allow_pickle=True)

      # Load embedding model
      # model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/models')
      # model = SentenceTransformer("all-MiniLM-L6-v2")
      # model = SentenceTransformer('/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/models/all-MiniLM-L6-v2')
      # model = SentenceTransformer('/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/models/models--sentence-transformers--all-MiniLM-L6-v2')
      model = SentenceTransformer('/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/models/models--sentence-transformers--all-MiniLM-L6-v2/snapshots/c9745ed1d9f207416be6d2e6f8de32d1f16199bf')

      
      query_embedding = model.encode([query])
      # top 3 results
      # D, I = index.search(np.array(query_embedding).astype("float32"), k=3)

      # top one result
      D, I = index.search(np.array(query_embedding).astype("float32"), k=1)

      retrived_results = ''
      # Retrieve top results
      for idx in I[0]:
         print(chunks[idx]['text'])  # or show title/code/etc.
         retrived_results+=chunks[idx]['text']+'\n'
      print(f'Retrived results: {retrived_results}')
      return retrived_results
   except Exception as e:
      print('Exception occurred while searching data from faiss index: error: {e}')
      return ''

if __name__ == '__main__':
   # Query
   # query = "How to draw an azimuthal projection map?"
   query = """

   1. Import Libraries: The program begins by importing necessary libraries, including `os`, `matplotlib`, `matplotlib.pyplot`, `numpy`, `mpl_toolkits.basemap`, and `h5py`.

   2. Define HDF5 File Constant: Create a constant for the HDF5 file name to be read.

   3. Read Data from HDF5:
      - Open the specified HDF5 file.
      - Access the 'cloud Water' dataset located at '/Grid/cloudWater'.
      - Extract the 0th slice along the x-axis, retaining all y and z data.
      - Retrieve the units of the dataset.

   4. Data Processing:
      - Replace `_FillValue` with NaN using numpy's `where` function based on the 'cloudWater' data.
      - Apply a mask to the cloudWater data where values are NaN using numpy's `ma.masked_where`.

   5. Create Geolocation Data:
      - Manually construct longitude and latitude arrays since geolocation data is absent in the HDF5 file.
      - Longitude array: 1440 values from -179.875 to 179.875.
      - Latitude array: 720 values from -89.875 to 89.875.

   6. Set Up Map Visualization:
      - Initialize a map object with cylindrical projection and low resolution.
      - Set latitude limits from -90 to 90 and longitude limits from -180 to 180.

   7. Draw Map Elements:
      - Add coastlines with a line width of 0.5.
      - Draw parallels at latitudes [-90, 0, 90] and meridians at longitudes [-180, 0, 180], spaced every 45 degrees.
      - Label the parallels and meridians appropriately.

   8. Finalize Visualization:
      - Add a colorbar with a label set to the dataset's units.
      - Set the plot title using the HDF5 file name and dataset name without slashes.
   """
   # index name list: ['h5py', 'python3_numpy', 'matplotlib_basemap_cartopy']
   print(get_top_k_matching_results(query, 'matplotlib_basemap_cartopy'))