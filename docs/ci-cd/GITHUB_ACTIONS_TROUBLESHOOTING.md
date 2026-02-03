# GitHub Actions Not Triggering - Troubleshooting Guide

## Issue
Pushed code to `main` branch but GitHub Actions workflows are not running automatically.

---

## Quick Checks

### 1. Verify Workflow Files Are Committed

```bash
# Check if workflow files are tracked by git
git ls-files .github/workflows/*.yml

# Check if there are uncommitted workflow files
git status .github/workflows/
```

**If workflow files are not committed:**
```bash
git add .github/workflows/*.yml
git commit -m "Add GitHub Actions workflows"
git push
```

### 2. Check GitHub Repository Settings

**Go to:** `https://github.com/dsahanovicigd/CURSOR_AI_DEMO/settings/actions`

**Verify:**
- ✅ **Actions** tab is enabled
- ✅ **Allow all actions and reusable workflows** is selected (or specific actions allowed)
- ✅ **Workflow permissions** are set correctly
- ✅ No branch protection rules blocking workflows

### 3. Check Workflow File Syntax

**Validate YAML syntax:**
```bash
# Install yamllint (optional)
pip install yamllint

# Check syntax
yamllint .github/workflows/qa-automation.yml
```

**Or use online validator:**
- https://www.yamllint.com/
- Copy workflow file content and validate

### 4. Check GitHub Actions Tab

**Go to:** `https://github.com/dsahanovicigd/CURSOR_AI_DEMO/actions`

**Look for:**
- Any failed workflow runs
- Any workflow runs at all
- Error messages

---

## Common Issues and Solutions

### Issue 1: GitHub Actions Not Enabled

**Symptom:** No workflows appear in Actions tab

**Solution:**
1. Go to repository Settings → Actions
2. Under "Actions permissions", select "Allow all actions and reusable workflows"
3. Save changes

### Issue 2: Workflow Files Not Committed

**Symptom:** Workflows exist locally but not in GitHub

**Solution:**
```bash
# Check what's not committed
git status

# Add and commit workflow files
git add .github/workflows/
git commit -m "Add CI/CD workflows"
git push origin main
```

### Issue 3: Branch Name Mismatch

**Symptom:** Pushed to different branch than configured

**Check:**
```bash
# Current branch
git branch --show-current

# Workflow triggers (should match)
cat .github/workflows/qa-automation.yml | grep -A 5 "branches:"
```

**Solution:** Either:
- Push to `main` or `develop` branch
- Or update workflow to include your branch name

### Issue 4: Workflow Syntax Error

**Symptom:** Workflow appears but shows error

**Check:**
- Go to Actions tab
- Click on failed workflow
- Check error message

**Common syntax errors:**
- Missing quotes around strings
- Incorrect indentation
- Invalid YAML structure

### Issue 5: Repository Settings Blocking Workflows

**Symptom:** Workflows disabled by organization/repository settings

**Check:**
1. Repository Settings → Actions → General
2. Verify "Allow all actions" is enabled
3. Check organization settings if applicable

---

## Step-by-Step Fix

### Step 1: Verify Workflow Files Are Pushed

```bash
cd /Users/dsahanovici/CURSOR_AI_DEMO

# Check if workflows are tracked
git ls-files .github/workflows/

# If empty or missing files, add them
git add .github/workflows/*.yml
git commit -m "Add GitHub Actions workflows"
git push origin main
```

### Step 2: Enable GitHub Actions

1. **Go to:** https://github.com/dsahanovicigd/CURSOR_AI_DEMO/settings/actions
2. **Under "Actions permissions":**
   - Select "Allow all actions and reusable workflows"
   - Or "Allow local actions and reusable workflows"
3. **Under "Workflow permissions":**
   - Select "Read and write permissions"
   - Check "Allow GitHub Actions to create and approve pull requests"
4. **Click "Save"**

### Step 3: Manually Trigger Workflow

**Option A: Via GitHub UI**
1. Go to: https://github.com/dsahanovicigd/CURSOR_AI_DEMO/actions
2. Select "QA Automation Pipeline" workflow
3. Click "Run workflow"
4. Select branch: `main`
5. Click "Run workflow"

**Option B: Make a Test Commit**
```bash
# Make a small change
echo "# Test" >> TEST.md
git add TEST.md
git commit -m "Test: Trigger CI/CD"
git push origin main
```

### Step 4: Check Workflow Status

1. Go to: https://github.com/dsahanovicigd/CURSOR_AI_DEMO/actions
2. Look for workflow runs
3. Click on a run to see details

---

## Verify Workflow Configuration

