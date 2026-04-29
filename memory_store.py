import faiss
import numpy as np
from embedding_model import get_embedding

dimension = 384
index = faiss.IndexFlatL2(dimension)

documents = []

def add_memory(text):
    embedding = get_embedding(text)
    index.add(np.array([embedding]).astype("float32"))
    documents.append(text)

def search_memory(query, k=3):
    if len(documents) == 0:
        return []

    query_vector = get_embedding(query)
    D, I = index.search(np.array([query_vector]).astype("float32"), k)

    return [documents[i] for i in I[0] if i < len(documents)]