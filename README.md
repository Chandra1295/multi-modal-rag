# OllaRAG: Multimodal PDF Question Answering System


An end-to-end RAG pipeline that understands both text and images in PDFs using Ollama LLMs and FAISS vector search.

## Features

- **Multimodal Understanding**: Processes text, tables, and images from PDFs
- **Local AI**: Runs entirely with Ollama LLMs (no API calls)
- **Efficient Retrieval**: FAISS vector store for low-latency search
- **Streamlit UI**: Intuitive interface for document Q&A
- **Self-Healing**: Automatic cleanup of temporary resources
- **Persistent Chat History**: Stores Q&A interactions in PostgreSQL

##  Tech Stack

| Component          | Technology               |
|--------------------|--------------------------|
| LLM Runtime        | Ollama (`llava:7b`)      |
| Embeddings         | `all-minilm`             |
| Vector Store       | FAISS                    |
| PDF Processing     | `unstructured.io`        |
| Frontend           | Streamlit                |
| Persistence        | PostgreSQL (chat history)|
| Deployment         | Docker (optional)        |

## ⚙️ Installation

### Prerequisites

1. Install [Ollama](https://ollama.ai/) and pull required models:
```bash
ollama pull llava:7b
ollama pull all-minilm

2. Install PostgreSQL and create database:
```bash
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql -c "CREATE DATABASE ollarag;"
sudo service postgresql start
sudo -i -u postgres

