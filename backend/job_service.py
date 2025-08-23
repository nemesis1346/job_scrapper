"""
Job Service for Web3 Job Seeker API.

This module contains the core business logic for:
- Fetching jobs from web3.careers API
- Processing and filtering job data
- Managing job refresh cycles
- Providing statistics and analytics

Author: Web3 Job Seeker Team
Date: 2024
"""

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any, Set
import requests
from bs4 import BeautifulSoup
import schedule
import time
from threading import Thread
import json
from collections import Counter, defaultdict

# Import our custom modules
from models import Job, TagInfo, Statistics
from config import settings, get_web3_careers_url

# Configure logging
logger = logging.getLogger(__name__)

class JobService:
    """
    Service class for managing job data and operations.
    
    This class handles all job-related operations including:
    - Fetching jobs from external APIs
    - Processing and storing job data
    - Filtering jobs based on various criteria
    - Providing statistics and analytics
    - Managing background refresh cycles
    """
    
    def __init__(self):
        """Initialize the JobService with empty data structures."""
        self.jobs: List[Job] = []
        self.jobs_by_id: Dict[int, Job] = {}
        self.tags_counter: Counter = Counter()
        self.companies_counter: Counter = Counter()
        self.countries_counter: Counter = Counter()
        self.last_refresh_time: Optional[datetime] = None
        self.is_refreshing: bool = False
        self.refresh_interval: int = settings.DEFAULT_REFRESH_INTERVAL
        
        logger.info("JobService initialized")
    
    async def initialize(self) -> None:
        """
        Initialize the service and fetch initial job data.
        
        This method is called on startup to populate the service with initial data.
        """
        logger.info("Initializing JobService...")
        await self.refresh_jobs()
        logger.info(f"JobService initialized with {len(self.jobs)} jobs")
    
    async def refresh_jobs(self) -> None:
        """
        Refresh job data from web3.careers API.
        
        This method fetches fresh job data and updates the internal storage.
        It handles rate limiting and error recovery.
        """
        if self.is_refreshing:
            logger.warning("Job refresh already in progress, skipping...")
            return
        
        self.is_refreshing = True
        start_time = datetime.now()
        
        try:
            logger.info("Starting job refresh...")
            
            # Fetch jobs for each tag
            new_jobs = []
            for tag in settings.DEFAULT_TAGS:
                try:
                    tag_jobs = await self._fetch_jobs_for_tag(tag)
                    new_jobs.extend(tag_jobs)
                    logger.info(f"Fetched {len(tag_jobs)} jobs for tag '{tag}'")
                    
                    # Small delay to avoid overwhelming the API
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"Error fetching jobs for tag '{tag}': {e}")
                    continue
            
            # Process and deduplicate jobs
            processed_jobs = self._process_jobs(new_jobs)
            
            # Update internal storage
            self._update_job_storage(processed_jobs)
            
            # Update statistics
            self._update_statistics()
            
            self.last_refresh_time = datetime.now()
            duration = (self.last_refresh_time - start_time).total_seconds()
            
            logger.info(f"Job refresh completed in {duration:.2f}s. Total jobs: {len(self.jobs)}")
            
        except Exception as e:
            logger.error(f"Error during job refresh: {e}")
            raise
        finally:
            self.is_refreshing = False
    
    async def _fetch_jobs_for_tag(self, tag: str) -> List[Dict[str, Any]]:
        """
        Fetch jobs for a specific tag from web3.careers API.
        
        Args:
            tag: The tag to search for
            
        Returns:
            List of job dictionaries from the API
            
        Raises:
            requests.RequestException: If the API request fails
        """
        url = get_web3_careers_url(tag)
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # The API returns jobs in the third element (index 2)
            if len(data) >= 3 and isinstance(data[2], list):
                return data[2]
            else:
                logger.warning(f"Unexpected API response structure for tag '{tag}'")
                return []
                
        except requests.RequestException as e:
            logger.error(f"API request failed for tag '{tag}': {e}")
            raise
    
    def _process_jobs(self, raw_jobs: List[Dict[str, Any]]) -> List[Job]:
        """
        Process raw job data into Job objects.
        
        This method:
        - Filters jobs by age and location
        - Processes job descriptions
        - Creates Job objects with proper validation
        - Deduplicates jobs
        
        Args:
            raw_jobs: List of raw job dictionaries from API
            
        Returns:
            List of processed Job objects
        """
        processed_jobs = []
        seen_job_ids = set()
        
        # Calculate cutoff date for job filtering (timezone-aware)
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=settings.JOB_AGE_DAYS)
        
        for raw_job in raw_jobs:
            try:
                # Skip if we've already seen this job
                job_id = raw_job.get('id')
                if job_id in seen_job_ids:
                    continue
                
                # Parse job date
                job_date = datetime.strptime(raw_job['date'], "%a, %d %b %Y %H:%M:%S %z")
                
                # Filter by date
                if job_date < cutoff_date:
                    continue
                
                # Filter by location (remote jobs only for now)
                country = raw_job.get('country', '').lower()
                location = raw_job.get('location', '').lower()
                
                if not (country in settings.REMOTE_LOCATIONS or 
                       location in settings.REMOTE_LOCATIONS):
                    continue
                
                # Process job description
                description_text = self._process_description(raw_job.get('description', ''))
                
                # Create Job object
                job_data = {
                    'id': job_id,
                    'title': raw_job.get('title', ''),
                    'company': raw_job.get('company', ''),
                    'location': raw_job.get('location', ''),
                    'country': raw_job.get('country', ''),
                    'city': raw_job.get('city'),
                    'description': raw_job.get('description', ''),
                    'description_text': description_text,
                    'apply_url': raw_job.get('apply_url', ''),
                    'tags': raw_job.get('tags', []),
                    'date': raw_job.get('date', ''),
                    'date_epoch': raw_job.get('date_epoch'),
                    'remote': True,  # All jobs are remote based on our filtering
                    'featured': raw_job.get('featured', False)
                }
                
                # Add optional fields if they exist
                if 'salary_min' in raw_job:
                    job_data['salary_min'] = raw_job['salary_min']
                if 'salary_max' in raw_job:
                    job_data['salary_max'] = raw_job['salary_max']
                if 'salary_currency' in raw_job:
                    job_data['salary_currency'] = raw_job['salary_currency']
                
                job = Job(**job_data)
                processed_jobs.append(job)
                seen_job_ids.add(job_id)
                
            except Exception as e:
                logger.error(f"Error processing job {raw_job.get('id', 'unknown')}: {e}")
                continue
        
        logger.info(f"Processed {len(processed_jobs)} jobs from {len(raw_jobs)} raw jobs")
        return processed_jobs
    
    def _process_description(self, description: str) -> str:
        """
        Process HTML job description into plain text.
        
        Args:
            description: HTML description string
            
        Returns:
            Plain text description
        """
        if not description:
            return ""
        
        try:
            soup = BeautifulSoup(description, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        except Exception as e:
            logger.warning(f"Error processing description: {e}")
            return description
    
    def _update_job_storage(self, new_jobs: List[Job]) -> None:
        """
        Update internal job storage with new jobs.
        
        Args:
            new_jobs: List of new Job objects
        """
        # Clear existing data
        self.jobs = new_jobs
        self.jobs_by_id = {job.id: job for job in new_jobs}
        
        logger.info(f"Updated job storage with {len(self.jobs)} jobs")
    
    def _update_statistics(self) -> None:
        """Update internal statistics counters."""
        # Reset counters
        self.tags_counter.clear()
        self.companies_counter.clear()
        self.countries_counter.clear()
        
        # Count occurrences
        for job in self.jobs:
            # Count tags
            for tag in job.tags:
                self.tags_counter[tag.lower()] += 1
            
            # Count companies
            self.companies_counter[job.company] += 1
            
            # Count countries
            self.countries_counter[job.country] += 1
        
        logger.debug(f"Updated statistics: {len(self.tags_counter)} tags, {len(self.companies_counter)} companies")
    
    def get_all_jobs(self) -> List[Job]:
        """
        Get all jobs in the system.
        
        Returns:
            List of all Job objects
        """
        return self.jobs.copy()
    
    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        """
        Get a specific job by its ID.
        
        Args:
            job_id: The job ID to look for
            
        Returns:
            Job object if found, None otherwise
        """
        return self.jobs_by_id.get(job_id)
    
    def get_filtered_jobs(
        self,
        tags: Optional[List[str]] = None,
        country: Optional[str] = None,
        company: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Job]:
        """
        Get filtered jobs based on various criteria.
        
        Args:
            tags: List of tags to filter by
            country: Country to filter by
            company: Company name to filter by
            limit: Maximum number of jobs to return
            offset: Number of jobs to skip
            
        Returns:
            List of filtered Job objects
        """
        filtered_jobs = self.jobs.copy()
        
        # Filter by tags
        if tags:
            tag_set = {tag.lower() for tag in tags}
            filtered_jobs = [
                job for job in filtered_jobs
                if any(tag.lower() in tag_set for tag in job.tags)
            ]
        
        # Filter by country
        if country:
            filtered_jobs = [
                job for job in filtered_jobs
                if job.country.lower() == country.lower()
            ]
        
        # Filter by company
        if company:
            filtered_jobs = [
                job for job in filtered_jobs
                if company.lower() in job.company.lower()
            ]
        
        # Apply pagination
        start_idx = offset
        end_idx = start_idx + limit
        paginated_jobs = filtered_jobs[start_idx:end_idx]
        
        return paginated_jobs
    
    def get_total_job_count(
        self,
        tags: Optional[List[str]] = None,
        country: Optional[str] = None,
        company: Optional[str] = None
    ) -> int:
        """
        Get total count of jobs matching the filters.
        
        Args:
            tags: List of tags to filter by
            country: Country to filter by
            company: Company name to filter by
            
        Returns:
            Total count of matching jobs
        """
        filtered_jobs = self.jobs.copy()
        
        # Apply same filters as get_filtered_jobs but without pagination
        if tags:
            tag_set = {tag.lower() for tag in tags}
            filtered_jobs = [
                job for job in filtered_jobs
                if any(tag.lower() in tag_set for tag in job.tags)
            ]
        
        if country:
            filtered_jobs = [
                job for job in filtered_jobs
                if job.country.lower() == country.lower()
            ]
        
        if company:
            filtered_jobs = [
                job for job in filtered_jobs
                if company.lower() in job.company.lower()
            ]
        
        return len(filtered_jobs)
    
    def get_available_tags(self) -> List[TagInfo]:
        """
        Get all available tags with their usage counts.
        
        Returns:
            List of TagInfo objects
        """
        tags = []
        for tag_name, count in self.tags_counter.most_common():
            # Determine tag category based on name
            category = self._categorize_tag(tag_name)
            
            tags.append(TagInfo(
                name=tag_name,
                count=count,
                category=category
            ))
        
        return tags
    
    def _categorize_tag(self, tag_name: str) -> str:
        """
        Categorize a tag based on its name.
        
        Args:
            tag_name: The tag name to categorize
            
        Returns:
            Category string
        """
        tag_lower = tag_name.lower()
        
        # Technology categories
        if tag_lower in ['solidity', 'rust', 'golang', 'python', 'javascript', 'typescript', 'java']:
            return 'programming_language'
        elif tag_lower in ['react', 'vue', 'angular', 'node', 'express', 'django', 'flask']:
            return 'framework'
        elif tag_lower in ['ethereum', 'bitcoin', 'polygon', 'arbitrum', 'optimism']:
            return 'blockchain'
        elif tag_lower in ['defi', 'dao', 'nft', 'gamefi', 'metaverse']:
            return 'web3_sector'
        elif tag_lower in ['smart-contracts', 'layer 2', 'zero knowledge', 'consensus']:
            return 'blockchain_technology'
        elif tag_lower in ['front end', 'back end', 'full stack', 'mobile', 'devops']:
            return 'role'
        else:
            return 'other'
    
    def get_statistics(self) -> Statistics:
        """
        Get comprehensive statistics about the job data.
        
        Returns:
            Statistics object with various metrics
        """
        if not self.jobs:
            return Statistics(
                total_jobs=0,
                remote_jobs=0,
                featured_jobs=0,
                total_companies=0,
                total_tags=0,
                jobs_by_country={},
                top_tags=[],
                top_companies=[],
                salary_stats={}
            )
        
        # Basic counts
        total_jobs = len(self.jobs)
        remote_jobs = sum(1 for job in self.jobs if job.remote)
        featured_jobs = sum(1 for job in self.jobs if job.featured)
        total_companies = len(self.companies_counter)
        total_tags = len(self.tags_counter)
        
        # Jobs by country
        jobs_by_country = dict(self.countries_counter)
        
        # Top tags
        top_tags = [
            TagInfo(name=tag, count=count, category=self._categorize_tag(tag))
            for tag, count in self.tags_counter.most_common(10)
        ]
        
        # Top companies
        top_companies = [
            {"name": company, "job_count": count}
            for company, count in self.companies_counter.most_common(10)
        ]
        
        # Salary statistics
        salaries = []
        for job in self.jobs:
            if job.salary_min:
                salaries.append(job.salary_min)
            if job.salary_max:
                salaries.append(job.salary_max)
        
        salary_stats = {}
        if salaries:
            salary_stats = {
                "average": sum(salaries) / len(salaries),
                "median": sorted(salaries)[len(salaries) // 2],
                "min": min(salaries),
                "max": max(salaries)
            }
        
        return Statistics(
            total_jobs=total_jobs,
            remote_jobs=remote_jobs,
            featured_jobs=featured_jobs,
            total_companies=total_companies,
            total_tags=total_tags,
            jobs_by_country=jobs_by_country,
            top_tags=top_tags,
            top_companies=top_companies,
            salary_stats=salary_stats
        )
    
    def start_background_refresh(self) -> None:
        """
        Start the background job refresh cycle.
        
        This method runs in a separate thread and refreshes jobs
        at regular intervals.
        """
        logger.info(f"Starting background refresh every {self.refresh_interval} seconds")
        
        def refresh_loop():
            while True:
                try:
                    # Schedule the refresh
                    schedule.every(self.refresh_interval).seconds.do(
                        lambda: asyncio.run(self.refresh_jobs())
                    )
                    
                    # Run pending tasks
                    while True:
                        schedule.run_pending()
                        time.sleep(1)
                        
                except Exception as e:
                    logger.error(f"Error in background refresh loop: {e}")
                    time.sleep(60)  # Wait before retrying
        
        # Start the refresh loop in a separate thread
        refresh_thread = Thread(target=refresh_loop, daemon=True)
        refresh_thread.start()
        
        logger.info("Background refresh started")
    
    def stop_background_refresh(self) -> None:
        """Stop the background refresh cycle."""
        schedule.clear()
        logger.info("Background refresh stopped")
    
    def set_refresh_interval(self, interval: int) -> None:
        """
        Set the refresh interval in seconds.
        
        Args:
            interval: New refresh interval in seconds
        """
        self.refresh_interval = interval
        logger.info(f"Refresh interval set to {interval} seconds")
