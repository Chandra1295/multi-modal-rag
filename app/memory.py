
from langchain_core.documents import Document
from utils.vectorstore import add_documents_to_vectorstore


def embed_chat_to_vector_db(vector_store, question, answer, user_id="anonymous"):
    """Embeds a single Q&A pair into the vector store as a memory"""
    try:
        content = f"Q: {question}\nA: {answer}"
        metadata = {"user_id": user_id}
        doc = Document(page_content=content, metadata=metadata)
        add_documents_to_vectorstore(vector_store, [doc])
    except Exception as e:
        raise Exception(f"Failed to embed chat memory: {str(e)}")
