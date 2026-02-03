# E2E Test Server Guide

## Do I Need to Stop the Server?

**Short Answer: No, you don't need to stop the server!**

## How It Works

### Playwright Configuration

Your `playwright.config.ts` has:
```typescript
webServer: {
  command: 'npm run dev',
  url: 'http://localhost:5173',
  reuseExistingServer: true, // ← This is the key setting
  timeout: 120 * 1000,
}
```

The `reuseExistingServer: true` setting tells Playwright to:
1. **Check if a server is already running** on `http://localhost:5173`
2. **If yes**: Use the existing server (don't start a new one)
3. **If no**: Start the server automatically

## Running `run-all-qa.sh`

When you run `./qa-automation/scripts/run-all-qa.sh`:

### ✅ Server Already Running (Recommended)
```bash
# Start your dev server (if not already running)
npm run dev

# In another terminal, run QA tests
./qa-automation/scripts/run-all-qa.sh
```

**Result**: Playwright detects the existing server and uses it. Tests run immediately.

### ⚠️ Server Not Running
```bash
# Just run QA tests
./qa-automation/scripts/run-all-qa.sh
```

**Result**: Playwright will:
1. Start the dev server automatically
2. Wait for it to be ready (up to 120 seconds)
3. Run the tests
4. Keep the server running (or stop it, depending on config)

## Current Issue

There's a known issue where Playwright sometimes tries to start the server even when `reuseExistingServer: true` is set, especially if:
- Multiple processes are using port 5173
- The server is running but Playwright can't detect it properly
- There are permission issues

## Solutions

### Option 1: Keep Server Running (Best)
```bash
# Terminal 1: Start server
npm run dev

# Terminal 2: Run QA tests
./qa-automation/scripts/run-all-qa.sh
```

### Option 2: Let Playwright Start Server
```bash
# Stop your dev server first
# Then run QA tests - Playwright will start it
./qa-automation/scripts/run-all-qa.sh
```

### Option 3: Skip E2E Tests Temporarily
```bash
# Skip E2E tests if server issues
SKIP_E2E=true ./qa-automation/scripts/run-all-qa.sh
```

## Verifying Server Status

Check if server is running:
```bash
# Check port 5173
lsof -ti:5173 && echo "✅ Server running" || echo "❌ Server not running"

# Or test connection
curl http://localhost:5173 > /dev/null 2>&1 && echo "✅ Server accessible" || echo "❌ Server not accessible"
```

## Troubleshooting

### Error: "listen EPERM: operation not permitted"

This happens when:
- Multiple processes try to bind to port 5173
- Playwright tries to start server even though one exists

**Fix**: Ensure only one dev server is running, or stop all servers before running tests.

### Tests Run But No Results

If tests run but `test-results/results.json` is missing:
1. Check if JSON reporter is configured in `playwright.config.ts`
2. Verify tests actually executed (check output)
3. Run: `npm run test -- --reporter=json`

### Server Starts But Tests Fail

If Playwright starts the server but tests fail:
1. Check server logs for errors
2. Verify `baseURL: 'http://localhost:5173'` matches your server
3. Ensure server is fully ready before tests run

## Best Practice

**Recommended Workflow:**
1. Start dev server manually: `npm run dev`
2. Wait for server to be ready
3. Run QA tests: `./qa-automation/scripts/run-all-qa.sh`
4. Playwright will reuse the existing server
5. Tests run faster (no server startup delay)

## Summary

| Scenario | Need to Stop Server? | What Happens |
|----------|----------------------|--------------|
| Server running + `reuseExistingServer: true` | ❌ No | Playwright uses existing server |
| Server not running | ❌ No | Playwright starts server automatically |
| Multiple servers on port | ⚠️ Yes | Stop extra servers to avoid conflicts |
| Permission errors | ⚠️ Maybe | Check port permissions or stop conflicting processes |

**Bottom Line**: With `reuseExistingServer: true`, you typically **don't need to stop the server**. However, if you encounter port conflicts or permission errors, stopping the server first may help.
