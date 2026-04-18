#!/bin/bash
# ============================================================
#   KL29 Royal Stream Bot — GitHub Push Script
#   Run this once inside your project folder
# ============================================================

set -e

REPO_URL="https://github.com/shareefshaji/tg-filestream-by-KL29ROYAL.git"

echo ""
echo "=================================================="
echo "   KL29 Royal Stream Bot - GitHub Push Script"
echo "=================================================="
echo ""

# Check git installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Init git if needed
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git branch -M main
fi

# Set remote
if git remote get-url origin &> /dev/null; then
    echo "🔗 Updating remote origin..."
    git remote set-url origin "$REPO_URL"
else
    echo "🔗 Adding remote origin..."
    git remote add origin "$REPO_URL"
fi

# Make sure .env is ignored
if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo ".env" >> .gitignore
    echo "✅ Added .env to .gitignore"
fi

# Stage all files
echo ""
echo "📦 Staging all files..."
git add .

# Commit
echo "💾 Committing..."
git commit -m "🚀 Initial commit - KL29 Royal Stream Bot with improved UI"

# Push
echo ""
echo "☁️  Pushing to GitHub..."
git push -u origin main --force

echo ""
echo "=================================================="
echo "✅ Done! All files pushed to GitHub successfully."
echo "🔗 Repo: $REPO_URL"
echo "=================================================="
echo ""
echo "📌 Next step: Deploy on Railway"
echo "   1. Go to https://railway.app"
echo "   2. New Project → Deploy from GitHub"
echo "   3. Select: tg-filestream-by-KL29ROYAL"
echo "   4. Add your environment variables"
echo "   5. Set start command: python -m WebStreamer"
echo ""
