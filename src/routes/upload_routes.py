from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from src.services.document_service import document_service
from src.services.embedding_service import embedding_service
from src.auth import get_current_user
import os
import aiofiles

router = APIRouter()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/")
async def upload_pdf(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        # Save file temporarily
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        print(f"Processing PDF: {file.filename}")
        
        embeddings = embedding_service.get_embeddings()
        chunks = await document_service.process_pdf(file_path, embeddings)
        
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return {
            "success": True,
            "message": "PDF processed successfully",
            "chunks": chunks,
            "filename": file.filename
        }
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))
