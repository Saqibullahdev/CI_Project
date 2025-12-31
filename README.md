# RAG AI Assistant - Python Backend

This is a Retrieval-Augmented Generation (RAG) application migrated to Python using FastAPI. It allows users to upload PDF documents, index them, and chat with an AI assistant that uses the document's content for context.

## 🚀 Features

- **FastAPI Backend**: High-performance, asynchronous Python web framework.
- **RAG Pipeline**: Powered by LangChain for document processing and retrieval.
- **Google Gemini**: Uses `gemini-2.0-flash` for high-quality responses and `text-embedding-004` for vector embeddings.
- **User Authentication**: Secure JWT-based registration and login system.
- **MongoDB**: Persistent storage for user data and chat history using Motor (async driver).
- **Usage Tracking**: Monitors token usage and chat counts for each user.
- **Dynamic System Prompts**: Toggle between different industry-specific personas (Legal, HR, Medical, etc.).

## 🛠️ Prerequisites

- **Python 3.10+**
- **MongoDB**: A running instance (local or Atlas)
- **Google AI API Key**: Get one from [Google AI Studio](https://aistudio.google.com/app/apikey)

## 📦 Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd rag-node-app
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory (or update the existing one):
   ```env
   PORT=3000
   MONGODB_URI=mongodb://localhost:27017/rag_app
   GOOGLE_API_KEY=your_actual_api_key_here
   JWT_SECRET=your_secret_jwt_key
   ```

## 🏃 Running the Application

Start the FastAPI server:
```bash
python main.py
```
Or use uvicorn directly:
```bash
uvicorn main:app --reload --port 3000
```

The application will be available at `http://localhost:3000`.

## 📖 API Documentation

FastAPI provides interactive documentation:
- **Swagger UI**: `http://localhost:3000/docs`
- **ReDoc**: `http://localhost:3000/redoc`

## 📁 Project Structure

```
├── main.py              # Main entry point
├── requirements.txt      # Python dependencies
├── src/
│   ├── auth.py          # JWT and Auth logic
│   ├── database.py      # MongoDB connection
│   ├── models.py        # Pydantic data models
│   ├── routes/          # API endpoints
│   └── services/        # Business logic & LangChain integrations
└── public/              # Frontend static files
```

## ⚖️ License

MIT
