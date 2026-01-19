export interface ProjectMetrics {
  totalTasks: number
  teamMembers: number
  activeProjects: number
  completionRate: number
  productivity?: number
}

export interface ProjectOverviewProps {
  title: string
  subtitle: string
  metrics: ProjectMetrics
  teamMembers: Array<{
    id: string
    name: string
    avatar: string
  }>
  onAddMember?: () => void
}

export interface ProgressData {
  label: string
  count: number
  color: string
  percentage: number
}

export interface PriorityData {
  label: string
  count: number
  color: string
}

export interface ProgressChartProps {
  progressData: ProgressData[]
  priorityData: PriorityData[]
  performanceMetrics: {
    productivity: number
    completionRate: number
    tasksDone: number
  }
}
