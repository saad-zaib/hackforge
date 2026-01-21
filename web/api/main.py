from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import logging
from .config import API_TITLE, API_VERSION, CORS_ORIGINS  
from .dependencies import get_database

logger = logging.getLogger(__name__)

app = FastAPI(
    title=API_TITLE,
    description="REST API for Dynamic Vulnerability Training Platform",
    version=API_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include all routers
try:
    from .routers import users, campaigns, machines, flags, blueprints, stats
    
    app.include_router(users.router)
    app.include_router(campaigns.router)
    app.include_router(machines.router)
    app.include_router(flags.router)
    app.include_router(blueprints.router)
    app.include_router(stats.router)
    
    logger.info("✓ All routers loaded successfully")
except ImportError as e:
    logger.error(f"✗ Failed to load routers: {e}")
    import traceback
    logger.error(traceback.format_exc())

@app.get("/health")
async def health_check():
    """Health check"""
    db_status = "not_connected"
    
    try:
        db = get_database()
        if db:
            db.users.find_one()
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": time.time()
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Hackforge API",
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║          HACKFORGE WEB API WITH DATABASE                  ║
╚═══════════════════════════════════════════════════════════╝

Starting API server...
MongoDB will be connected on first database operation.
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
