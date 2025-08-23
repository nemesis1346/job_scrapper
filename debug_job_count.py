#!/usr/bin/env python3
"""
Debug script to investigate low job count from web3.careers API
"""

import asyncio
import requests
import json
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
import sys
import os

# Define minimal settings for debugging
class DebugSettings:
    WEB3_CAREERS_TOKEN = "KWK9A42R5jgteRpxZo7EbdrZAFrNPj2R"
    WEB3_CAREERS_BASE_URL = "https://web3.career/api/v1"
    WEB3_CAREERS_LIMIT = 200
    JOB_AGE_DAYS = 4
    REMOTE_LOCATIONS = ['remote', 'Remote', 'anywhere', 'Anywhere']
    DEFAULT_TAGS = [
        'blockchain', 'javascript', 'backend', 'full stack', 'solidity',
        'ethereum', 'defi', 'smart-contracts', 'react', 'node', 'python',
        'rust', 'golang', 'web3', 'crypto', 'dao', 'nft', 'layer 2',
        'zero knowledge', 'front end', 'mobile', 'game dev', 'research'
    ]

def get_web3_careers_url(tag: str, limit: int = None) -> str:
    """Generate Web3.Careers API URL for a specific tag."""
    limit = limit or DebugSettings.WEB3_CAREERS_LIMIT
    return f"{DebugSettings.WEB3_CAREERS_BASE_URL}?tag={tag}&limit={limit}&token={DebugSettings.WEB3_CAREERS_TOKEN}"

async def debug_web3_careers_api():
    """Debug the web3.careers API to understand why we're getting so few jobs."""
    
    print("🔍 Debugging Web3.Careers API")
    print("=" * 50)
    
    # Test each tag individually
    for tag in DebugSettings.DEFAULT_TAGS:
        print(f"\n📋 Testing tag: '{tag}'")
        print("-" * 30)
        
        url = get_web3_careers_url(tag)
        print(f"URL: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response structure: {type(data)} with {len(data)} elements")
                
                # Check if we have the expected structure
                if len(data) >= 3 and isinstance(data[2], list):
                    jobs = data[2]
                    print(f"Jobs found: {len(jobs)}")
                    
                    if jobs:
                        # Show first job structure
                        print(f"First job keys: {list(jobs[0].keys())}")
                        
                        # Check date filtering
                        cutoff_date = datetime.now(timezone.utc) - timedelta(days=DebugSettings.JOB_AGE_DAYS)
                        print(f"Cutoff date: {cutoff_date}")
                        
                        recent_jobs = 0
                        remote_jobs = 0
                        total_jobs = len(jobs)
                        
                        for job in jobs:
                            try:
                                # Check date
                                job_date = datetime.strptime(job['date'], "%a, %d %b %Y %H:%M:%S %z")
                                if job_date >= cutoff_date:
                                    recent_jobs += 1
                                    
                                    # Check location
                                    country = job.get('country', '').lower()
                                    location = job.get('location', '').lower()
                                    
                                    if (country in DebugSettings.REMOTE_LOCATIONS or 
                                        location in DebugSettings.REMOTE_LOCATIONS):
                                        remote_jobs += 1
                            except Exception as e:
                                print(f"Error processing job date: {e}")
                        
                        print(f"Total jobs: {total_jobs}")
                        print(f"Recent jobs (within {DebugSettings.JOB_AGE_DAYS} days): {recent_jobs}")
                        print(f"Remote jobs: {remote_jobs}")
                        
                        # Show some sample jobs
                        if jobs:
                            print("\nSample jobs:")
                            for i, job in enumerate(jobs[:3]):
                                print(f"  {i+1}. {job.get('title', 'No title')} at {job.get('company', 'No company')}")
                                print(f"     Date: {job.get('date', 'No date')}")
                                print(f"     Location: {job.get('location', 'No location')} ({job.get('country', 'No country')})")
                                print(f"     Tags: {job.get('tags', [])}")
                                print()
                    else:
                        print("No jobs found in response")
                else:
                    print(f"Unexpected response structure: {data}")
                    
            else:
                print(f"Error response: {response.text}")
                
        except Exception as e:
            print(f"Error: {e}")
        
        # Small delay between requests
        await asyncio.sleep(1)
    
    print("\n" + "=" * 50)
    print("🔍 Summary of Issues:")
    print("1. Check if API is returning fewer jobs than expected")
    print("2. Check if date filtering is too restrictive")
    print("3. Check if location filtering is too restrictive")
    print("4. Check if API rate limiting is affecting results")
    print("5. Check if all tags are being processed correctly")

async def test_api_limits():
    """Test API limits and rate limiting."""
    print("\n🔍 Testing API Limits")
    print("=" * 30)
    
    # Test with different limits
    limits = [50, 100, 200, 500]
    tag = "blockchain"  # Use a popular tag
    
    for limit in limits:
        url = f"{DebugSettings.WEB3_CAREERS_BASE_URL}?tag={tag}&limit={limit}&token={DebugSettings.WEB3_CAREERS_TOKEN}"
        print(f"\nTesting limit: {limit}")
        print(f"URL: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if len(data) >= 3 and isinstance(data[2], list):
                    jobs = data[2]
                    print(f"Jobs returned: {len(jobs)}")
                else:
                    print("Unexpected response structure")
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Error: {e}")
        
        await asyncio.sleep(2)  # Longer delay for rate limiting test

async def test_date_filtering():
    """Test different date ranges to see if filtering is too restrictive."""
    print("\n🔍 Testing Date Filtering")
    print("=" * 30)
    
    tag = "blockchain"
    date_ranges = [1, 7, 14, 30, 60]  # Days
    
    for days in date_ranges:
        print(f"\nTesting {days} days ago cutoff")
        
        url = get_web3_careers_url(tag)
        try:
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if len(data) >= 3 and isinstance(data[2], list):
                    jobs = data[2]
                    
                    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
                    recent_jobs = 0
                    
                    for job in jobs:
                        try:
                            job_date = datetime.strptime(job['date'], "%a, %d %b %Y %H:%M:%S %z")
                            if job_date >= cutoff_date:
                                recent_jobs += 1
                        except:
                            pass
                    
                    print(f"Total jobs: {len(jobs)}")
                    print(f"Jobs within {days} days: {recent_jobs}")
                    
        except Exception as e:
            print(f"Error: {e}")
        
        await asyncio.sleep(1)

async def main():
    """Main debug function."""
    print("🚀 Starting Web3.Careers API Debug")
    print("=" * 50)
    
    # Test basic API functionality
    await debug_web3_careers_api()
    
    # Test API limits
    await test_api_limits()
    
    # Test date filtering
    await test_date_filtering()
    
    print("\n✅ Debug completed!")

if __name__ == "__main__":
    asyncio.run(main())
