from langchain.embeddings import HuggingFaceEmbeddings

def get_embedding_fucntion():
    return HuggingFaceEmbeddings(model_name='all-mpnet-base-v2')