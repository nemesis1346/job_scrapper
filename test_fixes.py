#!/usr/bin/env python3
"""
Test script to verify the fixes for low job count
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.append('backend')

# Import after adding to path
from job_service import JobService
from config import settings

async def test_job_fixes():
    """Test the job service with the new filtering logic."""
    
    print("🧪 Testing Job Service Fixes")
    print("=" * 50)
    
    # Initialize job service
    job_service = JobService()
    
    print(f"📋 Configuration:")
    print(f"   Job Age Days: {settings.JOB_AGE_DAYS}")
    print(f"   Remote Locations: {settings.REMOTE_LOCATIONS}")
    print(f"   Major Tech Hubs: {len(settings.MAJOR_TECH_HUBS)} countries")
    print(f"   Default Tags: {len(settings.DEFAULT_TAGS)} tags")
    print()
    
    # Test with a few popular tags first
    test_tags = ['blockchain', 'javascript', 'react', 'python', 'defi']
    
    total_jobs = 0
    for tag in test_tags:
        print(f"📋 Testing tag: '{tag}'")
        
        try:
            # Fetch jobs for this tag
            raw_jobs = await job_service._fetch_jobs_for_tag(tag)
            print(f"   Raw jobs from API: {len(raw_jobs)}")
            
            # Process jobs with new filtering
            processed_jobs = job_service._process_jobs(raw_jobs)
            print(f"   Processed jobs after filtering: {len(processed_jobs)}")
            
            total_jobs += len(processed_jobs)
            
            # Show some sample processed jobs
            if processed_jobs:
                print(f"   Sample jobs:")
                for i, job in enumerate(processed_jobs[:2]):
                    print(f"     {i+1}. {job.title} at {job.company}")
                    print(f"        Location: {job.location} ({job.country})")
                    print(f"        Remote: {job.remote}")
                    print(f"        Date: {job.date}")
                    print()
            else:
                print(f"   No jobs passed filtering")
                print()
                
        except Exception as e:
            print(f"   Error: {e}")
            print()
    
    print(f"🎯 Total jobs across {len(test_tags)} tags: {total_jobs}")
    print(f"📊 Average jobs per tag: {total_jobs / len(test_tags):.1f}")
    
    if total_jobs > 50:
        print("✅ SUCCESS: Job count significantly improved!")
    elif total_jobs > 20:
        print("⚠️  PARTIAL: Job count improved but could be better")
    else:
        print("❌ ISSUE: Job count still too low")
    
    print()
    print("🔍 Next steps:")
    print("1. Test with all tags")
    print("2. Check for duplicates")
    print("3. Verify job quality")
    print("4. Test API endpoints")

async def test_full_refresh():
    """Test the full job refresh process."""
    
    print("🔄 Testing Full Job Refresh")
    print("=" * 30)
    
    job_service = JobService()
    
    try:
        # Initialize and refresh jobs
        await job_service.initialize()
        
        # Get statistics
        stats = job_service.get_statistics()
        
        print(f"📊 Job Statistics:")
        print(f"   Total Jobs: {stats.total_jobs}")
        print(f"   Remote Jobs: {stats.remote_jobs}")
        print(f"   Featured Jobs: {stats.featured_jobs}")
        print(f"   Total Companies: {stats.total_companies}")
        print(f"   Total Tags: {stats.total_tags}")
        
        if stats.total_jobs > 100:
            print("✅ SUCCESS: Job count is now over 100!")
        elif stats.total_jobs > 50:
            print("⚠️  GOOD: Job count is over 50")
        else:
            print("❌ ISSUE: Job count still too low")
        
        # Show top tags
        print(f"\n🏷️  Top Tags:")
        for tag in stats.top_tags[:10]:
            print(f"   {tag.name}: {tag.count} jobs")
        
        # Show top companies
        print(f"\n🏢 Top Companies:")
        for company in stats.top_companies[:5]:
            print(f"   {company['name']}: {company['job_count']} jobs")
            
    except Exception as e:
        print(f"❌ Error during full refresh: {e}")

async def main():
    """Main test function."""
    print("🚀 Testing Job Service Fixes")
    print("=" * 50)
    
    # Test individual tag processing
    await test_job_fixes()
    
    print("\n" + "=" * 50)
    
    # Test full refresh
    await test_full_refresh()
    
    print("\n✅ Testing completed!")

if __name__ == "__main__":
    asyncio.run(main())
