"STEP 4 : STORE CHUNK EMBEDDINGS IN FAISS SO WE CAN SEARCH THEM LATER"


import os 
from langchain_community.embeddings import JinaEmbeddings
from langchain_community.vectorstores import FAISS

from MEDIQUEST_ASSISTANT import config
from MEDIQUEST_ASSISTANT.embeddings import get_embeddings_model

# def get_embeddings_model():
#     "Return a Jina embeddings model"
#     "MY NAME IS MOHAN"

#     return JinaEmbeddings(model_name =config.get_embeddings_model)



# build vectorstore usinf faiss


def build_vector_store(chunks):

    """Embedded every chunk and build
    a searchable FAISS index in memory"""

    embeddings_model = get_embeddings_model()
    return FAISS.from_documents(chunks, embeddings_model)



## SAVE VECTOR_STORE 


def save_vector_store(vector_store, path : str= config.VECTOR_STORE_PATH):
    """Save faiss index to disk so we dont't have to 
    rebuild it every time"""
    vector_store.save_local(path)



def load_vector_store(path: str = config.VECTOR_STORE_PATH):
    embeddings_model = get_embeddings_model()
    return FAISS.load_local(path, embeddings_model, allow_dangerous_deserialization=True)





def vector_store_exists(path: str = config.VECTOR_STORE_PATH) -> bool:

    return os.path.exists(os.path.join(path, "index.faiss"))


def get_retriever(vector_store, k:int = config.TOP_K_RESULTS):
    return vector_store.as_retriever(search_kwargs={"k": k})



