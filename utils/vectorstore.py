
from typing import List, Optional
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document


def init_vectorstore() -> FAISS:
    """Initialize FAISS vector store with a dummy doc"""
    try:
        embeddings = OllamaEmbeddings(model="all-minilm")
        dummy_text = ["Initialize"]
        return FAISS.from_texts(texts=dummy_text, embedding=embeddings)
    except Exception as e:
        raise Exception(f"Vector store initialization failed: {str(e)}")


def add_to_vectorstore(vector_store: FAISS, chunks: List[str]) -> FAISS:
    """Add plain text chunks to the vector store (e.g., from PDF)"""
    try:
        new_vectorstore = FAISS.from_texts(texts=chunks, embedding=vector_store.embeddings)

        if len(vector_store.index_to_docstore_id) > 0:
            vector_store.merge_from(new_vectorstore)
        else:
            vector_store = new_vectorstore

        return vector_store
    except Exception as e:
        raise Exception(f"Failed to add text chunks: {str(e)}")


def add_documents_to_vectorstore(vector_store: FAISS, docs: List[Document]) -> FAISS:
    """Add langchain Document objects to the vector store (e.g., chat memory)"""
    try:
        new_vectorstore = FAISS.from_documents(documents=docs, embedding=vector_store.embeddings)

        if len(vector_store.index_to_docstore_id) > 0:
            vector_store.merge_from(new_vectorstore)
        else:
            vector_store = new_vectorstore

        return vector_store
    except Exception as e:
        raise Exception(f"Failed to add Document objects: {str(e)}")


def get_retriever(
    vector_store: FAISS,
    search_type: str = "similarity",
    search_kwargs: Optional[dict] = None
) -> BaseRetriever:
    """Create retriever from the vector store"""
    if search_kwargs is None:
        search_kwargs = {"k": 4}
    return vector_store.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs
    )
