import os
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from rag_app.embedding import get_embedding_fucntion


current_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(current_dir, "docs")
persist_dir = os.path.join(current_dir, "data", "vector_store")


if not os.path.exists(persist_dir):
    print(f"Initializing vector store at {persist_dir}...")

    if not os.path.exists(docs_dir):
        raise FileNotFoundError(f"Cannot find {docs_dir}")
    

    doc_files = [f for f in os.listdir(docs_dir) if f.endswith(".pdf")]
    documents = []


    print("Loading PDF files...")
    for doc_file in doc_files:
        file_dir = os.path.join(docs_dir, doc_file)
        loader = PyPDFLoader(file_dir, extract_images=True)
        document = loader.load()
        documents.extend(document) # Using extend because document has already been a list


    print("Splitting text...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    print(f"Number of chunks: {len(docs)}")


    print("Creating batches...")
    batch_size = 5460
    batches = [docs[i:i+batch_size] for i in range(0, len(docs), batch_size)]


    print("Getting embedding function...")
    embedding = get_embedding_fucntion()


    print(f"Creating vectore store at {persist_dir}")
    db = Chroma.from_documents(batches[0], persist_directory=persist_dir, embedding=embedding)
    for batch in batches[1:]:
        db.add_documents(batch)


    print(f"Finished creating vector store at {persist_dir}")


    