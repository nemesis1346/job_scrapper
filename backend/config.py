"""
Configuration settings for the Web3 Job Seeker API.

This module manages all configuration settings including:
- API credentials and endpoints
- Database settings
- Application behavior settings
- Environment-specific configurations

Author: Web3 Job Seeker Team
Date: 2024
"""

import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings class using Pydantic for validation.
    
    This class manages all configuration settings with proper validation
    and default values. It supports both environment variables and .env files.
    """
    
    # API Configuration
    API_TITLE: str = Field(default="Web3 Job Seeker API", description="API title")
    API_VERSION: str = Field(default="1.0.0", description="API version")
    API_DESCRIPTION: str = Field(
        default="A comprehensive API for fetching and filtering Web3 jobs from web3.careers",
        description="API description"
    )
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    DEBUG: bool = Field(default=False, description="Debug mode")
    RELOAD: bool = Field(default=True, description="Auto-reload on code changes")
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(
        default=["*"],
        description="Allowed CORS origins"
    )
    CORS_CREDENTIALS: bool = Field(default=True, description="Allow CORS credentials")
    CORS_METHODS: List[str] = Field(
        default=["*"],
        description="Allowed CORS methods"
    )
    CORS_HEADERS: List[str] = Field(
        default=["*"],
        description="Allowed CORS headers"
    )
    
    # Web3.Careers API Configuration
    WEB3_CAREERS_TOKEN: str = Field(
        default=os.getenv("WEB3_CAREERS_TOKEN", "KWK9A42R5jgteRpxZo7EbdrZAFrNPj2R"),
        description="Web3.Careers API token"
    )
    WEB3_CAREERS_BASE_URL: str = Field(
        default="https://web3.career/api/v1",
        description="Web3.Careers API base URL"
    )
    WEB3_CAREERS_LIMIT: int = Field(default=200, description="Maximum jobs to fetch per request")
    
    # Job Filtering Configuration
    DEFAULT_JOB_LIMIT: int = Field(default=50, description="Default number of jobs per page")
    MAX_JOB_LIMIT: int = Field(default=200, description="Maximum jobs per page")
    DEFAULT_REFRESH_INTERVAL: int = Field(
        default=60,
        description="Default job refresh interval in seconds"
    )
    
    # Job Tags Configuration
    DEFAULT_TAGS: List[str] = Field(
        default=[
            'blockchain', 'javascript', 'backend', 'full stack', 'solidity',
            'ethereum', 'defi', 'smart-contracts', 'react', 'node', 'python',
            'rust', 'golang', 'web3', 'crypto', 'dao', 'nft', 'layer 2',
            'zero knowledge', 'front end', 'mobile', 'game dev', 'research',
            'typescript', 'nextjs', 'vue', 'angular', 'aws', 'docker', 'kubernetes',
            'machine-learning', 'ai', 'data-science', 'devops', 'security',
            'product-manager', 'design', 'marketing', 'sales', 'operations',
            'legal', 'finance', 'hr', 'community', 'content', 'support'
        ],
        description="Default tags to fetch jobs for"
    )
    
    # Date Filtering Configuration
    JOB_AGE_DAYS: int = Field(
        default=30,
        description="Maximum age of jobs to fetch (in days)"
    )
    
    # Remote Job Configuration
    REMOTE_LOCATIONS: List[str] = Field(
        default=['remote', 'Remote', 'anywhere', 'Anywhere'],
        description="Keywords that indicate remote work"
    )
    
    # Major Tech Hub Countries (for location filtering)
    MAJOR_TECH_HUBS: List[str] = Field(
        default=['united-states', 'united-kingdom', 'canada', 'germany', 'france', 'singapore', 'australia', 'netherlands', 'switzerland', 'ireland', 'portugal', 'spain', 'italy', 'belgium', 'austria', 'denmark', 'sweden', 'norway', 'finland', 'japan', 'south-korea', 'taiwan', 'hong-kong', 'india', 'brazil', 'mexico', 'argentina', 'chile', 'colombia', 'peru', 'uruguay', 'ecuador', 'south-africa', 'nigeria', 'kenya', 'ghana', 'uganda', 'tanzania', 'ethiopia', 'morocco', 'egypt', 'tunisia', 'algeria', 'libya', 'sudan', 'chad', 'niger', 'mali', 'burkina-faso', 'senegal', 'guinea', 'sierra-leone', 'liberia', 'ivory-coast', 'togo', 'benin', 'cameroon', 'central-african-republic', 'gabon', 'congo', 'democratic-republic-of-congo', 'angola', 'zambia', 'zimbabwe', 'botswana', 'namibia', 'lesotho', 'eswatini', 'madagascar', 'mauritius', 'seychelles', 'comoros', 'mayotte', 'reunion', 'saint-helena', 'ascension', 'tristan-da-cunha', 'falkland-islands', 'south-georgia', 'south-sandwich-islands', 'antarctica'],
        description="Major tech hub countries for location filtering"
    )
    
    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        description="Log format string"
    )
    
    # Cache Configuration
    CACHE_ENABLED: bool = Field(default=True, description="Enable caching")
    CACHE_TTL: int = Field(default=300, description="Cache TTL in seconds")
    
    # Rate Limiting Configuration
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Enable rate limiting")
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Requests per minute")
    RATE_LIMIT_WINDOW: int = Field(default=60, description="Rate limit window in seconds")
    
    # Database Configuration (for future use)
    DATABASE_URL: Optional[str] = Field(
        default=None,
        description="Database connection URL"
    )
    
    # Security Configuration
    SECRET_KEY: str = Field(
        default=os.getenv("SECRET_KEY", "your-secret-key-here"),
        description="Secret key for JWT tokens"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )
    
    # Monitoring Configuration
    ENABLE_METRICS: bool = Field(default=True, description="Enable metrics collection")
    METRICS_PORT: int = Field(default=9090, description="Metrics server port")
    
    class Config:
        """Pydantic configuration for Settings."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env file

