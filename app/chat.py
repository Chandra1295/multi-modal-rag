
import time
import asyncio
import streamlit as st
from app.helper import logger
from app.db import save_chat
from app.memory import embed_chat_to_vector_db


def handle_chat(retriever, rag_chain, uploaded_file, vector_store=None):
    if 'retriever' not in st.session_state:
        return None, None

    question = st.chat_input("Ask about the document...")
    if question:
        with st.spinner("🧠 Generating answer..."):
            try:
                start_time = time.time()

                # 1. Search chat memory (similar previous Q&A)
                memory_docs = vector_store.similarity_search(question, k=2) if vector_store else []

                # 2. Search document chunks (e.g., from PDF)
                doc_chunks = st.session_state.retriever.invoke(question)
                combined_docs = memory_docs + doc_chunks

                # 3. Create context for LLM
                context = "\n\n".join([doc.page_content for doc in combined_docs])

                # 4. Generate answer via RAG
                answer = asyncio.run(rag_chain.ainvoke({"question": question, "context": context}))
                st.chat_message("assistant").write(answer)

                # 5. Save to DB
                user_id = st.session_state.get("user_id", "anonymous")
                save_chat(
                    user_id=user_id,
                    question=question,
                    answer=answer,
                    context=context,
                    source_file=uploaded_file.name if uploaded_file else "N/A"
                )

                # 6. Embed to vectorstore for memory
                if vector_store:
                    embed_chat_to_vector_db(vector_store, question, answer, user_id=user_id)

                # 7. Show context
                with st.expander("🔍 See retrieved context"):
                    for i, doc in enumerate(combined_docs, 1):
                        st.markdown(f"**Chunk {i}**")
                        st.text(doc.page_content[:300] + "...")

                return question, answer

            except Exception as e:
                logger.error(f"Q&A failed: {str(e)}", exc_info=True)
                st.error("Answer generation failed.")
                return question, None

    return None, None
