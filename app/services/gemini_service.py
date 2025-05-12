import os
import json
import logging
import requests
import asyncio
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from app.core.logging import log

# Load environment variables if not already loaded
load_dotenv()

class GeminiService:
    """
    Service class for interacting with Google's Gemini-2.0-flash API
    """
    def __init__(self):
        # Get API key from environment variables
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            log.error("GEMINI_API_KEY not found in environment variables")
            raise ValueError("GEMINI_API_KEY not configured in .env file")
            
        # API URL for the gemini-2.0-flash model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }
        log.info("GeminiService initialized with gemini-2.0-flash model")

    async def generate_daily_plan(self, user_message: str, preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate a daily plan using Gemini API based on user's emotional state and preferences.
        
        Args:
            user_message: The user's post describing their feelings
            preferences: Optional dictionary of user preferences
        
        Returns:
            Daily plan data as a dictionary
        """
        preferences_str = json.dumps(preferences) if preferences else "{}"
        
        prompt = f"""
        Below is a message from someone experiencing grief. Create a compassionate and personalized daily plan 
        that supports their emotional well-being.
        
        USER MESSAGE: {user_message}
        
        USER PREFERENCES: {preferences_str}
        
        As an empathetic wellness planner, create a detailed daily structure that acknowledges their grief
        while helping them move through their day with care and purpose. The plan should include:
        
        1. Morning activities focused on gentle self-care and setting intentions
        2. Afternoon activities that provide healthy distraction and purpose
        3. Evening activities for reflection and rest
        4. Food recommendations that support emotional well-being
        5. Healing activities distributed throughout the day
        6. Memory rituals that honor their loss
        
        Format your response as strict JSON with no additional explanatory text:
        
        {{
            "morning": [
                {{"time": "8:00 AM", "activity": "Activity description", "benefit": "Why this helps"}}
            ],
            "afternoon": [
                {{"time": "1:00 PM", "activity": "Activity description", "benefit": "Why this helps"}}
            ],
            "evening": [
                {{"time": "7:00 PM", "activity": "Activity description", "benefit": "Why this helps"}}
            ],
            "food_recommendations": [
                {{"meal": "Breakfast/Lunch/Dinner/Snack", "suggestion": "Food suggestion", "benefit": "Emotional/nutritional benefit"}}
            ],
            "healing_activities": [
                {{"time": "Time", "activity": "Healing activity", "benefit": "Why this helps"}}
            ],
            "memory_rituals": [
                {{"activity": "Ritual description", "purpose": "Emotional purpose"}}
            ]
        }}
        """
        
        try:
            log.info("Generating daily plan with Gemini")
            response = await self.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response
            
            # Find JSON in the response if it's wrapped in markdown code blocks
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
                
            log.debug(f"Gemini raw response: {response_text[:100]}...")
            
            # Parse the JSON response
            plan_data = json.loads(response_text)
            return plan_data
            
        except json.JSONDecodeError as e:
            log.error(f"Error parsing Gemini response as JSON: {str(e)}")
            log.debug(f"Raw response: {response_text}")
            raise ValueError("Failed to parse Gemini response as valid JSON")
        except Exception as e:
            log.error(f"Error generating daily plan with Gemini: {str(e)}")
            raise

    async def generate_content(self, prompt: str) -> str:
        """
        Generate content using Google's Gemini API with gemini-2.0-flash model
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            String response from Gemini
        """
        try:
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.4,
                    "topP": 0.8,
                    "topK": 40,
                    "maxOutputTokens": 8192
                },
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ]
            }
            
            # Run the API call in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload
                )
            )
            
            if response.status_code != 200:
                log.error(f"API request failed with status code: {response.status_code}")
                log.error(f"Response: {response.text}")
                raise Exception(f"API request failed with status code: {response.status_code}")
                
            response_json = response.json()
            
            # Extract the content from the API response based on Gemini's response structure
            try:
                content_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
                return content_text
            except (KeyError, IndexError) as e:
                log.error(f"Unexpected response structure from Gemini API: {str(e)}")
                log.debug(f"Response JSON: {json.dumps(response_json)[:500]}...")
                raise ValueError(f"Unexpected response structure from Gemini API: {str(e)}")
            
        except Exception as e:
            log.error(f"Error generating content with Gemini API: {str(e)}")
            raise