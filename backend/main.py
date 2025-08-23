"""
Main FastAPI application for the Web3 Job Seeker backend.

This module provides a REST API for fetching and filtering Web3 jobs from web3.careers.
The API includes endpoints for:
- Fetching all jobs with optional filtering
- Getting available tags for filtering
- Refreshing job data
- Health check endpoint

Author: Web3 Job Seeker Team
Date: 2024
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime, timedelta
import asyncio
import logging
from typing import List, Optional, Dict, Any
import requests
from bs4 import BeautifulSoup
import schedule
import time
from threading import Thread
import json

# Import our custom modules
from job_service import JobService
from models import Job, JobResponse, TagResponse, HealthResponse
from config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Web3 Job Seeker API",
    description="A comprehensive API for fetching and filtering Web3 jobs from web3.careers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize job service
job_service = JobService()

@app.on_event("startup")
async def startup_event():
    """
    Initialize the application on startup.
    
    This function runs when the FastAPI application starts and:
    1. Initializes the job service
    2. Starts the background job refresh task
    3. Logs the startup completion
    """
    logger.info("Starting Web3 Job Seeker API...")
    
    # Initialize job service and fetch initial data
    await job_service.initialize()
    
    # Start background job refresh task
    background_task = Thread(target=job_service.start_background_refresh, daemon=True)
    background_task.start()
    
    logger.info("Web3 Job Seeker API started successfully!")

@app.get("/", response_model=Dict[str, str])
async def root():
    """
    Root endpoint providing basic API information.
    
    Returns:
        Dict containing API name and version
    """
    return {
        "message": "Web3 Job Seeker API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify API status.
    
    Returns:
        HealthResponse containing API status and job count
    """
    try:
        job_count = len(job_service.get_all_jobs())
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            job_count=job_count,
            last_refresh=job_service.last_refresh_time.isoformat() if job_service.last_refresh_time else None
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service unhealthy")

@app.get("/jobs", response_model=JobResponse)
async def get_jobs(
    tags: Optional[str] = Query(None, description="Comma-separated list of tags to filter by"),
    country: Optional[str] = Query(None, description="Country to filter by"),
    company: Optional[str] = Query(None, description="Company name to filter by"),
    limit: int = Query(50, ge=1, le=200, description="Maximum number of jobs to return"),
    offset: int = Query(0, ge=0, description="Number of jobs to skip for pagination")
):
    """
    Get filtered jobs based on various criteria.
    
    This endpoint allows filtering jobs by:
    - Tags (comma-separated list)
    - Country
    - Company name
    
    Args:
        tags: Comma-separated list of tags to filter by
        country: Country to filter by
        company: Company name to filter by
        limit: Maximum number of jobs to return (1-200)
        offset: Number of jobs to skip for pagination
    
    Returns:
        JobResponse containing filtered jobs and metadata
    """
    try:
        # Parse tags if provided
        tag_list = None
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",")]
        
        # Get filtered jobs
        filtered_jobs = job_service.get_filtered_jobs(
            tags=tag_list,
            country=country,
            company=company,
            limit=limit,
            offset=offset
        )
        
        # Get total count for pagination
        total_count = job_service.get_total_job_count(
            tags=tag_list,
            country=country,
            company=company
        )
        
        return JobResponse(
            jobs=filtered_jobs,
            total_count=total_count,
            limit=limit,
            offset=offset,
            filters={
                "tags": tag_list,
                "country": country,
                "company": company
            }
        )
        
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch jobs")

@app.get("/jobs/refresh")
async def refresh_jobs():
    """
    Manually trigger a job refresh.
    
    This endpoint forces an immediate refresh of job data from web3.careers.
    Useful for testing or when immediate updates are needed.
    
    Returns:
        Dict containing refresh status and job count
    """
    try:
        await job_service.refresh_jobs()
        job_count = len(job_service.get_all_jobs())
        
        return {
            "message": "Jobs refreshed successfully",
            "job_count": job_count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error refreshing jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh jobs")

@app.get("/tags", response_model=TagResponse)
async def get_available_tags():
    """
    Get all available tags for filtering.
    
    Returns:
        TagResponse containing all available tags and their usage counts
    """
    try:
        tags = job_service.get_available_tags()
        return TagResponse(tags=tags)
    except Exception as e:
        logger.error(f"Error fetching tags: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch tags")

@app.get("/jobs/{job_id}", response_model=Job)
async def get_job_by_id(job_id: int):
    """
    Get a specific job by its ID.
    
    Args:
        job_id: The unique identifier of the job
    
    Returns:
        Job object if found
    
    Raises:
        HTTPException: If job is not found
    """
    try:
        job = job_service.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch job")

@app.get("/stats")
async def get_stats():
    """
    Get statistics about the job data.
    
    Returns:
        Dict containing various statistics about the job data
    """
    try:
        stats = job_service.get_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")

if __name__ == "__main__":
    """
    Run the FastAPI application directly.
    
    This allows running the application with: python main.py
    """
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
