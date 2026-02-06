from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from src.database.session import create_db_and_tables

# Load environment variables only in development
if os.getenv("ENVIRONMENT") != "production":
    load_dotenv()

# Check if running on Hugging Face Spaces
is_hf_space = bool(os.getenv("SPACE_ID"))

# Create FastAPI app - Always enable docs for Hugging Face Spaces
app = FastAPI(
    title="Todo API",
    version="1.0.0",
    # Always enable documentation for Hugging Face Spaces
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure allowed origins based on environment
default_origins = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000"
if is_hf_space:
    # When running on Hugging Face Spaces, allow requests from Vercel deployments
    default_origins += f",https://{os.getenv('SPACE_ID', '').split('/')[-1]}.hf.space,https://*.vercel.app,https://*.vercel.com"

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", default_origins).split(",")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers for client-side access
    expose_headers=["Access-Control-Allow-Origin"]
)

# Include API routes
from src.api.routes import auth, tasks
from src.api.chat import router as chat_router

app.include_router(auth.router, prefix="/api", tags=["authentication"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(chat_router, prefix="/api", tags=["chat"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API", "environment": "huggingface" if is_hf_space else "local"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)