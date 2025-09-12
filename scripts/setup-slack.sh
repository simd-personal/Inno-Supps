#!/bin/bash

# Slack App Setup Script for Inno Supps PromptOps MVP
# This script helps you set up the Slack bot integration

echo "🤖 Setting up Slack Bot for Inno Supps PromptOps"
echo "================================================"

echo ""
echo "📋 Prerequisites:"
echo "1. You need admin access to a Slack workspace"
echo "2. You need to create a Slack app at https://api.slack.com/apps"
echo ""

echo "🔧 Step 1: Create a Slack App"
echo "1. Go to https://api.slack.com/apps"
echo "2. Click 'Create New App'"
echo "3. Choose 'From scratch'"
echo "4. Name: 'Inno Supps PromptOps'"
echo "5. Select your workspace"
echo "6. Click 'Create App'"
echo ""

echo "🔧 Step 2: Configure Bot Token Scopes"
echo "1. In your app settings, go to 'OAuth & Permissions'"
echo "2. Add these Bot Token Scopes:"
echo "   - app_mentions:read"
echo "   - chat:write"
echo "   - commands"
echo "   - incoming-webhook"
echo "   - users:read"
echo "3. Click 'Install to Workspace'"
echo "4. Copy the 'Bot User OAuth Token' (starts with xoxb-)"
echo ""

echo "🔧 Step 3: Create Slash Command"
echo "1. Go to 'Slash Commands' in your app settings"
echo "2. Click 'Create New Command'"
echo "3. Fill in:"
echo "   - Command: /inno"
echo "   - Request URL: http://your-domain.com/api/slack/command"
echo "   - Short Description: Inno Supps PromptOps commands"
echo "   - Usage Hint: summary today"
echo "4. Click 'Save'"
echo ""

echo "🔧 Step 4: Update Environment Variables"
echo "Add these to your .env file:"
echo "SLACK_BOT_TOKEN=xoxb-your-bot-token-here"
echo "SLACK_SIGNING_SECRET=your-signing-secret-here"
echo ""

echo "🔧 Step 5: Test the Integration"
echo "1. Start your application: make dev"
echo "2. In Slack, type: /inno summary today"
echo "3. You should see a daily summary"
echo ""

echo "✅ Slack setup complete!"
echo ""
echo "📚 For more details, see:"
echo "- README.md - Full setup instructions"
echo "- docs/playbook.md - Daily workflow guide"
echo ""

read -p "Press Enter to continue..."
