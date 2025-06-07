import os
import shutil
import sys
from rag_app.embedding import get_embedding_fucntion

from langchain.vectorstores import Chroma


CHROMA_DB_INSTANCE = None
IS_USING_IMAGE_RUNTIME = os.environ.get("IS_USING_IMAGE_RUNTIME", None)

CHROMA_PATH = 'data/vector_store'


def get_chroma_db():
    global CHROMA_DB_INSTANCE
    if not CHROMA_DB_INSTANCE:
        if IS_USING_IMAGE_RUNTIME:
            __import__("pysqlite3")
            sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
            copy_chroma_to_tmp()
        
        CHROMA_DB_INSTANCE = Chroma(persist_directory=get_runtime_chroma_path(), 
                                    embedding_function=get_embedding_fucntion())
        print(f"Init ChromaDB from {CHROMA_PATH}")

    return CHROMA_DB_INSTANCE
    

def copy_chroma_to_tmp(): # Chroma (using SQLite) always requires write access – even if you only want read access.
    runtime_chroma_path = get_runtime_chroma_path()

    if not os.path.exists(runtime_chroma_path):
        os.makedirs(runtime_chroma_path)

    tmp_contents = os.listdir(runtime_chroma_path)
    if len(tmp_contents) == 0:
        print(f"Copying ChromaDB from {CHROMA_PATH} to {runtime_chroma_path}...")
        shutil.copytree(CHROMA_PATH, runtime_chroma_path, dirs_exist_ok=True)

    else: 
        print(f"ChromaDB has already exist at {runtime_chroma_path}")

    
def get_runtime_chroma_path():
    if IS_USING_IMAGE_RUNTIME:
        return f'/tmp/{CHROMA_PATH}'
    else:
        return CHROMA_PATH


