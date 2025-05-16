import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.api import router as api_router
from app.core.config import settings
from app.core.logging import log
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Initialize FastAPI app
app = FastAPI(
    title="Grief Support API",
    description="API for providing emotional support and resources for those experiencing grief",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event handler
@app.on_event("startup")
async def startup_event():
    log.info(f"Starting application in {settings.app_env} environment")
    log.info(f"API documentation available at /docs and /redoc")
    
    # Validate required API keys are set
    # Removed groq_api_key check since it's no longer used
    if not settings.gemini_api_key:
        log.warning("GEMINI_API_KEY is not set. Day planning functionality will be limited.")
    # Removed youtube_api_key check since it's no longer used

# Shutdown event handler
@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down application")

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    Returns the current environment and status.
    """
    return {
        "status": "healthy",
        "environment": settings.app_env,
        "version": app.version
    }

@app.get("/")
async def root():
    return {"message": "Welcome to the Grief Support API. Visit /docs for API documentation."}

# Run the application with uvicorn when executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)