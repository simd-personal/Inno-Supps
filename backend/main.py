from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import os
import time
from contextlib import asynccontextmanager

from database import get_db, init_db
from routes import auth, generations, templates, workflows, compliance, slack, ai_agents, jobs
from services.llm_service import LLMService
from services.redis_service import RedisService
from config import settings
from services.redis_cache import cache

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
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(generations.router, prefix="/api/generations", tags=["generations"])
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])
app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])
app.include_router(compliance.router, prefix="/api/compliance", tags=["compliance"])
app.include_router(slack.router, prefix="/api/slack", tags=["slack"])
app.include_router(ai_agents.router, tags=["ai-agents"])
app.include_router(jobs.router, prefix="/api", tags=["jobs"])

@app.get("/")
async def root():
    return {
        "message": "Inno Supps API is running",
        "version": "1.0.0",
        "mock_mode": settings.mock_mode
    }

@app.get("/health")
async def health_check():
    # Check Redis connection
    redis_status = "healthy"
    try:
        cache.get("health_check")
    except Exception:
        redis_status = "unhealthy"
    
    return {
        "status": "healthy",
        "redis": redis_status,
        "mock_mode": settings.mock_mode
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
