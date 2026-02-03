# How to Check if GitHub Actions Workflows Are Running

Complete guide to monitoring and checking GitHub Actions workflow status.

---

## Method 1: GitHub Web UI (Easiest)

### Check Workflow Runs

**Direct Link:**
```
https://github.com/dsahanovicigd/CURSOR_AI_DEMO/actions
```

**Steps:**
1. Go to your repository on GitHub
2. Click the **"Actions"** tab (top navigation)
3. You'll see a list of all workflow runs
4. Each run shows:
   - ✅ Green checkmark = Success
   - ❌ Red X = Failed
   - 🟡 Yellow circle = In Progress
   - ⚪ Gray circle = Queued/Pending

### View Workflow Details

1. Click on any workflow run
2. See:
   - **Status** (Running, Completed, Failed)
   - **Jobs** list (each job shows its status)
   - **Duration** (how long it took)
   - **Commit** that triggered it
   - **Branch** it ran on

### Filter Workflows

- Use the sidebar to filter by:
  - Workflow name (e.g., "QA Automation Pipeline")
  - Status (All, Success, Failure, etc.)
  - Branch
  - Actor (who triggered it)

---

## Method 2: GitHub CLI (Command Line)

### Install GitHub CLI

**macOS:**
```bash
brew install gh
gh auth login
```

**Linux:**
```bash
# See https://cli.github.com/manual/installation
```

### Check Workflow Runs

```bash
# List all workflow runs
gh run list --repo dsahanovicigd/CURSOR_AI_DEMO

# List runs for specific workflow
gh workflow list --repo dsahanovicigd/CURSOR_AI_DEMO
gh run list --workflow=qa-automation.yml --repo dsahanovicigd/CURSOR_AI_DEMO

# Watch runs in real-time
gh run watch --repo dsahanovicigd/CURSOR_AI_DEMO

# View specific run details
gh run view <RUN_ID> --repo dsahanovicigd/CURSOR_AI_DEMO

# View logs for a run
gh run view <RUN_ID> --log --repo dsahanovicigd/CURSOR_AI_DEMO
```

### Check Workflow Status

```bash
# Get latest run status
gh run list --limit 1 --repo dsahanovicigd/CURSOR_AI_DEMO

# Check if workflows are running
gh run list --status in_progress --repo dsahanovicigd/CURSOR_AI_DEMO
```

---

## Method 3: GitHub API

### Check Workflow Runs

```bash
# Get all workflow runs
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/dsahanovicigd/CURSOR_AI_DEMO/actions/runs

# Get latest run
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/dsahanovicigd/CURSOR_AI_DEMO/actions/runs?per_page=1

# Get runs for specific workflow
curl -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/dsahanovicigd/CURSOR_AI_DEMO/actions/workflows/qa-automation.yml/runs"
```

### Parse JSON Response

```bash
# Get latest run status
curl -s -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/dsahanovicigd/CURSOR_AI_DEMO/actions/runs?per_page=1 | \
  jq -r '.workflow_runs[0] | "\(.status) - \(.conclusion) - \(.name)"'

# Check if any workflows are running
curl -s -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/dsahanovicigd/CURSOR_AI_DEMO/actions/runs?status=in_progress | \
  jq '.workflow_runs | length'
```

---

## Method 4: Email/Notifications

### Enable Email Notifications

1. Go to GitHub Settings: https://github.com/settings/notifications
2. Under "Actions", enable:
   - ✅ Workflow runs
   - ✅ Workflow run failures
   - ✅ Workflow run approvals

### Check Email

You'll receive emails when:
- Workflow starts
- Workflow completes (success or failure)
- Workflow requires approval

---

## Method 5: Status Badges

### Add Status Badge to README

Add this to your `README.md`:

```markdown
![QA Automation](https://github.com/dsahanovicigd/CURSOR_AI_DEMO/workflows/QA%20Automation%20Pipeline/badge.svg)
```

**Badge URLs:**
- Success: Green badge
- Failure: Red badge
- Running: Yellow badge

---

## Method 6: Browser Extension

### GitHub Actions Status Extension

**Chrome/Edge:**
- Install "GitHub Actions Status" extension
- Shows workflow status in browser toolbar

