# Groq LLM integration service
from groq import Groq
from app.core.config import settings
from app.core.logging import log

class LLMService:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = "llama3-70b-8192"
    
    async def generate_response(self, user_message: str, system_prompt: str = None, temperature: float = 0.7):
        """
        Generate a response using the Groq LLM API.
        
        Args:
            user_message: User's message to respond to
            system_prompt: System instructions for the model
            temperature: Controls randomness (higher = more random)
        
        Returns:
            The text response from the LLM
        """
        
        try:
            log.info(f"Generating LLM response with {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature,
                max_tokens=4096,
                top_p=1,
                stream=False
            )
            
            # Extract the response text
            response_text = response.choices[0].message.content
            return response_text
            
        except Exception as e:
            log.error(f"Error generating LLM response: {str(e)}")
            raise
    
    async def generate_content(self, prompt: str, temperature: float = 0.7):
        """
        Generate content using the Groq LLM API.
        This method exists for compatibility with other services.
        
        Args:
            prompt: The full prompt to send to the model
            temperature: Controls randomness (higher = more random)
        
        Returns:
            The text response from the LLM
        """
        # For generate_content, we treat the entire prompt as the user message
        # with no system prompt, to match how it's used in other services
        return await self.generate_response(
            user_message=prompt,
            system_prompt="You are a helpful AI assistant responding with raw content.",
            temperature=temperature
        )
