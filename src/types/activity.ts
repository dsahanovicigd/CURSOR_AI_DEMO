export type ActivityType = 'task_created' | 'task_completed' | 'comment' | 'assignment' | 'status_change'

export interface ActivityUser {
  name: string
  avatar: string
}

export interface ActivityItem {
  id: string
  type: ActivityType
  user: ActivityUser
  message: string
  timestamp: string
  relatedTask?: string
}

export interface ActivityFeedProps {
  activities: ActivityItem[]
  onViewAll?: () => void
}
