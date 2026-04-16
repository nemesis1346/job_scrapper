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


## 📁 File Structure

```
scripts/
├── test_apis.sh                    # Primary API tests
├── test_additional_apis.sh         # Community API tests
├── working_apis.txt               # Primary results
├── additional_working_apis.txt    # Community results
├── working_apis_combined.txt      # All working APIs
├── API_TESTING_GUIDE.md           # Full documentation
└── API_QUICK_REFERENCE.md         # This file
```


## 🔄 Regular Maintenance

```bash
# Weekly health check
./test_apis.sh && ./test_additional_apis.sh

# Check for new APIs
# Review working_apis_combined.txt
# Update scripts with new endpoints
```

