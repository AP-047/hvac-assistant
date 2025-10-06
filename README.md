# ☀️🧊 HVAC Design Assistant

**A smart AI-powered chatbot for HVAC engineering guidance using Retrieval-Augmented Generation (RAG)**

[![Live Demo](https://img.shields.io/badge/Live-Demo-blue?style=for-the-badge)](https://hvac-assistant.azurewebsites.net)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)](https://hub.docker.com)
[![Azure](https://img.shields.io/badge/Azure-Deployed-0078D4?style=for-the-badge&logo=microsoft-azure)](https://azure.microsoft.com)

## 🚀 Overview

The HVAC Design Assistant is a sophisticated full-stack application that combines modern web technologies with advanced AI to provide intelligent HVAC engineering consultations. Built with a focus on accuracy and user experience, it leverages Retrieval-Augmented Generation (RAG) to deliver contextually relevant responses backed by authoritative HVAC documentation.

## ✨ Key Features

- **🤖 Intelligent AI Responses**: Powered by Azure OpenAI with context-aware answer synthesis
- **📚 Document-Grounded Answers**: RAG implementation using 11 technical HVAC documents processed into 672+ vector embeddings
- **🎯 Smart Query Filtering**: Automatically detects and handles HVAC-related queries
- **💬 Real-time Chat Interface**: Responsive React frontend with professional UI/UX
- **🔍 Source Attribution**: Transparent source citations for all responses
- **🐳 Containerized Deployment**: Full Docker support with multi-stage builds
- **☁️ Cloud-Native**: Deployed on Azure with container registry integration
- **📱 Mobile-Responsive**: Optimized for all device sizes

## 🛠️ Technical Architecture

### Backend (FastAPI + Python)
- **Framework**: FastAPI with async/await patterns
- **AI Integration**: Azure OpenAI GPT-4 with custom prompt engineering
- **Vector Database**: Qdrant for semantic document search
- **Document Processing**: 11 technical HVAC documents processed into 672+ vector embeddings
- **Smart Retrieval**: Context-aware document filtering and relevance scoring

### Frontend (React + JavaScript)
- **Framework**: React 18 with modern hooks
- **Styling**: Custom CSS with responsive design
- **State Management**: React useState with real-time updates
- **HTML Rendering**: Safe HTML rendering with sanitization
- **UX Features**: Typing indicators, error handling, sample questions

### Infrastructure & DevOps
- **Containerization**: Multi-stage Docker builds for optimization
- **Cloud Platform**: Azure Web Apps for Containers
- **Container Registry**: Azure Container Registry with automated deployments
- **Database**: Qdrant vector database for document embeddings
- **CI/CD**: Docker-based deployment pipeline

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/AP-047/hvac-assistant.git
cd hvac-assistant
```

### 2. Environment Setup
```bash
# Backend environment
cd backend
cp .env.example .env
# Configure your Azure OpenAI and Qdrant credentials

# Frontend environment  
cd ../frontend
npm install
```

### 3. Docker Deployment (Recommended)
```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

### 4. Manual Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm start
```

## 🏗️ Project Structure

```
hvac-assistant/
├── 🐳 docker-compose.yml         # Multi-service orchestration
├── 📁 backend/
│   ├── 🐳 Dockerfile            # Python FastAPI container
│   ├── 📦 requirements.txt      # Python dependencies
│   └── 📁 app/
│       ├── 🚀 main.py           # FastAPI application entry
│       ├── 📁 routes/
│       │   └── 💬 chat.py       # Chat API endpoints
│       └── 📁 services/
│           ├── 🧠 llm.py        # AI response synthesis
│           └── 🔍 retrieval.py  # Document retrieval & filtering
├── 📁 frontend/
│   ├── 🐳 Dockerfile            # React production container
│   ├── 📦 package.json          # Node.js dependencies
│   └── 📁 src/
│       ├── ⚛️ App.js            # Main React component
│       └── 🎨 App.css           # Responsive styling
├── 📁 docs/sources/             # HVAC documentation corpus
└── 📁 scripts/
    └── 📊 ingest.py             # Document vectorization script
```

## 🔮 Future Enhancements

- [ ] **Multi-language Support**: Internationalization for global users
- [ ] **Advanced Filtering**: Filter by document type, date, or standard
- [ ] **User Authentication**: Personalized experience and usage tracking
- [ ] **Export Functionality**: Save conversations and generate reports
- [ ] **API Rate Limiting**: Enhanced security and usage management
- [ ] **Caching Layer**: Redis integration for improved response times

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Developed by AP-047** | [Portfolio](https://github.com/AP-047) | [LinkedIn](https://www.linkedin.com/in/ap047)

*Built with ❤️ for the HVAC engineering community*