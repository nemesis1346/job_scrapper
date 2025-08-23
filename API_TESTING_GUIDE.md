# API Testing Guide for Job Data Sources

## Overview

This guide explains how to use the API testing scripts to find and validate new job data sources for AI and blockchain positions. The scripts automatically test various APIs and save working ones for future implementation.

## Files

- `test_apis.sh` - Tests primary job APIs
- `test_additional_apis.sh` - Tests community and developer APIs
- `working_apis_combined.txt` - Combined list of all working APIs
- `API_TESTING_GUIDE.md` - This documentation

## Quick Start

### 1. Test Primary Job APIs

```bash
chmod +x test_apis.sh
./test_apis.sh
```

### 2. Test Additional APIs

```bash
chmod +x test_additional_apis.sh
./test_additional_apis.sh
```

### 3. View Results

```bash
cat working_apis.txt
cat additional_working_apis.txt
cat working_apis_combined.txt
```

## Script Details

### test_apis.sh

**Purpose**: Tests traditional job board APIs and major platforms

**APIs Tested**:

- RemoteOK API
- GitHub Jobs (legacy)
- Adzuna API
- USA Jobs API
- Reed UK API
- Work in Startups API
- CryptoJobsList API
- Indeed API
- LinkedIn API
- Google Jobs API
- Stack Overflow Jobs API
- AngelList Jobs API
- Dice API
- ZipRecruiter API
- SimplyHired API
- CareerBuilder API
- Monster API
- Glassdoor API
- Hired API
- Triplebyte API
- Vettery API
- The Ladders API
- ClearanceJobs API
- eFinancialCareers API
- HackerNews Who is Hiring
- Reddit Jobs API
- Discord Jobs API
- Telegram Jobs Bot API
- Slack Jobs API
- Discord Jobs Server

**Output**: `working_apis.txt`

### test_additional_apis.sh

**Purpose**: Tests community-based APIs and developer platforms

**APIs Tested**:

- HackerNews Firebase API
- Reddit JSON APIs (various subreddits)
- GitHub Search APIs
- Stack Exchange APIs (multiple tags)
- Community platforms

**Output**: `additional_working_apis.txt`

## How to Add New APIs

### 1. Edit the Script

Add a new API test to either script:

```bash
# Add this to test_apis.sh or test_additional_apis.sh
test_api "API Name" "https://api.example.com/endpoint" "Description of the API"
```

### 2. Test Function Parameters

The `test_api` function takes 3 parameters:

- **Name**: Human-readable name for the API
- **URL**: The API endpoint to test
- **Description**: Brief description of what the API provides

### 3. Example Addition

```bash
# Add this to test_apis.sh
test_api "New Job Board" "https://api.newjobboard.com/jobs?q=blockchain" "New job board with blockchain positions"
```

## API Categories

### Direct Job APIs

These provide actual job listings:

- ClearanceJobs
- HackerNews Who is Hiring
- GitHub Issues (with job labels)

### Community APIs

These provide community discussions that may contain job posts:

- Stack Exchange (various tags)
- HackerNews Firebase
- Reddit subreddits

### Repository APIs

These search repositories for job-related content:

- GitHub Repositories
- GitHub Topics

## Rate Limits and Authentication

### No Authentication Required

- Stack Exchange APIs (10,000 requests/day)
- HackerNews Firebase (no limit)
- ClearanceJobs (basic access)

### Authentication Required

- GitHub APIs (30/hour unauthenticated, 5000/hour authenticated)
- Slack APIs (requires bot token)
- Most traditional job APIs

### Web Scraping Fallbacks

When APIs don't work, consider web scraping:

- CryptoJobsList
- AngelList
- RemoteOK
- WeWorkRemotely

## Implementation Priority

### High Priority (Direct Job Data)

1. ClearanceJobs API
2. GitHub Issues API
3. GitHub Repositories API
4. Stack Exchange Jobs API

### Medium Priority (Community Data)

5. HackerNews Firebase API
6. Stack Exchange Blockchain API
7. Stack Exchange AI/ML APIs

### Low Priority (Web Scraping)

