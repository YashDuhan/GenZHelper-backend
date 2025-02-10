import os
import sys
from dotenv import load_dotenv

# Load environment variables FIRST, before other imports
load_dotenv()

from fastapi import FastAPI
# Module for CORS
from fastapi.middleware.cors import CORSMiddleware
# Routes are declared in this Directory
from app.api.routes import app_router

# Check if running in dev container or Vercel only
if not (os.getenv('IS_DEVCONTAINER') or os.getenv('VERCEL')):
    print("\nThis application can only run inside a dev container or on Vercel\n")
    # Forcefully exit the app
    sys.exit(1)

# Verify GROQ_API_KEY is present
if not os.getenv('GROQ_API_KEY'):
    print("\nMissing required environment variable: GROQ_API_KEY\n")
    sys.exit(1)

app = FastAPI(title="GenZHelper Backend")

# To enable cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include the router
app.include_router(app_router)