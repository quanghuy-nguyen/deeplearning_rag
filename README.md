# Deep Learning RAG Agent
This project implements a simple Retrieval-Augmented Generation (RAG). This is a system which answers user questions based on context extracted from PDF documents. Combined document retrieval with language generation.

## 🔍 Key Techniques & Methods
    - Used Sentence Transformers (all mpnet-base-v2) to create embedding vectors of text chunks, enabling semantic similarity search.
    - Applied semantic search (vector similarity) with ChromaDB to retrieve the most relevant text passages.
    - Combined the retrieved context with the user query and passed it to an LLM for generating text.
    - Deployed on AWS for scalable and serverless inference.

## 📂 Project Structure

```text
deeplearning_rag/
RAG_API/
├── rag-cdk-infra/
│ └── ...
├── image/
│ ├── src/
│ │ ├── rag_app/
│ │ │  ├── embedding.py
│ │ │  ├── get_chroma_db.py
│ │ │  ├── query_rag.py
│ │ │  └── test.py
│ │ │
│ │ ├── app_api_handler.py
│ │ ├── app_work_handler.py
│ │ ├── create_vector_store.py
│ │ ├── query_model.py
│ │ └── save_embed_model.py
│ ├── Dockerfile
│ └── requirements.txt
└── README.md

```

