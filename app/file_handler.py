import os
import time
import gc
import streamlit as st
from utils.parse_pdf import process_pdf, validate_pdf
from utils.vectorstore import add_to_vectorstore, get_retriever
from app.helper import logger, monitor

def handle_pdf_upload(vector_store, num_results, search_type):
    uploaded_file = st.file_uploader("Upload PDF (max 50MB)", type="pdf")
    if uploaded_file:
        try:
            validate_pdf(uploaded_file)
            file_size = uploaded_file.size / (1024 * 1024)
            with st.status("Processing document...", expanded=True) as status:
                os.makedirs("temp", exist_ok=True)
                temp_path = f"temp/{int(time.time())}_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                content = process_pdf(temp_path)
                if content:
                    vector_store = add_to_vectorstore(vector_store, content)
                    retriever = get_retriever(vector_store, search_type=search_type, search_kwargs={"k": num_results})
                    st.session_state['retriever'] = retriever
                    status.update(label="✅ Processing complete", state="complete")
                    monitor.log_processing_time(uploaded_file.name, file_size)
                else:
                    st.error("No extractable content found.")
                os.remove(temp_path)
        except Exception as e:
            logger.error(f"PDF processing failed: {str(e)}")
            st.error(f"Processing failed: {str(e)}")
        finally:
            gc.collect()
        return uploaded_file
    return None
