"Step2 : chop the document into small, searchable chunks."


from langchain_text_splitters import RecursiveCharacterTextSplitter

from MEDIQUEST_ASSISTANT import config

def split_into_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = config.CHUNK_SIZE,
        chunk_overlap = config.CHUNK_OVERLAP
    )
    return text_splitter.split_documents(documents)