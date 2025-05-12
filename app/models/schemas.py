from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal

class UserPostRequest(BaseModel):
    user_message: str = Field(..., description="User post describing their feelings or situation")

class MoodAnalysis(BaseModel):
    detected_mood: str = Field(..., description="Primary mood detected in the user's post")
    mood_intensity: int = Field(..., ge=1, le=10, description="Intensity of the mood on a scale of 1-10")
    grief_stage: Optional[str] = Field(None, description="Detected stage of grief if applicable")

class GriefResponse(BaseModel):
    emotional_validation: str = Field(..., description="Validation of user's emotions")
    mood_analysis: Optional[MoodAnalysis] = Field(None, description="Analysis of the user's emotional state")
    coping_strategies: List[str] = Field(..., description="Suggested coping strategies")

class PlannerRequest(BaseModel):
    user_message: str = Field(..., description="User post describing their feelings or situation")
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="User preferences for planning")

class DailyPlan(BaseModel):
    morning: List[Dict[str, str]] = Field(..., description="Morning activities")
    afternoon: List[Dict[str, str]] = Field(..., description="Afternoon activities")
    evening: List[Dict[str, str]] = Field(..., description="Evening activities")
    food_recommendations: List[Dict[str, str]] = Field(..., description="Food recommendations")
    healing_activities: List[Dict[str, str]] = Field(..., description="Healing activities")
    memory_rituals: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="Memory rituals")

class MoodBasedMediaRequest(BaseModel):
    user_message: str = Field(..., description="User post to analyze for mood")
    media_type: Literal["music", "videos", "inspiration", "comedy", "relaxation"] = Field(
        default="videos", 
        description="Type of media content to recommend"
    )
    max_results: int = Field(default=5, description="Maximum number of results to return")

class YouTubeVideo(BaseModel):
    title: str = Field(..., description="Video title")
    description: str = Field(..., description="Video description")
    thumbnail_url: str = Field(..., description="URL to video thumbnail image")
    video_url: str = Field(..., description="YouTube video URL")
    video_id: str = Field(..., description="YouTube video ID")
    relevance_explanation: Optional[str] = Field(None, description="Why this video matches the mood")

class MediaResponse(BaseModel):
    detected_mood: str = Field(..., description="Mood detected from user's post")
    search_query_used: str = Field(..., description="Search query generated based on mood")
    media_type: str = Field(..., description="Type of media recommended")
    recommendations: List[YouTubeVideo] = Field(..., description="List of recommended media items")


class unifiedRequest(BaseModel):
    """A unified request that can trigger multiple response types"""
    user_message: str
    
    # Control which analyses to perform
    include_grief_analysis: bool = True
    include_daily_plan: bool = False
    include_media_recommendations: bool = False
    
    # Daily plan parameters (only used if include_daily_plan is True)
    plan_preferences: Optional[dict] = None
    
    # Media recommendation parameters (only used if include_media_recommendations is True)
    media_type: Optional[str] = None
    max_media_results: Optional[int] = 5


class unifiedResponse(BaseModel):
    """A unified response containing multiple analysis results"""
    grief_response: Optional[GriefResponse] = None
    daily_plan: Optional[DailyPlan] = None
    media_recommendations: Optional[MediaResponse] = None