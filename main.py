from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from app.services.ai_vision import vision_service
from app.services.ai_coach import coach_service
from app.services.workout_analysis import workout_service
import os
import json
import google.generativeai as genai

app = FastAPI(title="FitCore AI Backend")

class FoodItem(BaseModel):
    name: str
    quantity: str
    unit: str
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float

class FoodAnalysisResponse(BaseModel):
    food_items: List[FoodItem]
    total_calories: float
    confidence: float
    alternatives: List[str]

class ChatRequest(BaseModel):
    message: str
    context: str
    history: List[dict]

class VoiceLogRequest(BaseModel):
    text: str
    context: str

class WorkoutAnalysisRequest(BaseModel):
    exercises: List[dict]
    duration_min: int
    goal: str

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/analyze-food", response_model=FoodAnalysisResponse)
async def analyze_food(image: UploadFile = File(...), meal_type: str = Form(...)):
    try:
        content = await image.read()
        result = await vision_service.analyze_food_image(content, meal_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        reply = await coach_service.get_coach_reply(
            request.message, 
            request.context, 
            request.history
        )
        return {"reply": reply, "actions": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/parse-voice")
async def parse_voice(request: VoiceLogRequest):
    try:
        prompt = f"""
        Convert this natural language food description into a structured JSON log.
        User Input: "{request.text}"
        User Context: {request.context}
        
        Return ONLY valid JSON in this format:
        {{
          "food_items": [{{ "name": "...", "quantity": "...", "unit": "...", "calories": 0, "protein_g": 0, "carbs_g": 0, "fat_g": 0, "fiber_g": 0 }}],
          "total_calories": 0
        }}
        """
        # Using Gemini 1.5 Flash for speed
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return json.loads(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-workout")
async def analyze_workout(request: WorkoutAnalysisRequest):
    try:
        result = await workout_service.analyze_workout(
            request.exercises,
            request.duration_min,
            request.goal
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
