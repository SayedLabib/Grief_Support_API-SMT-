import json
import logging
from app.services.gemini_service import GeminiService
from app.core.config import settings

log = logging.getLogger(__name__)

class MediaService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.gemini_api_key = settings.gemini_api_key
    
    async def get_mood_based_recommendations(self, user_message: str, media_type: str, max_results: int = 5):
        """
        Get media recommendations based on user's emotional state using Gemini only.
        """
        # First, analyze the mood
        mood_prompt = f'''
        Analyze the following message from someone experiencing grief or emotional difficulty:
        "{user_message}"
        Identify their emotional state and return only a single word or short phrase describing their primary mood.
        '''
        try:
            log.info(f"Analyzing mood for {media_type} recommendations")
            mood_response = await self.gemini_service.generate_content(mood_prompt)
            detected_mood = mood_response.strip()

            # Generate a Gemini prompt to get YouTube video recommendations
            rec_prompt = f'''
            You are a helpful assistant. Based on the mood "{detected_mood}" and the need for {media_type},
            recommend {max_results} YouTube videos that would be supportive or therapeutic for this emotional state.
            For each video, provide a JSON object with the following fields: title, description, thumbnail_url, video_url, video_id.
            Return a JSON array of these video objects. Do not include any extra text or explanation.
            '''
            rec_response = await self.gemini_service.generate_content(rec_prompt)
            # Try to parse the response as JSON
            try:
                video_results = json.loads(rec_response)
            except Exception as e:
                log.error(f"Failed to parse Gemini video recommendations as JSON: {str(e)} | Response: {rec_response}")
                raise ValueError("Gemini did not return valid JSON for video recommendations.")

            return {
                "detected_mood": detected_mood,
                "media_type": media_type,
                "recommendations": video_results
            }
        except Exception as e:
            log.error(f"Error getting media recommendations: {str(e)}")
            raise