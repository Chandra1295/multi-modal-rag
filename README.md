# Multimodal PDF Assistant

A local RAG (Retrieval-Augmented Generation) system that processes PDFs with both text and image understanding capabilities, built with Streamlit, Ollama, and LangChain.

![App Screenshot](screenshot.png)

## Features

- **Multimodal Processing**: Extracts and understands text, images, and tables from PDFs
- **Local Execution**: Runs entirely on your machine using Ollama LLMs
- **Memory Efficient**: Optimized for systems with 4GB+ RAM
- **Privacy Focused**: No data leaves your local environment
- **Configurable**: Adjust chunk sizes, creativity, and retrieval parameters


## File Documentation

### 1. `app.py`
**Main Application Controller**
- Handles file uploads and UI interactions
- Coordinates the processing pipeline
- Manages error handling and user feedback

**Key Functions:**
- `main()`: Application entry point
- File validation and processing workflow
- Interactive Q&A interface

### 2. `utils/parse_pdf.py`
**PDF Processing Engine**
- Extracts text, images and tables from PDFs
- Validates input files
- Splits content into optimized chunks

**Key Functions:**
- `validate_pdf()`: Checks file type and size
- `extract_content_from_pdf()`: Core extraction logic
- `process_pdf()`: Orchestrates the parsing pipeline

### 3. `utils/vectorstore.py`
**Vector Database Management**
- Handles document embeddings and storage
- Manages memory-efficient vector operations

**Key Functions:**
- `init_vectorstore()`: Creates in-memory vector store
- `add_to_vectorstore()`: Indexes processed content
- Cached embedding model loading

### 4. `utils/rag_chain.py`
**Question Answering System**
- Generates answers using retrieved context
- Configurable response generation

**Key Functions:**
- `setup_rag_chain()`: Initializes the LLM pipeline
- `generate_answer()`: Retrieves context and generates responses
- Customizable prompt templates

## Installation

1. **Install Ollama**:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh


   ollama pull all-minilm
   ollama pull llava:7b

   uv venv 
   uv add -r requirements.txt