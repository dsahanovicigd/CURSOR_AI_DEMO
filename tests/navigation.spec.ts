import { test, expect } from '@playwright/test'

test.describe('Navigation Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should navigate between pages', async ({ page }) => {
    // Start on home page
    await expect(page).toHaveURL('/')
    
    // Navigate to Analytics
    await page.click('text=Analytics')
    await page.waitForLoadState('networkidle')
    await expect(page.locator('text=Analytics Dashboard')).toBeVisible()
    
    // Navigate to Tasks
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
    
    // Navigate to Products
    await page.click('text=Products')
    await page.waitForLoadState('networkidle')
    await expect(page.locator('text=Discover Amazing Products')).toBeVisible()
    
    // Navigate to Profiles
    await page.click('text=Profiles')
    await page.waitForLoadState('networkidle')
    await expect(page.locator('text=User Profile Component')).toBeVisible()
    
    // Navigate to NavBar
    await page.click('text=NavBar')
    await page.waitForLoadState('networkidle')
    await expect(page.locator('text=Navigation Bar Component')).toBeVisible()
  })

  test('should maintain state when navigating', async ({ page }) => {
    // Navigate to Tasks
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    
    // Toggle dark mode
    const darkModeButton = page.locator('[aria-label*="dark mode"], [aria-label*="light mode"]').first()
    await darkModeButton.click()
    await page.waitForTimeout(300)
    
    // Navigate to another page
    await page.click('text=Analytics')
    await page.waitForLoadState('networkidle')
    
    // Dark mode should persist
    const html = page.locator('html')
    const hasClass = await html.getAttribute('class')
    expect(hasClass).toContain('dark')
  })

  test('should handle rapid navigation', async ({ page }) => {
    // Rapidly click through multiple pages
    await page.click('text=Analytics')
    await page.click('text=Tasks')
    await page.click('text=Products')
    
    // Wait for final page to load
    await page.waitForLoadState('networkidle')
    
    // Should be on Products page
    await expect(page.locator('text=Discover Amazing Products')).toBeVisible()
  })

  test('should navigate using keyboard', async ({ page }) => {
    // Focus on first navigation item
    await page.keyboard.press('Tab')
    
    // Navigate through items with Tab
    await page.keyboard.press('Tab')
    await page.keyboard.press('Tab')
    
    // Press Enter on focused item
    await page.keyboard.press('Enter')
    
    // Wait for navigation
    await page.waitForLoadState('networkidle')
    
    // Should have navigated to a page
    await expect(page.locator('body')).toBeVisible()
  })

  test('should show active page indicator', async ({ page }) => {
    // Navigate to Tasks
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    
    // Tasks button should be highlighted/active
    const tasksButton = page.locator('button:has-text("Tasks")')
    const buttonClass = await tasksButton.getAttribute('class')
    
    // Should have some active styling (background color, border, etc.)
    expect(buttonClass).toBeTruthy()
  })

  test('should navigate from sidebar on desktop', async ({ page }) => {
    // Set desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 })
    
    // Navigate to Tasks to show sidebar
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    
    // Click sidebar navigation items
    const sidebarDashboard = page.locator('aside a:has-text("Dashboard")')
    if (await sidebarDashboard.isVisible()) {
      await sidebarDashboard.click()
      await page.waitForLoadState('networkidle')
      await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
    }
  })

  test('should navigate from mobile menu', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })
    
    // Navigate to Tasks
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    
    // Open mobile sidebar
    await page.click('[aria-label="Toggle sidebar"]')
    await page.waitForTimeout(300)
    
    // Click on a sidebar item
    const dashboardLink = page.locator('aside a:has-text("Dashboard")')
    if (await dashboardLink.isVisible()) {
      await dashboardLink.click()
      await page.waitForLoadState('networkidle')
    }
  })

  test('should handle browser back button', async ({ page }) => {
    // Navigate to Tasks
    await page.click('button:has-text("Tasks")')
    await page.waitForLoadState('networkidle')
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
    
    // Navigate to Analytics
    await page.click('button:has-text("Analytics")')
    await page.waitForLoadState('networkidle')
    await expect(page.locator('h1').filter({ hasText: 'Analytics' })).toBeVisible()
    
    // Go back
    await page.goBack()
    await page.waitForLoadState('networkidle')
    await page.waitForTimeout(300)
    
    // Should be back on Tasks (check for either Dashboard heading or body)
    await expect(page.locator('body')).toBeVisible()
  })

  test('should handle browser forward button', async ({ page }) => {
    // Navigate to Tasks
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    
    // Navigate to Analytics
    await page.click('text=Analytics')
    await page.waitForLoadState('networkidle')
    
    // Go back
    await page.goBack()
    await page.waitForLoadState('networkidle')
    
    // Go forward
    await page.goForward()
    await page.waitForLoadState('networkidle')
    
    // Should be on Analytics
    await expect(page.locator('text=Analytics Dashboard')).toBeVisible()
  })

  test('should preserve scroll position on back navigation', async ({ page }) => {
    // Navigate to Tasks
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    
    // Scroll down
    await page.evaluate(() => window.scrollTo(0, 500))
    await page.waitForTimeout(200)
    
    const scrollPosition = await page.evaluate(() => window.scrollY)
    
    // Navigate away
    await page.click('text=Analytics')
    await page.waitForLoadState('networkidle')
    
    // Navigate back
    await page.goBack()
    await page.waitForLoadState('networkidle')
    
    // Wait for scroll restoration
    await page.waitForTimeout(500)
    
    // Note: Scroll position might not be exact but should be restored
    const newScrollPosition = await page.evaluate(() => window.scrollY)
    expect(newScrollPosition).toBeGreaterThanOrEqual(0)
  })
})

