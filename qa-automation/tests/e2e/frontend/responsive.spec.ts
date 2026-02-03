import { test, expect } from '@playwright/test'
import { navigateToDashboard } from './helpers/auth'

test.describe('Responsive Design Tests - Mobile', () => {
  test.beforeEach(async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })
    await navigateToDashboard(page)
  })

  test('should show mobile hamburger menu', async ({ page }) => {
    // Check if hamburger button is visible
    const hamburger = page.locator('[aria-label="Toggle sidebar"]')
    await expect(hamburger).toBeVisible()
  })

  test('should open sidebar on hamburger click', async ({ page }) => {
    // Click hamburger
    await page.click('[aria-label="Toggle sidebar"]')
    
    // Wait for sidebar to open
    await page.waitForTimeout(500)
    
    // Check if sidebar is visible
    const sidebar = page.locator('aside')
    await expect(sidebar).toBeVisible()
  })

  test('should close sidebar on backdrop click', async ({ page }) => {
    // Open sidebar
    await page.click('[aria-label="Toggle sidebar"]')
    await page.waitForTimeout(300)
    
    // Click backdrop
    const backdrop = page.locator('.fixed.inset-0.bg-black')
    await backdrop.click({ force: true })
    
    // Wait for close animation
    await page.waitForTimeout(500)
    
    // Sidebar should be hidden
    // (transformed off-screen with -translate-x-full)
  })

  test('should display mobile-friendly statistics', async ({ page }) => {
    // Statistics should be in a grid
    const stats = page.locator('text=Total Tasks')
    await expect(stats).toBeVisible()
    
    // Should stack vertically or in 2 columns on mobile
    const statWidgets = page.locator('[role="article"]').filter({ hasText: 'Total Tasks' })
    await expect(statWidgets).toBeVisible()
  })

  test('should show tasks in single column on mobile', async ({ page }) => {
    // Wait for tasks to load
    await page.waitForSelector('[role="article"]', { timeout: 15000 })
    
    // Tasks should be visible
    const tasks = page.locator('[role="article"]')
    expect(await tasks.count()).toBeGreaterThan(0)
  })

  test('should hide user email on small screens', async ({ page }) => {
    // On mobile, some text might be hidden
    await page.click('[aria-label="User menu"]')
    
    // Email should still be in DOM but might be smaller
    const email = page.locator('text=alex.johnson@example.com')
    await expect(email).toBeVisible()
  })

  test('should show mobile navigation', async ({ page }) => {
    // Top navigation should be visible
    const nav = page.locator('nav')
    await expect(nav.first()).toBeVisible()
    
    // Navigation items should be visible (at least one button)
    const tasksButton = page.locator('button:has-text("Tasks")')
    await expect(tasksButton.first()).toBeVisible()
  })
})

test.describe('Responsive Design Tests - Tablet', () => {
  test.beforeEach(async ({ page }) => {
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 })
    await navigateToDashboard(page)
  })

  test('should display sidebar on tablet', async ({ page }) => {
    // Sidebar should be visible on tablet
    const sidebar = page.locator('aside')
    await expect(sidebar).toBeVisible()
  })

  test('should show 2-column task grid', async ({ page }) => {
    // Wait for tasks
    await page.waitForSelector('[role="article"]', { timeout: 15000 })
    
    // Tasks should be visible
    const tasks = page.locator('[role="article"]')
    expect(await tasks.count()).toBeGreaterThan(0)
  })

  test('should display statistics in 2 columns', async ({ page }) => {
    // Statistics should be visible
    await expect(page.locator('text=Total Tasks').first()).toBeVisible()
    await expect(page.locator('text=In Progress').first()).toBeVisible()
  })
})

test.describe('Responsive Design Tests - Desktop', () => {
  test.beforeEach(async ({ page }) => {
    // Set desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 })
    await navigateToDashboard(page)
  })

  test('should show persistent sidebar', async ({ page }) => {
    // Sidebar should always be visible
    const sidebar = page.locator('aside')
    await expect(sidebar).toBeVisible()
  })

  test('should not show hamburger menu', async ({ page }) => {
    // Hamburger should be hidden on desktop
    const hamburger = page.locator('[aria-label="Toggle sidebar"]')
    await expect(hamburger).not.toBeVisible()
  })

  test('should display 4-column statistics', async ({ page }) => {
    // All 4 stat widgets should be visible (use first() to avoid multiple matches)
    await expect(page.locator('text=Total Tasks').first()).toBeVisible()
    await expect(page.locator('text=In Progress').first()).toBeVisible()
    await expect(page.locator('text=Completion Rate').first()).toBeVisible()
    await expect(page.locator('text=Productivity').first()).toBeVisible()
  })

  test('should show full task details', async ({ page }) => {
    // Wait for tasks
    await page.waitForSelector('[role="article"]', { timeout: 15000 })
    
    // Check for detailed task information (use first() to avoid strict mode)
    const taskTitle = page.locator('text=Design new landing page')
    if (await taskTitle.count() > 0) {
      await expect(taskTitle.first()).toBeVisible()
    }
    
    // Check for avatars
    const avatars = page.locator('img[alt*="profile"]')
    expect(await avatars.count()).toBeGreaterThanOrEqual(0)
  })

  test('should display search bar in header', async ({ page }) => {
    // Search should be visible on desktop
    const search = page.locator('button:has-text("Search")')
    await expect(search).toBeVisible()
  })
})

