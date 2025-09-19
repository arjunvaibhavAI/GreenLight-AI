import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

DB_FAISS_PATH = "vector_store/faiss_index"

def get_retriever():
    """
    create and return a retriever object from the local FAISS vector store,
    using a local HuggingFace embedding model.
    """
    # vector store path exists
    if not os.path.exists(DB_FAISS_PATH):
        raise FileNotFoundError(f"Vector store not found at {DB_FAISS_PATH}")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    print("Retriever embeddings created successfully.")
    return retriever

# test the retriever directly
if __name__ == "__main__":
    print("testing the local retriever tool...")
    
    esg_retriever = get_retriever()
    
    query = "What are the disclosure requirements for GHG emissions?"
    
    relevant_docs = esg_retriever.invoke(query)
    
    print(f"\n--- Top search results for the query: '{query}' ---")
    
    # results
    for i, doc in enumerate(relevant_docs):
        print(f"\n--- Result {i+1} ---")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}, Page: {doc.metadata.get('page', 'Unknown')}")
        print(f"Content: {doc.page_content[:500]}...")