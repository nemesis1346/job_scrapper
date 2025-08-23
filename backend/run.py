#!/usr/bin/env python3
"""
Startup script for the Web3 Job Seeker Backend.

This script provides an easy way to start the FastAPI server with proper configuration.
It can be run directly or used as a module.

Usage:
    python run.py
    python run.py --host 0.0.0.0 --port 8000 --reload
"""

import argparse
import uvicorn
import logging
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from main import app
from config import settings

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=settings.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log')
        ]
    )

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Web3 Job Seeker Backend")
    parser.add_argument(
        "--host",
        default=settings.HOST,
        help=f"Host to bind to (default: {settings.HOST})"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.PORT,
        help=f"Port to bind to (default: {settings.PORT})"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        default=settings.RELOAD,
        help="Enable auto-reload on code changes"
    )
    parser.add_argument(
        "--log-level",
        default=settings.LOG_LEVEL,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help=f"Log level (default: {settings.LOG_LEVEL})"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    # Log startup information
    logger = logging.getLogger(__name__)
    logger.info("Starting Web3 Job Seeker Backend...")
    logger.info(f"Host: {args.host}")
    logger.info(f"Port: {args.port}")
    logger.info(f"Reload: {args.reload}")
    logger.info(f"Log Level: {args.log_level}")
    
    try:
        # Start the server
        uvicorn.run(
            "main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level=args.log_level.lower(),
            access_log=True
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
