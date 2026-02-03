# Pip Cache Fix - Conditional Caching

## Issue
The `flask_api/requirements.txt` file exists locally but is **not tracked in git**. When GitHub Actions checks out the code, the file doesn't exist, causing cache errors:
```
Error: No file matched to [flask_api/requirements.txt or **/pyproject.toml]
```

## Root Cause
- File exists locally: ✅ Yes
- File tracked in git: ❌ No (untracked)
- File available in CI: ❌ No

## Solution
Made pip caching **conditional** - check if file exists before using cache-dependency-path.

## Fix Applied

### Pattern Used
```yaml
- name: Check flask_api directory exists
  id: check_flask_api
  run: |
    if [ -f "flask_api/requirements.txt" ]; then
      echo "exists=true" >> $GITHUB_OUTPUT
    else
      echo "exists=false" >> $GITHUB_OUTPUT
      echo "Warning: flask_api/requirements.txt not found, skipping pip cache"
    fi

- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: ${{ env.PYTHON_VERSION }}
    cache: ${{ steps.check_flask_api.outputs.exists == 'true' && 'pip' || '' }}
    cache-dependency-path: ${{ steps.check_flask_api.outputs.exists == 'true' && 'flask_api/requirements.txt' || '' }}
```

## Files Modified

1. `.github/workflows/ci-cd.yml` - 5 instances fixed
2. `.github/workflows/ci-cd-optimized.yml` - 2 instances fixed

## Behavior

- **If file exists**: Uses pip cache normally
- **If file doesn't exist**: Skips cache but continues workflow (no error)

## Alternative Solution (Recommended)

**Commit the requirements.txt file to git:**
```bash
git add flask_api/requirements.txt
git commit -m "Add flask_api requirements.txt to repository"
git push origin main
```

This will enable caching in CI and improve build performance.

## Next Steps

1. **Immediate fix**: Conditional caching (already applied) ✅
2. **Long-term fix**: Commit `flask_api/requirements.txt` to git
3. **Verify**: Workflows should now run without cache errors
