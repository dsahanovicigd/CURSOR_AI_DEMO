/**
 * Login Page Object Model
 */
import { Page } from '@playwright/test';
import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
  // Selectors
  readonly emailInput = () => this.page.locator('input[type="email"], input[name="email"]');
  readonly passwordInput = () => this.page.locator('input[type="password"], input[name="password"]');
  readonly loginButton = () => this.page.locator('button:has-text("Login"), button:has-text("Sign In")');
  readonly errorMessage = () => this.page.locator('[role="alert"], .error-message, .alert-error');
  readonly forgotPasswordLink = () => this.page.locator('a:has-text("Forgot"), a:has-text("Reset")');
  readonly registerLink = () => this.page.locator('a:has-text("Register"), a:has-text("Sign Up")');

  constructor(page: Page) {
    super(page);
  }

  /**
   * Navigate to login page
   */
  async goto(): Promise<void> {
    await super.goto('/login');
  }

  /**
   * Perform login
   */
  async login(email: string, password: string): Promise<void> {
    await this.fillInput(this.emailInput(), email);
    await this.fillInput(this.passwordInput(), password);
    await this.clickElement(this.loginButton());
    await this.waitForPageLoad();
  }

  /**
   * Verify error message is displayed
   */
  async verifyErrorMessage(expectedMessage?: string): Promise<void> {
    if (expectedMessage) {
      await this.verifyText(this.errorMessage(), expectedMessage);
    } else {
      await this.verifyVisible(this.errorMessage());
    }
  }

  /**
   * Verify login form is visible
   */
  async verifyLoginForm(): Promise<void> {
    await this.verifyVisible(this.emailInput());
    await this.verifyVisible(this.passwordInput());
    await this.verifyVisible(this.loginButton());
  }
}
