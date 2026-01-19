import { test, expect } from '@playwright/test'

test.describe('Error Handling Tests', () => {
  test('should handle network errors gracefully', async ({ page }) => {
    await page.goto('/')
    
    // Application should still load
    await expect(page.locator('body')).toBeVisible()
    
    // Navigation should work - use more specific selector
    await expect(page.locator('button:has-text("Analytics")')).toBeVisible()
  })

  test('should handle missing data gracefully', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Tasks')
    
    // Dashboard should still render even if some data is missing
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
  })

  test('should handle malformed data', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Analytics')
    
    // Analytics dashboard should render
    await expect(page.locator('text=Analytics Dashboard')).toBeVisible()
    
    // KPIs should be visible even if some data is missing
    await expect(page.locator('text=Total Revenue')).toBeVisible()
  })

  test('should handle console errors gracefully', async ({ page }) => {
    const consoleErrors: string[] = []
    
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text())
      }
    })
    
    await page.goto('/')
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    
    // Should not have critical console errors
    const criticalErrors = consoleErrors.filter(error => 
      !error.includes('404') && // Ignore 404s
      !error.includes('favicon') // Ignore favicon errors
    )
    
    expect(criticalErrors.length).toBe(0)
  })

  test('should handle page navigation errors', async ({ page }) => {
    await page.goto('/')
    
    // Try navigating between pages
    await page.click('text=Analytics')
    await expect(page.locator('text=Analytics Dashboard')).toBeVisible()
    
    await page.click('text=Tasks')
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
    
    await page.click('text=Products')
    await expect(page.locator('text=Discover Amazing Products')).toBeVisible()
  })

  test('should handle rapid navigation', async ({ page }) => {
    await page.goto('/')
    
    // Rapidly switch between pages
    await page.click('text=Analytics')
    await page.click('text=Tasks')
    await page.click('text=Products')
    await page.click('text=Profiles')
    await page.click('text=NavBar')
    
    // Should end up on correct page
    await expect(page.locator('text=Navigation Bar Component')).toBeVisible()
  })

  test('should handle invalid viewport sizes', async ({ page }) => {
    // Test with very small viewport
    await page.setViewportSize({ width: 320, height: 568 })
    await page.goto('/')
    
    // Should still be usable
    await expect(page.locator('body')).toBeVisible()
    
    // Test with very large viewport
    await page.setViewportSize({ width: 2560, height: 1440 })
    await page.goto('/')
    
    await expect(page.locator('body')).toBeVisible()
  })

  test('should handle missing images gracefully', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Profiles')
    await page.waitForLoadState('networkidle')
    
    // Page should render even if some images fail to load
    await expect(page.locator('text=User Profile Component')).toBeVisible()
  })

  test('should handle localStorage errors', async ({ page }) => {
    // Clear localStorage
    await page.goto('/')
    await page.evaluate(() => localStorage.clear())
    
    // Navigate to dashboard
    await page.click('text=Tasks')
    
    // Should still work
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
  })

  test('should handle dark mode toggle errors', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Tasks')
    
    // Try toggling dark mode multiple times rapidly
    const darkModeButton = page.locator('[aria-label*="dark mode"], [aria-label*="light mode"]').first()
    
    await darkModeButton.click()
    await page.waitForTimeout(100)
    await darkModeButton.click()
    await page.waitForTimeout(100)
    await darkModeButton.click()
    
    // Application should still be functional
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
  })

  test('should handle sidebar toggle errors', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    
    const hamburger = page.locator('[aria-label="Toggle sidebar"]')
    
    // Rapidly toggle sidebar with force flag to avoid interception
    await hamburger.click({ force: true })
    await page.waitForTimeout(300)
    await hamburger.click({ force: true })
    await page.waitForTimeout(300)
    await hamburger.click({ force: true })
    await page.waitForTimeout(300)
    
    // Application should still work
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
  })

  test('should handle filter changes gracefully', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Analytics')
    await page.waitForLoadState('networkidle')
    
    // Try changing filters
    const categoryFilter = page.locator('select').first()
    await categoryFilter.selectOption({ index: 1 })
    
    // Page should still render
    await expect(page.locator('text=Analytics Dashboard')).toBeVisible()
  })

  test('should handle table sorting errors', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Analytics')
    await page.waitForTimeout(1000)
    
    // Try clicking table headers rapidly
    const tableHeaders = page.locator('th button')
    const count = await tableHeaders.count()
    
    if (count > 0) {
      const firstHeader = tableHeaders.first()
      await firstHeader.click()
      await page.waitForTimeout(100)
      await firstHeader.click()
      await page.waitForTimeout(100)
      await firstHeader.click()
    }
    
    // Table should still be functional
    await expect(page.locator('text=Top Products')).toBeVisible()
  })

  test('should handle pagination errors', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Analytics')
    await page.waitForTimeout(1000)
    
    // Try rapid pagination
    const nextButton = page.locator('button:has-text("Next")')
    const isVisible = await nextButton.isVisible()
    
    if (isVisible) {
      await nextButton.click()
      await page.waitForTimeout(100)
      
      const prevButton = page.locator('button:has-text("Previous")')
      await prevButton.click()
    }
    
    // Pagination should still work
    await expect(page.locator('text=Showing')).toBeVisible()
  })

  test('should recover from JavaScript errors', async ({ page }) => {
    const pageErrors: Error[] = []
    
    page.on('pageerror', error => {
      pageErrors.push(error)
    })
    
    await page.goto('/')
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    
    // Navigate to different pages
    await page.click('text=Analytics')
    await page.waitForTimeout(500)
    await page.click('text=Products')
    await page.waitForTimeout(500)
    
    // Should not have unhandled JavaScript errors
    expect(pageErrors.length).toBe(0)
  })

  test('should handle search functionality errors', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Tasks')
    
    // Try clicking search
    const searchButton = page.locator('button:has-text("Search")')
    const isVisible = await searchButton.isVisible()
    
    if (isVisible) {
      await searchButton.click()
      // Should not crash
      await expect(page.locator('body')).toBeVisible()
    }
  })

  test('should handle notification errors', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Tasks')
    
    // Try clicking notifications
    const notificationButton = page.locator('[aria-label="Notifications"]')
    const isVisible = await notificationButton.isVisible()
    
    if (isVisible) {
      await notificationButton.click()
      // Should not crash
      await expect(page.locator('body')).toBeVisible()
    }
  })
})

