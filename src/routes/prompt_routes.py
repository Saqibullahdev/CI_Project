from fastapi import APIRouter, HTTPException
from src.services.prompt_service import prompt_service
from pydantic import BaseModel

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

class PresetRequest(BaseModel):
    preset: str

@router.get("/")
async def get_current_prompt():
    return {"prompt": prompt_service.get_current_prompt()}

@router.post("/set")
async def set_custom_prompt(req: PromptRequest):
    try:
        prompt_service.set_custom_prompt(req.prompt)
        return {"success": True, "message": "System prompt updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/presets")
async def get_presets():
    return prompt_service.get_preset_details()

@router.post("/preset")
async def set_preset(req: PresetRequest):
    try:
        prompt_service.set_prompt_by_preset(req.preset)
        return {"success": True, "message": f"System prompt updated to {req.preset}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