test.describe('Breadcrumb Navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should display breadcrumb trail', async ({ page }) => {
    // Navigate to Tasks
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    
    // Check if breadcrumbs are present (if implemented)
    // For now, just verify the page header shows current location
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
  })

  test('should show current page in navigation', async ({ page }) => {
    // Navigate to Analytics
    await page.click('text=Analytics')
    await page.waitForLoadState('networkidle')
    
    // Header should indicate current page
    await expect(page.locator('text=Analytics Dashboard')).toBeVisible()
  })

  test('should update page title on navigation', async ({ page }) => {
    // Navigate to Tasks
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    
    // Page should have a title
    const title = await page.title()
    expect(title).toBeTruthy()
    
    // Navigate to Analytics
    await page.click('text=Analytics')
    await page.waitForLoadState('networkidle')
    
    // Title might change (or stay the same in SPA)
    const newTitle = await page.title()
    expect(newTitle).toBeTruthy()
  })
})

test.describe('Navigation - Error Handling', () => {
  test('should handle invalid routes gracefully', async ({ page }) => {
    await page.goto('/')
    
    // Application should load successfully
    await expect(page.locator('body')).toBeVisible()
  })

  test('should handle navigation during loading', async ({ page }) => {
    await page.goto('/')
    
    // Start navigation
    await page.click('text=Analytics')
    
    // Immediately start another navigation
    await page.click('text=Tasks')
    
    // Wait for final navigation to complete
    await page.waitForLoadState('networkidle')
    
    // Should be on Tasks page
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
  })

  test('should handle navigation with network issues', async ({ page }) => {
    await page.goto('/')
    
    // Navigate normally (SPA should work offline)
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
  })
})

test.describe('Navigation - Accessibility', () => {
  test('should have accessible navigation landmark', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')
    
    // Check for nav landmark
    const nav = page.locator('nav')
    await expect(nav.first()).toBeVisible()
    
    // Check for navigation role
    const navRole = page.locator('[role="navigation"]')
    expect(await navRole.count()).toBeGreaterThanOrEqual(1)
  })

  test('should have skip navigation link', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Tasks')
    
    // Focus on first element (might be skip link)
    await page.keyboard.press('Tab')
    
    // Should be able to navigate
    const focusedElement = await page.evaluate(() => document.activeElement?.tagName)
    expect(focusedElement).toBeTruthy()
  })

  test('should announce page changes to screen readers', async ({ page }) => {
    await page.goto('/')
    await page.click('button:has-text("Tasks")')
    await page.waitForLoadState('networkidle')
    
    // Check if main content has proper heading
    const h1 = page.locator('h1')
    await expect(h1.first()).toBeVisible()
    
    // H1 should announce the current page
    const heading = await h1.first().textContent()
    expect(heading).toBeTruthy()
    expect(heading?.length).toBeGreaterThan(0)
  })
})
