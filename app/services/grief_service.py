import json
import logging
import re
from app.services.llm_service import LLMService
from app.core.config import settings

log = logging.getLogger(__name__)

class GriefService:
    def __init__(self):
        self.llm_service = LLMService()
        self.gemini_api_key = settings.gemini_api_key
    
    async def analyze_and_respond(self, user_message: str):
        """
        Analyze user's message and provide emotional support with coping strategies
        
        Args:
            user_message: User's message describing their feelings or situation
            
        Returns:
            Dictionary with emotional validation, mood analysis, and coping strategies
        """
        prompt = f"""
        Analyze the following message from someone experiencing grief or emotional difficulty:
        "{user_message}"
        
        Format your response as JSON with the following structure:
        {{
            "emotional_validation": "A compassionate validation of their emotions and experience",
            "mood_analysis": {{
                "detected_mood": "Primary emotional state detected (e.g., sadness, anger, denial)",
                "mood_intensity": 7,
                "grief_stage": "Identified stage of grief if applicable (e.g., denial, anger, bargaining, depression, acceptance)"
            }},
            "coping_strategies": [
                "1. Specific, actionable coping strategy 1",
                "2. Specific, actionable coping strategy 2",
                "3. Specific, actionable coping strategy 3", 
                "4. Specific, actionable coping strategy 4",
                "5. Specific, actionable coping strategy 5"
            ]
        }}
        
        Note for coping_strategies: Format each strategy with a number at the beginning (1., 2., etc.)
        
        Ensure the response is compassionate, validating, and provides practical strategies.
        Make sure your JSON is properly formatted with double quotes around keys and string values.
        Provide ONLY the JSON in your response, with no additional text before or after.
        """
        
        try:
            log.info("Analyzing user message and generating grief response")
            response_text = await self.llm_service.generate_content(prompt)
            
            # Parse JSON response
            try:
                # First attempt direct parsing
                response_data = json.loads(response_text)
            except json.JSONDecodeError as e:
                log.warning(f"Initial JSON parsing failed: {str(e)}")
                log.debug(f"Raw response: {response_text}")
                
                # Try to extract JSON if it's embedded in text 
                # Find the outermost JSON object using regex
                json_pattern = r'\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{(?:[^{}])*\}))*\}))*\}'
                matches = re.findall(json_pattern, response_text)
                
                if matches:
                    # Try parsing the largest match (most likely the complete JSON)
                    matches.sort(key=len, reverse=True)
                    for potential_json in matches:
                        try:
                            response_data = json.loads(potential_json)
                            log.info("Successfully extracted and parsed JSON using regex")
                            break
                        except json.JSONDecodeError:
                            continue
                    else:  # No break occurred
                        raise ValueError("Found potential JSON objects but couldn't parse any of them")
                else:
                    # Fallback to basic extraction
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        json_text = response_text[json_start:json_end]
                        try:
                            response_data = json.loads(json_text)
                            log.info("Successfully extracted and parsed JSON using basic extraction")
                        except json.JSONDecodeError as inner_e:
                            log.error(f"Error parsing extracted JSON: {str(inner_e)}")
                            log.debug(f"Extracted JSON: {json_text}")
                            raise ValueError(f"Extracted JSON is still malformed: {str(inner_e)}")
                    else:
                        raise ValueError("Couldn't extract JSON from response")
            
            return response_data
            
        except Exception as e:
            log.error(f"Error creating grief response: {str(e)}")
            raise