import os
import google.generativeai as genai
from typing import List, Dict
from .prompts import COACH_SYSTEM_PROMPT

class GeminiCoachService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    async def get_coach_reply(self, message: str, context: str, history: List[Dict]) -> str:
        try:
            # Construct chat history for Gemini
            chat = self.model.start_chat(history=[])
            
            system_instruction = COACH_SYSTEM_PROMPT.format(context=context)
            
            # Since Gemini models can take system instructions in the constructor or as first message
            # We'll prepend it to the message or use the system_instruction feature if available
            full_prompt = f"SYSTEM INSTRUCTION: {system_instruction}\n\nUSER MESSAGE: {message}"
            
            response = chat.send_message(full_prompt)
            return response.text
        except Exception as e:
            print(f"Error in GeminiCoachService: {e}")
            return "I'm having a little trouble thinking. Can you try again?"

coach_service = GeminiCoachService()
