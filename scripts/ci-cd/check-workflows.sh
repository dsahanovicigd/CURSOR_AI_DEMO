#!/bin/bash
# Quick script to check GitHub Actions workflow status

REPO="dsahanovicigd/CURSOR_AI_DEMO"
REPO_URL="https://github.com/$REPO"

echo "🔍 Checking GitHub Actions workflows for: $REPO"
echo ""

# Check if gh CLI is installed
if command -v gh &> /dev/null; then
    # Check if authenticated
    if gh auth status &>/dev/null; then
        echo "📊 Latest Workflow Runs:"
        gh run list --repo $REPO --limit 5
        
        echo ""
        echo "🔄 Currently Running:"
        RUNNING=$(gh run list --status in_progress --repo $REPO --limit 5)
        if [ -z "$RUNNING" ]; then
            echo "   No workflows currently running"
        else
            echo "$RUNNING"
        fi
        
        echo ""
        echo "✅ Latest Successful Run:"
        gh run list --status success --repo $REPO --limit 1
        
        echo ""
        echo "❌ Latest Failed Run:"
        FAILED=$(gh run list --status failure --repo $REPO --limit 1)
        if [ -z "$FAILED" ]; then
            echo "   No recent failures"
        else
            echo "$FAILED"
        fi
        
        echo ""
        echo "📋 Available Workflows:"
        gh workflow list --repo $REPO
    else
        echo "⚠️  GitHub CLI not authenticated. Run: gh auth login"
        echo ""
        echo "🌐 View workflows in browser:"
        echo "$REPO_URL/actions"
    fi
else
    echo "⚠️  GitHub CLI not installed."
    echo ""
    echo "📦 Install with:"
    echo "   brew install gh"
    echo "   gh auth login"
    echo ""
    echo "🌐 Or view workflows in browser:"
    echo "$REPO_URL/actions"
fi

echo ""
echo "🔗 Direct Links:"
echo "   Actions: $REPO_URL/actions"
echo "   Settings: $REPO_URL/settings/actions"
