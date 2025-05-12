import json
import logging
from app.services.gemini_service import GeminiService
from app.services.youtube_service import YouTubeService

log = logging.getLogger(__name__)

class MediaService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.youtube_service = YouTubeService()
    
    async def get_mood_based_recommendations(self, user_message: str, media_type: str, max_results: int = 5):
        """
        Get media recommendations based on user's emotional state
        
        Args:
            user_message: User's message to analyze for mood
            media_type: Type of media to recommend (music, videos, inspiration, comedy, relaxation)
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with mood analysis and media recommendations
        """
        # First, analyze the mood
        mood_prompt = f"""
        Analyze the following message from someone experiencing grief or emotional difficulty:
        "{user_message}"
        
        Identify their emotional state and return only a single word or short phrase describing their primary mood.
        """
        
        try:
            log.info(f"Analyzing mood for {media_type} recommendations")
            mood_response = await self.gemini_service.generate_content(mood_prompt)
            detected_mood = mood_response.strip()
            
            # Generate appropriate search query based on mood and media type
            query_prompt = f"""
            Create a YouTube search query for someone experiencing "{detected_mood}" mood who needs {media_type}.
            The query should help find content that would be therapeutic or supportive for this emotional state.
            Return only the search query text, nothing else.
            """
            
            query_response = await self.gemini_service.generate_content(query_prompt)
            search_query = query_response.strip()
            
            # Get YouTube recommendations
            videos = await self.youtube_service.search_videos(search_query, max_results)
            
            # For each video, generate a relevance explanation
            video_results = []
            for video in videos:
                explanation_prompt = f"""
                Explain in one brief sentence why this video titled "{video['title']}" might help someone 
                feeling {detected_mood} who is looking for {media_type} content.
                Keep it compassionate and supportive.
                """
                relevance = await self.gemini_service.generate_content(explanation_prompt)
                
                video_results.append({
                    "title": video["title"],
                    "description": video["description"],
                    "thumbnail_url": video["thumbnail_url"],
                    "video_url": video["video_url"],
                    "video_id": video["video_id"],
                    "relevance_explanation": relevance.strip()
                })
            
            return {
                "detected_mood": detected_mood,
                "search_query_used": search_query,
                "media_type": media_type,
                "recommendations": video_results
            }
            
        except Exception as e:
            log.error(f"Error getting media recommendations: {str(e)}")
            raise