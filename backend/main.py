import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uvicorn
import os

def main():
    port = int(os.getenv("PORT", 7860))
    print(f"Starting Todo API server on port {port}")

    # Determine if we're in production
    is_production = os.getenv("ENVIRONMENT") == "production"

    # Run the FastAPI application
    # Import here to ensure the module is properly loaded
    from src.main import app

    if is_production:
        # Production settings
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            reload=False  # Disable hot reload in production
        )
    else:
        # Development settings
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            reload=True  # Enable hot reload for development
        )


if __name__ == "__main__":
    main()
