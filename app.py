
# import os
# import asyncio
# import time
# import nest_asyncio
# import streamlit as st

# st.set_page_config(page_title="Multimodal PDF Assistant", page_icon="📄", layout="centered")

# from app.helper import logger, monitor, get_or_create_user_id
# from app.core import initialize_system
# from app.cleanup import cleanup_resources
# from app.ui import sidebar_controls, show_chat_history
# from app.file_handler import handle_pdf_upload
# from app.chat import handle_chat
# from app.memory import embed_chat_to_vector_db

# # Apply async patches
# nest_asyncio.apply()
# if not hasattr(asyncio, '_nest_patched'):
#     asyncio._nest_patched = True
# os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
# os.environ['STREAMLIT_SERVER_ENABLE_FILE_WATCHER'] = 'false'

# def main():
#     # Enable debug mode via URL
#     if st.query_params.get("debug"):
#         st.session_state.debug_mode = True
    
#     st.title("Multimodal PDF Assistant")
    
#     # Initialize user session first
#     user_id = get_or_create_user_id()
#     st.session_state["user_id"] = user_id
#     st.write(f"User ID: {st.session_state['user_id']}")

    
#     # Debug output
#     if st.session_state.get("debug_mode"):
#         st.write(f"Debug: User ID = {user_id}")
    
#     # Load settings
#     temperature, num_results, search_type = sidebar_controls()
    
#     # Initialize system components
#     system_objects = initialize_system()
#     if not system_objects:
#         st.error("System initialization failed")
#         return
    
#     retriever, rag_chain, vector_store = system_objects
#     st.session_state.update({
#         "retriever": retriever,
#         "rag_chain": rag_chain,
#         "vector_store": vector_store
#     })
    
#     # Show chat history before handling new input
#     show_chat_history()
    
#     # Handle file upload and chat
#     uploaded_file = handle_pdf_upload(vector_store, num_results, search_type)

#     # Handle Q&A logic
#     question, answer = handle_chat(retriever, rag_chain, uploaded_file, vector_store=vector_store)

#     # NEW: Embed chat to vector DB
#     if question and answer:
#         embed_chat_to_vector_db(
#             vector_store=vector_store,
#             question=question,
#             answer=answer,
#             user_id=user_id
#         )


# if __name__ == "__main__":
#     # Initialize monitoring
#     monitor.start_time = time.time()
    
#     try:
#         # Windows-specific setup
#         if os.name == 'nt':
#             asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
#         # Cleanup and initialize
#         cleanup_resources()
#         logger.info("Application starting")
        
#         # Run main app
#         main()
        
#     except Exception as e:
#         logger.critical(f"Fatal error: {str(e)}", exc_info=True)
#         st.error("Critical application error. Please refresh.")
        
#     finally:
#         try:
#             cleanup_resources()
#             logger.info(f"Session completed in {time.time() - monitor.start_time:.2f}s")
#         except Exception as e:
#             logger.error(f"Cleanup error: {str(e)}")




import os
import asyncio
import time
import nest_asyncio
import streamlit as st

# Streamlit setup
st.set_page_config(page_title="Multimodal PDF Assistant", page_icon="📄", layout="centered")

# Import app modules
from app.helper import logger, monitor, get_or_create_user_id
from app.core import initialize_system
from app.cleanup import cleanup_resources
from app.ui import sidebar_controls, show_chat_history
from app.file_handler import handle_pdf_upload
from app.chat import handle_chat
from app.memory import embed_chat_to_vector_db

# Async patching
nest_asyncio.apply()
if not hasattr(asyncio, '_nest_patched'):
    asyncio._nest_patched = True

# Environment setup
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ['STREAMLIT_SERVER_ENABLE_FILE_WATCHER'] = 'false'

def main():
    # Debug mode
    if st.query_params.get("debug"):
        st.session_state.debug_mode = True

    st.title("📄 Multimodal PDF Assistant")

    # Session user ID
    user_id = get_or_create_user_id()
    st.session_state["user_id"] = user_id
    if st.session_state.get("debug_mode"):
        st.write(f"Debug Mode ON | User ID: {user_id}")

    # Sidebar settings
    temperature, num_results, search_type = sidebar_controls()

    # Initialize RAG + vector store
    system_objects = initialize_system()
    if not system_objects:
        st.error("❌ System initialization failed")
        return

    retriever, rag_chain, vector_store = system_objects
    st.session_state.update({
        "retriever": retriever,
        "rag_chain": rag_chain,
        "vector_store": vector_store
    })

    # Show previous chat history
    show_chat_history()

    # File upload + chunking
    uploaded_file = handle_pdf_upload(vector_store, num_results, search_type)

    # Handle chat (Q&A logic)
    question, answer = handle_chat(
        retriever=retriever,
        rag_chain=rag_chain,
        uploaded_file=uploaded_file,
        vector_store=vector_store  # ✅ embed into vectorstore here
    )

    # ✅ Save Q&A pair into vector store to enable recall
    if question and answer:
        embed_chat_to_vector_db(
            vector_store=vector_store,
            question=question,
            answer=answer,
            user_id=user_id
        )


if __name__ == "__main__":
    monitor.start_time = time.time()
    try:
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        cleanup_resources()
        logger.info("🚀 Application starting")
        main()

    except Exception as e:
        logger.critical(f"❗ Fatal error: {str(e)}", exc_info=True)
        st.error("Critical application error. Please refresh.")

    finally:
        try:
            cleanup_resources()
            logger.info(f"🧹 Session completed in {time.time() - monitor.start_time:.2f}s")
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}")
