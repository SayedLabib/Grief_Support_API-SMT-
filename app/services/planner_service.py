import json
import logging
from app.services.gemini_service import GeminiService
from app.core.config import settings

log = logging.getLogger(__name__)

class PlannerService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.gemini_api_key = settings.gemini_api_key
    
    async def create_daily_plan(self, user_message: str, preferences: dict = None):
        """
        Create a personalized daily plan based on user's grief state and preferences.
        
        Args:
            user_message: The user's message describing their emotional state
            preferences: Optional dict of user preferences (wake time, interests, etc.)
            
        Returns:
            Dictionary with daily plan structure
        """
        if preferences is None:
            preferences = {}
            
        # Build prompt for Gemini model
        prompt = f"""
        Create a supportive daily plan for someone experiencing grief who shared:
        "{user_message}"
        
        User preferences: {json.dumps(preferences)}
        
        Format your response as JSON with the following structure:
        {{
            "morning": [
                {{"time": "7:00 AM", "activity": "Gentle wake up with deep breathing", "benefit": "Helps center yourself"}}
            ],
            "afternoon": [
                {{"time": "12:00 PM", "activity": "Light lunch with nutrient-rich foods", "benefit": "Provides energy"}}
            ],
            "evening": [
                {{"time": "7:00 PM", "activity": "Relaxing activity like reading", "benefit": "Wind down before bed"}}
            ],
            "food_recommendations": [
                {{"meal": "Breakfast", "food": "Oatmeal with berries", "benefit": "Steady energy and antioxidants"}}
            ],
            "healing_activities": [
                {{"activity": "10-minute journaling", "benefit": "Process emotions", "how_to": "Write freely about feelings"}}
            ],
            "memory_rituals": [
                {{"ritual": "Looking at photos", "benefit": "Honors memories", "guidance": "Set a specific time"}}
            ]
        }}
        
        Ensure all sections have at least 3 items, and the plan is sensitive to the person's grief state.
        Make sure your JSON is properly formatted.
        """
        
        try:
            log.info("Creating daily plan based on user's grief state")
            response_text = await self.gemini_service.generate_content(prompt)
            
            # Parse JSON response
            try:
                plan_data = json.loads(response_text)
            except json.JSONDecodeError:
                log.error("Failed to parse Gemini response as JSON")
                # Extract JSON if it's embedded in text
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_text = response_text[json_start:json_end]
                    plan_data = json.loads(json_text)
                else:
                    raise ValueError("Couldn't extract JSON from response")
                    
            # Ensure all required fields are present
            required_fields = ["morning", "afternoon", "evening", "food_recommendations", "healing_activities"]
            for field in required_fields:
                if field not in plan_data:
                    plan_data[field] = []
                    
            if "memory_rituals" not in plan_data:
                plan_data["memory_rituals"] = []
                
            return plan_data
            
        except Exception as e:
            log.error(f"Error creating daily plan: {str(e)}")
            raise