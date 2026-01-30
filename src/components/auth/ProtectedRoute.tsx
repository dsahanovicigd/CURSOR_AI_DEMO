import { ReactNode } from 'react'
import { useAuth } from '../../context/AuthContext'
import LoginForm from './LoginForm'

interface ProtectedRouteProps {
  children: ReactNode
  fallback?: ReactNode
}

const ProtectedRoute = ({ children, fallback }: ProtectedRouteProps) => {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900 p-4">
        {fallback || <LoginForm />}
      </div>
    )
  }

  return <>{children}</>
}

export default ProtectedRoute
