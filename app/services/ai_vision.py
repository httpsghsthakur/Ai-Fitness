import os
import google.generativeai as genai
from typing import List, Dict
from PIL import Image
import io
import json
from .prompts import FOOD_ANALYSIS_PROMPT

class GeminiVisionService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def analyze_food_image(self, image_bytes: bytes, meal_type: str) -> Dict:
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            prompt = FOOD_ANALYSIS_PROMPT + f"\nMeal Type: {meal_type}"
            
            response = self.model.generate_content([prompt, image])
            
            # Extract JSON from the response text
            text = response.text
            # Simple cleanup in case Gemini adds markdown backticks
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
            return json.loads(text)
        except Exception as e:
            print(f"Error in GeminiVisionService: {e}")
            return {
                "food_items": [],
                "total_calories": 0,
                "confidence": 0,
                "alternatives": ["Error analyzing image"]
            }

vision_service = GeminiVisionService()
