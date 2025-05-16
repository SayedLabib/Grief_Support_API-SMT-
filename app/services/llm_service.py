# Groq LLM integration service
from app.core.config import settings
from app.core.logging import log
from app.services.gemini_service import GeminiService

class LLMService:
    def __init__(self):
        self.model = settings.gemini_model
        self.gemini_api_key = settings.gemini_api_key
        self.gemini_service = GeminiService()
    
    async def generate_response(self, user_message: str, system_prompt: str = None, temperature: float = 0.7):
        """
        Generate a response using the Gemini LLM API.
        
        Args:
            user_message: User's message to respond to
            system_prompt: System instructions for the model
            temperature: Controls randomness (higher = more random)
        
        Returns:
            The text response from the LLM
        """
        # Use GeminiService to generate the response
        # You may want to pass system_prompt and temperature if GeminiService supports them
        return await self.gemini_service.generate_content(user_message)
    
    async def generate_content(self, prompt: str, temperature: float = 0.7):
        """
        Generate content using the Gemini LLM API.
        This method exists for compatibility with other services.
        
        Args:
            prompt: The full prompt to send to the model
            temperature: Controls randomness (higher = more random)
        
        Returns:
            The text response from the LLM
        """
        return await self.generate_response(
            user_message=prompt,
            system_prompt="You are a helpful AI assistant responding with raw content.",
            temperature=temperature
        )
