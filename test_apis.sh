#!/bin/bash

# Test various job APIs for AI and blockchain jobs
# Save working APIs to a file

echo "Testing job APIs for AI and blockchain jobs..."
echo "=============================================="

# Create output file
OUTPUT_FILE="working_apis.txt"
echo "# Working Job APIs for AI and Blockchain Jobs" > $OUTPUT_FILE
echo "# Generated on $(date)" >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

# Function to test API and save if working
test_api() {
    local name="$1"
    local url="$2"
    local description="$3"
    
    echo "Testing: $name"
    echo "URL: $url"
    
    # Test the API
    response=$(curl -s -w "%{http_code}" "$url" 2>/dev/null)
    http_code="${response: -3}"
    content="${response%???}"
    
    echo "HTTP Code: $http_code"
    
    # Check if response is valid JSON or contains job data
    if [[ $http_code == "200" ]] && [[ -n "$content" ]]; then
        echo "✅ WORKING: $name"
        echo "## $name" >> $OUTPUT_FILE
        echo "URL: $url" >> $OUTPUT_FILE
        echo "Description: $description" >> $OUTPUT_FILE
        echo "" >> $OUTPUT_FILE
    else
        echo "❌ FAILED: $name"
    fi
    
    echo "----------------------------------------"
}

# Test various APIs

# 1. RemoteOK API
test_api "RemoteOK" "https://api.remoteok.io/v1/jobs.json" "Remote jobs including blockchain/AI"

# 2. GitHub Jobs (legacy)
test_api "GitHub Jobs" "https://jobs.github.com/positions.json?description=blockchain" "GitHub job board"

# 3. Adzuna API (test with demo credentials)
test_api "Adzuna" "https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=test&app_key=test&results_per_page=5&what=blockchain" "Adzuna job search API"

# 4. USA Jobs API
test_api "USA Jobs" "https://api.usa.gov/jobs/search.json?query=blockchain" "US government jobs"

# 5. Reed UK API
test_api "Reed UK" "https://api.reed.co.uk/v1/jobs/search?keywords=blockchain" "UK job search API"

# 6. Work in Startups API
test_api "Work in Startups" "https://api.workinstartups.com/job-board-api/jobs/" "Startup jobs"

# 7. CryptoJobsList API
test_api "CryptoJobsList" "https://api.cryptojobslist.com/jobs" "Crypto jobs API"

# 8. Indeed API (test endpoint)
test_api "Indeed" "https://api.indeed.com/ads/apisearch?publisher=test&q=blockchain&l=&sort=&radius=&st=&jt=&start=&limit=&fromage=&filter=&latlong=1&co=us&chnl=&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2" "Indeed job search"

# 9. LinkedIn API (test endpoint)
test_api "LinkedIn" "https://api.linkedin.com/v2/jobs?keywords=blockchain" "LinkedIn jobs API"

# 10. Google Jobs API (test endpoint)
test_api "Google Jobs" "https://jobs.googleapis.com/v3/jobs/search?query=blockchain" "Google Jobs API"

# 11. Stack Overflow Jobs API
test_api "Stack Overflow Jobs" "https://api.stackexchange.com/2.3/jobs?order=desc&sort=creation&tagged=blockchain&site=stackoverflow" "Stack Overflow jobs"

# 12. AngelList Jobs API
test_api "AngelList" "https://api.angel.co/1/jobs" "AngelList startup jobs"

# 13. Dice API
test_api "Dice" "https://api.dice.com/v1/jobs/search?q=blockchain" "Dice tech jobs"

# 14. ZipRecruiter API
test_api "ZipRecruiter" "https://api.ziprecruiter.com/jobs/v1?search=blockchain" "ZipRecruiter jobs"

# 15. SimplyHired API
test_api "SimplyHired" "https://api.simplyhired.com/v1/jobs?q=blockchain" "SimplyHired jobs"

# 16. CareerBuilder API
test_api "CareerBuilder" "https://api.careerbuilder.com/v1/jobs?keywords=blockchain" "CareerBuilder jobs"

# 17. Monster API
test_api "Monster" "https://api.monster.com/v1/jobs/search?q=blockchain" "Monster jobs"

# 18. Glassdoor API
test_api "Glassdoor" "https://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=test&t.k=test&action=jobs-prog&jobTitle=blockchain" "Glassdoor jobs"

# 19. Hired API
test_api "Hired" "https://api.hired.com/v1/jobs?q=blockchain" "Hired tech jobs"

# 20. Triplebyte API
test_api "Triplebyte" "https://api.triplebyte.com/v1/jobs?q=blockchain" "Triplebyte tech jobs"

# 21. Vettery API
test_api "Vettery" "https://api.vettery.com/v1/jobs?q=blockchain" "Vettery jobs"

# 22. The Ladders API
test_api "The Ladders" "https://api.theladders.com/v1/jobs?q=blockchain" "The Ladders jobs"

# 23. ClearanceJobs API
test_api "ClearanceJobs" "https://api.clearancejobs.com/v1/jobs?q=blockchain" "ClearanceJobs"

# 24. eFinancialCareers API
test_api "eFinancialCareers" "https://api.efinancialcareers.com/v1/jobs?q=blockchain" "eFinancialCareers"

# 25. HackerNews Who is Hiring
test_api "HN Who is Hiring" "https://hacker-news.firebaseio.com/v0/item/123456.json" "HackerNews job posts"

# 26. Reddit Jobs API
test_api "Reddit Jobs" "https://www.reddit.com/r/forhire/search.json?q=blockchain&restrict_sr=on&t=all&sort=new" "Reddit forhire subreddit"

# 27. Discord Jobs API (if exists)
test_api "Discord Jobs" "https://api.discord.com/v1/guilds/123456/messages?channel_id=123456" "Discord job channels"

# 28. Telegram Jobs Bot API
test_api "Telegram Jobs" "https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getUpdates" "Telegram job bots"

# 29. Slack Jobs API
test_api "Slack Jobs" "https://slack.com/api/conversations.history?channel=jobs" "Slack job channels"

# 30. Discord Jobs Server
test_api "Discord Jobs Server" "https://discord.com/api/v9/channels/123456/messages" "Discord job servers"

echo ""
echo "Testing completed!"
echo "Working APIs saved to: $OUTPUT_FILE"
echo ""
echo "Summary of working APIs:"
echo "========================"
if [ -s "$OUTPUT_FILE" ]; then
    cat "$OUTPUT_FILE"
else
    echo "No working APIs found."
fi
