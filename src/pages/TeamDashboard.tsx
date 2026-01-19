import { useState, useMemo } from 'react'
import { useDarkMode } from '../hooks/useDarkMode'
import Sidebar from '../components/dashboard/Sidebar'
import DashboardHeader from '../components/dashboard/DashboardHeader'
import { sampleTasks, dashboardStats } from '../data/sampleTasks'
import { sampleUserProfile } from '../data/sampleNavigation'
import Avatar from '../components/common/Avatar'

// Activity Feed Item Type
interface ActivityItem {
  id: string
  type: 'task_created' | 'task_completed' | 'comment' | 'assignment' | 'status_change'
  user: {
    name: string
    avatar: string
  }
  message: string
  timestamp: string
  relatedTask?: string
}

// Sample Activity Data
const recentActivities: ActivityItem[] = [
  {
    id: '1',
    type: 'task_completed',
    user: {
      name: 'Alex Johnson',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    message: 'completed Database optimization',
    timestamp: '2 hours ago',
    relatedTask: 'Database optimization'
  },
  {
    id: '2',
    type: 'comment',
    user: {
      name: 'Sarah Chen',
      avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    message: 'commented on Design new landing page',
    timestamp: '3 hours ago',
    relatedTask: 'Design new landing page'
  },
  {
    id: '3',
    type: 'assignment',
    user: {
      name: 'John Doe',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    message: 'was assigned to Fix authentication bug',
    timestamp: '5 hours ago',
    relatedTask: 'Fix authentication bug'
  },
  {
    id: '4',
    type: 'status_change',
    user: {
      name: 'John Doe',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    message: 'moved Fix authentication bug to In Review',
    timestamp: '6 hours ago',
    relatedTask: 'Fix authentication bug'
  },
  {
    id: '5',
    type: 'task_created',
    user: {
      name: 'Lisa Anderson',
      avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    message: 'created Security audit',
    timestamp: '1 day ago',
    relatedTask: 'Security audit'
  },
  {
    id: '6',
    type: 'task_completed',
    user: {
      name: 'David Lee',
      avatar: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    message: 'completed Customer feedback analysis',
    timestamp: '2 days ago',
    relatedTask: 'Customer feedback analysis'
  }
]

const TeamDashboard = () => {
  const { isDarkMode, toggleDarkMode } = useDarkMode()
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [tasks] = useState(sampleTasks)

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

  const handleLogout = () => {
    console.log('Logging out...')
  }

  const quickActions = [
    { icon: '➕', label: 'New Task', color: 'bg-blue-600 hover:bg-blue-700', action: () => console.log('Create Task') },
    { icon: '📊', label: 'Reports', color: 'bg-purple-600 hover:bg-purple-700', action: () => console.log('View Reports') },
    { icon: '👥', label: 'Team', color: 'bg-green-600 hover:bg-green-700', action: () => console.log('Manage Team') },
    { icon: '⚙️', label: 'Settings', color: 'bg-gray-600 hover:bg-gray-700', action: () => console.log('Settings') }
  ]

  // Activity icon mapping
  const getActivityIcon = (type: ActivityItem['type']) => {
    switch (type) {
      case 'task_completed':
        return <div className="w-8 h-8 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center">
          <svg className="w-5 h-5 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        </div>
      case 'task_created':
        return <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
          <svg className="w-5 h-5 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
        </div>
      case 'comment':
        return <div className="w-8 h-8 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center">
          <svg className="w-5 h-5 text-purple-600 dark:text-purple-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M2 5a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H4a2 2 0 01-2-2V5z" />
          </svg>
        </div>
      case 'assignment':
        return <div className="w-8 h-8 bg-orange-100 dark:bg-orange-900/30 rounded-full flex items-center justify-center">
          <svg className="w-5 h-5 text-orange-600 dark:text-orange-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
          </svg>
        </div>
      case 'status_change':
        return <div className="w-8 h-8 bg-yellow-100 dark:bg-yellow-900/30 rounded-full flex items-center justify-center">
          <svg className="w-5 h-5 text-yellow-600 dark:text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
          </svg>
        </div>
    }
  }

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900 overflow-hidden">
      {/* Sidebar */}
      <Sidebar 
        isOpen={isSidebarOpen} 
        onClose={() => setIsSidebarOpen(false)} 
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <DashboardHeader
          user={sampleUserProfile}
          onMenuClick={() => setIsSidebarOpen(!isSidebarOpen)}
          isDarkMode={isDarkMode}
          onToggleDarkMode={toggleDarkMode}
          onLogout={handleLogout}
        />

        {/* Content Area */}
        <main className="flex-1 overflow-y-auto">
          <div className="p-4 lg:p-6 space-y-6">
            {/* Project Overview Header */}
            <div className="bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-2xl p-6 md:p-8 text-white shadow-2xl">
              <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
                      <span className="text-2xl">🚀</span>
                    </div>
                    <div>
                      <h1 className="text-2xl md:text-3xl font-bold">Team Collaboration Dashboard</h1>
                      <p className="text-blue-100">Project Overview & Activity</p>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-4 mt-4">
                    <div className="bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
                      <div className="text-2xl font-bold">{tasks.length}</div>
                      <div className="text-sm text-blue-100">Total Tasks</div>
                    </div>
                    <div className="bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
                      <div className="text-2xl font-bold">{teamMembers.length}</div>
                      <div className="text-sm text-blue-100">Team Members</div>
                    </div>
                    <div className="bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
                      <div className="text-2xl font-bold">{dashboardStats.activeProjects}</div>
                      <div className="text-sm text-blue-100">Active Projects</div>
                    </div>
                    <div className="bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
                      <div className="text-2xl font-bold">{dashboardStats.completionRate}%</div>
                      <div className="text-sm text-blue-100">Completion Rate</div>
                    </div>
                  </div>
                </div>

                {/* Team Member Avatars */}
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
                  <div className="text-sm font-medium text-blue-100 mb-3">Team Members</div>
                  <div className="flex flex-wrap gap-2">
                    {teamMembers.map((member) => (
                      <div key={member.id} className="relative group">
                        <Avatar
                          src={member.avatar}
                          alt={member.name}
                          size="md"
                          className="ring-2 ring-white/50 hover:ring-white transition-all cursor-pointer transform hover:scale-110"
                        />
                        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                          {member.name}
                        </div>
                      </div>
                    ))}
                    <button className="w-10 h-10 rounded-full bg-white/20 border-2 border-white/50 border-dashed flex items-center justify-center hover:bg-white/30 transition-colors">
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Action Buttons */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 md:gap-4">
              {quickActions.map((action, index) => (
                <button
                  key={index}
                  onClick={action.action}
                  className={`${action.color} text-white rounded-xl p-4 md:p-6 shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1 active:scale-95`}
                >
                  <div className="text-3xl mb-2">{action.icon}</div>
                  <div className="font-semibold text-sm md:text-base">{action.label}</div>
                </button>
              ))}
            </div>

            {/* Main Dashboard Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left Column - Task Progress & Priority */}
              <div className="lg:col-span-2 space-y-6">
                {/* Task Progress Chart */}
                <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                      <span className="text-2xl">📊</span>
                      Task Progress Overview
                    </h2>
                    <select className="px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
                      <option>This Week</option>
                      <option>This Month</option>
                      <option>This Quarter</option>
                    </select>
                  </div>

                  {/* Progress Bars */}
                  <div className="space-y-4">
                    {progressData.map((item, index) => (
                      <div key={index}>
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <div className={`w-3 h-3 rounded-full ${item.color}`}></div>
                            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                              {item.label}
                            </span>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-bold text-gray-900 dark:text-white">
                              {item.count}
                            </span>
                            <span className="text-xs text-gray-500 dark:text-gray-400">
                              ({item.percentage.toFixed(0)}%)
                            </span>
                          </div>
                        </div>
                        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                          <div 
                            className={`${item.color} h-3 rounded-full transition-all duration-500 relative overflow-hidden`}
                            style={{ width: `${item.percentage}%` }}
                          >
                            <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Visual Chart */}
                  <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                    <div className="flex items-end justify-between gap-2 h-40">
                      {progressData.map((item, index) => (
                        <div key={index} className="flex-1 flex flex-col items-center gap-2">
                          <div className="w-full flex items-end justify-center" style={{ height: '100%' }}>
                            <div 
                              className={`w-full ${item.color} rounded-t-lg transition-all duration-500 hover:opacity-80 cursor-pointer relative group`}
                              style={{ height: `${item.percentage}%`, minHeight: '20px' }}
                            >
                              <div className="absolute inset-0 flex items-center justify-center text-white font-bold text-sm">
                                {item.count}
                              </div>
                            </div>
                          </div>
                          <div className="text-xs font-medium text-gray-600 dark:text-gray-400 text-center">
                            {item.label}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Priority Breakdown */}
                <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
                  <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2 mb-6">
                    <span className="text-2xl">🎯</span>
                    Priority Breakdown
                  </h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {priorityData.map((item, index) => (
                      <div key={index} className={`${item.color} rounded-lg p-4 text-center`}>
                        <div className="text-3xl font-bold mb-1">{item.count}</div>
                        <div className="text-sm font-medium">{item.label}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Team Performance Stats */}
                <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
                  <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2 mb-6">
                    <span className="text-2xl">📈</span>
                    Team Performance
                  </h2>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                    <div className="text-center">
                      <div className="w-20 h-20 mx-auto mb-3 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
                        <span className="text-3xl font-bold text-green-600 dark:text-green-400">
                          {dashboardStats.productivity}%
                        </span>
                      </div>
                      <div className="text-sm font-semibold text-gray-900 dark:text-white">Productivity</div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">Above target</div>
                    </div>
                    <div className="text-center">
                      <div className="w-20 h-20 mx-auto mb-3 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                        <span className="text-3xl font-bold text-blue-600 dark:text-blue-400">
                          {dashboardStats.completionRate}%
                        </span>
                      </div>
                      <div className="text-sm font-semibold text-gray-900 dark:text-white">Completion Rate</div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">This week</div>
                    </div>
                    <div className="text-center">
                      <div className="w-20 h-20 mx-auto mb-3 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
                        <span className="text-3xl font-bold text-purple-600 dark:text-purple-400">
                          {tasks.filter(t => t.status === 'completed').length}
                        </span>
                      </div>
                      <div className="text-sm font-semibold text-gray-900 dark:text-white">Tasks Done</div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">This week</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Column - Recent Activity Feed */}
              <div className="space-y-6">
                {/* Recent Activity */}
                <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                      <span className="text-2xl">🔔</span>
                      Recent Activity
                    </h2>
                    <button className="text-sm text-blue-600 dark:text-blue-400 hover:underline">
                      View All
                    </button>
                  </div>

                  <div className="space-y-4 max-h-[600px] overflow-y-auto">
                    {recentActivities.map((activity) => (
                      <div 
                        key={activity.id}
                        className="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors cursor-pointer"
                      >
                        {getActivityIcon(activity.type)}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <Avatar 
                              src={activity.user.avatar}
                              alt={activity.user.name}
                              size="sm"
                            />
                            <p className="text-sm text-gray-900 dark:text-white font-medium">
                              {activity.user.name}
                            </p>
                          </div>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            {activity.message}
                          </p>
                          <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                            {activity.timestamp}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

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
        </main>
      </div>
    </div>
  )
}

export default TeamDashboard