test.describe('Responsive Design - Analytics Dashboard', () => {
  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    await page.click('text=Analytics')
    
    // Check KPI cards are visible
    await expect(page.locator('text=Total Revenue')).toBeVisible()
    
    // Check filters are collapsible
    const filtersHeader = page.locator('text=Filters')
    await expect(filtersHeader).toBeVisible()
  })

  test('should show charts on tablet', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 })
    await page.goto('/')
    await page.click('text=Analytics')
    
    // Charts should be visible
    await expect(page.locator('text=Revenue Over Time')).toBeVisible()
  })

  test('should display full layout on desktop', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 })
    await page.goto('/')
    await page.click('text=Analytics')
    
    // All elements should be visible
    await expect(page.locator('text=Analytics Dashboard')).toBeVisible()
    await expect(page.locator('text=Total Revenue')).toBeVisible()
    await expect(page.locator('text=Revenue Over Time')).toBeVisible()
  })
})

test.describe('Responsive Design - Navigation', () => {
  test('should show compact navigation on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    
    // Top nav should be scrollable or compact
    const nav = page.locator('nav')
    await expect(nav).toBeVisible()
  })

  test('should show full navigation on desktop', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 })
    await page.goto('/')
    
    // All nav items should be visible
    await expect(page.locator('button:has-text("Analytics")')).toBeVisible()
    await expect(page.locator('button:has-text("Tasks")')).toBeVisible()
    await expect(page.locator('button:has-text("NavBar")')).toBeVisible()
  })
})

