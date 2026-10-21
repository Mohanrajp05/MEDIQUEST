"All settings for the app live jere, in one place"


import os
from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")



## VECTOR STORES


#IN MEMORY 
# PERSISTENT MEMORY = stores vectors in 
# cloud memory = directly stores in cloud

VECTOR_STORE_PATH = os.path.join("data", 'faiss_index')

DATA_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "Disease and Disorder.pdf",
)


##MODELS 


LLM_MODEL_NAME = "openai/gpt-oss-120B"

EMBEDDING_MODEL_NAME ="jina-embeddings-v5-text-small"


##Chunk /TEXT SPLITTING CONFIG 

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50



# RETERIVAL RESULTS 
TOP_K_RESULTS = 5

##SYSTEM INSTRUCTIONS

SYSTEM_PROMPT = (
    "YOU ARE A MEDICAL ASSISTANT WHO WILL HELP TO KNOW ABOUT THEIR DISEASE AND DISORDER"

)


def _check_api_keys():
    "Stop early with a clear message if a required API key is missing"
    if not GROQ_API_KEY:
        raise RuntimeError("Missing GROQ_API_KEY. Please add it to your env")
    if not JINA_API_KEY:
        raise RuntimeError("Missing JINA_API_KEY. Please add it to your env")



