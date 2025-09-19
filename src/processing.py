import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
# from langchain_ollama import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# paths
PDF_PATH = "data/knowledge_base/GRI_Standards.pdf"
DB_FAISS_PATH = "vector_store/faiss_index"

def create_vector_db():
    """
    This function creates a FAISS vector store from a PDF document.
    """
    print("Starting the vector database process...")

    # load the PDF document
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"Successfully loaded {len(documents)} pages from the PDF.")

    # split the document into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)
    print(f"Split the document into {len(docs)} chunks.")

    # embeddings for the chunks

    # embeddings = OpenAIEmbeddings()
    # embeddings = OllamaEmbeddings(model="phi3:3.8b")

    # HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # FAISS vector store and save it locally
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(DB_FAISS_PATH)
    print(f"Vector store created and saved at: {DB_FAISS_PATH}")

if __name__ == "__main__":
    create_vector_db()