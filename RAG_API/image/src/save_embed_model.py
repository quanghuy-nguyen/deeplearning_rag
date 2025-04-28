from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

model.save_pretrained('./all-mpnet-base-v2')