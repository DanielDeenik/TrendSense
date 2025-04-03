"""
Standalone script to run the FastAPI backend
"""
import os
import sys
import uvicorn

def run_fastapi():
    """Run the FastAPI backend directly"""
    # Add backend directory to path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    # Get port from environment or use default
    port = int(os.environ.get('PORT', 8000))
    
    print(f"Starting FastAPI backend on http://0.0.0.0:{port}")
    
    # Run the FastAPI application
    uvicorn.run(
        "backend.simple_api:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )

if __name__ == '__main__':
    run_fastapi()