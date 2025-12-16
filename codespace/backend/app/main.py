"""
Main FastAPI application entry point.

This is where we create the FastAPI app, configure CORS,
register all routers, and initialize the database.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
import socketio
from fastapi.staticfiles import StaticFiles
from app.routers import auth, profiles, posts, datemates, ai, messages, upload
from app.utils.socketio_server import sio

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    description="Backend API for FlirtNet dating application"
)

# Configure CORS (allow frontend to make requests)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS],
    allow_origins=[], # Use regex for maximum compatibility
    allow_origin_regex=r".*", # Allow any origin (including local network IPs)
    allow_credentials=True, # Allow credentials (cookies/headers) with regex
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register all routers
app.include_router(auth.router)
app.include_router(profiles.router)
app.include_router(posts.router)
app.include_router(datemates.router)
app.include_router(ai.router)
app.include_router(messages.router)
app.include_router(upload.router)


@app.on_event("startup")
def startup_event():
    """
    Run when the application starts.
    Initialize the database (create tables if they don't exist).
    """
    print("🚀 Starting FlirtNet backend...")
    init_db()
    print(f"✅ Database initialized successfully!")
    print(f"✅ Server ready at http://localhost:8000")
    print(f"📚 API docs at http://localhost:8000/docs")
    print(f"🔌 Socket.IO ready at http://localhost:8000/socket.io/")


@app.get("/")
def root():
    """Root endpoint - health check."""
    return {
        "app": settings.APP_NAME,
        "status": "running",
        "message": "Welcome to FlirtNet API! Visit /docs for API documentation."
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Mount Socket.IO app - this becomes the main ASGI application
socket_app = socketio.ASGIApp(sio, app, socketio_path='/socket.io')

if __name__ == "__main__":
    import uvicorn
    # Use socket_app instead of app to enable Socket.IO
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)
