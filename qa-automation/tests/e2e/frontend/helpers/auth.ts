/**
 * Authentication Helper for E2E Tests
 * Handles login flow and ensures user is authenticated before accessing protected routes
 */
import { Page } from '@playwright/test'

/**
 * Test credentials to try (in order of preference)
 */
const TEST_CREDENTIALS = [
  { username: 'testcustomer', password: 'customerpassword123' },
  { username: 'testuser', password: 'password123' },
  { username: 'testuser', password: 'testpass' }
]

/**
 * Ensures user is authenticated. If login form is shown, attempts to login.
 * @param page Playwright page object
 * @returns Promise that resolves when user is authenticated
 */
export async function ensureAuthenticated(page: Page): Promise<void> {
  // Wait for any loading states
  await page.waitForLoadState('networkidle')
  
  // Wait for ProtectedRoute loading state to complete (if any)
  const loadingSpinner = page.locator('text=Loading, .animate-spin')
  try {
    await loadingSpinner.waitFor({ state: 'hidden', timeout: 5000 })
  } catch {
    // Loading spinner might not appear or already gone
  }
  
  // Wait a moment for React to render
  await page.waitForTimeout(500)
  
  // Check if login form is displayed (user not authenticated)
  const usernameInput = page.locator('input[id="username"], input[type="text"][placeholder*="username" i]')
  const passwordInput = page.locator('input[id="password"], input[type="password"]')
  const loginButton = page.locator('button:has-text("Sign In"), button:has-text("Login")')
  
  const isLoginFormVisible = await usernameInput.isVisible().catch(() => false)
  
  if (isLoginFormVisible) {
    // User needs to login - try credentials in order
    let loginSuccessful = false
    
    for (const creds of TEST_CREDENTIALS) {
      try {
        await usernameInput.fill(creds.username)
        await passwordInput.fill(creds.password)
        await loginButton.click()
        
        // Wait for login to complete
        await page.waitForLoadState('networkidle')
        await page.waitForTimeout(2000)
        
        // Check if we're still on login page
        const stillOnLogin = await usernameInput.isVisible().catch(() => false)
        if (!stillOnLogin) {
          loginSuccessful = true
          break
        }
      } catch (e) {
        // Try next credentials
        continue
      }
    }
    
    if (!loginSuccessful) {
      throw new Error(
        'Authentication required but login failed with all test credentials.\n' +
        'Please ensure test user is seeded (run: python flask_api/seed_test_user.py) or user is pre-authenticated.'
      )
    }
  }
}

/**
 * Navigates to Dashboard (Tasks page) and ensures authentication
 * @param page Playwright page object
 * @param waitForContent Whether to wait for dashboard content to load (default: true)
 */
export async function navigateToDashboard(
  page: Page,
  waitForContent: boolean = true
): Promise<void> {
  await page.goto('/')
  await page.click('text=Tasks')
  await page.waitForLoadState('networkidle')
  
  // Ensure user is authenticated
  await ensureAuthenticated(page)
  
  if (waitForContent) {
    // Wait for dashboard content to appear
    try {
      await Promise.race([
        page.waitForSelector('text=Total Tasks', { timeout: 15000, state: 'visible' }),
        page.waitForSelector('text=In Progress', { timeout: 15000, state: 'visible' }),
        page.waitForSelector('text=Good morning', { timeout: 15000, state: 'visible' }),
        page.waitForSelector('h1:has-text("Dashboard")', { timeout: 15000, state: 'visible' })
      ])
    } catch (error) {
      const url = page.url()
      const pageTitle = await page.title().catch(() => 'Unknown')
      
      // Check what's actually visible on the page
      const usernameInput = page.locator('input[id="username"]')
      const hasLoginForm = await usernameInput.isVisible().catch(() => false)
      const hasLoading = await page.locator('text=Loading').isVisible().catch(() => false)
      
      let diagnosticInfo = `URL: ${url}\nTitle: ${pageTitle}\n`
      if (hasLoginForm) {
        diagnosticInfo += 'Status: Login form is displayed (authentication required)\n'
      } else if (hasLoading) {
        diagnosticInfo += 'Status: Page is still loading\n'
      } else {
        diagnosticInfo += 'Status: Dashboard content did not appear\n'
      }
      
      throw new Error(
        `Dashboard content did not load after clicking Tasks.\n` +
        `${diagnosticInfo}` +
        `Expected to see "Total Tasks", "In Progress", "Good morning", or "Dashboard" heading.`
      )
    }
    
    // Wait for React to finish rendering
    await page.waitForTimeout(1000)
  }
}
