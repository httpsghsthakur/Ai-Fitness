import os
from typing import List, Dict
from openai import OpenAI
from .prompts import WORKOUT_ANALYSIS_PROMPT

class WorkoutAnalysisService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def analyze_workout(self, exercises: List[Dict], duration_min: int, goal: str) -> Dict:
        try:
            prompt = WORKOUT_ANALYSIS_PROMPT.format(
                exercises=exercises,
                goal=goal
            )
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error calling WorkoutAnalysisService: {e}")
            return {
                "calories_burned": 0,
                "muscle_groups": [],
                "intensity_score": 0,
                "recovery_days": 0,
                "next_session_suggestion": "Error analyzing workout.",
                "form_tips": []
            }

workout_service = WorkoutAnalysisService()
