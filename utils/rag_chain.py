

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """You are a helpful document assistant. Answer based on the context.
Context: {context}
Question: {question}
Answer concisely and accurately. If unsure, say "I don't know"."""

def setup_rag_chain():
    """Initialize RAG components"""
    try:
        llm = OllamaLLM(
            model="llava:7b",
            temperature=0.3,
            num_ctx=2048
        )
        prompt = ChatPromptTemplate.from_template(template)
        return prompt | llm
    except Exception as e:
        raise Exception(f"Failed to initialize RAG chain: {str(e)}")

# def generate_answer(rag_chain, vector_store, question, k=2):
#     """Generate answer using RAG pipeline"""
#     try:
#         docs = vector_store.similarity_search(question, k=k)
#         context = "\n\n".join([d.page_content for d in docs])
#         return rag_chain.invoke({
#             "question": question,
#             "context": context[:3000]  # Context window limit
#         })
#     except Exception as e:
#         raise Exception(f"Answer generation failed: {str(e)}")

def generate_answer(rag_chain, source, question, k=2):
    """Handle both vector_store and retriever inputs"""
    if hasattr(source, 'invoke'):  # It's a retriever
        docs = source.invoke(question)
    else:  # It's a vector_store
        docs = source.similarity_search(question, k=k)
    
    context = "\n\n".join([d.page_content for d in docs])
    return rag_chain.invoke({"question": question, "context": context})