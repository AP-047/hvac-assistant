# ☀️🧊 HVAC Design Assistant

**A smart AI-powered chatbot for HVAC engineering guidance using Retrieval-Augmented Generation (RAG)**

[![Live Demo](https://img.shields.io/badge/Live-Demo-blue?style=for-the-badge)](https://hvac-assistant.azurewebsites.net)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)](https://hub.docker.com)
[![Azure](https://img.shields.io/badge/Azure-Deployed-0078D4?style=for-the-badge&logo=microsoft-azure)](https://azure.microsoft.com)

## 🚀 Overview

The HVAC Design Assistant is a sophisticated full-stack application that combines modern web technologies with advanced AI to provide intelligent HVAC engineering consultations. Built with a focus on accuracy and user experience, it leverages Retrieval-Augmented Generation (RAG) to deliver contextually relevant responses backed by authoritative HVAC documentation.

## ✨ Key Features

- **🤖 Intelligent AI Responses**: Powered by Azure OpenAI with context-aware answer synthesis
- **📚 Document-Grounded Answers**: RAG implementation using 672+ vectorized HVAC documents
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
- **Document Processing**: 672 HVAC documents vectorized and indexed
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

## 📋 Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+ with pip
- **Docker** and Docker Compose
- **Azure OpenAI** API access
- **Qdrant** vector database

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

## 🔧 API Documentation

### Chat Endpoint
```http
POST /api/chat
Content-Type: application/json

{
  "message": "What are the basics of HVAC system design?"
}
```

**Response:**
```json
{
  "response": "# HVAC System Design Basics\n\n**HVAC systems** integrate...",
  "sources": [
    {
      "filename": "HVAC_Design_Manual.pdf",
      "chunk_id": "chunk_123",
      "snippet": "HVAC system design involves..."
    }
  ]
}
```

## 🧠 AI & Machine Learning Features

- **Retrieval-Augmented Generation (RAG)**: Combines pre-trained LLM knowledge with domain-specific HVAC documents
- **Semantic Search**: Vector similarity search using sentence transformers
- **Context Synthesis**: Intelligent merging of retrieved documents with LLM-generated content
- **Query Classification**: Automatic detection of HVAC-related vs. general queries
- **Source Attribution**: Transparent citation of source documents for accountability

## 🎯 Use Cases

- **HVAC Engineers**: Quick reference for design standards and best practices
- **Students**: Learning resource with authoritative documentation
- **Consultants**: Rapid access to technical specifications and guidelines
- **Facility Managers**: Understanding system requirements and maintenance

## 🔮 Future Enhancements

- [ ] **Multi-language Support**: Internationalization for global users
- [ ] **Advanced Filtering**: Filter by document type, date, or standard
- [ ] **User Authentication**: Personalized experience and usage tracking
- [ ] **Export Functionality**: Save conversations and generate reports
- [ ] **API Rate Limiting**: Enhanced security and usage management
- [ ] **Caching Layer**: Redis integration for improved response times

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Technical Highlights

This project demonstrates proficiency in:

- **Full-Stack Development**: React frontend + FastAPI backend integration
- **AI/ML Engineering**: RAG implementation with vector databases
- **Cloud Architecture**: Azure deployment with container orchestration  
- **DevOps Practices**: Docker containerization and automated deployments
- **API Design**: RESTful API with proper error handling and documentation
- **Database Management**: Vector database optimization and query performance
- **UI/UX Design**: Responsive, accessible interface with modern design patterns

---

**Developed by AP-047** | [Portfolio](https://github.com/AP-047) | [LinkedIn](#)

*Built with ❤️ for the HVAC engineering community*