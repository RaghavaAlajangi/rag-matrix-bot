# 🔎 RAG Matrix Bot

<!-- [![CI](https://github.com/RaghavaAlajangi/rag-matrix-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/RaghavaAlajangi/rag-matrix-bot/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/RaghavaAlajangi/rag-matrix-bot/branch/main/graph/badge.svg?token=Z4FAPNDJWN)](https://codecov.io/gh/RaghavaAlajangi/rag-matrix-bot) -->

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-brightgreen)](https://www.langchain.com/)
[![Qdrant](https://img.shields.io/badge/Vector%20DB-Qdrant-orange)](https://qdrant.tech/)
[![Redis](https://img.shields.io/badge/ChatSessions-Redis-red)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-informational)](https://www.docker.com/)
[![License](https://img.shields.io/github/license/RaghavaAlajangi/rag-matrix-bot)](LICENSE)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-Swagger_UI-green?logo=swagger)](http://localhost:8000/docs)


> ⚡ A modular **Retrieval-Augmented Generation (RAG)** stack with **FastAPI backend**, **Matrix bot integration**, and **data ingestion pipeline** using Qdrant.  

---

## 📌 Features
- 📂 **Data Ingestion** → Upload & index documents into **Qdrant**  
- 🤖 **Matrix Bot** → Chat with the RAG system inside **Matrix rooms**  
- 🚀 **FastAPI Backend** → Serve embeddings, retrieval & generation endpoints  
- 🔑 **Session Management** → Powered by **Redis**  
- 🐳 **Containerized** with Docker Compose  
- 📝 Built with **LangChain, OpenAI, Docling, Qdrant**  

---


## 📂 Project Structure
```
├── rag_backend/        # FastAPI app (RAG endpoint)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│
├── matrixbot/          # Matrix Nio bot for chat interface and Redis session
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│
├── data_ingest/        # Ingest & index data into Qdrant
│   ├── requirements.txt
│   └── tests/
│
├── docker-compose.yml
└── README.md

```

## ⚙️ Setup & Run

#### 1️⃣ Clone repo
```
git clone https://github.com/yourname/rag-project.git
cd rag-project

```
#### 2️⃣ Environment variables

#### 3️⃣ Run with Docker Compose
```
docker-compose up --build
```

#### 4️⃣ Access services
- FastAPI docs → http://localhost:8000/docs
- Qdrant UI → http://localhost:6333/dashboard
- Matrix Bot → Join your Matrix room

## 🧪 Testing

## 🚀 Roadmap

- Support multiple LLM providers (Anthropic, DeepSeek, etc.)

-  Add PDF/Docx ingestion pipelines

-  Extend Matrix bot with custom commands

## 🤝 Contributing

PRs are welcome! Please follow conventional commits and run tests before submitting.