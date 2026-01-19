import { useMemo } from 'react'
import { Task } from '../../types/task.types'
import { ActivityItem } from '../../types/activity'
import ProjectOverview from './ProjectOverview'
import QuickActions, { QuickAction } from './QuickActions'
import ProgressChart from './ProgressChart'
import ActivityFeed from './ActivityFeed'
import Avatar from '../common/Avatar'

interface TeamDashboardProps {
  tasks: Task[]
  activities: ActivityItem[]
  stats: {
    productivity: number
    completionRate: number
    activeProjects: number
  }
  onTaskCreate?: () => void
  onReportsView?: () => void
  onTeamManage?: () => void
  onSettingsOpen?: () => void
  onActivityViewAll?: () => void
  onAddMember?: () => void
}

const TeamDashboard = ({
  tasks,
  activities,
  stats,
  onTaskCreate,
  onReportsView,
  onTeamManage,
  onSettingsOpen,
  onActivityViewAll,
  onAddMember,
}: TeamDashboardProps) => {
  // Calculate team members from tasks
  const teamMembers = useMemo(() => {
    const members = new Map()
    tasks.forEach(task => {
      if (task.assignee) {
        members.set(task.assignee.id, task.assignee)
      }
    })
    return Array.from(members.values())
  }, [tasks])

  // Calculate progress data
  const progressData = useMemo(() => {
    const statusCounts = {
      todo: tasks.filter(t => t.status === 'todo').length,
      inProgress: tasks.filter(t => t.status === 'in-progress').length,
      review: tasks.filter(t => t.status === 'review').length,
      completed: tasks.filter(t => t.status === 'completed').length
    }
    
    return [
      { label: 'To Do', count: statusCounts.todo, color: 'bg-gray-400', percentage: (statusCounts.todo / tasks.length) * 100 },
      { label: 'In Progress', count: statusCounts.inProgress, color: 'bg-blue-500', percentage: (statusCounts.inProgress / tasks.length) * 100 },
      { label: 'In Review', count: statusCounts.review, color: 'bg-purple-500', percentage: (statusCounts.review / tasks.length) * 100 },
      { label: 'Completed', count: statusCounts.completed, color: 'bg-green-500', percentage: (statusCounts.completed / tasks.length) * 100 }
    ]
  }, [tasks])

  // Priority breakdown
  const priorityData = useMemo(() => {
    const counts = {
      urgent: tasks.filter(t => t.priority === 'urgent').length,
      high: tasks.filter(t => t.priority === 'high').length,
      medium: tasks.filter(t => t.priority === 'medium').length,
      low: tasks.filter(t => t.priority === 'low').length
    }
    return [
      { label: 'Urgent', count: counts.urgent, color: 'text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-400' },
      { label: 'High', count: counts.high, color: 'text-orange-600 bg-orange-100 dark:bg-orange-900/30 dark:text-orange-400' },
      { label: 'Medium', count: counts.medium, color: 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30 dark:text-yellow-400' },
      { label: 'Low', count: counts.low, color: 'text-blue-600 bg-blue-100 dark:bg-blue-900/30 dark:text-blue-400' }
    ]
  }, [tasks])

  // Quick actions configuration
  const quickActions: QuickAction[] = [
    { icon: '➕', label: 'New Task', color: 'bg-blue-600 hover:bg-blue-700', action: () => onTaskCreate?.() },
    { icon: '📊', label: 'Reports', color: 'bg-purple-600 hover:bg-purple-700', action: () => onReportsView?.() },
    { icon: '👥', label: 'Team', color: 'bg-green-600 hover:bg-green-700', action: () => onTeamManage?.() },
    { icon: '⚙️', label: 'Settings', color: 'bg-gray-600 hover:bg-gray-700', action: () => onSettingsOpen?.() }
  ]

  // Performance metrics
  const performanceMetrics = {
    productivity: stats.productivity,
    completionRate: stats.completionRate,
    tasksDone: tasks.filter(t => t.status === 'completed').length
  }

  // Project metrics
  const projectMetrics = {
    totalTasks: tasks.length,
    teamMembers: teamMembers.length,
    activeProjects: stats.activeProjects,
    completionRate: stats.completionRate,
    productivity: stats.productivity
  }

  return (
    <div className="p-4 lg:p-6 space-y-6">
      {/* Project Overview Header */}
      <ProjectOverview
        title="Team Collaboration Dashboard"
        subtitle="Project Overview & Activity"
        metrics={projectMetrics}
        teamMembers={teamMembers}
        onAddMember={onAddMember}
      />

      {/* Quick Action Buttons */}
      <QuickActions actions={quickActions} />

      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Task Progress & Priority */}
        <ProgressChart
          progressData={progressData}
          priorityData={priorityData}
          performanceMetrics={performanceMetrics}
        />

        {/* Right Column - Activity Feed and Other Widgets */}
        <div className="space-y-6">
          <ActivityFeed
            activities={activities}
            onViewAll={onActivityViewAll}
          />

          {/* Upcoming Deadlines */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2 mb-6">
              <span className="text-2xl">⏰</span>
              Upcoming Deadlines
            </h2>
            <div className="space-y-3">
              {tasks
                .filter(t => t.status !== 'completed' && t.dueDate)
                .sort((a, b) => new Date(a.dueDate!).getTime() - new Date(b.dueDate!).getTime())
                .slice(0, 5)
                .map((task) => (
                  <div 
                    key={task.id}
                    className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg hover:shadow-md transition-shadow"
                  >
                    {task.assignee && (
                      <Avatar 
                        src={task.assignee.avatar}
                        alt={task.assignee.name}
                        size="sm"
                      />
                    )}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                        {task.title}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Due: {new Date(task.dueDate!).toLocaleDateString()}
                      </p>
                    </div>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      task.priority === 'urgent' 
                        ? 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400'
                        : task.priority === 'high'
                        ? 'bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400'
                        : 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400'
                    }`}>
                      {task.priority}
                    </span>
                  </div>
                ))}
            </div>
          </div>

          {/* Team Workload */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2 mb-6">
              <span className="text-2xl">💼</span>
              Team Workload
            </h2>
            <div className="space-y-4">
              {teamMembers.slice(0, 5).map((member) => {
                const memberTasks = tasks.filter(t => t.assignee?.id === member.id && t.status !== 'completed')
                const workload = (memberTasks.length / tasks.length) * 100
                
                return (
                  <div key={member.id}>
                    <div className="flex items-center gap-3 mb-2">
                      <Avatar 
                        src={member.avatar}
                        alt={member.name}
                        size="sm"
                      />
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm font-medium text-gray-900 dark:text-white">
                            {member.name}
                          </span>
                          <span className="text-xs text-gray-500 dark:text-gray-400">
                            {memberTasks.length} tasks
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full transition-all duration-500 ${
                              workload > 30 ? 'bg-red-500' : workload > 20 ? 'bg-yellow-500' : 'bg-green-500'
                            }`}
                            style={{ width: `${Math.min(workload, 100)}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TeamDashboard
