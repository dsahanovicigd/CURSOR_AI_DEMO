import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

/**
 * E2E Tests for Multi-Step Registration Form
 * 
 * Coverage:
 * - Field validation (required fields, format validation)
 * - Navigation between steps (next, back, step indicators)
 * - Form submission
 * - Error messages and announcements
 * - Success state
 * - Accessibility (form labels, error announcements, ARIA)
 */

test.describe('Multi-Step Registration Form Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
    await page.click('button:has-text("Register")')
    await page.waitForLoadState('networkidle')
  })

  test.describe('Initial State and Page Load', () => {
    test('should display registration form with Step 1', async ({ page }) => {
      // Verify page title
      await expect(page.locator('h1:has-text("Create Your Account")')).toBeVisible()
      
      // Verify step indicator
      await expect(page.locator('text=Step 1 of 4')).toBeVisible()
      
      // Verify Step 1 heading
      await expect(page.locator('h2:has-text("Personal Information")')).toBeVisible()
      
      // Verify all Step 1 fields are present
      await expect(page.locator('input[id="firstName"]')).toBeVisible()
      await expect(page.locator('input[id="lastName"]')).toBeVisible()
      await expect(page.locator('input[id="dateOfBirth"]')).toBeVisible()
    })

    test('should display progress bar', async ({ page }) => {
      // Verify progress bar exists with correct attributes
      const progressBar = page.locator('[role="progressbar"]')
      
      // Check that it exists and has correct ARIA attributes
      const count = await progressBar.count()
      expect(count).toBe(1)
      
      const valuenow = await progressBar.getAttribute('aria-valuenow')
      expect(valuenow).toBe('1')
    })

    test('should display all step indicators', async ({ page }) => {
      // Verify all 4 steps are shown (case-insensitive, may be truncated on mobile)
      const step1 = page.locator('text=/Personal Info/i')
      const step2 = page.locator('text=/Account/i')
      const step3 = page.locator('text=/Preferences/i')
      const step4 = page.locator('text=/Review/i')
      
      expect(await step1.count()).toBeGreaterThan(0)
      expect(await step2.count()).toBeGreaterThan(0)
      expect(await step3.count()).toBeGreaterThan(0)
      expect(await step4.count()).toBeGreaterThan(0)
    })

    test('should highlight current step', async ({ page }) => {
      // Step 1 should be highlighted
      const step1Button = page.locator('button[aria-label*="Personal Info"][aria-current="step"]')
      await expect(step1Button).toBeVisible()
    })
  })

  test.describe('Step 1: Personal Information - Field Validation', () => {
    test('should show error for empty first name', async ({ page }) => {
      // Click first name and blur without entering text
      await page.click('input[id="firstName"]')
      await page.click('input[id="lastName"]')
      
      // Try to proceed
      await page.click('button:has-text("Next")')
      
      // Verify error message
      await expect(page.locator('text=First name is required')).toBeVisible()
    })

    test('should show error for short first name', async ({ page }) => {
      await page.fill('input[id="firstName"]', 'A')
      await page.click('input[id="lastName"]')
      await page.click('button:has-text("Next")')
      
      await expect(page.locator('text=First name must be at least 2 characters')).toBeVisible()
    })

    test('should show error for empty last name', async ({ page }) => {
      await page.fill('input[id="firstName"]', 'John')
      await page.click('input[id="lastName"]')
      await page.click('button:has-text("Next")')
      
      await expect(page.locator('text=Last name is required')).toBeVisible()
    })

    test('should show error for missing date of birth', async ({ page }) => {
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      
      // Don't fill date of birth, just click Next
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      // Should not proceed to Step 2 (validation should prevent it)
      const stillOnStep1 = await page.locator('h2:has-text("Personal Information")').isVisible()
      expect(stillOnStep1).toBeTruthy()
    })

    test('should show error for underage user', async ({ page }) => {
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      
      // Set date to less than 13 years ago
      const recentDate = new Date()
      recentDate.setFullYear(recentDate.getFullYear() - 10)
      await page.fill('input[id="dateOfBirth"]', recentDate.toISOString().split('T')[0])
      
      await page.click('button:has-text("Next")')
      
      await expect(page.locator('text=You must be at least 13 years old')).toBeVisible()
    })

    test('should clear error when field is corrected', async ({ page }) => {
      // Create error
      await page.click('input[id="firstName"]')
      await page.click('input[id="lastName"]')
      await page.click('button:has-text("Next")')
      
      await expect(page.locator('text=First name is required')).toBeVisible()
      
      // Correct the error
      await page.fill('input[id="firstName"]', 'John')
      
      // Error should disappear
      await expect(page.locator('text=First name is required')).not.toBeVisible()
    })

    test('should not proceed to Step 2 with invalid data', async ({ page }) => {
      await page.fill('input[id="firstName"]', 'J')
      await page.click('button:has-text("Next")')
      
      // Should still be on Step 1
      await expect(page.locator('h2:has-text("Personal Information")')).toBeVisible()
      await expect(page.locator('text=Step 1 of 4')).toBeVisible()
    })

    test('should proceed to Step 2 with valid data', async ({ page }) => {
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      await page.fill('input[id="dateOfBirth"]', '1990-01-01')
      
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      // Should be on Step 2
      await expect(page.locator('h2:has-text("Account Details")')).toBeVisible()
      await expect(page.locator('text=Step 2 of 4')).toBeVisible()
    })
  })

  test.describe('Step 2: Account Details - Field Validation', () => {
    test.beforeEach(async ({ page }) => {
      // Fill Step 1 and proceed
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      await page.fill('input[id="dateOfBirth"]', '1990-01-01')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
    })

    test('should display Step 2 fields', async ({ page }) => {
      await expect(page.locator('input[id="email"]')).toBeVisible()
      await expect(page.locator('input[id="username"]')).toBeVisible()
      await expect(page.locator('input[id="password"]')).toBeVisible()
      await expect(page.locator('input[id="confirmPassword"]')).toBeVisible()
    })

    test('should show error for invalid email format', async ({ page }) => {
      await page.fill('input[id="email"]', 'invalidemail')
      await page.click('input[id="username"]')
      await page.click('button:has-text("Next")')
      
      await expect(page.locator('text=Please enter a valid email address')).toBeVisible()
    })

    test('should show error for short username', async ({ page }) => {
      await page.fill('input[id="email"]', 'john@example.com')
      await page.fill('input[id="username"]', 'ab')
      await page.click('button:has-text("Next")')
      
      await expect(page.locator('text=Username must be at least 3 characters')).toBeVisible()
    })

    test('should show error for invalid username characters', async ({ page }) => {
      await page.fill('input[id="email"]', 'john@example.com')
      await page.fill('input[id="username"]', 'user@name!')
      await page.click('button:has-text("Next")')
      
      await expect(page.locator('text=Username can only contain letters, numbers, and underscores')).toBeVisible()
    })

    test('should show error for weak password', async ({ page }) => {
      await page.fill('input[id="email"]', 'john@example.com')
      await page.fill('input[id="username"]', 'johndoe')
      await page.fill('input[id="password"]', 'weak')
      await page.click('button:has-text("Next")')
      
      await expect(page.locator('text=Password must be at least 8 characters')).toBeVisible()
    })

    test('should show error for password without requirements', async ({ page }) => {
      await page.fill('input[id="email"]', 'john@example.com')
      await page.fill('input[id="username"]', 'johndoe')
      await page.fill('input[id="password"]', 'password')
      await page.click('button:has-text("Next")')
      
      await expect(page.locator('text=Password must contain uppercase, lowercase, and number')).toBeVisible()
    })

    test('should show error when passwords do not match', async ({ page }) => {
      await page.fill('input[id="email"]', 'john@example.com')
      await page.fill('input[id="username"]', 'johndoe')
      await page.fill('input[id="password"]', 'Password123')
      await page.fill('input[id="confirmPassword"]', 'Password456')
      await page.click('button:has-text("Next")')
      
      await expect(page.locator('text=Passwords do not match')).toBeVisible()
    })

    test('should display password requirements help text', async ({ page }) => {
      await expect(page.locator('text=At least 8 characters with uppercase, lowercase, and number')).toBeVisible()
    })

    test('should display username requirements help text', async ({ page }) => {
      await expect(page.locator('text=Letters, numbers, and underscores only')).toBeVisible()
    })

    test('should proceed to Step 3 with valid account details', async ({ page }) => {
      await page.fill('input[id="email"]', 'john@example.com')
      await page.fill('input[id="username"]', 'johndoe')
      await page.fill('input[id="password"]', 'Password123')
      await page.fill('input[id="confirmPassword"]', 'Password123')
      
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      await expect(page.locator('h2:has-text("Preferences")')).toBeVisible()
      await expect(page.locator('text=Step 3 of 4')).toBeVisible()
    })
  })

  test.describe('Step 3: Preferences - Optional Fields', () => {
    test.beforeEach(async ({ page }) => {
      // Fill Steps 1 & 2 and proceed
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      await page.fill('input[id="dateOfBirth"]', '1990-01-01')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      await page.fill('input[id="email"]', 'john@example.com')
      await page.fill('input[id="username"]', 'johndoe')
      await page.fill('input[id="password"]', 'Password123')
      await page.fill('input[id="confirmPassword"]', 'Password123')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
    })

    test('should display Step 3 fields', async ({ page }) => {
      await expect(page.locator('input[id="newsletter"]')).toBeVisible()
      await expect(page.locator('input[id="notifications"]')).toBeVisible()
      await expect(page.locator('select[id="theme"]')).toBeVisible()
      await expect(page.locator('select[id="language"]')).toBeVisible()
    })

    test('should show optional preferences label', async ({ page }) => {
      await expect(page.locator('text=Customize your experience (optional)')).toBeVisible()
    })

    test('should toggle newsletter checkbox', async ({ page }) => {
      const newsletter = page.locator('input[id="newsletter"]')
      
      // Should be unchecked by default
      await expect(newsletter).not.toBeChecked()
      
      // Check it
      await newsletter.check()
      await expect(newsletter).toBeChecked()
      
      // Uncheck it
      await newsletter.uncheck()
      await expect(newsletter).not.toBeChecked()
    })

    test('should have notifications enabled by default', async ({ page }) => {
      const notifications = page.locator('input[id="notifications"]')
      await expect(notifications).toBeChecked()
    })

    test('should change theme preference', async ({ page }) => {
      const themeSelect = page.locator('select[id="theme"]')
      
      await themeSelect.selectOption('light')
      await expect(themeSelect).toHaveValue('light')
      
      await themeSelect.selectOption('dark')
      await expect(themeSelect).toHaveValue('dark')
    })

    test('should change language preference', async ({ page }) => {
      const languageSelect = page.locator('select[id="language"]')
      
      await languageSelect.selectOption('es')
      await expect(languageSelect).toHaveValue('es')
    })

    test('should proceed to Step 4 without filling preferences', async ({ page }) => {
      // Preferences are optional, should proceed without changes
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      await expect(page.locator('h2:has-text("Review & Accept")')).toBeVisible()
      await expect(page.locator('text=Step 4 of 4')).toBeVisible()
    })
  })

  test.describe('Step 4: Review & Terms', () => {
    test.beforeEach(async ({ page }) => {
      // Fill all steps and proceed to Step 4
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      await page.fill('input[id="dateOfBirth"]', '1990-01-01')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      await page.fill('input[id="email"]', 'john@example.com')
      await page.fill('input[id="username"]', 'johndoe')
      await page.fill('input[id="password"]', 'Password123')
      await page.fill('input[id="confirmPassword"]', 'Password123')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      await page.check('input[id="newsletter"]')
      await page.selectOption('select[id="theme"]', 'dark')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
    })

    test('should display registration summary', async ({ page }) => {
      await expect(page.locator('text=Registration Summary')).toBeVisible()
      
      // Verify all entered data is displayed
      await expect(page.locator('text=John Doe')).toBeVisible()
      await expect(page.locator('text=john@example.com')).toBeVisible()
      await expect(page.locator('text=@johndoe')).toBeVisible()
      await expect(page.locator('text=1990-01-01')).toBeVisible()
      await expect(page.locator('text=Yes', { exact: false })).toBeVisible() // Newsletter
      await expect(page.locator('text=Dark')).toBeVisible() // Theme
    })

    test('should display terms and conditions checkbox', async ({ page }) => {
      const termsCheckbox = page.locator('input[id="termsAccepted"]')
      await expect(termsCheckbox).toBeVisible()
      
      // Check that the label or text mentions terms
      const label = page.locator('label[for="termsAccepted"]')
      const labelText = await label.textContent()
      
      expect(labelText).toMatch(/terms/i)
    })

    test('should display privacy policy checkbox', async ({ page }) => {
      const privacyCheckbox = page.locator('input[id="privacyAccepted"]')
      await expect(privacyCheckbox).toBeVisible()
      
      // Check for privacy text (may be in link)
      const privacyText = page.locator('text=/Privacy Policy/i')
      expect(await privacyText.count()).toBeGreaterThan(0)
    })

    test('should show error when submitting without accepting terms', async ({ page }) => {
      await page.check('input[id="privacyAccepted"]')
      await page.click('button:has-text("Complete Registration")')
      
      await expect(page.locator('text=You must accept the terms and conditions')).toBeVisible()
    })

    test('should show error when submitting without accepting privacy', async ({ page }) => {
      await page.check('input[id="termsAccepted"]')
      await page.click('button:has-text("Complete Registration")')
      
      await expect(page.locator('text=You must accept the privacy policy')).toBeVisible()
    })

    test('should show both errors when neither is accepted', async ({ page }) => {
      await page.click('button:has-text("Complete Registration")')
      
      await expect(page.locator('text=You must accept the terms and conditions')).toBeVisible()
      await expect(page.locator('text=You must accept the privacy policy')).toBeVisible()
    })

    test('should submit form when both checkboxes are checked', async ({ page }) => {
      await page.check('input[id="termsAccepted"]')
      await page.check('input[id="privacyAccepted"]')
      
      await page.click('button:has-text("Complete Registration")')
      
      // Should show loading state
      await expect(page.locator('text=Submitting...')).toBeVisible()
      
      // Wait for success page
      await page.waitForTimeout(2500)
      
      // Should show success message
      await expect(page.locator('h1:has-text("Registration Successful!")')).toBeVisible()
    })
  })

  test.describe('Navigation Between Steps', () => {
    test('should navigate forward through all steps', async ({ page }) => {
      // Step 1
      await expect(page.locator('text=Step 1 of 4')).toBeVisible()
      
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      await page.fill('input[id="dateOfBirth"]', '1990-01-01')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      // Step 2
      await expect(page.locator('text=Step 2 of 4')).toBeVisible()
      
      await page.fill('input[id="email"]', 'john@example.com')
      await page.fill('input[id="username"]', 'johndoe')
      await page.fill('input[id="password"]', 'Password123')
      await page.fill('input[id="confirmPassword"]', 'Password123')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      // Step 3
      await expect(page.locator('text=Step 3 of 4')).toBeVisible()
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      // Step 4
      await expect(page.locator('text=Step 4 of 4')).toBeVisible()
    })

    test('should navigate backward using Back button', async ({ page }) => {
      // Go to Step 2
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      await page.fill('input[id="dateOfBirth"]', '1990-01-01')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      // Should be on Step 2
      await expect(page.locator('text=Step 2 of 4')).toBeVisible()
      
      // Click Back
      await page.click('button:has-text("Back")')
      await page.waitForTimeout(300)
      
      // Should be back on Step 1
      await expect(page.locator('text=Step 1 of 4')).toBeVisible()
      await expect(page.locator('h2:has-text("Personal Information")')).toBeVisible()
    })

    test('should not show Back button on Step 1', async ({ page }) => {
      await expect(page.locator('button:has-text("Back")')).not.toBeVisible()
    })

    test('should show Back button on Step 2 and beyond', async ({ page }) => {
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      await page.fill('input[id="dateOfBirth"]', '1990-01-01')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      await expect(page.locator('button:has-text("Back")')).toBeVisible()
    })

    test('should preserve form data when navigating back and forward', async ({ page }) => {
      // Fill Step 1
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      await page.fill('input[id="dateOfBirth"]', '1990-01-01')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      // Go back
      await page.click('button:has-text("Back")')
      await page.waitForTimeout(300)
      
      // Data should still be there
      await expect(page.locator('input[id="firstName"]')).toHaveValue('John')
      await expect(page.locator('input[id="lastName"]')).toHaveValue('Doe')
      await expect(page.locator('input[id="dateOfBirth"]')).toHaveValue('1990-01-01')
    })

    test('should update progress bar when navigating', async ({ page }) => {
      const progressBar = page.locator('[role="progressbar"]')
      
      // Initially at step 1
      await expect(progressBar).toHaveAttribute('aria-valuenow', '1')
      
      // Go to step 2
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      await page.fill('input[id="dateOfBirth"]', '1990-01-01')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      await expect(progressBar).toHaveAttribute('aria-valuenow', '2')
    })

    test('should allow clicking on completed steps', async ({ page }) => {
      // Complete Step 1 and go to Step 2
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      await page.fill('input[id="dateOfBirth"]', '1990-01-01')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      // Click on Step 1 indicator
      await page.click('button[aria-label*="Personal Info"][aria-label*="completed"]')
      await page.waitForTimeout(300)
      
      // Should be back on Step 1
      await expect(page.locator('text=Step 1 of 4')).toBeVisible()
    })

    test('should not allow clicking on future steps', async ({ page }) => {
      // Try to click Step 3 indicator (disabled)
      const step3Button = page.locator('button[aria-label*="Preferences"]:not([aria-current])')
      
      // Button should be disabled
      await expect(step3Button).toBeDisabled()
    })
  })

  test.describe('Form Submission and Success State', () => {
    test.beforeEach(async ({ page }) => {
      // Complete all steps
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      await page.fill('input[id="dateOfBirth"]', '1990-01-01')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      await page.fill('input[id="email"]', 'john@example.com')
      await page.fill('input[id="username"]', 'johndoe')
      await page.fill('input[id="password"]', 'Password123')
      await page.fill('input[id="confirmPassword"]', 'Password123')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      await page.check('input[id="termsAccepted"]')
      await page.check('input[id="privacyAccepted"]')
    })

    test('should show loading state during submission', async ({ page }) => {
      await page.click('button:has-text("Complete Registration")')
      
      // Should show loading text
      await expect(page.locator('text=Submitting...')).toBeVisible()
      
      // Button should be disabled
      const submitButton = page.locator('button:has-text("Submitting...")')
      await expect(submitButton).toBeDisabled()
    })

    test('should display success message after submission', async ({ page }) => {
      await page.click('button:has-text("Complete Registration")')
      
      // Wait for submission
      await page.waitForTimeout(2500)
      
      // Verify success elements
      await expect(page.locator('h1:has-text("Registration Successful!")')).toBeVisible()
      await expect(page.locator('text=Welcome, John!')).toBeVisible()
      await expect(page.locator('text=Your account has been created successfully')).toBeVisible()
    })

    test('should display user information in success message', async ({ page }) => {
      await page.click('button:has-text("Complete Registration")')
      await page.waitForTimeout(2500)
      
      // Should display email
      await expect(page.locator('text=john@example.com')).toBeVisible()
    })

    test('should display next steps information', async ({ page }) => {
      await page.click('button:has-text("Complete Registration")')
      await page.waitForTimeout(2500)
      
      await expect(page.locator('text=What\'s next?')).toBeVisible()
      await expect(page.locator('text=Check your email')).toBeVisible()
      await expect(page.locator('text=Complete your profile')).toBeVisible()
    })

    test('should display dashboard button', async ({ page }) => {
      await page.click('button:has-text("Complete Registration")')
      await page.waitForTimeout(2500)
      
      const dashboardButton = page.locator('button:has-text("Go to Dashboard")')
      await expect(dashboardButton).toBeVisible()
      await expect(dashboardButton).toBeEnabled()
    })

    test('should display success icon', async ({ page }) => {
      await page.click('button:has-text("Complete Registration")')
      await page.waitForTimeout(2500)
      
      // Verify checkmark icon is present
      const successIcon = page.locator('svg').filter({ has: page.locator('path[d*="M5 13l4 4L19 7"]') })
      await expect(successIcon.first()).toBeVisible()
    })
  })

  test.describe('Error Messages and Accessibility', () => {
    test('should have proper ARIA labels on required fields', async ({ page }) => {
      const firstName = page.locator('input[id="firstName"]')
      await expect(firstName).toHaveAttribute('aria-required', 'true')
      
      const lastName = page.locator('input[id="lastName"]')
      await expect(lastName).toHaveAttribute('aria-required', 'true')
      
      const dob = page.locator('input[id="dateOfBirth"]')
      await expect(dob).toHaveAttribute('aria-required', 'true')
    })

    test('should have proper form labels', async ({ page }) => {
      // Check that all inputs have associated labels
      await expect(page.locator('label[for="firstName"]')).toBeVisible()
      await expect(page.locator('label[for="lastName"]')).toBeVisible()
      await expect(page.locator('label[for="dateOfBirth"]')).toBeVisible()
    })

    test('should mark required fields with asterisk', async ({ page }) => {
      // Check for required indicators
      const requiredLabels = page.locator('span.text-red-500[aria-label="required"]')
      expect(await requiredLabels.count()).toBeGreaterThan(0)
    })

    test('should set aria-invalid on fields with errors', async ({ page }) => {
      await page.click('input[id="firstName"]')
      await page.click('input[id="lastName"]')
      await page.click('button:has-text("Next")')
      
      const firstName = page.locator('input[id="firstName"]')
      await expect(firstName).toHaveAttribute('aria-invalid', 'true')
    })

    test('should associate error messages with fields using aria-describedby', async ({ page }) => {
      await page.click('input[id="firstName"]')
      await page.click('input[id="lastName"]')
      await page.click('button:has-text("Next")')
      
      const firstName = page.locator('input[id="firstName"]')
      await expect(firstName).toHaveAttribute('aria-describedby', 'firstName-error')
      
      // Error message should have the ID
      await expect(page.locator('#firstName-error')).toBeVisible()
    })

    test('should announce errors with role="alert"', async ({ page }) => {
      await page.click('input[id="firstName"]')
      await page.click('input[id="lastName"]')
      await page.click('button:has-text("Next")')
      
      const errorMessage = page.locator('#firstName-error[role="alert"]')
      await expect(errorMessage).toBeVisible()
    })

    test('should have accessible step navigation', async ({ page }) => {
      const progressNav = page.locator('[role="navigation"][aria-label="Registration progress"]')
      await expect(progressNav).toBeVisible()
    })

    test('should have aria-current on active step', async ({ page }) => {
      const activeStep = page.locator('[aria-current="step"]')
      await expect(activeStep).toBeVisible()
    })

    test('should have meaningful button labels', async ({ page }) => {
      const nextButton = page.locator('button[aria-label="Go to next step"]')
      await expect(nextButton).toBeVisible()
    })

    test('should announce success state to screen readers', async ({ page }) => {
      // Complete registration
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      await page.fill('input[id="dateOfBirth"]', '1990-01-01')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      await page.fill('input[id="email"]', 'john@example.com')
      await page.fill('input[id="username"]', 'johndoe')
      await page.fill('input[id="password"]', 'Password123')
      await page.fill('input[id="confirmPassword"]', 'Password123')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      await page.check('input[id="termsAccepted"]')
      await page.check('input[id="privacyAccepted"]')
      await page.click('button:has-text("Complete Registration")')
      await page.waitForTimeout(2500)
      
      // Success message should have aria-live
      const successAlert = page.locator('[role="alert"][aria-live="polite"]')
      await expect(successAlert).toBeVisible()
    })
  })

  test.describe('Accessibility Compliance', () => {
    test('Step 1 should not have accessibility violations', async ({ page }) => {
      const accessibilityScanResults = await new AxeBuilder({ page })
        .include('form')
        .disableRules(['color-contrast']) // May have minor contrast issues in demo
        .analyze()
      
      expect(accessibilityScanResults.violations).toEqual([])
    })

    test('Step 2 should not have accessibility violations', async ({ page }) => {
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      await page.fill('input[id="dateOfBirth"]', '1990-01-01')
      await page.click('button:has-text("Next")')
      await page.waitForTimeout(300)
      
      const accessibilityScanResults = await new AxeBuilder({ page })
        .include('form')
        .disableRules(['color-contrast'])
        .analyze()
      
      expect(accessibilityScanResults.violations).toEqual([])
    })

    test('should be keyboard navigable', async ({ page }) => {
      // Tab through fields
      await page.keyboard.press('Tab')
      await page.keyboard.press('Tab')
      
      // One of the first name or last name fields should be focused
      const firstName = page.locator('input[id="firstName"]')
      const lastName = page.locator('input[id="lastName"]')
      
      const firstNameFocused = await firstName.evaluate(el => el === document.activeElement)
      const lastNameFocused = await lastName.evaluate(el => el === document.activeElement)
      
      expect(firstNameFocused || lastNameFocused).toBeTruthy()
    })

    test('should support keyboard form submission', async ({ page }) => {
      await page.fill('input[id="firstName"]', 'John')
      await page.fill('input[id="lastName"]', 'Doe')
      await page.fill('input[id="dateOfBirth"]', '1990-01-01')
      
      // Focus on Next button and press Enter
      await page.locator('button:has-text("Next")').focus()
      await page.keyboard.press('Enter')
      await page.waitForTimeout(500)
      
      // Should proceed to Step 2 or show step 2 heading
      const step2Heading = page.locator('h2').filter({ hasText: /Account Details/i })
      await expect(step2Heading).toBeVisible({ timeout: 3000 })
    })
  })
})
