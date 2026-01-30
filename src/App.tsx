import { useState } from 'react'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/auth/ProtectedRoute'
import ProfileDemo from './pages/ProfileDemo'
import ProductShowcase from './pages/ProductShowcase'
import NavBarDemo from './pages/NavBarDemo'
import Dashboard from './pages/Dashboard'
import AnalyticsDashboard from './pages/AnalyticsDashboard'
import RegistrationForm from './pages/RegistrationForm'
import TeamDashboardPage from './pages/TeamDashboardPage'
import KanbanPage from './pages/KanbanPage'
import SocialFeedPage from './pages/SocialFeedPage'

type PageType = 'analytics' | 'dashboard' | 'navbar' | 'products' | 'profile' | 'register' | 'team' | 'kanban' | 'social'

function App() {
  const [currentPage, setCurrentPage] = useState<PageType>('analytics')

  return (
    <AuthProvider>
      <div className="min-h-screen">
        {/* Navigation Bar */}
        <nav className="bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg sticky top-0 z-50">
        <div className="container mx-auto px-2 md:px-4">
          <div className="flex items-center justify-between py-3 md:py-4">
            <div className="flex items-center gap-2 md:gap-3">
              <div className="w-8 h-8 md:w-10 md:h-10 bg-white rounded-lg flex items-center justify-center">
                <span className="text-xl md:text-2xl">🎨</span>
              </div>
              <h1 className="text-lg md:text-2xl font-bold hidden sm:block">Component Showcase</h1>
            </div>
            
            <div className="flex gap-1 md:gap-2 overflow-x-auto">
              <button
                onClick={() => setCurrentPage('analytics')}
                className={`px-2 md:px-4 py-2 rounded-lg font-medium transition-all text-xs md:text-base whitespace-nowrap ${
                  currentPage === 'analytics'
                    ? 'bg-white text-blue-600 shadow-lg'
                    : 'bg-blue-700 hover:bg-blue-800'
                }`}
              >
                <span className="hidden sm:inline">📊 </span>Analytics
              </button>
              <button
                onClick={() => setCurrentPage('dashboard')}
                className={`px-2 md:px-4 py-2 rounded-lg font-medium transition-all text-xs md:text-base whitespace-nowrap ${
                  currentPage === 'dashboard'
                    ? 'bg-white text-blue-600 shadow-lg'
                    : 'bg-blue-700 hover:bg-blue-800'
                }`}
              >
                <span className="hidden sm:inline">📋 </span>Tasks
              </button>
              <button
                onClick={() => setCurrentPage('navbar')}
                className={`px-2 md:px-4 py-2 rounded-lg font-medium transition-all text-xs md:text-base whitespace-nowrap ${
                  currentPage === 'navbar'
                    ? 'bg-white text-blue-600 shadow-lg'
                    : 'bg-blue-700 hover:bg-blue-800'
                }`}
              >
                <span className="hidden sm:inline">🧭 </span>NavBar
              </button>
              <button
                onClick={() => setCurrentPage('products')}
                className={`px-2 md:px-4 py-2 rounded-lg font-medium transition-all text-xs md:text-base whitespace-nowrap ${
                  currentPage === 'products'
                    ? 'bg-white text-blue-600 shadow-lg'
                    : 'bg-blue-700 hover:bg-blue-800'
                }`}
              >
                <span className="hidden sm:inline">🛍️ </span>Products
              </button>
              <button
                onClick={() => setCurrentPage('profile')}
                className={`px-2 md:px-4 py-2 rounded-lg font-medium transition-all text-xs md:text-base whitespace-nowrap ${
                  currentPage === 'profile'
                    ? 'bg-white text-purple-600 shadow-lg'
                    : 'bg-purple-700 hover:bg-purple-800'
                }`}
              >
                <span className="hidden sm:inline">👤 </span>Profiles
              </button>
              <button
                onClick={() => setCurrentPage('register')}
                className={`px-2 md:px-4 py-2 rounded-lg font-medium transition-all text-xs md:text-base whitespace-nowrap ${
                  currentPage === 'register'
                    ? 'bg-white text-green-600 shadow-lg'
                    : 'bg-green-600 hover:bg-green-700'
                }`}
              >
                <span className="hidden sm:inline">📝 </span>Register
              </button>
              <button
                onClick={() => setCurrentPage('team')}
                className={`px-2 md:px-4 py-2 rounded-lg font-medium transition-all text-xs md:text-base whitespace-nowrap ${
                  currentPage === 'team'
                    ? 'bg-white text-indigo-600 shadow-lg'
                    : 'bg-indigo-600 hover:bg-indigo-700'
                }`}
              >
                <span className="hidden sm:inline">👥 </span>Team
              </button>
              <button
                onClick={() => setCurrentPage('kanban')}
                className={`px-2 md:px-4 py-2 rounded-lg font-medium transition-all text-xs md:text-base whitespace-nowrap ${
                  currentPage === 'kanban'
                    ? 'bg-white text-pink-600 shadow-lg'
                    : 'bg-pink-600 hover:bg-pink-700'
                }`}
              >
                <span className="hidden sm:inline">📋 </span>Kanban
              </button>
              <button
                onClick={() => setCurrentPage('social')}
                className={`px-2 md:px-4 py-2 rounded-lg font-medium transition-all text-xs md:text-base whitespace-nowrap ${
                  currentPage === 'social'
                    ? 'bg-white text-teal-600 shadow-lg'
                    : 'bg-teal-600 hover:bg-teal-700'
                }`}
              >
                <span className="hidden sm:inline">💬 </span>Social
              </button>
            </div>
          </div>
        </div>
      </nav>

        {/* Page Content */}
        {currentPage === 'analytics' && <AnalyticsDashboard />}
        {currentPage === 'dashboard' && (
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        )}
        {currentPage === 'navbar' && <NavBarDemo />}
        {currentPage === 'products' && <ProductShowcase />}
        {currentPage === 'profile' && <ProfileDemo />}
        {currentPage === 'register' && <RegistrationForm />}
        {currentPage === 'team' && <TeamDashboardPage />}
        {currentPage === 'kanban' && <KanbanPage />}
        {currentPage === 'social' && <SocialFeedPage />}
      </div>
    </AuthProvider>
  )
}

export default App
