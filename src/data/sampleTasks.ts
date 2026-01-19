import { Task, DashboardStats } from '../types/task.types'

export const sampleTasks: Task[] = [
  {
    id: '1',
    title: 'Design new landing page',
    description: 'Create mockups for the new product landing page with focus on conversion optimization',
    status: 'in-progress',
    priority: 'high',
    assignee: {
      id: '1',
      name: 'Sarah Chen',
      avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    dueDate: '2026-01-25',
    tags: ['Design', 'UI/UX', 'Marketing'],
    progress: 65,
    createdAt: '2026-01-15',
    updatedAt: '2026-01-19'
  },
  {
    id: '2',
    title: 'Fix authentication bug',
    description: 'Users reporting issues with social login on mobile devices',
    status: 'review',
    priority: 'urgent',
    assignee: {
      id: '2',
      name: 'John Doe',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    dueDate: '2026-01-20',
    tags: ['Bug', 'Backend', 'Critical'],
    progress: 90,
    createdAt: '2026-01-18',
    updatedAt: '2026-01-19'
  },
  {
    id: '3',
    title: 'Update documentation',
    description: 'Add API documentation for the new v2 endpoints',
    status: 'todo',
    priority: 'medium',
    assignee: {
      id: '3',
      name: 'Emma Wilson',
      avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    dueDate: '2026-01-28',
    tags: ['Documentation', 'API'],
    progress: 10,
    createdAt: '2026-01-16',
    updatedAt: '2026-01-17'
  },
  {
    id: '4',
    title: 'Implement dark mode',
    description: 'Add dark mode support across the entire application',
    status: 'in-progress',
    priority: 'medium',
    assignee: {
      id: '4',
      name: 'Michael Brown',
      avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    dueDate: '2026-01-30',
    tags: ['Frontend', 'UI', 'Enhancement'],
    progress: 45,
    createdAt: '2026-01-10',
    updatedAt: '2026-01-19'
  },
  {
    id: '5',
    title: 'Database optimization',
    description: 'Optimize slow queries and add proper indexes',
    status: 'completed',
    priority: 'high',
    assignee: {
      id: '5',
      name: 'Alex Johnson',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    dueDate: '2026-01-18',
    tags: ['Backend', 'Performance', 'Database'],
    progress: 100,
    createdAt: '2026-01-12',
    updatedAt: '2026-01-18'
  },
  {
    id: '6',
    title: 'Mobile app testing',
    description: 'Conduct thorough testing on iOS and Android devices',
    status: 'todo',
    priority: 'high',
    dueDate: '2026-01-26',
    tags: ['Testing', 'Mobile', 'QA'],
    progress: 0,
    createdAt: '2026-01-19',
    updatedAt: '2026-01-19'
  },
  {
    id: '7',
    title: 'Setup CI/CD pipeline',
    description: 'Configure automated deployment with GitHub Actions',
    status: 'in-progress',
    priority: 'medium',
    assignee: {
      id: '6',
      name: 'Lisa Anderson',
      avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    dueDate: '2026-01-27',
    tags: ['DevOps', 'Automation'],
    progress: 30,
    createdAt: '2026-01-14',
    updatedAt: '2026-01-19'
  },
  {
    id: '8',
    title: 'Customer feedback analysis',
    description: 'Review and categorize recent customer feedback from surveys',
    status: 'completed',
    priority: 'low',
    assignee: {
      id: '7',
      name: 'David Lee',
      avatar: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    dueDate: '2026-01-15',
    tags: ['Research', 'Customer Success'],
    progress: 100,
    createdAt: '2026-01-08',
    updatedAt: '2026-01-15'
  },
  {
    id: '9',
    title: 'Refactor payment service',
    description: 'Improve payment processing code and add better error handling',
    status: 'review',
    priority: 'high',
    assignee: {
      id: '2',
      name: 'John Doe',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    dueDate: '2026-01-24',
    tags: ['Backend', 'Refactoring', 'Payments'],
    progress: 85,
    createdAt: '2026-01-16',
    updatedAt: '2026-01-19'
  },
  {
    id: '10',
    title: 'Security audit',
    description: 'Conduct comprehensive security audit of the application',
    status: 'todo',
    priority: 'urgent',
    dueDate: '2026-01-22',
    tags: ['Security', 'Audit', 'Compliance'],
    progress: 0,
    createdAt: '2026-01-19',
    updatedAt: '2026-01-19'
  }
]

export const dashboardStats: DashboardStats = {
  tasks: {
    total: 10,
    completed: 2,
    inProgress: 4,
    todo: 3,
    overdue: 1
  },
  productivity: 87,
  completionRate: 75,
  activeProjects: 5
}