### Check Trigger Configuration

**File:** `.github/workflows/qa-automation.yml`

**Should have:**
```yaml
on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main
      - develop
```

### Verify File Location

Workflows must be in:
```
.github/workflows/*.yml
```

**Check:**
```bash
ls -la .github/workflows/
```

**Should see:**
- `qa-automation.yml`
- `basic-ci-cd.yml`
- `ci-cd-optimized.yml`
- etc.

---

## Testing Workflow Manually

### Test 1: Validate YAML Syntax

```bash
# Using Python
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/qa-automation.yml'))"
```

### Test 2: Check Workflow File

```bash
# Verify file exists and is readable
cat .github/workflows/qa-automation.yml | head -30
```

### Test 3: Create Test Commit

```bash
# Make a small change to trigger workflow
echo "test" >> .github/test-trigger.txt
git add .github/test-trigger.txt
git commit -m "test: trigger CI/CD"
git push origin main
```

---

## GitHub Actions Status Check

### Check if Actions Are Enabled

**Via GitHub API:**
```bash
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/dsahanovicigd/CURSOR_AI_DEMO/actions/workflows
```

**Or visit:**
https://github.com/dsahanovicigd/CURSOR_AI_DEMO/actions

### Check Recent Workflow Runs

**Via GitHub API:**
```bash
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/dsahanovicigd/CURSOR_AI_DEMO/actions/runs
```

---

## Quick Fix Script

```bash
#!/bin/bash
# Quick fix for GitHub Actions not triggering

cd /Users/dsahanovici/CURSOR_AI_DEMO

echo "1. Checking workflow files..."
if [ -d ".github/workflows" ]; then
    echo "✅ Workflows directory exists"
    ls -la .github/workflows/*.yml
else
    echo "❌ Workflows directory missing"
    exit 1
fi

echo ""
echo "2. Checking if workflows are tracked by git..."
if git ls-files .github/workflows/*.yml > /dev/null 2>&1; then
    echo "✅ Workflow files are tracked"
    git ls-files .github/workflows/*.yml
else
    echo "❌ Workflow files not tracked - adding them..."
    git add .github/workflows/*.yml
    git commit -m "Add GitHub Actions workflows"
    git push origin main
fi

echo ""
echo "3. Current branch:"
git branch --show-current

echo ""
echo "4. Recent commits:"
git log --oneline -3

echo ""
echo "✅ Check complete!"
echo ""
echo "Next steps:"
echo "1. Go to: https://github.com/dsahanovicigd/CURSOR_AI_DEMO/settings/actions"
echo "2. Enable 'Allow all actions and reusable workflows'"
echo "3. Go to: https://github.com/dsahanovicigd/CURSOR_AI_DEMO/actions"
echo "4. Manually trigger a workflow or make a new commit"
```

---

## Most Likely Causes

Based on your situation:

1. **GitHub Actions not enabled** (most common)
   - Go to repository settings and enable Actions

2. **Workflow files not pushed to GitHub**
   - Check if `.github/workflows/` files are committed
   - Push them if missing

3. **Branch protection rules**
   - Check repository settings for branch protection
   - May need to allow workflows to run

---

## Immediate Action Items

1. ✅ **Verify workflows are committed:**
   ```bash
   git ls-files .github/workflows/
   ```

2. ✅ **Enable GitHub Actions:**
   - Visit: https://github.com/dsahanovicigd/CURSOR_AI_DEMO/settings/actions
   - Enable Actions permissions

3. ✅ **Manually trigger workflow:**
   - Visit: https://github.com/dsahanovicigd/CURSOR_AI_DEMO/actions
   - Click "Run workflow" on "QA Automation Pipeline"

4. ✅ **Make a test commit:**
   ```bash
   echo "test" >> test.txt
   git add test.txt
   git commit -m "test: trigger CI/CD"
   git push origin main
   ```

---

## Still Not Working?

If workflows still don't trigger:

1. **Check GitHub status:** https://www.githubstatus.com/
2. **Check repository visibility:** Private repos may have restrictions
3. **Check organization settings:** If repo is in an organization
4. **Review GitHub Actions logs:** Check for any error messages
5. **Contact GitHub support:** If all else fails

---

## Verification Checklist

- [ ] Workflow files exist in `.github/workflows/`
- [ ] Workflow files are committed to git
- [ ] Workflow files are pushed to GitHub
- [ ] GitHub Actions enabled in repository settings
- [ ] Branch name matches workflow trigger (`main` or `develop`)
- [ ] No syntax errors in workflow files
- [ ] Repository has Actions permissions enabled
- [ ] No branch protection rules blocking workflows
