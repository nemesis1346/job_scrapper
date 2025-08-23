"""
Pydantic models for the Web3 Job Seeker API.

This module defines the data structures used throughout the API for:
- Job data representation
- API request/response models
- Validation and serialization

Author: Web3 Job Seeker Team
Date: 2024
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class JobType(str, Enum):
    """Enumeration of possible job types."""
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"

class ExperienceLevel(str, Enum):
    """Enumeration of experience levels."""
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"

class Job(BaseModel):
    """
    Job data model representing a single job posting.
    
    This model includes all the essential information about a job:
    - Basic job details (title, company, location)
    - Technical requirements (tags, skills)
    - Application information (URL, salary)
    - Metadata (dates, ID)
    """
    
    id: int = Field(..., description="Unique job identifier")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Job location")
    country: str = Field(..., description="Country where the job is located")
    city: Optional[str] = Field(None, description="City where the job is located")
    
    # Job details
    description: str = Field(..., description="Full job description")
    description_text: Optional[str] = Field(None, description="Plain text version of description")
    
    # Application info
    apply_url: str = Field(..., description="URL to apply for the job")
    salary_min: Optional[int] = Field(None, description="Minimum salary in USD")
    salary_max: Optional[int] = Field(None, description="Maximum salary in USD")
    salary_currency: Optional[str] = Field("USD", description="Salary currency")
    
    # Technical details
    tags: List[str] = Field(default_factory=list, description="List of job tags/skills")
    job_type: Optional[JobType] = Field(None, description="Type of employment")
    experience_level: Optional[ExperienceLevel] = Field(None, description="Required experience level")
    
    # Dates
    date: str = Field(..., description="Job posting date")
    date_epoch: Optional[int] = Field(None, description="Job posting date as epoch timestamp")
    
    # Additional metadata
    remote: bool = Field(False, description="Whether the job is remote")
    featured: bool = Field(False, description="Whether the job is featured")
    
    @validator('description_text', pre=True, always=True)
    def set_description_text(cls, v, values):
        """
        Automatically generate plain text description from HTML description.
        
        This validator ensures that if description_text is not provided,
        it will be automatically generated from the HTML description.
        """
        if v is None and 'description' in values:
            # This will be handled in the service layer with BeautifulSoup
            return values['description']
        return v
    
    @validator('remote', pre=True, always=True)
    def set_remote_status(cls, v, values):
        """
        Automatically determine if job is remote based on location/country.
        
        This validator checks if the job location indicates remote work.
        """
        if v is False:  # Only set if not already True
            location = values.get('location', '').lower()
            country = values.get('country', '').lower()
            return location in ['remote', 'anywhere'] or country in ['remote', 'anywhere']
        return v
    
    class Config:
        """Pydantic configuration for the Job model."""
        # Allow extra fields from API responses
        extra = "allow"
        # Use enum values for serialization
        use_enum_values = True
        # Example data for documentation
        json_schema_extra = {
            "example": {
                "id": 12345,
                "title": "Senior Solidity Developer",
                "company": "DeFi Protocol Inc",
                "location": "Remote",
                "country": "Remote",
                "city": None,
                "description": "<p>We are looking for a Senior Solidity Developer...</p>",
                "description_text": "We are looking for a Senior Solidity Developer...",
                "apply_url": "https://example.com/apply/12345",
                "salary_min": 80000,
                "salary_max": 150000,
                "salary_currency": "USD",
                "tags": ["solidity", "ethereum", "defi", "smart-contracts"],
                "job_type": "full-time",
                "experience_level": "senior",
                "date": "Mon, 15 Jan 2024 10:30:00 +0000",
                "date_epoch": 1705312200,
                "remote": True,
                "featured": False
            }
        }

class JobResponse(BaseModel):
    """
    Response model for job listing endpoints.
    
    This model wraps job data with pagination and filtering information
    to provide a complete response structure.
    """
    
    jobs: List[Job] = Field(..., description="List of job postings")
    total_count: int = Field(..., description="Total number of jobs matching the filters")
    limit: int = Field(..., description="Maximum number of jobs returned")
    offset: int = Field(..., description="Number of jobs skipped for pagination")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Applied filters")
    
    class Config:
        """Pydantic configuration for the JobResponse model."""
        json_schema_extra = {
            "example": {
                "jobs": [],
                "total_count": 150,
                "limit": 50,
                "offset": 0,
                "filters": {
                    "tags": ["solidity", "ethereum"],
                    "country": "Remote",
                    "company": None
                }
            }
        }

class TagInfo(BaseModel):
    """
    Information about a specific tag.
    
    This model provides metadata about tags including usage statistics.
    """
    
    name: str = Field(..., description="Tag name")
    count: int = Field(..., description="Number of jobs using this tag")
    category: Optional[str] = Field(None, description="Tag category (e.g., 'technology', 'framework')")
    
    class Config:
        """Pydantic configuration for the TagInfo model."""
        json_schema_extra = {
            "example": {
                "name": "solidity",
                "count": 45,
                "category": "technology"
            }
        }

class TagResponse(BaseModel):
    """
    Response model for tag listing endpoints.
    
    This model provides all available tags with their usage statistics.
    """
    
    tags: List[TagInfo] = Field(..., description="List of available tags")
    total_tags: int = Field(..., description="Total number of unique tags")
    
    @validator('total_tags', pre=True, always=True)
    def set_total_tags(cls, v, values):
        """Automatically set total_tags based on tags list length."""
        if v is None and 'tags' in values:
            return len(values['tags'])
        return v
    
    class Config:
        """Pydantic configuration for the TagResponse model."""
        json_schema_extra = {
            "example": {
                "tags": [
                    {"name": "solidity", "count": 45, "category": "technology"},
                    {"name": "ethereum", "count": 32, "category": "blockchain"}
                ],
                "total_tags": 2
            }
        }

class HealthResponse(BaseModel):
    """
    Response model for health check endpoint.
    
    This model provides system health information including
    job count and last refresh time.
    """
    
    status: str = Field(..., description="Service status (healthy/unhealthy)")
    timestamp: str = Field(..., description="Current timestamp")
    job_count: int = Field(..., description="Total number of jobs in the system")
    last_refresh: Optional[str] = Field(None, description="Last job refresh timestamp")
    
    class Config:
        """Pydantic configuration for the HealthResponse model."""
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-15T10:30:00Z",
                "job_count": 150,
                "last_refresh": "2024-01-15T10:25:00Z"
            }
        }

class JobFilters(BaseModel):
    """
    Model for job filtering parameters.
    
    This model defines all possible filtering options for job searches.
    """
    
    tags: Optional[List[str]] = Field(None, description="List of tags to filter by")
    country: Optional[str] = Field(None, description="Country to filter by")
    company: Optional[str] = Field(None, description="Company name to filter by")
    job_type: Optional[JobType] = Field(None, description="Job type to filter by")
    experience_level: Optional[ExperienceLevel] = Field(None, description="Experience level to filter by")
    remote_only: Optional[bool] = Field(None, description="Filter for remote jobs only")
    salary_min: Optional[int] = Field(None, description="Minimum salary filter")
    salary_max: Optional[int] = Field(None, description="Maximum salary filter")
    
    class Config:
        """Pydantic configuration for the JobFilters model."""
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "tags": ["solidity", "ethereum"],
                "country": "Remote",
                "company": None,
                "job_type": "full-time",
                "experience_level": "senior",
                "remote_only": True,
                "salary_min": 80000,
                "salary_max": None
            }
        }

class Statistics(BaseModel):
    """
    Model for system statistics.
    
    This model provides comprehensive statistics about the job data.
    """
    
    total_jobs: int = Field(..., description="Total number of jobs")
    remote_jobs: int = Field(..., description="Number of remote jobs")
    featured_jobs: int = Field(..., description="Number of featured jobs")
    total_companies: int = Field(..., description="Number of unique companies")
    total_tags: int = Field(..., description="Number of unique tags")
    jobs_by_country: Dict[str, int] = Field(..., description="Job count by country")
    top_tags: List[TagInfo] = Field(..., description="Most popular tags")
    top_companies: List[Dict[str, Any]] = Field(..., description="Companies with most job postings")
    salary_stats: Dict[str, Any] = Field(..., description="Salary statistics")
    
    class Config:
        """Pydantic configuration for the Statistics model."""
        json_schema_extra = {
            "example": {
                "total_jobs": 150,
                "remote_jobs": 120,
                "featured_jobs": 15,
                "total_companies": 45,
                "total_tags": 67,
                "jobs_by_country": {"Remote": 120, "USA": 20, "UK": 10},
                "top_tags": [
                    {"name": "solidity", "count": 45, "category": "technology"},
                    {"name": "ethereum", "count": 32, "category": "blockchain"}
                ],
                "top_companies": [
                    {"name": "DeFi Protocol Inc", "job_count": 8},
                    {"name": "Crypto Startup", "job_count": 5}
                ],
                "salary_stats": {
                    "average": 95000,
                    "median": 90000,
                    "min": 50000,
                    "max": 200000
                }
            }
        }
