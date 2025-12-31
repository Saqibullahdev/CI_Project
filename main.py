import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

from src.database import connect_db
from src.routes import auth_routes, chat_routes, upload_routes, prompt_routes

app = FastAPI(title="RAG Python Backend")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
async def startup_event():
    await connect_db()
    print("✓ Connected to MongoDB")
    
    # Check for API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_google_api_key_here":
        print("\n❌ ERROR: Google API Key is missing or invalid!")
        print("📝 Please update your .env file with a valid GOOGLE_API_KEY")
    else:
        print("✓ Google API Key detected")

# Include Routes
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(chat_routes.router, prefix="/api/chat", tags=["Chat"])
app.include_router(upload_routes.router, prefix="/api/upload", tags=["Upload"])
app.include_router(prompt_routes.router, prefix="/api/system-prompt", tags=["System Prompt"])

# Serve Static Files (Frontend)
app.mount("/", StaticFiles(directory="public", html=True), name="static")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
