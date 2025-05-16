import logging
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.core.config import settings

log = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self):
        self.api_key = settings.gemini_api_key
        
    async def search_videos(self, query: str, max_results: int = 5):
        """
        Search YouTube for videos matching the query
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of video information dictionaries
        """
        try:
            youtube = build("youtube", "v3", developerKey=self.api_key)
            
            # Search for videos
            search_response = youtube.search().list(
                q=query,
                part="snippet",
                maxResults=max_results,
                type="video",
                videoEmbeddable="true",
                safeSearch="strict"
            ).execute()
            
            # Process search results
            videos = []
            for item in search_response.get("items", []):
                video_id = item["id"]["videoId"]
                snippet = item["snippet"]
                
                video_data = {
                    "title": snippet["title"],
                    "description": snippet["description"],
                    "thumbnail_url": snippet["thumbnails"]["high"]["url"],
                    "video_url": f"https://www.youtube.com/watch?v={video_id}",
                    "video_id": video_id
                }
                
                videos.append(video_data)
                
            return videos
            
        except HttpError as e:
            log.error(f"YouTube API error: {str(e)}")
            raise
        except Exception as e:
            log.error(f"Error searching YouTube videos: {str(e)}")
            raise
