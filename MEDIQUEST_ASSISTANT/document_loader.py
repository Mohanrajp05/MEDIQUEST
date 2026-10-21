"Step1 read the raw data from the data folder."

from langchain_community.document_loaders import PyMuPDFLoader
from MEDIQUEST_ASSISTANT import config


def load_document(file_path: str = config.DATA_FILE_PATH):
    "Load a .txt file and return it as a list of Langchain Document"
    loader = PyMuPDFLoader(file_path)
    return loader.load()  