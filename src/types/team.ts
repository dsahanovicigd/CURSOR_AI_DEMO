export interface TeamMember {
  id: string
  name: string
  avatar: string
  role?: string
  status?: 'online' | 'offline' | 'away'
}

export interface TeamMembersProps {
  members: TeamMember[]
  onAddMember?: () => void
}

export interface TeamStats {
  totalTasks: number
  teamMembers: number
  activeProjects: number
  completionRate: number
}
