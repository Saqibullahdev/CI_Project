from fastapi import APIRouter, Depends, HTTPException, Body
from src.services.document_service import document_service
from src.services.chat_service import chat_service
from src.services.prompt_service import prompt_service
from src.auth import get_current_user
from src.database import get_db
import math

router = APIRouter()

@router.post("/")
async def chat(
    message: str = Body(..., embed=True),
    user: dict = Depends(get_current_user)
):
    try:
        user_id = str(user["_id"])
        username = user["username"]
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
            
        if not document_service.has_document():
            raise HTTPException(status_code=400, detail="Please upload a PDF first")
            
        print(f"Query ({username}): {message}")
        
        # Get recent history
        raw_history = await chat_service.get_recent_history(user_id, 6)
        # Reverse history for chronological order in prompt
        history = raw_history[::-1]
        
        # Retrieve context
        context_chunks = await document_service.search_similar_documents(message, 4)
        context = "\n\n".join(context_chunks)
        
        # Build prompt
        prompt = prompt_service.build_prompt(context, message, history)
        
        # Get response
        answer = await chat_service.generate_response(prompt)
        
        # Estimate tokens
        tokens_used = math.ceil((len(message) + len(answer)) / 4)
        
        # Update metrics and save messages
        db = get_db()
        await chat_service.save_message(user_id, "user", message)
        await chat_service.save_message(user_id, "assistant", answer)
        
        # Update user usage
        await db.users.update_one(
            {"_id": user["_id"]},
            {"$inc": {"chatCount": 1, "totalTokens": tokens_used}}
        )
        
        print(f"Answer: {answer[:100]}...")
        
        return {
            "success": True,
            "answer": answer,
            "sources": len(context_chunks),
            "historyCount": len(history),
            "usage": {
                "tokensUsed": tokens_used,
                "totalTokens": user.get("totalTokens", 0) + tokens_used,
                "chatCount": user.get("chatCount", 0) + 1
            }
        }
    except Exception as e:
        print(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
