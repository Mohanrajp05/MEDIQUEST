" STEP 6: CONNECT TO THE LLM"


from langchain_groq import ChatGroq

from MEDIQUEST_ASSISTANT import config


def get_llm():
    return ChatGroq(model=config.LLM_MODEL_NAME, temperature=0)