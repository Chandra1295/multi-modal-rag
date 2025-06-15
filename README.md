# OllaRAG: Multimodal PDF Question Answering System

![Demo Screenshot](demo.gif) <!-- Add screenshot later -->

An end-to-end RAG pipeline that understands both text and images in PDFs using Ollama LLMs and FAISS vector search.

## Features

- **Multimodal Understanding**: Processes text, tables, and images from PDFs
- **Local AI**: Runs entirely with Ollama LLMs (no API calls)
- **Efficient Retrieval**: FAISS vector store for low-latency search
- **Streamlit UI**: Intuitive interface for document Q&A
- **Self-Healing**: Automatic cleanup of temporary resources

## Tech Stack

| Component               | Technology                          |
|-------------------------|-------------------------------------|
| LLM Runtime             | Ollama (llava:7b)                  |
| Embeddings              | all-minilm                         |
| Vector Store            | FAISS                              |
| PDF Processing          | unstructured.io                    |
| Frontend                | Streamlit                          |
| Deployment              | Docker (optional)                  |

## Installation

### Prerequisites

1. Install [Ollama](https://ollama.ai/) and pull required models:
```bash
ollama pull llava:7b
ollama pull all-minilm