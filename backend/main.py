from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import os
from contextlib import asynccontextmanager

from database import get_db, init_db
from routes import auth, generations, templates, workflows, compliance, slack, ai_agents
from services.llm_service import LLMService
from services.redis_service import RedisService

# Initialize services
llm_service = LLMService()
redis_service = RedisService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Inno Supps PromptOps API",
    description="AI-powered prompt generation and workflow automation for supplement marketing",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(generations.router, prefix="/api/generations", tags=["generations"])
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])
app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])
app.include_router(compliance.router, prefix="/api/compliance", tags=["compliance"])
app.include_router(slack.router, prefix="/api/slack", tags=["slack"])
app.include_router(ai_agents.router, tags=["ai-agents"])

@app.get("/")
async def root():
    return {"message": "Inno Supps PromptOps API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
