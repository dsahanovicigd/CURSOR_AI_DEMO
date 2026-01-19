import { useState } from 'react'
import { useDarkMode } from '../hooks/useDarkMode'
import { DashboardProvider } from '../context/DashboardContext'
import Sidebar from '../components/dashboard/Sidebar'
import DashboardHeader from '../components/dashboard/DashboardHeader'
import TeamDashboard from '../components/TeamDashboard/TeamDashboard'
import { sampleTasks, dashboardStats } from '../data/sampleTasks'
import { sampleUserProfile } from '../data/sampleNavigation'
import { ActivityItem } from '../types/activity'

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

const TeamDashboardPage = () => {
  const { isDarkMode, toggleDarkMode } = useDarkMode()
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [tasks] = useState(sampleTasks)

  const handleLogout = () => {
    console.log('Logging out...')
  }

  const handleTaskCreate = () => {
    console.log('Create Task')
  }

  const handleReportsView = () => {
    console.log('View Reports')
  }

  const handleTeamManage = () => {
    console.log('Manage Team')
  }

  const handleSettingsOpen = () => {
    console.log('Settings')
  }

  const handleActivityViewAll = () => {
    console.log('View All Activities')
  }

  const handleAddMember = () => {
    console.log('Add Team Member')
  }

  // Context value for shared state
  const dashboardContextValue = {
    isDarkMode,
    toggleDarkMode,
    user: {
      id: '1',
      name: sampleUserProfile.name,
      email: sampleUserProfile.email,
      avatar: sampleUserProfile.avatar
    }
  }

  return (
    <DashboardProvider value={dashboardContextValue}>
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
            <TeamDashboard
              tasks={tasks}
              activities={recentActivities}
              stats={dashboardStats}
              onTaskCreate={handleTaskCreate}
              onReportsView={handleReportsView}
              onTeamManage={handleTeamManage}
              onSettingsOpen={handleSettingsOpen}
              onActivityViewAll={handleActivityViewAll}
              onAddMember={handleAddMember}
            />
          </main>
        </div>
      </div>
    </DashboardProvider>
  )
}

export default TeamDashboardPage
