#!/bin/bash

# GitHub Issues Setup Script for Web3 Job Seeker
# This script helps you set up environment variables and run the GitHub issues creator

echo "🚀 GitHub Issues Setup for Web3 Job Seeker"
echo "=========================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    echo "# GitHub Configuration" > .env
    echo "export GITHUB_TOKEN='your_github_token_here'" >> .env
    echo "export GITHUB_REPO='your_username/your_repo_name'" >> .env
    echo ""
    echo "✅ Created .env file"
    echo "📝 Please edit .env file with your actual values:"
    echo "   - GITHUB_TOKEN: Your GitHub Personal Access Token"
    echo "   - GITHUB_REPO: Your repository (format: username/repo-name)"
    echo ""
    echo "💡 To get a GitHub token:"
    echo "   1. Go to GitHub.com → Settings → Developer settings → Personal access tokens"
    echo "   2. Generate new token (classic)"
    echo "   3. Select 'repo' scope"
    echo ""
    read -p "Press Enter after you've updated the .env file..."
fi

# Load environment variables
if [ -f ".env" ]; then
    echo "📂 Loading environment variables from .env..."
    source .env
fi

# Check if required variables are set
if [ -z "$GITHUB_TOKEN" ] || [ "$GITHUB_TOKEN" = "your_github_token_here" ]; then
    echo "❌ GITHUB_TOKEN not set or still has default value"
    echo "Please update the .env file with your actual GitHub token"
    exit 1
fi

if [ -z "$GITHUB_REPO" ] || [ "$GITHUB_REPO" = "your_username/your_repo_name" ]; then
    echo "❌ GITHUB_REPO not set or still has default value"
    echo "Please update the .env file with your actual repository (format: username/repo-name)"
    exit 1
fi

echo "✅ Environment variables loaded:"
echo "   Repository: $GITHUB_REPO"
echo "   Token: ${GITHUB_TOKEN:0:10}..." # Show first 10 chars for security

# Check if python-dotenv is installed
echo "🔍 Checking dependencies..."
if ! python3 -c "import dotenv" 2>/dev/null; then
    echo "📦 Installing python-dotenv..."
    pip3 install python-dotenv
fi

# Check if requests is installed
if ! python3 -c "import requests" 2>/dev/null; then
    echo "📦 Installing requests..."
    pip3 install requests
fi

echo "✅ Dependencies ready"

# Confirm before running
echo ""
echo "🎯 Ready to create GitHub issues!"
echo "This will:"
echo "   - Create labels in your repository"
echo "   - Create 4 critical issues (skipping existing ones)"
echo "   - Repository: $GITHUB_REPO"
echo "   - Prevent duplicate issues automatically"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔧 Options:"
    echo "1. Create issues (with duplicate prevention)"
    echo "2. Test duplicate prevention functionality"
    echo "3. Both"
    echo ""
    read -p "Choose option (1/2/3): " -n 1 -r
    echo ""
    
    case $REPLY in
        1)
            echo "🚀 Running GitHub issues creator..."
            python3 create_github_issues.py
            ;;
        2)
            echo "🧪 Testing duplicate prevention..."
            python3 test_duplicate_prevention.py
            ;;
        3)
            echo "🧪 Testing duplicate prevention..."
            python3 test_duplicate_prevention.py
            echo ""
            echo "🚀 Running GitHub issues creator..."
            python3 create_github_issues.py
            ;;
        *)
            echo "❌ Invalid option"
            exit 1
            ;;
    esac
else
    echo "❌ Cancelled"
    exit 0
fi
