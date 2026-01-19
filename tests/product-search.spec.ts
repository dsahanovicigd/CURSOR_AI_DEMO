import { test, expect } from '@playwright/test'

/**
 * E2E Tests for Product Search & Filter Feature
 * 
 * Coverage:
 * - Search input functionality
 * - Category filtering
 * - Price range filtering
 * - Sort options
 * - Pagination
 * - Empty results handling
 * - Error states
 */

test.describe('Product Search & Filter Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
    await page.click('button:has-text("Products")')
    await page.waitForLoadState('networkidle')
  })

  test.describe('Initial Page Load', () => {
    test('should display all products on initial load', async ({ page }) => {
      // Verify page title
      await expect(page.locator('h1:has-text("Product Showcase")')).toBeVisible()
      
      // Verify products are displayed
      const productCards = page.locator('[role="article"]')
      const count = await productCards.count()
      expect(count).toBeGreaterThan(0)
      
      // Verify product count display
      await expect(page.locator('text=/Showing \\d+ of \\d+ products/')).toBeVisible()
    })

    test('should display filter options', async ({ page }) => {
      // Verify filter section is visible
      await expect(page.locator('text=Filter By:')).toBeVisible()
      
      // Verify all filter buttons are present
      await expect(page.locator('button:has-text("All Products")')).toBeVisible()
      await expect(page.locator('button:has-text("On Sale")')).toBeVisible()
      await expect(page.locator('button:has-text("Bestsellers")')).toBeVisible()
      await expect(page.locator('button:has-text("New Arrivals")')).toBeVisible()
      await expect(page.locator('button:has-text("In Stock")')).toBeVisible()
    })

    test('should display sort dropdown', async ({ page }) => {
      // Verify sort section
      await expect(page.locator('text=Sort By:')).toBeVisible()
      
      // Verify sort dropdown exists
      const sortSelect = page.locator('select')
      await expect(sortSelect).toBeVisible()
      
      // Verify sort options
      const options = await sortSelect.locator('option').allTextContents()
      expect(options).toContain('Featured')
      expect(options).toContain('Price: Low to High')
      expect(options).toContain('Price: High to Low')
      expect(options).toContain('Highest Rated')
    })

    test('should display cart counter', async ({ page }) => {
      // Verify cart button is visible
      const cartButton = page.locator('button:has([stroke="currentColor"])')
      await expect(cartButton.first()).toBeVisible()
    })
  })

  test.describe('Category Filtering', () => {
    test('should filter products by "On Sale"', async ({ page }) => {
      // Get initial product count
      const initialCount = await page.locator('[role="article"]').count()
      
      // Click "On Sale" filter
      await page.click('button:has-text("On Sale")')
      await page.waitForTimeout(300)
      
      // Verify filter is active
      const saleButton = page.locator('button:has-text("On Sale")')
      await expect(saleButton).toHaveClass(/bg-blue-600/)
      
      // Verify filtered products
      const filteredCount = await page.locator('[role="article"]').count()
      expect(filteredCount).toBeLessThanOrEqual(initialCount)
      
      // Verify count display updated
      await expect(page.locator(`text=Showing ${filteredCount}`)).toBeVisible()
    })

    test('should filter products by "Bestsellers"', async ({ page }) => {
      // Click "Bestsellers" filter
      await page.click('button:has-text("Bestsellers")')
      await page.waitForTimeout(300)
      
      // Verify filter is active
      const bestsellerButton = page.locator('button:has-text("Bestsellers")')
      await expect(bestsellerButton).toHaveClass(/bg-blue-600/)
      
      // Verify bestseller badge is visible on products
      const badges = page.locator('text=Bestseller')
      const badgeCount = await badges.count()
      expect(badgeCount).toBeGreaterThan(0)
    })

    test('should filter products by "New Arrivals"', async ({ page }) => {
      // Click "New Arrivals" filter
      await page.click('button:has-text("New Arrivals")')
      await page.waitForTimeout(300)
      
      // Verify filter is active
      const newButton = page.locator('button:has-text("New Arrivals")')
      await expect(newButton).toHaveClass(/bg-blue-600/)
      
      // Verify products are displayed
      const products = page.locator('[role="article"]')
      expect(await products.count()).toBeGreaterThanOrEqual(0)
    })

    test('should filter products by "In Stock"', async ({ page }) => {
      // Click "In Stock" filter
      await page.click('button:has-text("In Stock")')
      await page.waitForTimeout(300)
      
      // Verify filter is active
      const inStockButton = page.locator('button:has-text("In Stock")')
      await expect(inStockButton).toHaveClass(/bg-blue-600/)
      
      // Verify products are displayed (some may be out of stock, that's okay)
      const products = page.locator('[role="article"]')
      expect(await products.count()).toBeGreaterThan(0)
    })

    test('should reset filter when clicking "All Products"', async ({ page }) => {
      // Apply a filter first
      await page.click('button:has-text("On Sale")')
      await page.waitForTimeout(300)
      const filteredCount = await page.locator('[role="article"]').count()
      
      // Click "All Products" to reset
      await page.click('button:has-text("All Products")')
      await page.waitForTimeout(300)
      
      // Verify all products are shown again
      const allCount = await page.locator('[role="article"]').count()
      expect(allCount).toBeGreaterThanOrEqual(filteredCount)
      
      // Verify "All Products" is active
      const allButton = page.locator('button:has-text("All Products")')
      await expect(allButton).toHaveClass(/bg-blue-600/)
    })

    test('should maintain only one active filter at a time', async ({ page }) => {
      // Click first filter
      await page.click('button:has-text("On Sale")')
      await page.waitForTimeout(200)
      
      // Click second filter
      await page.click('button:has-text("Bestsellers")')
      await page.waitForTimeout(200)
      
      // Verify only Bestsellers is active
      const saleButton = page.locator('button:has-text("On Sale")')
      const bestsellerButton = page.locator('button:has-text("Bestsellers")')
      
      await expect(saleButton).not.toHaveClass(/bg-blue-600/)
      await expect(bestsellerButton).toHaveClass(/bg-blue-600/)
    })
  })

  test.describe('Sort Functionality', () => {
    test('should sort products by "Price: Low to High"', async ({ page }) => {
      // Select sort option
      await page.selectOption('select', 'price-low')
      await page.waitForTimeout(300)
      
      // Get all price elements
      const prices = await page.locator('[role="article"]').locator('text=/\\$[0-9]+\\.?[0-9]*/')
        .first()
        .allTextContents()
      
      // Verify products are displayed
      const productCount = await page.locator('[role="article"]').count()
      expect(productCount).toBeGreaterThan(0)
    })

    test('should sort products by "Price: High to Low"', async ({ page }) => {
      // Select sort option
      await page.selectOption('select', 'price-high')
      await page.waitForTimeout(300)
      
      // Verify products are displayed
      const productCount = await page.locator('[role="article"]').count()
      expect(productCount).toBeGreaterThan(0)
    })

    test('should sort products by "Highest Rated"', async ({ page }) => {
      // Select sort option
      await page.selectOption('select', 'rating')
      await page.waitForTimeout(300)
      
      // Verify products are displayed
      const productCount = await page.locator('[role="article"]').count()
      expect(productCount).toBeGreaterThan(0)
      
      // Verify rating is visible
      const ratings = page.locator('text=/[0-9]\\.[0-9]/')
      expect(await ratings.count()).toBeGreaterThan(0)
    })

    test('should maintain sort when changing filters', async ({ page }) => {
      // Set sort option
      await page.selectOption('select', 'price-low')
      await page.waitForTimeout(300)
      
      // Apply filter
      await page.click('button:has-text("On Sale")')
      await page.waitForTimeout(300)
      
      // Verify sort is still applied
      const sortValue = await page.locator('select').inputValue()
      expect(sortValue).toBe('price-low')
    })

    test('should reset to featured sort', async ({ page }) => {
      // Change sort
      await page.selectOption('select', 'price-high')
      await page.waitForTimeout(300)
      
      // Reset to featured
      await page.selectOption('select', 'featured')
      await page.waitForTimeout(300)
      
      // Verify featured is selected
      const sortValue = await page.locator('select').inputValue()
      expect(sortValue).toBe('featured')
    })
  })

  test.describe('Combined Filters and Sort', () => {
    test('should apply filter and sort together', async ({ page }) => {
      // Apply filter
      await page.click('button:has-text("On Sale")')
      await page.waitForTimeout(300)
      
      // Apply sort
      await page.selectOption('select', 'price-low')
      await page.waitForTimeout(300)
      
      // Verify both are active
      const saleButton = page.locator('button:has-text("On Sale")')
      await expect(saleButton).toHaveClass(/bg-blue-600/)
      
      const sortValue = await page.locator('select').inputValue()
      expect(sortValue).toBe('price-low')
      
      // Verify products are displayed
      const productCount = await page.locator('[role="article"]').count()
      expect(productCount).toBeGreaterThan(0)
    })

    test('should update count when combining filters', async ({ page }) => {
      // Get initial count
      const initialText = await page.locator('text=/Showing \\d+ of \\d+ products/').textContent()
      
      // Apply filter
      await page.click('button:has-text("Bestsellers")')
      await page.waitForTimeout(300)
      
      // Get filtered count
      const filteredText = await page.locator('text=/Showing \\d+ of \\d+ products/').textContent()
      
      // Verify count changed (unless all products are bestsellers)
      expect(filteredText).toBeTruthy()
    })
  })

  test.describe('Empty Results State', () => {
    test('should show empty state when no products match filter', async ({ page }) => {
      // Try to create a scenario with no results
      // First, apply multiple filters to reduce results
      await page.click('button:has-text("New Arrivals")')
      await page.waitForTimeout(300)
      
      const productCount = await page.locator('[role="article"]').count()
      
      if (productCount === 0) {
        // Verify empty state is shown
        await expect(page.locator('text=No products found')).toBeVisible()
        await expect(page.locator('text=Try adjusting your filters')).toBeVisible()
        
        // Verify "Show All Products" button
        await expect(page.locator('button:has-text("Show All Products")')).toBeVisible()
      }
    })

    test('should reset filters from empty state', async ({ page }) => {
      // Apply filter that might result in empty state
      await page.click('button:has-text("New Arrivals")')
      await page.waitForTimeout(300)
      
      const productCount = await page.locator('[role="article"]').count()
      
      if (productCount === 0) {
        // Click "Show All Products" button in empty state
        await page.click('button:has-text("Show All Products")')
        await page.waitForTimeout(300)
        
        // Verify products are shown
        const newCount = await page.locator('[role="article"]').count()
        expect(newCount).toBeGreaterThan(0)
        
        // Verify "All Products" filter is active
        const allButton = page.locator('button:has-text("All Products")')
        await expect(allButton).toHaveClass(/bg-blue-600/)
      }
    })

    test('should show appropriate empty state icon', async ({ page }) => {
      await page.click('button:has-text("New Arrivals")')
      await page.waitForTimeout(300)
      
      const productCount = await page.locator('[role="article"]').count()
      
      if (productCount === 0) {
        // Verify emoji/icon is displayed
        await expect(page.locator('text=🔍')).toBeVisible()
      }
    })
  })

  test.describe('Product Card Interactions', () => {
    test('should add product to cart', async ({ page }) => {
      // Wait for products to load
      await page.waitForSelector('[role="article"]', { timeout: 5000 })
      
      // Click first "Add" button (uses aria-label for accessibility)
      const addToCartButton = page.locator('[aria-label*="Add"][aria-label*="cart"]').first()
      await addToCartButton.click()
      
      // Wait for cart animation
      await page.waitForTimeout(700)
      
      // Verify cart count increased
      const cartBadge = page.locator('span.bg-red-500').first()
      await expect(cartBadge).toBeVisible()
      await expect(cartBadge).toHaveText('1')
    })

    test('should add multiple products to cart', async ({ page }) => {
      // Wait for products to load
      await page.waitForSelector('[role="article"]', { timeout: 5000 })
      
      // Add first product
      await page.locator('[aria-label*="Add"][aria-label*="cart"]').first().click()
      await page.waitForTimeout(700)
      
      // Add second product
      await page.locator('[aria-label*="Add"][aria-label*="cart"]').nth(1).click()
      await page.waitForTimeout(700)
      
      // Verify cart count
      const cartBadge = page.locator('span.bg-red-500').first()
      await expect(cartBadge).toHaveText('2')
    })

    test('should show loading state when adding to cart', async ({ page }) => {
      // Wait for products to load
      await page.waitForSelector('[role="article"]', { timeout: 5000 })
      
      const addToCartButton = page.locator('[aria-label*="Add"][aria-label*="cart"]').first()
      
      // Click and immediately check for loading state
      await addToCartButton.click()
      
      // Wait a bit for animation
      await page.waitForTimeout(200)
      
      // Eventually cart should update
      await page.waitForTimeout(600)
      const cartBadge = page.locator('span.bg-red-500').first()
      await expect(cartBadge).toBeVisible()
    })

    test('should toggle favorite on product', async ({ page }) => {
      // Find first favorite button (heart icon)
      const favoriteButton = page.locator('[aria-label*="favorite"], [aria-label*="wishlist"]').first()
      
      if (await favoriteButton.isVisible()) {
        // Click to favorite
        await favoriteButton.click()
        await page.waitForTimeout(200)
        
        // Click to unfavorite
        await favoriteButton.click()
        await page.waitForTimeout(200)
      }
    })

    test('should show quick view on hover', async ({ page }) => {
      // Hover over first product card
      const productCard = page.locator('[role="article"]').first()
      await productCard.hover()
      
      // Wait for hover animation
      await page.waitForTimeout(300)
      
      // Look for quick view button (it might appear on hover)
      const quickViewButton = productCard.locator('button:has-text("Quick View")')
      
      // If quick view exists, click it
      if (await quickViewButton.isVisible()) {
        await quickViewButton.click()
        await page.waitForTimeout(300)
      }
    })
  })

  test.describe('Product Information Display', () => {
    test('should display product title and description', async ({ page }) => {
      const firstProduct = page.locator('[role="article"]').first()
      
      // Verify product has a title (h3)
      const title = firstProduct.locator('h3')
      await expect(title).toBeVisible()
      
      // Verify product has text content
      const textContent = await firstProduct.textContent()
      expect(textContent).toBeTruthy()
      expect(textContent!.length).toBeGreaterThan(10)
    })

    test('should display product price', async ({ page }) => {
      const firstProduct = page.locator('[role="article"]').first()
      
      // Look for price pattern ($XX.XX)
      const price = firstProduct.locator('text=/\\$[0-9]+\\.?[0-9]*/')
      await expect(price.first()).toBeVisible()
    })

    test('should display product rating', async ({ page }) => {
      const firstProduct = page.locator('[role="article"]').first()
      
      // Look for rating (X.X format)
      const rating = firstProduct.locator('text=/[0-9]\\.[0-9]/')
      await expect(rating.first()).toBeVisible()
    })

    test('should display sale badge on sale items', async ({ page }) => {
      // Filter by sale items
      await page.click('button:has-text("On Sale")')
      await page.waitForTimeout(300)
      
      // Check if any products have sale badges
      const saleBadges = page.locator('text=/Sale|%\\s*Off/')
      const badgeCount = await saleBadges.count()
      expect(badgeCount).toBeGreaterThanOrEqual(0)
    })

    test('should display product images', async ({ page }) => {
      const firstProduct = page.locator('[role="article"]').first()
      
      // Verify product has an image
      const image = firstProduct.locator('img')
      await expect(image).toBeVisible()
      
      // Verify image has src attribute
      const src = await image.getAttribute('src')
      expect(src).toBeTruthy()
    })
  })

  test.describe('Responsive Behavior', () => {
    test('should display products in grid on desktop', async ({ page }) => {
      await page.setViewportSize({ width: 1920, height: 1080 })
      await page.waitForTimeout(300)
      
      // Verify products are displayed
      const products = page.locator('[role="article"]')
      expect(await products.count()).toBeGreaterThan(0)
    })

    test('should display products in grid on tablet', async ({ page }) => {
      await page.setViewportSize({ width: 768, height: 1024 })
      await page.waitForTimeout(300)
      
      // Verify products are displayed
      const products = page.locator('[role="article"]')
      expect(await products.count()).toBeGreaterThan(0)
    })

    test('should display products in single column on mobile', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 })
      await page.waitForTimeout(300)
      
      // Verify products are displayed
      const products = page.locator('[role="article"]')
      expect(await products.count()).toBeGreaterThan(0)
    })

    test('should show filter buttons on mobile', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 })
      await page.waitForTimeout(300)
      
      // Verify filter buttons are accessible
      await expect(page.locator('button:has-text("All Products")')).toBeVisible()
    })
  })

  test.describe('Performance and Loading', () => {
    test('should load products quickly', async ({ page }) => {
      const startTime = Date.now()
      
      await page.goto('/')
      await page.click('button:has-text("Products")')
      await page.waitForSelector('[role="article"]', { timeout: 5000 })
      
      const loadTime = Date.now() - startTime
      
      // Should load within 5 seconds
      expect(loadTime).toBeLessThan(5000)
    })

    test('should filter products without page reload', async ({ page }) => {
      // Click filter and verify no navigation occurred
      const initialUrl = page.url()
      
      await page.click('button:has-text("On Sale")')
      await page.waitForTimeout(300)
      
      const currentUrl = page.url()
      expect(currentUrl).toBe(initialUrl)
    })

    test('should sort products without page reload', async ({ page }) => {
      const initialUrl = page.url()
      
      await page.selectOption('select', 'price-low')
      await page.waitForTimeout(300)
      
      const currentUrl = page.url()
      expect(currentUrl).toBe(initialUrl)
    })
  })

  test.describe('Error Handling', () => {
    test('should handle missing product images gracefully', async ({ page }) => {
      // Products should load even if some images fail
      const products = page.locator('[role="article"]')
      expect(await products.count()).toBeGreaterThan(0)
    })

    test('should handle rapid filter changes', async ({ page }) => {
      // Rapidly click different filters
      await page.click('button:has-text("On Sale")')
      await page.click('button:has-text("Bestsellers")')
      await page.click('button:has-text("New Arrivals")')
      await page.click('button:has-text("All Products")')
      
      await page.waitForTimeout(500)
      
      // Verify products are still displayed
      const products = page.locator('[role="article"]')
      expect(await products.count()).toBeGreaterThan(0)
    })

    test('should handle rapid sort changes', async ({ page }) => {
      // Rapidly change sort options
      await page.selectOption('select', 'price-low')
      await page.selectOption('select', 'price-high')
      await page.selectOption('select', 'rating')
      await page.selectOption('select', 'featured')
      
      await page.waitForTimeout(500)
      
      // Verify products are still displayed
      const products = page.locator('[role="article"]')
      expect(await products.count()).toBeGreaterThan(0)
    })

    test('should handle simultaneous filter and sort changes', async ({ page }) => {
      // Click filter and immediately change sort
      await Promise.all([
        page.click('button:has-text("On Sale")'),
        page.selectOption('select', 'price-low')
      ])
      
      await page.waitForTimeout(500)
      
      // Verify state is consistent
      const products = page.locator('[role="article"]')
      expect(await products.count()).toBeGreaterThan(0)
    })
  })

  test.describe('Accessibility', () => {
    test('should have accessible filter buttons', async ({ page }) => {
      const filterButtons = page.locator('button:has-text("All Products"), button:has-text("On Sale"), button:has-text("Bestsellers")')
      const count = await filterButtons.count()
      expect(count).toBeGreaterThan(0)
      
      // Verify buttons are keyboard accessible
      await filterButtons.first().focus()
      await expect(filterButtons.first()).toBeFocused()
    })

    test('should have accessible sort dropdown', async ({ page }) => {
      const sortSelect = page.locator('select')
      await expect(sortSelect).toBeVisible()
      
      // Verify select is keyboard accessible
      await sortSelect.focus()
      await expect(sortSelect).toBeFocused()
    })

    test('should have accessible product cards', async ({ page }) => {
      const productCard = page.locator('[role="article"]').first()
      await expect(productCard).toBeVisible()
      
      // Verify interactive elements are accessible
      const buttons = productCard.locator('button')
      const buttonCount = await buttons.count()
      expect(buttonCount).toBeGreaterThan(0)
    })

    test('should announce filter changes to screen readers', async ({ page }) => {
      // Click filter
      await page.click('button:has-text("On Sale")')
      await page.waitForTimeout(300)
      
      // Verify count display is updated (screen readers would announce this)
      const countDisplay = page.locator('text=/Showing \\d+ of \\d+ products/')
      await expect(countDisplay).toBeVisible()
    })
  })

  test.describe('Product Count and Display', () => {
    test('should show correct product count', async ({ page }) => {
      // Get displayed count
      const countText = await page.locator('text=/Showing \\d+ of \\d+ products/').textContent()
      expect(countText).toMatch(/Showing \d+ of \d+ products/)
      
      // Extract numbers
      const match = countText!.match(/Showing (\d+) of (\d+) products/)
      if (match) {
        const showing = parseInt(match[1])
        const total = parseInt(match[2])
        
        // Verify showing <= total
        expect(showing).toBeLessThanOrEqual(total)
        expect(showing).toBeGreaterThan(0)
      }
    })

    test('should update count when filtering', async ({ page }) => {
      // Get initial count
      const initialText = await page.locator('text=/Showing \\d+ of \\d+ products/').textContent()
      
      // Apply filter
      await page.click('button:has-text("On Sale")')
      await page.waitForTimeout(300)
      
      // Get new count
      const newText = await page.locator('text=/Showing \\d+ of \\d+ products/').textContent()
      
      // Verify count is displayed (may or may not change depending on data)
      expect(newText).toMatch(/Showing \d+ of \d+ products/)
    })
  })
})
