/**
 * Task Management Page Object Model
 */
import { Page } from '@playwright/test';
import { BasePage } from './BasePage';

export class TaskPage extends BasePage {
  // Selectors
  readonly taskTitleInput = () => this.page.locator('input[name="title"], input[placeholder*="Title"]');
  readonly taskDescriptionInput = () => this.page.locator('textarea[name="description"], textarea[placeholder*="Description"]');
  readonly prioritySelect = () => this.page.locator('select[name="priority"], [data-testid="priority-select"]');
  readonly dueDateInput = () => this.page.locator('input[type="date"], input[name="dueDate"]');
  readonly assigneeSelect = () => this.page.locator('select[name="assignee"], [data-testid="assignee-select"]');
  readonly saveButton = () => this.page.locator('button:has-text("Save"), button:has-text("Create")');
  readonly cancelButton = () => this.page.locator('button:has-text("Cancel")');
  readonly deleteButton = () => this.page.locator('button:has-text("Delete"), [aria-label="Delete"]');
  readonly confirmDeleteButton = () => this.page.locator('button:has-text("Confirm"), button:has-text("Yes")');
  readonly completeCheckbox = () => this.page.locator('input[type="checkbox"][name="completed"], [data-testid="complete-checkbox"]');
  readonly taskModal = () => this.page.locator('[role="dialog"], .modal, [data-testid="task-modal"]');

  constructor(page: Page) {
    super(page);
  }

  /**
   * Navigate to tasks page
   */
  async goto(): Promise<void> {
    await super.goto('/tasks');
  }

  /**
   * Create a new task
   */
  async createTask(taskData: {
    title: string;
    description?: string;
    priority?: string;
    dueDate?: string;
    assignee?: string;
  }): Promise<void> {
    await this.fillInput(this.taskTitleInput(), taskData.title);
    
    if (taskData.description) {
      await this.fillInput(this.taskDescriptionInput(), taskData.description);
    }
    
    if (taskData.priority) {
      await this.selectOption(this.prioritySelect(), taskData.priority);
    }
    
    if (taskData.dueDate) {
      await this.fillInput(this.dueDateInput(), taskData.dueDate);
    }
    
    if (taskData.assignee) {
      await this.selectOption(this.assigneeSelect(), taskData.assignee);
    }
    
    await this.clickElement(this.saveButton());
    await this.waitForPageLoad();
  }

  /**
   * Edit task
   */
  async editTask(taskId: string, updates: Partial<{
    title: string;
    description: string;
    priority: string;
  }>): Promise<void> {
    // Click on task to open edit modal
    const taskCard = this.page.locator(`[data-testid="task-${taskId}"], .task-${taskId}`);
    await this.clickElement(taskCard);
    await this.waitForVisible(this.taskModal());

    if (updates.title) {
      await this.fillInput(this.taskTitleInput(), updates.title);
    }
    
    if (updates.description) {
      await this.fillInput(this.taskDescriptionInput(), updates.description);
    }
    
    if (updates.priority) {
      await this.selectOption(this.prioritySelect(), updates.priority);
    }
    
    await this.clickElement(this.saveButton());
    await this.waitForPageLoad();
  }

  /**
   * Delete task
   */
  async deleteTask(taskId: string): Promise<void> {
    const taskCard = this.page.locator(`[data-testid="task-${taskId}"], .task-${taskId}`);
    await this.hover(taskCard);
    await this.clickElement(this.deleteButton());
    await this.clickElement(this.confirmDeleteButton());
    await this.waitForPageLoad();
  }

  /**
   * Mark task as complete
   */
  async markComplete(taskId: string): Promise<void> {
    const checkbox = this.page.locator(`[data-testid="task-${taskId}"] input[type="checkbox"]`);
    await this.check(checkbox);
    await this.waitForPageLoad();
  }

  /**
   * Mark task as incomplete
   */
  async markIncomplete(taskId: string): Promise<void> {
    const checkbox = this.page.locator(`[data-testid="task-${taskId}"] input[type="checkbox"]`);
    await this.uncheck(checkbox);
    await this.waitForPageLoad();
  }

  /**
   * Verify task is displayed
   */
  async verifyTaskDisplayed(taskTitle: string): Promise<void> {
    await this.verifyText(this.page.locator(`text=${taskTitle}`), taskTitle);
  }
}
