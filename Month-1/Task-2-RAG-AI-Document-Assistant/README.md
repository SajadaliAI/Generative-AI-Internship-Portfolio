# AI Document Assistant 📚

A Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask questions based on their content.

## Features

- Upload PDF, TXT, and DOCX files
- Extract and process document content
- Generate embeddings using HuggingFace
- Store embeddings in FAISS
- Retrieve relevant document chunks
- Ask questions using Google Gemini
- Provide answers based on uploaded documents

## Tech Stack

- Python
- Streamlit
- LangChain
- Google Gemini
- HuggingFace Embeddings
- FAISS

## How It Works

1. User uploads a document.
2. The document is loaded and split into chunks.
3. HuggingFace converts the chunks into embeddings.
4. Embeddings are stored in FAISS.
5. User asks a question.
6. Relevant chunks are retrieved using similarity search.
7. Google Gemini generates the final answer using the retrieved context.

## Installation

```bash
pip install -r requirements.txt


Run
streamlit run App.py