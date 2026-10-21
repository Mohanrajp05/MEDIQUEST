"STEP 3 TURN TEXT INTO VETORS USING JINA"


from langchain_community.embeddings import JinaEmbeddings

from MEDIQUEST_ASSISTANT import config

def get_embeddings_model():
    """
    RETURNS A JINA EMBEDDING MODELS
    
    """
    return JinaEmbeddings(model_name = config.EMBEDDING_MODEL_NAME)


