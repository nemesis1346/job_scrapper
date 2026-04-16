#!/bin/bash

# Test additional job APIs for AI and blockchain jobs
# Save working APIs to a file

echo "Testing additional job APIs for AI and blockchain jobs..."
echo "========================================================"

# Create output file
OUTPUT_FILE="additional_working_apis.txt"
echo "# Additional Working Job APIs for AI and Blockchain Jobs" > $OUTPUT_FILE
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

# Test additional APIs

# 1. HackerNews Firebase API (real endpoint)
test_api "HackerNews Firebase" "https://hacker-news.firebaseio.com/v0/topstories.json" "HackerNews top stories"

# 2. HackerNews Who is Hiring (real endpoint)
test_api "HN Who is Hiring Real" "https://hacker-news.firebaseio.com/v0/item/123456.json" "HackerNews job posts"

# 3. Reddit JSON API (public)
test_api "Reddit JSON" "https://www.reddit.com/r/forhire.json" "Reddit forhire subreddit"

# 4. Reddit Search JSON
test_api "Reddit Search" "https://www.reddit.com/search.json?q=blockchain+job&restrict_sr=on&t=all&sort=new" "Reddit search for blockchain jobs"

# 5. Reddit r/cryptocurrencyjobs
test_api "Reddit Crypto Jobs" "https://www.reddit.com/r/cryptocurrencyjobs.json" "Reddit cryptocurrency jobs"

# 6. Reddit r/blockchainjobs
test_api "Reddit Blockchain Jobs" "https://www.reddit.com/r/blockchainjobs.json" "Reddit blockchain jobs"

# 7. Reddit r/ethdev
test_api "Reddit ETH Dev" "https://www.reddit.com/r/ethdev.json" "Reddit Ethereum development"

# 8. Reddit r/ethereum
test_api "Reddit Ethereum" "https://www.reddit.com/r/ethereum.json" "Reddit Ethereum community"

# 9. Reddit r/defi
test_api "Reddit DeFi" "https://www.reddit.com/r/defi.json" "Reddit DeFi community"

# 10. Reddit r/artificial
test_api "Reddit AI" "https://www.reddit.com/r/artificial.json" "Reddit AI community"

# 11. Reddit r/MachineLearning
test_api "Reddit ML" "https://www.reddit.com/r/MachineLearning.json" "Reddit Machine Learning"

# 12. Reddit r/datascience
test_api "Reddit Data Science" "https://www.reddit.com/r/datascience.json" "Reddit Data Science"

# 13. GitHub API (public repos)
test_api "GitHub Repos" "https://api.github.com/search/repositories?q=blockchain+jobs" "GitHub repositories with blockchain jobs"

# 14. GitHub Issues (job postings)
test_api "GitHub Issues" "https://api.github.com/search/issues?q=label:job+blockchain" "GitHub issues with job labels"

# 15. GitHub Topics
test_api "GitHub Topics" "https://api.github.com/search/repositories?q=topic:blockchain+topic:jobs" "GitHub repositories with blockchain and jobs topics"

# 16. Stack Exchange API (working endpoint)
test_api "Stack Exchange" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=blockchain&site=stackoverflow" "Stack Overflow blockchain questions"

# 17. Stack Exchange Jobs (different endpoint)
test_api "Stack Exchange Jobs" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=jobs&site=stackoverflow" "Stack Overflow job questions"

# 18. Stack Exchange AI
test_api "Stack Exchange AI" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=artificial-intelligence&site=stackoverflow" "Stack Overflow AI questions"

# 19. Stack Exchange ML
test_api "Stack Exchange ML" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=machine-learning&site=stackoverflow" "Stack Overflow ML questions"

# 20. Stack Exchange Solidity
test_api "Stack Exchange Solidity" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=solidity&site=stackoverflow" "Stack Overflow Solidity questions"

# 21. Stack Exchange Ethereum
test_api "Stack Exchange Ethereum" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=ethereum&site=stackoverflow" "Stack Overflow Ethereum questions"

# 22. Stack Exchange Web3
test_api "Stack Exchange Web3" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=web3&site=stackoverflow" "Stack Overflow Web3 questions"

# 23. Stack Exchange DeFi
test_api "Stack Exchange DeFi" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=defi&site=stackoverflow" "Stack Overflow DeFi questions"

# 24. Stack Exchange NFT
test_api "Stack Exchange NFT" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=nft&site=stackoverflow" "Stack Overflow NFT questions"

# 25. Stack Exchange Smart Contracts
test_api "Stack Exchange Smart Contracts" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=smart-contracts&site=stackoverflow" "Stack Overflow Smart Contracts questions"

# 26. Stack Exchange Rust
test_api "Stack Exchange Rust" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=rust&site=stackoverflow" "Stack Overflow Rust questions"

# 27. Stack Exchange Python
test_api "Stack Exchange Python" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=python&site=stackoverflow" "Stack Overflow Python questions"

# 28. Stack Exchange JavaScript
test_api "Stack Exchange JavaScript" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=javascript&site=stackoverflow" "Stack Overflow JavaScript questions"

# 29. Stack Exchange React
test_api "Stack Exchange React" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=react&site=stackoverflow" "Stack Overflow React questions"

# 30. Stack Exchange Node.js
test_api "Stack Exchange Node.js" "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged=node.js&site=stackoverflow" "Stack Overflow Node.js questions"

echo ""
echo "Additional testing completed!"
echo "Working APIs saved to: $OUTPUT_FILE"
echo ""
echo "Summary of working APIs:"
echo "========================"
if [ -s "$OUTPUT_FILE" ]; then
    cat "$OUTPUT_FILE"
else
    echo "No working APIs found."
fi
