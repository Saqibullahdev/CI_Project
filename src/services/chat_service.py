import os
from langchain_google_genai import ChatGoogleGenerativeAI
from src.database import get_db
from src.models import MessageModel
from bson import ObjectId
from datetime import datetime

class ChatService:
    def __init__(self):
        self.chat_model = None

    def initialize(self, api_key: str):
        if not api_key:
            raise Exception("GOOGLE_API_KEY is required for chat functionality")
        
        self.chat_model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", # Updated to a common available version or matching Node's intent
            google_api_key=api_key,
            temperature=0.7
        )
        print("✓ Chat model initialized")

    async def generate_response(self, prompt: str):
        if not self.chat_model:
            # Auto-init if possible
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                self.initialize(api_key)
            else:
                raise Exception("Chat model not initialized")
        
        response = self.chat_model.invoke(prompt)
        return response.content

    async def save_message(self, user_id: str, role: str, content: str):
        db = get_db()
        message = {
            "userId": ObjectId(user_id),
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        }
        await db.messages.insert_one(message)

    async def get_recent_history(self, user_id: str, limit: int = 10):
        db = get_db()
        cursor = db.messages.find({"userId": ObjectId(user_id)}).sort("timestamp", -1).limit(limit)
        history = await cursor.to_list(length=limit)
        return history

chat_service = ChatService()
