# Grief Support API

An AI-powered support system for individuals experiencing grief, offering personalized guidance, resources, and emotional support.

## Overview

The Grief Support API uses advanced language models to analyze user messages, understand their emotional state, and provide tailored support for grief processing. The system offers:

- **Emotional validation** and acknowledgment of grief experiences
- **Personalized coping strategies** based on detected emotional states
- **Resource recommendations** including videos, music, and reading materials
- **Daily planning assistance** with healing activities and memory rituals
- **Mood-sensitive content** from YouTube and other sources

The API leverages Groq's Llama3-70b-8192 model for grief analysis and Google's Gemini model for day planning, creating a comprehensive support system for grief management.

## Technical Architecture

### Directory Structure

```
Grief_Support_API/
│
├── app/                              # Main application package
│   ├── api/                          # API-related code
│   │   ├── routes/                   # API endpoints
│   │   │   ├── __init__.py           # Router aggregation
│   │   │   ├── grief_support.py      # Grief analysis endpoints
│   │   │   ├── resources.py          # Resource recommendation endpoints
│   │   │   ├── youtube.py            # YouTube search endpoints
│   ├── core/                         # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py                 # Configuration settings
│   │   └── logging.py                # Logging setup
│   ├── models/                       # Data models
│   │   ├── __init__.py
│   │   └── schemas.py                # Pydantic models
│   ├── services/                     # Business logic
│   │   ├── __init__.py
│   │   ├── llm_service.py            # Groq LLM service
│   │   ├── gemini_service.py         # Google Gemini service
│   │   ├── grief_analyzer.py         # Grief analysis service
│   │   ├── planner_service.py        # Day planner service
│   │   └── youtube_service.py        # YouTube API integration
│   └── main.py                       # FastAPI application entry point
├── .env                              # Environment variables
├── .gitignore                        # Git ignore file
├── docker-compose.yml                # Docker Compose configuration
├── Dockerfile                        # Docker configuration
└── requirements.txt                  # Project dependencies
```

### Key Components

#### API Routes

- **`grief_support.py`**: Analyzes user messages for grief context and emotional state
- **`resources.py`**: Provides curated resources based on grief type and emotional needs
- **`youtube.py`**: Delivers mood-appropriate video content from YouTube

#### Services

- **`llm_service.py`**: Interfaces with Groq's Llama3-70b-8192 for natural language processing
- **`gemini_service.py`**: Leverages Google's Gemini model for structured day planning
- **`grief_analyzer.py`**: Processes user messages to identify grief stages and emotional states
- **`planner_service.py`**: Generates customized daily plans with self-care activities
- **`youtube_service.py`**: Analyzes mood and recommends appropriate YouTube content

#### Core and Models

- **`config.py`**: Manages environment variables and application settings
- **`logging.py`**: Provides structured logging throughout the application
- **`schemas.py`**: Defines data structures for API requests and responses

## API Endpoints

### Grief Analysis

```
POST /api/grief/analyze
```
Analyzes a user's message to provide emotional validation, coping strategies, and recommended resources.

**Request:**
```json
{
  "user_message": "I lost my mother last week and I feel so empty inside."
}
```

**Response:**
```json
{
  "emotional_validation": "I'm deeply sorry about the loss of your mother...",
  "mood_analysis": {
    "detected_mood": "sad",
    "mood_intensity": 8,
    "grief_stage": "early grief"
  },
  "coping_strategies": [
    "Allow yourself space to feel the emotions...",
    "Consider creating a small memorial ritual..."
  ],
  "music_recommendations": [...],
  "video_recommendations": [...],
  "journal_recommendations": [...]
}
```

### Daily Planner

```
POST /api/planner/daily
```
Creates a structured daily plan tailored to the user's emotional state.

**Request:**
```json
{
  "user_message": "I'm struggling with my grief today and don't know how to get through the day.",
  "preferences": {
    "wake_up_time": "7:00 AM",
    "interests": ["nature", "reading"]
  }
}
```

**Response:**
```json
{
  "morning": [
    {"time": "7:00 AM", "activity": "Gentle wake-up with deep breathing", "benefit": "Helps center yourself at the start of the day"}
  ],
  "afternoon": [...],
  "evening": [...],
  "food_recommendations": [...],
  "healing_activities": [...],
  "memory_rituals": [...]
}
```

### Media Recommendations

```
POST /api/youtube/mood-based
```
Provides YouTube content recommendations based on mood analysis.

**Request:**
```json
{
  "user_message": "I'm feeling overwhelmed with sadness today.",
  "media_type": "videos",
  "max_results": 3
}
```

**Response:**
```json
{
  "detected_mood": "sad",
  "search_query_used": "uplifting content for grief",
  "videos": [
    {
      "title": "Finding Peace After Loss",
      "description": "This content may help lift your spirits during this difficult time",
      "thumbnail_url": "https://i.ytimg.com/vi/...",
      "video_url": "https://www.youtube.com/watch?v=...",
      "video_id": "...",
      "relevance_explanation": "This content was selected to support you in your sad state"
    },
    ...
  ]
}
```

## Setup and Installation

### Environment Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Grief_Support_API.git
   cd Grief_Support_API
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix/MacOS:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following variables:
   ```
   GROQ_API_KEY=your_groq_api_key
   GEMINI_API_KEY=your_gemini_api_key
   YOUTUBE_API_KEY=your_youtube_api_key
   APP_ENV=development
   LOG_LEVEL=INFO
   ```

### Running the Application

#### Local Development
```
uvicorn app.main:app --reload
```

### Deploymnet
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
```

#### Docker Deployment
```
docker-compose up --build
```

Access the API documentation at: `http://localhost:8000/docs`

## Technology Stack

- **FastAPI**: Modern, high-performance web framework
- **Groq API**: Access to Llama3-70b-8192 for advanced NLP capabilities
- **Google Gemini API**: Structured planning and content generation
- **YouTube Data API**: Content recommendation based on emotional state
- **Docker**: Containerization for consistent deployment
- **Pydantic**: Data validation and settings management

## Contributing

Contributions to the Grief Support API are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project aims to provide support for those experiencing grief and should not replace professional mental health services
- For immediate crisis support, please contact appropriate mental health crisis services in your region


