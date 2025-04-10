# RAG Chatbot using LangChain

## Project description

An AI chatbot with Retrieval-Augmented Generation (RAG) capabilities, 
supporting document uploads (PDF/DOCX/HTML), 
with usage of LLaMA models, and chat history persistence.

Project is based on an example described in 
[this article](https://blog.futuresmart.ai/building-a-production-ready-rag-chatbot-with-fastapi-and-langchain).

---

## Features
- Document upload and indexing
- Content-aware chat with history
- Support for LLaMA (via Ollama)
- Document deletion and management
- SQLite logging for auditability

---

## Tech Stack

|  Component  |              Technology              |
|:-----------:|:------------------------------------:|
|   Backend   |               FastAPI                |
|  Frontend   |              Streamlit               |
|  Vector DB  |               ChromaDB               |
|     NLP     | LangChain + HuggingFace/HFEmbeddings |
|   Models    |           LLaMA 3, LLaMA 2           |
|  Database   |               SQLite3                |

---

## Project structure

```
├── application_api/ # FastAPI backend
│ ├── utils/ # Chroma/LangChain utilities
│ ├── model/ # Pydantic validation models
│ └── api.py # API endpoints
├── ui/ # Streamlit frontend
│ ├── components/ # UI components
│ ├── utils/ # UI utils
│ └── streamlit_app.py # Streamlit app
├── requirements.txt # Dependencies
└── main.py # Streamlit app entry point
```

## API Endpoints

|  Endpoint   | Method |       Description       |
|:-----------:|:------:|:-----------------------:|
|      /      |  POST  |   Submit chat queries   | 
| /upload-doc |  POST  | Upload/index documents  | 
| /list-docs  |  GET   | List uploaded documents |
| /delete-doc |  POST  |  Delete document by ID  | 

---

## Setup & Installation

### 1. Clone repository

```bash
git clone https://github.com/oden73/RAG_Chatbot_with_LangChain.git
cd RAG_Chatbot_with_LangChain
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Required services

1. [Install Ollama](https://ollama.com/?spm=a2ty_o01.29997173.0.0.347bc9217JUT45)
2. Launch Ollama with ```ollama serve```
3. Install LLaMA models with ```ollama pull <model_name>```

## Usage

Start Backend
```bash
uvicorn application_api.api:app --reload --port 8000
```

Start Frontend
```bash
streamlit run main.py
```
