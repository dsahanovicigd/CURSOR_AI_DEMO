export type TaskStatus = 'todo' | 'in-progress' | 'review' | 'completed'
export type TaskPriority = 'low' | 'medium' | 'high' | 'urgent'

export interface Task {
  id: string
  title: string
  description: string
  status: TaskStatus
  priority: TaskPriority
  assignee?: TaskAssignee
  dueDate?: string
  tags?: string[]
  progress?: number
  createdAt: string
  updatedAt: string
}

export interface TaskAssignee {
  id: string
  name: string
  avatar: string
}

export interface TaskStats {
  total: number
  completed: number
  inProgress: number
  todo: number
  overdue: number
}

export interface DashboardStats {
  tasks: TaskStats
  productivity: number
  completionRate: number
  activeProjects: number
}
