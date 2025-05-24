from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import unifiedRequest, unifiedResponse
from app.services.grief_service import GriefService
from app.services.planner_service import PlannerService
from app.services.media_service import MediaService
import logging

router = APIRouter()
log = logging.getLogger(__name__)

# Dependency injection
def get_grief_service():
    return GriefService()

def get_planner_service():
    return PlannerService()

def get_media_service():
    return MediaService()


# A unified Approach to handle multiple analyses in one request

@router.post("/unified-analysis", response_model=unifiedResponse)
async def unified_response(
    request: unifiedRequest,
    grief_service: GriefService = Depends(get_grief_service),
    planner_service: PlannerService = Depends(get_planner_service),
    media_service: MediaService = Depends(get_media_service)
):
    """
    Process a single request to get multiple responses:
    - Grief analysis and emotional support
    - Personalized daily plan
    - Media recommendations based on emotional state
    
    The response includes only the requested analysis types.
    """
    response = unifiedResponse()
    
    try:
        # Process grief analysis if requested
        if request.include_grief_analysis:
            grief_response = await grief_service.analyze_and_respond(request.user_message)
            response.grief_response = grief_response
        
        # Process daily plan if requested
        if request.include_daily_plan:
            daily_plan = await planner_service.create_daily_plan(
                request.user_message, 
                request.plan_preferences
            )
            response.daily_plan = daily_plan
        
        # Process media recommendations if requested
        if request.include_media_recommendations:
            media_recommendations = await media_service.get_mood_based_recommendations(
                request.user_message,
                request.media_type,
                request.max_media_results
            )
            response.media_recommendations = media_recommendations
        
        return response
    except Exception as e:
        log.error(f"Error processing unified analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process unified analysis: {str(e)}")