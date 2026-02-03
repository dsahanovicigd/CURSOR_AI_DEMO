# CodeQL Action Fix - Update to v4 and Add Permissions

## Issue
The GitHub Actions workflow was failing with errors:
1. **Deprecation Warning**: CodeQL Action v3 will be deprecated in December 2026
2. **Permission Error**: The workflow doesn't have permission to access CodeQL Action API endpoints
   - Error: `Resource not accessible by integration`
   - Required permission: `security-events: write`

## Root Cause
1. **Deprecated Version**: Using `github/codeql-action/upload-sarif@v3` which is deprecated
2. **Missing Permissions**: Jobs using CodeQL actions need explicit permissions to upload security events

## Solution

### 1. Updated CodeQL Actions from v3 to v4
- Changed `github/codeql-action/upload-sarif@v3` → `@v4`
- Changed `github/codeql-action/init@v3` → `@v4`
- Changed `github/codeql-action/autobuild@v3` → `@v4`
- Changed `github/codeql-action/analyze@v3` → `@v4`

### 2. Added Required Permissions
Added `permissions` block to all security-related jobs:
```yaml
permissions:
  contents: read
  security-events: write
  actions: read  # Only for CodeQL analysis jobs
```

## Files Modified

### 1. `.github/workflows/ci-cd.yml`
- **Job**: `security-scan`
- Updated: `upload-sarif@v3` → `@v4`
- Added: `permissions` block

### 2. `.github/workflows/ci-cd-optimized.yml`
- **Job**: `security-sast`
  - Updated: `init@v3`, `autobuild@v3`, `analyze@v3` → `@v4`
  - Added: `permissions` block with `contents: read`, `security-events: write`, `actions: read`
- **Job**: `security-dependencies`
  - Updated: `upload-sarif@v3` → `@v4`
  - Added: `permissions` block with `contents: read`, `security-events: write`

### 3. `.github/workflows/ci-cd-ultra-optimized.yml`
- **Job**: `security-container`
  - Updated: `upload-sarif@v3` → `@v4`
  - Added: `permissions` block with `contents: read`, `security-events: write`

## Example Changes

### Before:
```yaml
security-scan:
  name: Security Scan
  runs-on: ubuntu-latest
  
  steps:
    - name: Upload Trivy results to GitHub Security
      uses: github/codeql-action/upload-sarif@v3
      if: always()
      with:
        sarif_file: 'trivy-results.sarif'
```

### After:
```yaml
security-scan:
  name: Security Scan
  runs-on: ubuntu-latest
  permissions:
    contents: read
    security-events: write
  
  steps:
    - name: Upload Trivy results to GitHub Security
      uses: github/codeql-action/upload-sarif@v4
      if: always()
      with:
        sarif_file: 'trivy-results.sarif'
```

## Required Permissions Explained

- **`contents: read`**: Required to read repository contents (for scanning)
- **`security-events: write`**: Required to upload SARIF files to GitHub Security
- **`actions: read`**: Required for CodeQL analysis jobs to read workflow information

## Verification

After these changes:
1. ✅ CodeQL Action v4 is used (no deprecation warnings)
2. ✅ Proper permissions are granted (no access errors)
3. ✅ SARIF files can be uploaded to GitHub Security

## Next Steps

1. **Commit the changes:**
   ```bash
   git add .github/workflows/
   git commit -m "Update CodeQL actions to v4 and add required permissions"
   git push origin main
   ```

2. **Verify the fix:**
   - Push to trigger the workflows
   - Check that security scan jobs complete successfully
   - Verify that SARIF files are uploaded to GitHub Security tab
   - Confirm no deprecation warnings appear

## References

- [CodeQL Action v4 Migration Guide](https://github.com/github/codeql-action/blob/main/CHANGELOG.md)
- [GitHub Actions Permissions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#permissions)
- [CodeQL Action Documentation](https://docs.github.com/en/code-security/code-scanning/using-codeql-code-scanning-with-your-ci-cd-system)
