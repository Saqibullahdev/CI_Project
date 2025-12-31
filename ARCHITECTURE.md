# Modularized Code Structure

## 📁 Project Structure

```
rag-node-app/
├── server.js                    # Entry point
├── config.js                    # System prompt configurations
├── .env                         # Environment variables
├── package.json                 # Dependencies
├── src/
│   ├── app.js                   # Main application setup
│   ├── services/                # Business logic layer
│   │   ├── embeddingService.js  # Google embeddings management
│   │   ├── chatService.js       # Gemini chat model
│   │   ├── documentService.js   # PDF processing & vector store
│   │   └── promptService.js     # System prompt management
│   ├── routes/                  # API endpoints
│   │   ├── upload.js            # POST /api/upload
│   │   ├── chat.js              # POST /api/chat
│   │   └── prompt.js            # GET/POST /api/system-prompt
│   └── middleware/              # Express middleware
│       ├── upload.js            # Multer file upload config
│       └── errorHandler.js      # Centralized error handling
├── public/                      # Frontend files
│   ├── index.html
│   ├── style.css
│   └── script.js
└── uploads/                     # Temporary PDF storage
```

## 🏗️ Architecture Overview

### **Separation of Concerns**

1. **Services Layer** (`src/services/`)
   - Contains all business logic
   - Manages AI models and document processing
   - Singleton pattern for state management

2. **Routes Layer** (`src/routes/`)
   - Handles HTTP requests/responses
   - Delegates to services for business logic
   - Thin controllers pattern

3. **Middleware Layer** (`src/middleware/`)
   - Request preprocessing (file uploads)
   - Error handling
   - Reusable across routes

## 📦 Module Descriptions

### **Services**

#### `embeddingService.js`
- Initializes Google Generative AI embeddings
- Singleton instance for embedding model
- Handles embedding generation for documents

```javascript
const embeddingService = require('./services/embeddingService');
await embeddingService.initialize(apiKey);
const embeddings = embeddingService.getEmbeddings();
```

#### `chatService.js`
- Manages Gemini chat model
- Generates responses based on prompts
- Configurable temperature and model version

```javascript
const chatService = require('./services/chatService');
chatService.initialize(apiKey);
const answer = await chatService.generateResponse(prompt);
```

#### `documentService.js`
- PDF parsing and text extraction
- Text chunking with RecursiveCharacterTextSplitter
- Vector store creation and similarity search
- Document lifecycle management

```javascript
const documentService = require('./services/documentService');
const chunks = await documentService.processPDF(filePath, embeddings);
const results = await documentService.searchSimilarDocuments(query, 4);
```

#### `promptService.js`
- System prompt management
- Preset and custom prompt handling
- Prompt template building

```javascript
const promptService = require('./services/promptService');
promptService.setPromptByPreset('customerSupport');
const prompt = promptService.buildPrompt(context, question);
```

### **Routes**

#### `upload.js`
- Handles PDF file uploads
- Processes documents through documentService
- Returns processing results

#### `chat.js`
- Receives user questions
- Retrieves relevant context from vector store
- Generates AI responses

#### `prompt.js`
- GET: Returns current prompt and available presets
- POST: Updates system prompt (preset or custom)
- GET /presets: Returns detailed preset information

### **Middleware**

#### `upload.js`
- Multer configuration for file uploads
- PDF validation
- File size limits (10MB)

#### `errorHandler.js`
- Centralized error handling
- Consistent error responses
- Logging

## 🔄 Request Flow

### Upload Flow
```
Client → upload.js (route) → documentService.processPDF() 
     → embeddingService.getEmbeddings() → Vector Store → Response
```

### Chat Flow
```
Client → chat.js (route) → documentService.searchSimilarDocuments()
     → promptService.buildPrompt() → chatService.generateResponse() → Response
```

## ✅ Benefits of Modularization

1. **Maintainability**
   - Each module has a single responsibility
   - Easy to locate and fix bugs
   - Clear code organization

2. **Testability**
   - Services can be unit tested independently
   - Mock dependencies easily
   - Isolated testing of business logic

3. **Scalability**
   - Easy to add new routes or services
   - Can swap implementations (e.g., different embedding providers)
   - Horizontal scaling friendly

4. **Reusability**
   - Services can be used across multiple routes
   - Middleware can be applied to any route
   - DRY principle enforced

5. **Readability**
   - Clear file structure
   - Logical grouping of related code
   - Self-documenting architecture

## 🔧 Adding New Features

### Add a New Route
1. Create file in `src/routes/`
2. Import required services
3. Define route handlers
4. Register in `src/app.js`

### Add a New Service
1. Create file in `src/services/`
2. Export singleton or class
3. Import in routes that need it

### Add New Middleware
1. Create file in `src/middleware/`
2. Export middleware function
3. Apply in `src/app.js` or specific routes

## 🧪 Testing (Future Enhancement)

Suggested structure:
```
tests/
├── unit/
│   ├── services/
│   ├── routes/
│   └── middleware/
└── integration/
    └── api/
```

## 📝 Notes

- All services use singleton pattern for state management
- Routes are thin and delegate to services
- Error handling is centralized
- Configuration is environment-based
- No breaking changes to API endpoints