# Create global settings instance
settings = Settings()

# Additional configuration functions
def get_web3_careers_url(tag: str, limit: Optional[int] = None) -> str:
    """
    Generate Web3.Careers API URL for a specific tag.
    
    Args:
        tag: The tag to search for
        limit: Optional limit override
    
    Returns:
        Complete API URL
    """
    limit = limit or settings.WEB3_CAREERS_LIMIT
    return f"{settings.WEB3_CAREERS_BASE_URL}?tag={tag}&limit={limit}&token={settings.WEB3_CAREERS_TOKEN}"

def get_allowed_origins() -> List[str]:
    """
    Get list of allowed CORS origins.
    
    Returns:
        List of allowed origins
    """
    if "*" in settings.CORS_ORIGINS:
        return ["*"]
    return settings.CORS_ORIGINS

def is_development() -> bool:
    """
    Check if running in development mode.
    
    Returns:
        True if in development mode
    """
    return settings.DEBUG or os.getenv("ENVIRONMENT", "development").lower() == "development"

def is_production() -> bool:
    """
    Check if running in production mode.
    
    Returns:
        True if in production mode
    """
    return os.getenv("ENVIRONMENT", "development").lower() == "production"

# Environment-specific configurations
class DevelopmentSettings(Settings):
    """Development-specific settings."""
    DEBUG: bool = True
    RELOAD: bool = True
    LOG_LEVEL: str = "DEBUG"

class ProductionSettings(Settings):
    """Production-specific settings."""
    DEBUG: bool = False
    RELOAD: bool = False
    LOG_LEVEL: str = "WARNING"
    CORS_ORIGINS: List[str] = ["https://yourdomain.com"]  # Update with your domain

# Function to get appropriate settings based on environment
def get_settings() -> Settings:
    """
    Get appropriate settings based on environment.
    
    Returns:
        Settings instance for current environment
    """
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    if environment == "production":
        return ProductionSettings()
    else:
        return DevelopmentSettings()

# Export the main settings instance
__all__ = ["settings", "get_web3_careers_url", "get_allowed_origins", "get_settings"]
