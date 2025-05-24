import json
import logging
from app.services.gemini_service import GeminiService
from app.services.youtube_service import YouTubeService
from app.core.config import settings

log = logging.getLogger(__name__)

class MediaService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.youtube_service = YouTubeService()
        self.tavily_api_key = settings.tavily_api_key
    
    async def get_mood_based_recommendations(self, user_message: str, media_type: str, max_results: int = 5):
        """
        Get media recommendations based on user's mood using Tavily API for music
        
        Args:
            user_message: User's message to analyze for mood
            media_type: Type of media to recommend (music, videos, etc)
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with mood analysis and media recommendations
        """
        try:
            # Default to "music" if media_type is None or empty
            media_type = "music" if not media_type else media_type.lower()
            
            # Verify we're requesting music (only supported media type)
            if media_type != "music":
                log.warning(f"Unsupported media type: {media_type}. Only 'music' is supported.")
                raise ValueError(f"Only music recommendations are supported, got: {media_type}")
                
            # Check if Tavily API key is configured
            if not self.tavily_api_key:
                log.error("Tavily API key not configured for music recommendations")
                raise ValueError("Tavily API key not configured in .env file")
            
            # Step 1: Analyze mood from user message using Gemini
            log.info(f"Analyzing mood for music recommendations")
            mood_prompt = f'''
            Analyze the following message from someone experiencing grief or emotional difficulty:
            "{user_message}"
            Identify their emotional state and return only a single word or short phrase describing their primary mood.
            '''
            mood_response = await self.gemini_service.generate_content(mood_prompt)
            detected_mood = mood_response.strip()
            log.info(f"Detected mood: {detected_mood}")
            
            # Step 2: Create search query for music based on mood
            query_prompt = f'''
            Create a search query for finding YouTube music videos that would help someone feeling "{detected_mood}".
            The music should be therapeutic and supportive for this emotional state.
            Return only the search query text, nothing else.
            Example: "calming piano music for anxiety and stress relief"
            '''
            query_response = await self.gemini_service.generate_content(query_prompt)
            search_query = query_response.strip()
            log.info(f"Generated search query: {search_query}")
            
            # Step 3: Use Tavily to search for YouTube music videos
            videos = await self.youtube_service.search_videos(search_query, max_results)
            
            # Step 4: For each video, generate a relevance explanation
            video_results = []
            for video in videos:
                explanation_prompt = f'''
                Explain in one brief, compassionate sentence why the music video titled 
                "{video['title']}" might help someone feeling {detected_mood}.
                '''
                relevance = await self.gemini_service.generate_content(explanation_prompt)
                
                video["relevance_explanation"] = relevance.strip()
                video_results.append(video)
            
            # Return the results with mood analysis
            return {
                "detected_mood": detected_mood,
                "search_query_used": search_query,
                "media_type": "music",
                "recommendations": video_results
            }
                
        except Exception as e:
            log.error(f"Error getting music recommendations: {str(e)}")
            raise