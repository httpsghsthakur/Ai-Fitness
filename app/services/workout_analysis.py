import os
import google.generativeai as genai
from typing import List, Dict
import json
from .prompts import WORKOUT_ANALYSIS_PROMPT

class GeminiWorkoutService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def analyze_workout(self, exercises: List[Dict], duration_min: int, goal: str) -> Dict:
        try:
            prompt = WORKOUT_ANALYSIS_PROMPT.format(
                exercises=exercises,
                goal=goal
            ) + "\nReturn ONLY valid JSON."
            
            response = self.model.generate_content(prompt)
            
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
            return json.loads(text)
        except Exception as e:
            print(f"Error in GeminiWorkoutService: {e}")
            return {
                "calories_burned": 0,
                "muscle_groups": [],
                "intensity_score": 0,
                "recovery_days": 0,
                "next_session_suggestion": "Error analyzing workout.",
                "form_tips": []
            }

workout_service = GeminiWorkoutService()
