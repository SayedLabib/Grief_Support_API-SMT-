import logging
import json
import aiohttp
import os
from app.core.config import settings

log = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self):
        # Use environment variable directly to ensure we have the latest value
        self.tavily_api_key = os.getenv("TAVILY_API_KEY") or settings.tavily_api_key
        self.tavily_search_url = "https://api.tavily.com/search"
        
    async def search_videos(self, query: str, max_results: int = 5):
        """
        Search for YouTube music videos using Tavily API
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of video information dictionaries
        """
        try:
            if not self.tavily_api_key:
                log.error("Tavily API key not configured")
                raise ValueError("Tavily API key not configured in .env file")
                
            log.info(f"Searching for music with Tavily API: {query}")
            search_query = f"{query} youtube music therapy videos"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.tavily_api_key}"  # Correct format for Tavily API
            }
            
            payload = {
                "query": search_query,
                "search_depth": "advanced",
                "include_domains": ["youtube.com"],
                "max_results": max_results
            }
            
            async with aiohttp.ClientSession() as session:
                log.info(f"Using Tavily API key: {self.tavily_api_key[:5]}...")
                log.info(f"Headers: Authorization: Bearer {self.tavily_api_key[:5]}...")
                async with session.post(
                    self.tavily_search_url,
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # Process search results
                        videos = []
                        for item in result.get("results", []):
                            # Extract video ID from URL if possible
                            url = item.get("url", "")
                            video_id = ""
                            if "v=" in url:
                                video_id = url.split("v=")[1].split("&")[0]
                            
                            video_data = {
                                "title": item.get("title", ""),
                                "description": item.get("content", ""),
                                "thumbnail_url": item.get("image_url", "") or "",  # Default to empty string if None
                                "video_url": url,
                                "video_id": video_id
                            }
                            videos.append(video_data)
                        
                        log.info(f"Found {len(videos)} music videos with Tavily")
                        return videos
                    else:
                        error_text = await response.text()
                        log.error(f"Tavily API error: {response.status} - {error_text}")
                        raise Exception(f"Tavily API error: {response.status}")
                
        except Exception as e:
            log.error(f"Error searching with Tavily: {str(e)}")
            raise
