#!/bin/bash
# Automated deployment script for Todo Full-Stack Application

set -e  # Exit on any error

echo "🚀 Starting deployment of Todo Full-Stack Application..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."
if ! command_exists git; then
    echo "❌ Git is not installed. Please install Git and try again."
    exit 1
fi

if ! command_exists curl; then
    echo "❌ Curl is not installed. Please install Curl and try again."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "📦 Initializing new git repository..."
    git init
    git add .
    git commit -m "Initial commit: Todo Full-Stack Application with deployment configuration"
fi

# Check for uncommitted changes
if [[ -z $(git status -s) ]]; then
    echo "✅ Working directory is clean"
else
    echo "📝 You have uncommitted changes. Please commit them before deploying:"
    git status
    read -p "Do you want to commit all changes? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "Prepare for deployment"
    else
        echo "❌ Please commit your changes before deploying"
        exit 1
    fi
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git branch -M main
read -p "Enter your GitHub repository URL (or press Enter to skip GitHub push): " github_url
if [ ! -z "$github_url" ]; then
    git remote add origin "$github_url" 2>/dev/null || git remote set-url origin "$github_url"
    git push -u origin main
    echo "✅ Successfully pushed to GitHub"
else
    echo "⏭️  Skipping GitHub push"
fi

echo ""
echo "🎉 Deployment preparation completed!"
echo ""
echo "Next steps:"
echo "1. For Backend Deployment (to Render):"
echo "   - Go to https://render.com"
echo "   - Connect your GitHub repository"
echo "   - Create a new Web Service with the backend folder"
echo "   - Use build command: pip install -r requirements.txt"
echo "   - Use start command: uvicorn src.main:app --host=0.0.0.0 --port=\$PORT"
echo "   - Set environment variables from backend/.env.example"
echo ""
echo "2. For Frontend Deployment (to Vercel):"
echo "   - Go to https://vercel.com"
echo "   - Connect your GitHub repository"
echo "   - Import the project and select the frontend folder"
echo "   - Set NEXT_PUBLIC_API_BASE_URL to your backend URL"
echo ""
echo "3. Update CORS settings in your backend to allow your frontend domain"
echo ""
echo "💡 Pro tip: Check the README.md file for detailed deployment instructions"