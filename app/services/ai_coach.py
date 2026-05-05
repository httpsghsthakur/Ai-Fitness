import os
from typing import List, Dict
import anthropic
from .prompts import COACH_SYSTEM_PROMPT

class AICoachService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def get_coach_reply(self, message: str, context: str, history: List[Dict]) -> str:
        try:
            # Construct messages for Claude
            messages = []
            for msg in history:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            messages.append({"role": "user", "content": message})

            response = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=500,
                system=COACH_SYSTEM_PROMPT.format(context=context),
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error calling AICoachService: {e}")
            return "I'm having trouble connecting right now. Please try again later."

coach_service = AICoachService()
