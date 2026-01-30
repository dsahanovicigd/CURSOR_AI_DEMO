import { useState } from 'react'
import { useDarkMode } from '../hooks/useDarkMode'
import { useAuth } from '../context/AuthContext'
import Sidebar from '../components/dashboard/Sidebar'
import DashboardHeader from '../components/dashboard/DashboardHeader'
import StatWidget from '../components/dashboard/StatWidget'
import TaskCard from '../components/dashboard/TaskCard'
import KanbanBoard from '../components/kanban/KanbanBoard'
import { sampleTasks, dashboardStats } from '../data/sampleTasks'

type ViewMode = 'list' | 'kanban'

const Dashboard = () => {
  const { isDarkMode, toggleDarkMode } = useDarkMode()
  const { user, logout } = useAuth()
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [tasks] = useState(sampleTasks)
  const [viewMode, setViewMode] = useState<ViewMode>('list')

  const stats = dashboardStats

  const handleLogout = () => {
    logout() // Instant logout - clears tokens and user state immediately
    // ProtectedRoute will detect logout and redirect to login
  }

  // Create user profile from auth context
  const userProfile = user ? {
    name: user.name || user.username,
    email: user.email,
    avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(user.name || user.username)}&background=667eea&color=fff`
  } : {
    name: 'Guest',
    email: '',
    avatar: 'https://ui-avatars.com/api/?name=Guest&background=gray&color=fff'
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
          user={userProfile}
          onMenuClick={() => setIsSidebarOpen(!isSidebarOpen)}
          isDarkMode={isDarkMode}
          onToggleDarkMode={toggleDarkMode}
          onLogout={handleLogout}
        />

        {/* Content Area */}
        <main className="flex-1 overflow-y-auto">
          <div className="p-4 lg:p-6 space-y-6">
            {/* Welcome Section */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 md:p-8 text-white">
              <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                <div>
                  <h2 className="text-2xl md:text-3xl font-bold mb-2">
                    Good morning, {userProfile.name.split(' ')[0]}! 👋
                  </h2>
                  <p className="text-blue-100">
                    You have {stats.tasks.inProgress} tasks in progress and {stats.tasks.todo} tasks to start
                  </p>
                </div>
                <button className="px-6 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-blue-50 transition-colors shadow-lg">
                  Create New Task
                </button>
              </div>
            </div>

            {/* Statistics Widgets */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
              <StatWidget
                title="Total Tasks"
                value={stats.tasks.total}
                icon="📋"
                subtitle={`${stats.tasks.completed} completed`}
                trend={{ value: 12, isPositive: true }}
                color="blue"
              />
              <StatWidget
                title="In Progress"
                value={stats.tasks.inProgress}
                icon="⏱️"
                subtitle="Active tasks"
                trend={{ value: 8, isPositive: true }}
                color="purple"
              />
              <StatWidget
                title="Completion Rate"
                value={`${stats.completionRate}%`}
                icon="✅"
                subtitle="This week"
                trend={{ value: 5, isPositive: true }}
                color="green"
              />
              <StatWidget
                title="Productivity"
                value={`${stats.productivity}%`}
                icon="🎯"
                subtitle="Above average"
                trend={{ value: 3, isPositive: false }}
                color="orange"
              />
            </div>

            {/* View Mode Toggle */}
            <div className="flex items-center justify-between bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">Task Management</h2>
              <div className="flex gap-2">
                <button
                  onClick={() => setViewMode('list')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    viewMode === 'list'
                      ? 'bg-blue-600 text-white shadow-lg'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  📋 List View
                </button>
                <button
                  onClick={() => setViewMode('kanban')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    viewMode === 'kanban'
                      ? 'bg-blue-600 text-white shadow-lg'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  📊 Kanban View
                </button>
              </div>
            </div>

            {/* Tasks Section */}
            {viewMode === 'list' ? (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Tasks by Status */}
                <div className="lg:col-span-2 space-y-6">
                {/* In Progress Tasks */}
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
                      <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                      In Progress
                      <span className="px-2 py-1 text-xs font-bold bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 rounded-full">
                        {tasks.filter(t => t.status === 'in-progress').length}
                      </span>
                    </h3>
                    <button className="text-sm text-blue-600 dark:text-blue-400 hover:underline">
                      View All
                    </button>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {tasks
                      .filter(task => task.status === 'in-progress')
                      .slice(0, 4)
                      .map(task => (
                        <TaskCard key={task.id} task={task} />
                      ))}
                  </div>
                </div>

                {/* To Do Tasks */}
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
                      <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
                      To Do
                      <span className="px-2 py-1 text-xs font-bold bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-full">
                        {tasks.filter(t => t.status === 'todo').length}
                      </span>
                    </h3>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {tasks
                      .filter(task => task.status === 'todo')
                      .map(task => (
                        <TaskCard key={task.id} task={task} />
                      ))}
                  </div>
                </div>
              </div>

              {/* Sidebar - Recent Activity & Quick Stats */}
              <div className="space-y-6">
                {/* Quick Stats Card */}
                <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
                    Quick Stats
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-gray-600 dark:text-gray-400">Completed</span>
                        <span className="text-sm font-semibold text-gray-900 dark:text-white">
                          {stats.tasks.completed}/{stats.tasks.total}
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div 
                          className="bg-green-500 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${(stats.tasks.completed / stats.tasks.total) * 100}%` }}
                        />
                      </div>
                    </div>
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-gray-600 dark:text-gray-400">In Progress</span>
                        <span className="text-sm font-semibold text-gray-900 dark:text-white">
                          {stats.tasks.inProgress}/{stats.tasks.total}
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div 
                          className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${(stats.tasks.inProgress / stats.tasks.total) * 100}%` }}
                        />
                      </div>
                    </div>
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-gray-600 dark:text-gray-400">To Do</span>
                        <span className="text-sm font-semibold text-gray-900 dark:text-white">
                          {stats.tasks.todo}/{stats.tasks.total}
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div 
                          className="bg-gray-400 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${(stats.tasks.todo / stats.tasks.total) * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Review Tasks */}
                <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                    <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
                    In Review
                  </h3>
                  <div className="space-y-3">
                    {tasks
                      .filter(task => task.status === 'review')
                      .map(task => (
                        <TaskCard key={task.id} task={task} />
                      ))}
                  </div>
                </div>

                {/* Completed Tasks */}
                <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                    Completed
                  </h3>
                  <div className="space-y-3">
                    {tasks
                      .filter(task => task.status === 'completed')
                      .slice(0, 2)
                      .map(task => (
                        <div 
                          key={task.id}
                          className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg"
                        >
                          <div className="flex-shrink-0 w-8 h-8 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                            <svg className="w-5 h-5 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                              {task.title}
                            </p>
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                              Completed
                            </p>
                          </div>
                        </div>
                      ))}
                  </div>
                </div>
              </div>
            </div>
            ) : (
              <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
                <KanbanBoard />
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}

export default Dashboard