---

## Quick Status Check Script

Create a script to quickly check workflow status:

```bash
#!/bin/bash
# check-workflows.sh

REPO="dsahanovicigd/CURSOR_AI_DEMO"

echo "🔍 Checking GitHub Actions workflows for: $REPO"
echo ""

# Check if gh CLI is installed
if command -v gh &> /dev/null; then
    echo "📊 Latest Workflow Runs:"
    gh run list --repo $REPO --limit 5
    
    echo ""
    echo "🔄 Currently Running:"
    gh run list --status in_progress --repo $REPO
    
    echo ""
    echo "✅ Latest Successful Run:"
    gh run list --status success --repo $REPO --limit 1
    
    echo ""
    echo "❌ Latest Failed Run:"
    gh run list --status failure --repo $REPO --limit 1
else
    echo "⚠️  GitHub CLI not installed. Install with: brew install gh"
    echo ""
    echo "🌐 View workflows in browser:"
    echo "https://github.com/$REPO/actions"
fi
```

**Usage:**
```bash
chmod +x check-workflows.sh
./check-workflows.sh
```

---

## Real-Time Monitoring

### Watch Workflows Live

**Using GitHub CLI:**
```bash
# Watch latest run
gh run watch --repo dsahanovicigd/CURSOR_AI_DEMO

# Watch specific run
gh run watch <RUN_ID> --repo dsahanovicigd/CURSOR_AI_DEMO
```

**Using Browser:**
1. Go to Actions tab
2. Click on a running workflow
3. Browser auto-refreshes to show progress

---

## Understanding Workflow Status

### Status Types

| Status | Icon | Meaning |
|--------|------|---------|
| **Queued** | ⚪ Gray | Waiting to start |
| **In Progress** | 🟡 Yellow | Currently running |
| **Completed** | ✅ Green | Successfully finished |
| **Failed** | ❌ Red | Failed with errors |
| **Cancelled** | ⚫ Black | Manually cancelled |
| **Skipped** | ⚪ Gray | Skipped due to conditions |

### Job Status

Within each workflow run, you'll see individual jobs:
- Each job can have its own status
- Click on a job to see detailed logs
- Jobs run in parallel or sequentially (depending on `needs`)

---

## Troubleshooting: Workflows Not Showing

### If workflows don't appear in Actions tab:

1. **Check if workflows are committed:**
   ```bash
   git ls-files .github/workflows/
   ```

2. **Check if workflows are pushed:**
   ```bash
   git log --oneline --all -- .github/workflows/
   ```

3. **Verify GitHub Actions is enabled:**
   - Go to: https://github.com/dsahanovicigd/CURSOR_AI_DEMO/settings/actions
   - Ensure "Allow all actions" is enabled

4. **Check workflow file syntax:**
   - Workflows must be valid YAML
   - File extension must be `.yml` or `.yaml`
   - Must be in `.github/workflows/` directory

---

## Quick Reference

### Web UI
```
https://github.com/dsahanovicigd/CURSOR_AI_DEMO/actions
```

### GitHub CLI Commands
```bash
gh run list                    # List all runs
gh run watch                   # Watch latest run
gh run view <ID>               # View run details
gh run view <ID> --log         # View logs
gh workflow list               # List workflows
```

### API Endpoints
```
GET /repos/{owner}/{repo}/actions/runs
GET /repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs
GET /repos/{owner}/{repo}/actions/runs/{run_id}
```

---

## Example: Check After Push

After pushing code:

```bash
# 1. Push your code
git push origin main

# 2. Wait a few seconds
sleep 5

# 3. Check workflow status
gh run list --repo dsahanovicigd/CURSOR_AI_DEMO --limit 1

# Or open in browser
open https://github.com/dsahanovicigd/CURSOR_AI_DEMO/actions
```

---

## Summary

**Easiest Method:** Open https://github.com/dsahanovicigd/CURSOR_AI_DEMO/actions

**Command Line:** `gh run list --repo dsahanovicigd/CURSOR_AI_DEMO`

**API:** `curl https://api.github.com/repos/dsahanovicigd/CURSOR_AI_DEMO/actions/runs`

**Email:** Enable notifications in GitHub settings
