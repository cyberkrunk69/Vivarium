#!/usr/bin/env python3
import json, faiss, numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-mpnet-base-v2')
with open('learned_lessons.json') as f:
    lessons = json.load(f)

vectors = model.encode([l['content'] for l in lessons], show_progress_bar=True)
dim = vectors.shape[1]
index = faiss.IndexFlatIP(dim)          # inner product = cosine after norm
faiss.normalize_L2(vectors)
index.add(vectors)

# Persist
faiss.write_index(index, 'knowledge_index.faiss')
# Save metadata mapping (id ↔ position) separately