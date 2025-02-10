from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Tuple
from .llm.llm import GenZTranslator

# Initialize the translator
translator = GenZTranslator()

# Default route
async def root():
    return {"message": "Welcome to the GenZHelper Backend"}

# Health check route
async def health_check():
    return {"status": "ok"}

# Request validations
class StyleTag(BaseModel):
    value: str
    label: str

"""
 Actual request schema example:
 {
     "latest_prompt": "Sorry, for texting you so much",
     "prev_convo": [
         ["Hello", "me"],
         ["Hey", "me"],
         ["???", "me"],
         ["Please reply", "me"],
         ["What?", "them"]
     ],
     "general_instruction": "she's angry ig",
     "genziness_score": 5,
     "mood": "sad",
     "gender": "female",
     "objective": "crush",
     "style_tags": [
         {
             "value": "all_lowercase",
             "label": "⬇️ All Lowercase"
         }
     ],
     "word_limit": 20
 }
"""

class ConvertRequest(BaseModel):
    latest_prompt: str
    prev_convo: Optional[List[Tuple[str, str]]] = []
    general_instruction: Optional[str] = None
    genziness_score: int
    mood: Optional[str] = "happy"
    gender: Optional[str] = None
    objective: Optional[str] = "casual"
    style_tags: Optional[List[StyleTag]] = []
    word_limit: Optional[int] = 40

# Convert route
async def convert(request: ConvertRequest):
    try:
        request_data = {
            "latest_prompt": request.latest_prompt,
            "prev_convo": request.prev_convo,
            "general_instruction": request.general_instruction,
            "genziness_score": request.genziness_score,
            "mood": request.mood,
            "gender": request.gender,
            "objective": request.objective,
            "style_tags": [tag.dict() for tag in request.style_tags] if request.style_tags else [],
            "word_limit": request.word_limit
        }

        # Get translation from GenZTranslator
        result = translator.translate(request_data)
        
        if not result or "response" not in result:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate response"
            )

        return result

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )
