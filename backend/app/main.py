
from fastapi import FastAPI

app = FastAPI(
    title="DineVoice AI",
    description="AI-powered restaurant voice receptionist",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to DineVoice AI!",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "DineVoice AI"
    }
