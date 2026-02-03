# Lighthouse Error Fix

## Issue
Lighthouse error: "Chrome prevented page load with an interstitial. Make sure you are testing the correct URL and that the server is properly responding to all requests."

## Root Cause
The preview server cannot start on port 4173 due to permission issues (`EPERM: operation not permitted`).

## Solutions

### Option 1: Use Existing Server (Recommended)
If you have a dev server running, Lighthouse will use it automatically:

```bash
# Terminal 1: Start dev server
npm run dev

# Terminal 2: Run Lighthouse
bash qa-automation/scripts/run-lighthouse.sh
# Or use the fix-all-tests script
bash qa-automation/scripts/fix-all-tests.sh
```

### Option 2: Fix Port Permissions
Check what's using port 4173:

```bash
lsof -i :4173
# Kill the process if needed
kill -9 <PID>
```

### Option 3: Use Different Port
The script now tries port 4174 if 4173 is unavailable.

### Option 4: Manual Server Start
Start the preview server manually before running Lighthouse:

```bash
# Build and start preview server
npm run build
npm run preview -- --port 4173 --host 127.0.0.1

# In another terminal, run Lighthouse
npx lighthouse http://localhost:4173 --output=json --output-path=qa-automation/reports/lighthouse-results.json
```

### Option 5: Use npx Lighthouse (No Server Needed)
If you have a deployed URL, test that instead:

```bash
npx lighthouse https://your-deployed-url.com --output=json --output-path=qa-automation/reports/lighthouse-results.json
```

## Updated Scripts

1. **`qa-automation/scripts/fix-all-tests.sh`** - Updated with better error handling
2. **`qa-automation/scripts/run-lighthouse.sh`** - Standalone Lighthouse runner with server management

## Testing

Run the standalone Lighthouse script:

```bash
bash qa-automation/scripts/run-lighthouse.sh
```

This script will:
1. Check if a server is already running
2. Build the frontend if needed
3. Start a preview server on an available port
4. Run Lighthouse
5. Clean up the server

## Chrome Flags

The script uses these Chrome flags to avoid interstitial issues:
- `--headless` - Run in headless mode
- `--no-sandbox` - Disable sandbox (needed in some environments)
- `--disable-gpu` - Disable GPU acceleration
- `--disable-dev-shm-usage` - Use /tmp instead of /dev/shm

---

**Status:** Fixed with improved error handling and fallback options