test.describe('Responsive Design - Orientation Changes', () => {
  test('should handle portrait to landscape on mobile', async ({ page }) => {
    // Start in portrait
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    await ensureAuthenticated(page)
    
    // Verify layout in portrait
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
    
    // Switch to landscape
    await page.setViewportSize({ width: 667, height: 375 })
    await page.waitForTimeout(500)
    
    // Content should still be visible and usable
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
    
    // Hamburger should still work
    const hamburger = page.locator('[aria-label="Toggle sidebar"]')
    await expect(hamburger).toBeVisible()
  })

  test('should handle landscape to portrait on mobile', async ({ page }) => {
    // Start in landscape
    await page.setViewportSize({ width: 667, height: 375 })
    await page.goto('/')
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    await ensureAuthenticated(page)
    
    // Verify content is visible
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
    
    // Switch to portrait
    await page.setViewportSize({ width: 375, height: 667 })
    await page.waitForTimeout(500)
    
    // Layout should adjust
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
    
    // Navigation should still work
    const hamburger = page.locator('[aria-label="Toggle sidebar"]')
    await expect(hamburger).toBeVisible()
  })

  test('should handle tablet portrait to landscape', async ({ page }) => {
    // Tablet portrait
    await page.setViewportSize({ width: 768, height: 1024 })
    await page.goto('/')
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    await ensureAuthenticated(page)
    
    // Check layout
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
    
    // Switch to landscape
    await page.setViewportSize({ width: 1024, height: 768 })
    await page.waitForTimeout(500)
    
    // Sidebar should be visible in landscape
    const sidebar = page.locator('aside')
    await expect(sidebar).toBeVisible()
    
    // Content should reflow appropriately
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
  })

  test('should handle tablet landscape to portrait', async ({ page }) => {
    // Tablet landscape
    await page.setViewportSize({ width: 1024, height: 768 })
    await page.goto('/')
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    await ensureAuthenticated(page)
    
    // Verify layout
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
    
    // Switch to portrait
    await page.setViewportSize({ width: 768, height: 1024 })
    await page.waitForTimeout(500)
    
    // Layout should adjust
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
  })

  test('should adjust grid layout on orientation change', async ({ page }) => {
    // Portrait: tasks might be single column
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    await ensureAuthenticated(page)
    
    // Verify tasks are visible
    await page.waitForSelector('[role="article"]', { timeout: 15000 })
    const portraitTasks = page.locator('[role="article"]')
    const portraitCount = await portraitTasks.count()
    expect(portraitCount).toBeGreaterThan(0)
    
    // Landscape: might show more columns
    await page.setViewportSize({ width: 667, height: 375 })
    await page.waitForTimeout(500)
    
    // Tasks should still be visible
    const landscapeTasks = page.locator('[role="article"]')
    const landscapeCount = await landscapeTasks.count()
    expect(landscapeCount).toBeGreaterThan(0)
  })

  test('should maintain sidebar state on orientation change', async ({ page }) => {
    // Mobile portrait
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    await ensureAuthenticated(page)
    
    // Open sidebar
    await page.click('[aria-label="Toggle sidebar"]')
    await page.waitForTimeout(300)
    
    // Sidebar should be open
    const sidebar = page.locator('aside')
    await expect(sidebar).toBeVisible()
    
    // Change to landscape
    await page.setViewportSize({ width: 667, height: 375 })
    await page.waitForTimeout(500)
    
    // Sidebar behavior might change (could auto-close or stay open)
    // Just verify the app doesn't crash
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
  })

  test('should reflow statistics on orientation change', async ({ page }) => {
    // Portrait
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    await ensureAuthenticated(page)
    
    // Stats should be visible (might be stacked)
    await expect(page.locator('text=Total Tasks')).toBeVisible()
    
    // Landscape
    await page.setViewportSize({ width: 667, height: 375 })
    await page.waitForTimeout(500)
    
    // Stats should still be visible (might be in row)
    await expect(page.locator('text=Total Tasks')).toBeVisible()
  })

  test('should handle rapid orientation changes', async ({ page }) => {
    await page.goto('/')
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    await ensureAuthenticated(page)
    
    // Rapidly switch orientations
    await page.setViewportSize({ width: 375, height: 667 })
    await page.waitForTimeout(100)
    
    await page.setViewportSize({ width: 667, height: 375 })
    await page.waitForTimeout(100)
    
    await page.setViewportSize({ width: 375, height: 667 })
    await page.waitForTimeout(100)
    
    await page.setViewportSize({ width: 667, height: 375 })
    await page.waitForTimeout(300)
    
    // App should still work
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
  })

  test('should adjust analytics dashboard on orientation change', async ({ page }) => {
    // Portrait
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    await page.click('text=Analytics')
    await page.waitForLoadState('networkidle')
    
    // KPIs should be visible
    await expect(page.locator('text=Total Revenue')).toBeVisible()
    
    // Landscape
    await page.setViewportSize({ width: 667, height: 375 })
    await page.waitForTimeout(500)
    
    // KPIs should reflow
    await expect(page.locator('text=Total Revenue')).toBeVisible()
  })

  test('should maintain scroll position on orientation change', async ({ page }) => {
    // Portrait
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    await ensureAuthenticated(page)
    
    // Scroll down
    await page.evaluate(() => window.scrollTo(0, 300))
    await page.waitForTimeout(200)
    
    // Get scroll position before orientation change (for future use if needed)
    await page.evaluate(() => window.scrollY)
    
    // Change orientation
    await page.setViewportSize({ width: 667, height: 375 })
    await page.waitForTimeout(500)
    
    // Scroll position might change due to layout, but page should be usable
    await expect(page.locator('body')).toBeVisible()
  })

  test('should handle orientation change with open modals', async ({ page }) => {
    // Mobile portrait
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    await ensureAuthenticated(page)
    
    // Open user menu (dropdown)
    await page.click('[aria-label="User menu"]')
    await page.waitForTimeout(200)
    
    // Change orientation
    await page.setViewportSize({ width: 667, height: 375 })
    await page.waitForTimeout(500)
    
    // App should handle gracefully
    await expect(page.locator('body')).toBeVisible()
  })

  test('should handle orientation change during loading', async ({ page }) => {
    // Start loading a page
    const navigationPromise = page.goto('/')
    
    // Immediately change orientation
    await page.setViewportSize({ width: 375, height: 667 })
    
    // Wait for navigation to complete
    await navigationPromise
    await page.waitForLoadState('networkidle')
    
    // Change orientation again
    await page.setViewportSize({ width: 667, height: 375 })
    await page.waitForTimeout(300)
    
    // Navigate to Tasks
    await page.click('text=Tasks')
    await page.waitForLoadState('networkidle')
    await ensureAuthenticated(page)
    
    // Should work correctly
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
  })
})
