/**
 * Dashboard Page Object Model
 */
import { Page } from '@playwright/test';
import { BasePage } from './BasePage';

export class DashboardPage extends BasePage {
  // Selectors
  readonly pageTitle = () => this.page.locator('h1, [data-testid="dashboard-title"]');
  readonly taskList = () => this.page.locator('[data-testid="task-list"], .task-list, .tasks');
  readonly taskCard = (index: number = 0) => this.page.locator('[data-testid="task-card"], .task-card').nth(index);
  readonly createTaskButton = () => this.page.locator('button:has-text("Create"), button:has-text("Add Task")');
  readonly filterDropdown = () => this.page.locator('select[name="filter"], [data-testid="filter"]');
  readonly searchInput = () => this.page.locator('input[type="search"], input[placeholder*="Search"]');
  readonly statsCards = () => this.page.locator('[data-testid="stat-card"], .stat-card');
  readonly userMenu = () => this.page.locator('[aria-label="User menu"], [data-testid="user-menu"]');
  readonly logoutButton = () => this.page.locator('button:has-text("Logout"), button:has-text("Sign Out")');

  constructor(page: Page) {
    super(page);
  }

  /**
   * Navigate to dashboard
   */
  async goto(): Promise<void> {
    await super.goto('/dashboard');
  }

  /**
   * Verify dashboard is loaded
   */
  async verifyDashboardLoaded(): Promise<void> {
    await this.verifyVisible(this.pageTitle());
    await this.waitForPageLoad();
  }

  /**
   * Get task count
   */
  async getTaskCount(): Promise<number> {
    return await this.taskList().count();
  }

  /**
   * Click create task button
   */
  async clickCreateTask(): Promise<void> {
    await this.clickElement(this.createTaskButton());
  }

  /**
   * Filter tasks by status
   */
  async filterByStatus(status: string): Promise<void> {
    await this.selectOption(this.filterDropdown(), status);
    await this.waitForPageLoad();
  }

  /**
   * Search tasks
   */
  async searchTasks(query: string): Promise<void> {
    await this.fillInput(this.searchInput(), query);
    await this.waitForPageLoad();
  }

  /**
   * Get stats card value
   */
  async getStatValue(statName: string): Promise<string> {
    const statCard = this.page.locator(`[data-testid="stat-${statName}"], .stat-${statName}`);
    return await this.getText(statCard);
  }

  /**
   * Logout
   */
  async logout(): Promise<void> {
    await this.clickElement(this.userMenu());
    await this.clickElement(this.logoutButton());
    await this.waitForPageLoad();
  }
}
