# app/memory.py

from langchain_core.documents import Document
from utils.vectorstore import add_documents_to_vectorstore

def embed_chat_to_vector_db(vector_store, question, answer, user_id=None):
    text = f"Q: {question}\nA: {answer}"
    metadata = {
        "source": "chat_history",
        "user_id": user_id
    }
    doc = Document(page_content=text, metadata=metadata)
    updated_vectorstore = add_documents_to_vectorstore(vector_store, [doc])
    return updated_vectorstore
