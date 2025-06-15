from app.helper import logger
from utils.vectorstore import init_vectorstore
from utils.rag_chain import setup_rag_chain

def initialize_system():
    try:
        vector_store = init_vectorstore()
        rag_chain = setup_rag_chain()
        logger.info("System initialized successfully")
        return None, rag_chain, vector_store  # retriever will be set later after PDF
    except Exception as e:
        logger.error(f"System initialization failed: {str(e)}")
        return None
