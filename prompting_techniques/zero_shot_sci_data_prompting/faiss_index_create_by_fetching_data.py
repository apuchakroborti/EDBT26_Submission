import re
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# === Step 1: Load and Parse Chunks from File ===

def parse_chunks(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    raw_chunks = content.split("=== CHUNK START ===")
    chunks = []

    for raw in raw_chunks:
        if "=== CHUNK END ===" not in raw:
            continue

        # Extract parts
        title_match = re.search(r"Title:\s*(.+)", raw)
        explanation_match = re.search(r"Explanation:\s*(.*?)\nCode:", raw, re.DOTALL)
        code_match = re.search(r"Code:\s*(.+?)\s*$", raw, re.DOTALL)

        if not (title_match and explanation_match and code_match):
            continue

        title = title_match.group(1).strip()
        explanation = explanation_match.group(1).strip()
        code = code_match.group(1).strip()

        # Combine for embedding
        combined_text = f"Title: {title}\n\nExplanation:\n{explanation}\n\nCode:\n{code}"
        combined_text = combined_text.replace('=== CHUNK END ===', '')
        chunks.append({
            "title": title,
            "explanation": explanation,
            "code": code,
            "text": combined_text
        })
        # print(f'\n\ncombined_text:\n{combined_text}')
    return chunks


# === Step 2: Embed the Chunks ===

def embed_chunks(chunks, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings, chunks


# === Step 3: Create and Save FAISS Index ===

def create_faiss_index(embeddings, dim, index_path):
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))
    faiss.write_index(index, index_path)
    return index


# === Step 4: Save Metadata (Optional) ===

def save_metadata(chunks, metadat_path):
    np.save(metadat_path, chunks, allow_pickle=True)


# === RUN EVERYTHING ===

if __name__ == "__main__":
    PROJECT_BASE_PATH = "/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data" 
    h5py_doc_file_location = f"{PROJECT_BASE_PATH}/retrieval/notes/h5py_notes.txt"
    python3_numpy_doc_file_location = f"{PROJECT_BASE_PATH}/retrieval/notes/python3_numpy_notes.txt"
    matplotlib_basemap_cartopy_doc_file_location = f"{PROJECT_BASE_PATH}/retrieval/notes/matplotlib_basemap_cartopy_notes.txt"

    h5py_faiss_index_path = f"{PROJECT_BASE_PATH}/prompting_techniques/zero_shot_sci_data_prompting/faiss_index/h5py_projections_index.faiss"
    h5py_faiss_metadata_path = f"{PROJECT_BASE_PATH}/prompting_techniques/zero_shot_sci_data_prompting/faiss_metadata/h5py_projections_chunks_metadata.npy"

    python3_numpy_faiss_index_path = f"{PROJECT_BASE_PATH}/prompting_techniques/zero_shot_sci_data_prompting/faiss_index/python3_numpy_projections_index.faiss"
    python3_numpy_faiss_metadata_path = f"{PROJECT_BASE_PATH}/prompting_techniques/zero_shot_sci_data_prompting/faiss_metadata/python3_numpy_projections_chunks_metadata.npy"

    matplotlib_basemap_cartopy_faiss_index_path = f"{PROJECT_BASE_PATH}/prompting_techniques/zero_shot_sci_data_prompting/faiss_index/matplotlib_basemap_cartopy_projections_index.faiss"
    matplotlib_basemap_cartopy_faiss_metadata_path = f"{PROJECT_BASE_PATH}/prompting_techniques/zero_shot_sci_data_prompting/faiss_metadata/matplotlib_basemap_cartopy_projections_chunks_metadata.npy"


    # for h5py notes
    h5py_chunks = parse_chunks(h5py_doc_file_location)  # your input file
    h5py_embeddings, h5py_chunks = embed_chunks(h5py_chunks)
    
    h5py_dim = h5py_embeddings[0].shape[0]
    h5py_index = create_faiss_index(h5py_embeddings, h5py_dim, h5py_faiss_index_path)    
    save_metadata(h5py_chunks, h5py_faiss_metadata_path)
    print(f"✅ Created h5py_projections_index FAISS index with {len(h5py_chunks)} entries.")

    # for python3 numpy notes
    python3_numpy_chunks = parse_chunks(python3_numpy_doc_file_location)  # your input file
    python3_numpy_embeddings, python3_numpy_chunks = embed_chunks(python3_numpy_chunks)
    
    python3_numpy_dim = python3_numpy_embeddings[0].shape[0]
    python3_numpy_index = create_faiss_index(python3_numpy_embeddings, python3_numpy_dim, python3_numpy_faiss_index_path)    
    save_metadata(python3_numpy_chunks, python3_numpy_faiss_metadata_path)
    print(f"✅ Created python3_numpy_projections_index FAISS index with {len(python3_numpy_chunks)} entries.")

    # for matplotlib, basemap, and cartopy
    matplotlib_basemap_cartopy_chunks = parse_chunks(matplotlib_basemap_cartopy_doc_file_location)  # your input file
    matplotlib_basemap_cartopy_embeddings, matplotlib_basemap_cartopy_chunks = embed_chunks(matplotlib_basemap_cartopy_chunks)
    
    matplotlib_basemap_cartopy_dim = matplotlib_basemap_cartopy_embeddings[0].shape[0]
    matplotlib_basemap_cartopy_index = create_faiss_index(matplotlib_basemap_cartopy_embeddings, matplotlib_basemap_cartopy_dim, matplotlib_basemap_cartopy_faiss_index_path)    
    save_metadata(matplotlib_basemap_cartopy_chunks, matplotlib_basemap_cartopy_faiss_metadata_path)
    print(f"✅ Created matplotlib_basemap_cartopy_projections_index FAISS index with {len(matplotlib_basemap_cartopy_chunks)} entries.")