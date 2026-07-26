# ☀️🧊 HVAC Technical Assistant

**A smart AI-powered chatbot for HVAC (Heating, ventilation and air conditioning) engineering guidance using RAG (Retrieval-Augmented Generation)**

[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)](https://hub.docker.com)
[![Azure](https://img.shields.io/badge/Azure-Originally_Deployed-0078D4?style=for-the-badge&logo=microsoft-azure)](https://azure.microsoft.com)
[![Render](https://img.shields.io/badge/Render-Backend-46E3B7?style=for-the-badge&logo=render)](https://render.com)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-DC2626?style=for-the-badge&logo=qdrant)](https://qdrant.tech)

## 🚀 Overview

The HVAC Technical Assistant is a full-stack application that demonstrates modern web technologies integrated with Generative AI to provide HVAC technical support and guidance. Built with a focus on user experience and scalability, it uses Retrieval-Augmented Generation (RAG) to deliver responses by combining technical HVAC documentation with GenAI-powered insights.

> ℹ️ **Quick Note**: Powered by technical HVAC documents processed into 670+ vector embeddings. Responses are intended as general engineering guidance.

---

## ☁️ Cloud Architecture & Deployment Evolution

This application demonstrates full-stack cloud engineering across multiple platforms:

### 🔹 Initial Deployment: Microsoft Azure (Azure Student Subscription)
- **Container Registry**: Azure Container Registry (ACR) for multi-stage Docker images.
- **Web App Hosting**: Azure Web Apps for Containers running FastAPI and Nginx React containers.
- **Database**: Dedicated containerized Qdrant Vector database on Azure.

### 🔹 Current Production Stack: Cost-Optimized Zero-Cost Architecture
To ensure high availability after the Azure Student Plan completed, the application architecture was optimized for a 100% free production tier:
- **Backend API**: Render.com Web Service (Python / FastAPI)
- **Vector Database**: Qdrant Cloud Free Tier (Managed Cosine Vector Indexing)
- **LLM Engine**: Google Gemini 1.5 Flash API / Smart RAG Fallback
- **Frontend Hosting**: Vercel Static Web Hosting

---

## ✨ Key Features

- **🤖 Intelligent AI Responses**: Powered by Google Gemini 1.5 Flash with context-aware RAG answer synthesis
- **📚 Document-Grounded Answers**: RAG implementation using 11 technical HVAC documents processed into 670+ vector embeddings
- **🎯 Smart Query Filtering**: Automatically detects and handles HVAC-related queries
- **💬 Real-time Chat Interface**: Responsive React frontend with professional UI/UX
- **🔍 Source Attribution**: Transparent source citations for all responses
- **🐳 Containerized Deployment**: Full Docker & Docker Compose support
- **🔒 Secure Secret Management**: Environment-variable based key management with zero hardcoded credentials

---

## 🛠️ Technical Architecture

```
                                 ┌───────────────────────────────┐
                                 │     Vercel / React Client     │
                                 └──────────────┬────────────────┘
                                                │
                                                ▼
┌──────────────────────────┐     ┌───────────────────────────────┐
│   Qdrant Cloud (Vector)  │ <── │ Render.com FastAPI Backend    │
│   (670+ HVAC Embeddings) │     │ (Gemini RAG Synthesis)        │
└──────────────────────────┘     └───────────────────────────────┘
```

---

## 🔐 Environment Variables & Security

To ensure safety, **no API keys or credentials are stored in this repository**. All secrets are handled via environment variables locally (via `.env`) or configured in host platform dashboards (Render / Vercel Secrets).

### Required Environment Variables

To run or deploy this application, configure the following variables:

| Variable | Description | Example |
| :--- | :--- | :--- |
| `QDRANT_URL` | Qdrant Cluster Endpoint | `https://your-cluster-id.cloud.qdrant.io` |
| `QDRANT_API_KEY` | Qdrant Cluster API Key | `your_qdrant_api_key` |
| `GEMINI_API_KEY` | Google Gemini API Key | `your_gemini_api_key` |

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/AP-047/hvac-assistant.git
cd hvac-assistant
```

### 2. Environment Setup
Create a `.env` file in the `backend/` directory:
```bash
# backend/.env
QDRANT_URL=https://your-qdrant-cluster.cloud.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Docker Compose Deployment (Recommended for Local Testing)
```bash
docker-compose up --build
```
Access the application:
- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`

### 4. Manual Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm start
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Developed by AP-047** | [Portfolio](https://github.com/AP-047) | [LinkedIn](https://www.linkedin.com/in/ap047)