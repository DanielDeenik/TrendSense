#!/usr/bin/env python3
"""
Standalone script to run the FastAPI Storytelling backend
"""
import os
import sys
import uvicorn

def run_storytelling_api():
    """Run the FastAPI Storytelling backend directly"""
    print("Starting FastAPI Storytelling backend...")
    
    # Set the Python path to include the backend directory
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    sys.path.insert(0, backend_dir)
    
    # Change to the backend directory
    os.chdir(backend_dir)
    
    # Print environment variables for debugging (without values)
    print("\nEnvironment variables:")
    print(f"OPENAI_API_KEY exists: {bool(os.getenv('OPENAI_API_KEY'))}")
    print(f"DATABASE_URL exists: {bool(os.getenv('DATABASE_URL'))}")
    
    # Run the FastAPI application
    print("\nStarting Storytelling API server on port 8080...")
    uvicorn.run("storytelling_api:app", host="0.0.0.0", port=8080, log_level="info")

if __name__ == "__main__":
    run_storytelling_api()
