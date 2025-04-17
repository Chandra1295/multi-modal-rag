# import os
# import gc
# import logging
# import asyncio
# import nest_asyncio
# import streamlit as st
# from utils.parse_pdf import process_pdf, validate_pdf
# from utils.vectorstore import init_vectorstore, add_to_vectorstore
# from utils.rag_chain import setup_rag_chain, generate_answer

# nest_asyncio.apply() 
# # Configure logging
# if not os.path.exists("logs"):
#     os.makedirs("logs")

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler("logs/app.log"),
#         logging.StreamHandler(),
#         logging.handlers.RotatingFileHandler(
#             "logs/app.log", maxBytes=1e6, backupCount=3
#         )
#     ]
# )

# def main():
#     st.set_page_config(
#         page_title="Multimodal PDF Assistant",
#         page_icon="📄",
#         layout="centered"
#     )
    
#     st.title("📄 Multimodal PDF Assistant")
    
#     # Initialize components
#     try:
#         vector_store = init_vectorstore()
#         rag_chain = setup_rag_chain()
#     except Exception as e:
#         st.error(f"Initialization failed: {str(e)}")
#         return

#     # Sidebar settings
#     with st.sidebar:
#         st.header("Settings")
#         temperature = st.slider("Response Creativity", 0.0, 1.0, 0.3)
#         num_results = st.slider("Retrieved Chunks", 1, 5, 2)
#         st.divider()
#         st.caption("System Status: Operational")

#     # File processing
#     uploaded_file = st.file_uploader(
#         "Upload PDF (max 50MB)",
#         type="pdf",
#         accept_multiple_files=False
#     )

#     if uploaded_file:
#         try:
#             validate_pdf(uploaded_file)
            
#             with st.status("Processing document...", expanded=True) as status:
#                 # Save to temp file
#                 os.makedirs("temp", exist_ok=True)
#                 temp_path = f"temp/{uploaded_file.name}"
                
#                 with open(temp_path, "wb") as f:
#                     f.write(uploaded_file.getbuffer())
                
#                 # Process PDF
#                 st.write("Extracting content...")
#                 content = process_pdf(temp_path)
                
#                 if content:
#                     st.write("Indexing document...")
#                     add_to_vectorstore(vector_store, content)
#                     status.update(label="Processing complete", state="complete")
#                     st.success("Document ready for queries!")
#                     st.session_state['vector_store'] = vector_store
#                 else:
#                     st.error("No extractable content found")
                
#                 os.remove(temp_path)  # Cleanup
                
#         except Exception as e:
#             st.error(f"Error: {str(e)}")
#         finally:
#             gc.collect()

#     # Question answering
#     if 'vector_store' in st.session_state:
#         question = st.chat_input("Ask about the document...")
#         if question:
#             try:
#                 with st.spinner("Generating answer..."):
#                     answer = generate_answer(
#                         rag_chain,
#                         st.session_state.vector_store,
#                         question,
#                         k=num_results
#                     )
#                     st.chat_message("assistant").write(answer)
#             except Exception as e:
#                 st.error(f"Error generating answer: {str(e)}")

# if __name__ == "__main__":
#     main()


import os
import gc
import logging
import asyncio
import nest_asyncio
import streamlit as st
from utils.parse_pdf import process_pdf, validate_pdf
from utils.vectorstore import init_vectorstore, add_to_vectorstore, get_retriever
from utils.rag_chain import setup_rag_chain, generate_answer

nest_asyncio.apply() 

# Configure logging
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler(),
        logging.handlers.RotatingFileHandler(
            "logs/app.log", maxBytes=1e6, backupCount=3
        )
    ]
)

def main():
    st.set_page_config(
        page_title="Multimodal PDF Assistant",
        page_icon="📄",
        layout="centered"
    )
    
    st.title("📄 Multimodal PDF Assistant")
    
    # Initialize components
    try:
        vector_store = init_vectorstore()
        rag_chain = setup_rag_chain()
    except Exception as e:
        st.error(f"Initialization failed: {str(e)}")
        return

    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        temperature = st.slider("Response Creativity", 0.0, 1.0, 0.3)
        num_results = st.slider("Retrieved Chunks", 1, 5, 2)
        search_type = st.selectbox(
            "Search Strategy",
            ["similarity", "mmr", "similarity_score_threshold"],
            index=0
        )
        st.divider()
        st.caption("System Status: Operational")

    # File processing
    uploaded_file = st.file_uploader(
        "Upload PDF (max 50MB)",
        type="pdf",
        accept_multiple_files=False
    )

    if uploaded_file:
        try:
            validate_pdf(uploaded_file)
            
            with st.status("Processing document...", expanded=True) as status:
                # Save to temp file
                os.makedirs("temp", exist_ok=True)
                temp_path = f"temp/{uploaded_file.name}"
                
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process PDF
                st.write("Extracting content...")
                content = process_pdf(temp_path)
                
                if content:
                    st.write("Indexing document...")
                    vector_store = add_to_vectorstore(vector_store, content)
                    
                    # Initialize retriever after adding documents
                    retriever = get_retriever(
                        vector_store,
                        search_type=search_type,
                        search_kwargs={"k": num_results}
                    )
                    
                    status.update(label="Processing complete", state="complete")
                    st.success("Document ready for queries!")
                    
                    # Store in session state
                    st.session_state['retriever'] = retriever
                else:
                    st.error("No extractable content found")
                
                os.remove(temp_path)  # Cleanup
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            gc.collect()

    # Question answering
    if 'retriever' in st.session_state:
        question = st.chat_input("Ask about the document...")
        if question:
            try:
                with st.spinner("Generating answer..."):
                    # Use the retriever from session state
                    docs = st.session_state.retriever.invoke(question)
                    context = "\n\n".join([d.page_content for d in docs])
                    
                    answer = rag_chain.invoke({
                        "question": question,
                        "context": context
                    })
                    
                    st.chat_message("assistant").write(answer)
                    
                    # Optional: Show retrieved chunks
                    with st.expander("See retrieved context"):
                        for i, doc in enumerate(docs, 1):
                            st.markdown(f"**Chunk {i}** (Score: {doc.metadata.get('score', 'N/A')})")
                            st.text(doc.page_content[:300] + "...")
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")

if __name__ == "__main__":
    main()