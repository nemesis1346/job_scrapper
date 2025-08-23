# API Testing Quick Reference

## 🚀 Quick Commands

```bash
# Test all APIs
./test_apis.sh && ./test_additional_apis.sh

# View results
cat working_apis_combined.txt

# Test single API manually
curl -s -w "%{http_code}" "https://api.example.com/endpoint"
```

## 📋 Working APIs Summary

### ✅ Direct Job APIs

- **ClearanceJobs**: `https://api.clearancejobs.com/v1/jobs?q=blockchain`
- **HackerNews Who is Hiring**: `https://hacker-news.firebaseio.com/v0/item/{id}.json`
- **GitHub Issues**: `https://api.github.com/search/issues?q=label:job+blockchain`

### ✅ Community APIs

- **Stack Exchange Blockchain**: `https://api.stackexchange.com/2.3/questions?tagged=blockchain&site=stackoverflow`
- **Stack Exchange AI**: `https://api.stackexchange.com/2.3/questions?tagged=artificial-intelligence&site=stackoverflow`
- **Stack Exchange ML**: `https://api.stackexchange.com/2.3/questions?tagged=machine-learning&site=stackoverflow`

### ✅ Repository APIs

- **GitHub Repositories**: `https://api.github.com/search/repositories?q=blockchain+jobs`
- **GitHub Topics**: `https://api.github.com/search/repositories?q=topic:blockchain+topic:jobs`

## 🔧 Add New API

```bash
# Add to test_apis.sh
test_api "API Name" "https://api.example.com/endpoint" "Description"

# Run test
./test_apis.sh
```

## 📊 Rate Limits

| API            | Rate Limit                | Auth Required |
| -------------- | ------------------------- | ------------- |
| Stack Exchange | 10,000/day                | No            |
| GitHub         | 30/hour (unauthenticated) | Optional      |
| HackerNews     | No limit                  | No            |
| ClearanceJobs  | Unknown                   | No            |

## 🚨 Common Issues

| Status Code | Meaning         | Solution           |
| ----------- | --------------- | ------------------ |
| 200         | ✅ Success      | API is working     |
| 401         | ❌ Unauthorized | Add authentication |
| 403         | ❌ Forbidden    | Check API key      |
| 404         | ❌ Not Found    | Verify endpoint    |
| 429         | ❌ Rate Limited | Add delays         |

## 📁 File Structure

```
python_job_seeker/
├── test_apis.sh                    # Primary API tests
├── test_additional_apis.sh         # Community API tests
├── working_apis.txt               # Primary results
├── additional_working_apis.txt    # Community results
├── working_apis_combined.txt      # All working APIs
├── API_TESTING_GUIDE.md           # Full documentation
└── API_QUICK_REFERENCE.md         # This file
```

## 🎯 Implementation Priority

1. **High**: ClearanceJobs, GitHub Issues, Stack Exchange Jobs
2. **Medium**: HackerNews, Stack Exchange Blockchain/AI
3. **Low**: Web scraping fallbacks

## 🔄 Regular Maintenance

```bash
# Weekly health check
./test_apis.sh && ./test_additional_apis.sh

# Check for new APIs
# Review working_apis_combined.txt
# Update scripts with new endpoints
```

## 📞 Need Help?

- Check `API_TESTING_GUIDE.md` for detailed documentation
- Review HTTP status codes above
- Test manually with curl commands
- Check API documentation for authentication requirements