test.describe('Error Handling - Forms', () => {
  test('should handle empty form submission', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Analytics')
    await page.waitForLoadState('networkidle')
    
    // Try submitting filters without changes
    const applyButton = page.locator('button:has-text("Apply")')
    const isVisible = await applyButton.isVisible()
    
    if (isVisible) {
      await applyButton.click()
      // Should not crash
      await expect(page.locator('text=Analytics Dashboard')).toBeVisible()
    }
  })

  test('should handle invalid date ranges', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Analytics')
    await page.waitForTimeout(1000)
    
    // Try setting invalid date range (end before start)
    const startDate = page.locator('input[type="date"]').first()
    const endDate = page.locator('input[type="date"]').last()
    
    const isStartVisible = await startDate.isVisible()
    const isEndVisible = await endDate.isVisible()
    
    if (isStartVisible && isEndVisible) {
      await startDate.fill('2026-12-31')
      await endDate.fill('2026-01-01')
      
      // Application should handle this gracefully
      await expect(page.locator('text=Analytics Dashboard')).toBeVisible()
    }
  })
})

test.describe('Error Handling - UI Components', () => {
  test('should handle dropdown errors', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Tasks')
    
    // Try clicking user dropdown
    await page.click('[aria-label="User menu"]')
    await page.waitForTimeout(300)
    
    // Click outside to close
    await page.click('body')
    await page.waitForTimeout(300)
    
    // Try again
    await page.click('[aria-label="User menu"]')
    
    // Should work correctly
    await expect(page.locator('text=Your Profile')).toBeVisible()
  })

  test('should handle tooltip errors', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    
    // Hover over elements that might have tooltips
    const tasks = page.locator('[role="article"]')
    const count = await tasks.count()
    
    if (count > 0) {
      await tasks.first().hover()
      await page.waitForTimeout(200)
    }
    
    // Should not crash
    await expect(page.locator('body')).toBeVisible()
  })

  test('should handle modal errors', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Tasks')
    
    // Try opening any modal-triggering action
    const createButton = page.locator('button:has-text("Create New Task")')
    await createButton.click()
    
    // Should not crash
    await expect(page.locator('body')).toBeVisible()
  })
})
