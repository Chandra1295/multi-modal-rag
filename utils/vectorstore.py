

# from langchain_ollama import OllamaEmbeddings
# from langchain_core.vectorstores import InMemoryVectorStore

# def init_vectorstore():
#     """Initialize vector store with embeddings"""
#     try:
#         embeddings = OllamaEmbeddings(model="all-minilm")
#         return InMemoryVectorStore(embeddings)
#     except Exception as e:
#         raise Exception(f"Vector store initialization failed: {str(e)}")

# def add_to_vectorstore(vector_store, chunks):
#     """Add processed chunks to vector store"""
#     try:
#         vector_store.add_texts(chunks)
#     except Exception as e:
#         raise Exception(f"Failed to add documents: {str(e)}")


from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.retrievers import BaseRetriever
from typing import List, Optional

def init_vectorstore() -> FAISS:
    """Initialize FAISS vector store with embeddings"""
    try:
        embeddings = OllamaEmbeddings(model="all-minilm")
        # Initialize empty FAISS index
        return FAISS.from_texts(
            texts=[""],  # Empty initial document
            embedding=embeddings
        )
    except Exception as e:
        raise Exception(f"Vector store initialization failed: {str(e)}")

def add_to_vectorstore(vector_store: FAISS, chunks: List[str]) -> FAISS:
    """Add processed chunks to vector store"""
    try:
        # Get existing embeddings
        embeddings = vector_store.embeddings
        
        # Create new FAISS instance with updated documents
        new_vectorstore = FAISS.from_texts(
            texts=chunks,
            embedding=embeddings
        )
        
        # Merge with existing store if needed
        if len(vector_store.index_to_docstore_id) > 1:  # More than just our initial empty doc
            vector_store.merge_from(new_vectorstore)
        else:
            vector_store = new_vectorstore
            
        return vector_store
    except Exception as e:
        raise Exception(f"Failed to add documents: {str(e)}")

def get_retriever(
    vector_store: FAISS,
    search_type: str = "similarity",
    search_kwargs: Optional[dict] = None
) -> BaseRetriever:
    """Create configured retriever from vector store"""
    if search_kwargs is None:
        search_kwargs = {"k": 4}  # Default to 4 retrieved chunks
        
    return vector_store.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs
    )