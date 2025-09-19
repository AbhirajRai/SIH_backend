from fastapi import APIRouter
from pydantic import BaseModel
from app.nlp_services.toxicity_service import analyze_toxicity  # <-- updated import

router = APIRouter()

class TextRequest(BaseModel):
    text: str

@router.post("/nlp/toxicity")
async def toxicity_endpoint(request: TextRequest):
    return analyze_toxicity(request.text)