8. Web scraping of job sites
9. Additional community sources

## Testing New API Endpoints

### 1. Manual Testing

```bash
# Test a single API endpoint
curl -s -w "%{http_code}" "https://api.example.com/endpoint" | tail -c 3
```

### 2. Check Response

```bash
# Get full response
curl -s "https://api.example.com/endpoint" | jq .
```

### 3. Add to Script

If the API works, add it to the appropriate script.

## Common HTTP Status Codes

- **200**: Success - API is working
- **401**: Unauthorized - Requires authentication
- **403**: Forbidden - Access denied
- **404**: Not Found - Endpoint doesn't exist
- **429**: Too Many Requests - Rate limited
- **500**: Server Error - API is down

## Best Practices

### 1. Rate Limiting

- Respect API rate limits
- Implement exponential backoff
- Use authentication when available

### 2. Error Handling

- Always check HTTP status codes
- Handle timeouts gracefully
- Log failed requests for debugging

### 3. Data Validation

- Verify response format (JSON, XML, etc.)
- Check for required fields
- Validate data quality

### 4. Caching

- Cache successful responses
- Implement TTL (Time To Live)
- Store failed requests to avoid retrying

## Integration with Job Service

### 1. Add New Data Source

```python
# In job_service.py
def fetch_from_new_api(self):
    """Fetch jobs from new API source."""
    try:
        response = requests.get("https://api.example.com/jobs")
        if response.status_code == 200:
            return self._process_new_api_data(response.json())
    except Exception as e:
        logger.error(f"Error fetching from new API: {e}")
    return []
```

### 2. Update Configuration

```python
# In config.py
class Settings(BaseSettings):
    NEW_API_URL: str = "https://api.example.com"
    NEW_API_KEY: Optional[str] = None
```

### 3. Add to Refresh Loop

```python
# In job_service.py
def refresh_jobs(self):
    """Refresh jobs from all sources."""
    all_jobs = []

    # Existing sources
    all_jobs.extend(self._fetch_web3_careers_jobs())

    # New sources
    all_jobs.extend(self.fetch_from_new_api())

    return self._process_jobs(all_jobs)
```

## Troubleshooting

### Common Issues

1. **API Returns 403 Forbidden**

   - Check if authentication is required
   - Verify API key/token
   - Check user agent requirements

2. **API Returns 404 Not Found**

   - Verify endpoint URL
   - Check API documentation
   - Ensure correct version

3. **API Returns 429 Too Many Requests**

   - Implement rate limiting
   - Add delays between requests
   - Use authentication for higher limits

4. **Empty or Invalid Response**
   - Check response format
   - Verify query parameters
   - Test with different search terms

### Debugging Commands

```bash
# Test with verbose output
curl -v "https://api.example.com/endpoint"

# Test with custom headers
curl -H "Authorization: Bearer token" "https://api.example.com/endpoint"

# Test with different user agent
curl -H "User-Agent: Mozilla/5.0" "https://api.example.com/endpoint"
```

## Future Enhancements

### 1. Automated Testing

- Schedule regular API tests
- Monitor API health
- Alert on failures

### 2. Data Quality Metrics

- Track response times
- Monitor data freshness
- Measure job relevance

### 3. Multi-Source Aggregation

- Combine data from multiple APIs
- Remove duplicates
- Rank by relevance

### 4. Machine Learning Integration

- Predict job relevance
- Auto-tag jobs
- Suggest similar positions

## Maintenance

### Regular Tasks

1. **Weekly**: Run API tests to check health
2. **Monthly**: Review and update API endpoints
3. **Quarterly**: Evaluate new API sources
4. **Annually**: Update rate limits and authentication

### Monitoring

- Track API response times
- Monitor error rates
- Log successful/failed requests
- Alert on service degradation

## Conclusion

These scripts provide a systematic approach to discovering and validating new job data sources. By regularly testing APIs and maintaining the working list, you can ensure your job aggregator has access to the most current and relevant job postings in the AI and blockchain space.

Remember to:

- Respect API terms of service
- Implement proper error handling
- Monitor rate limits
- Keep documentation updated
- Test new sources before production use
