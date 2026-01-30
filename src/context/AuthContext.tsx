import { createContext, useContext, useState, useEffect, ReactNode, useRef } from 'react'
import { authAPI } from '../services/api'
import { setupTokenRefresh } from '../utils/tokenManager'

interface User {
  id: number
  username: string
  email: string
  name?: string
}

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const refreshCleanupRef = useRef<(() => void) | null>(null)

  // Check if user is authenticated on mount
  useEffect(() => {
    checkAuth()
  }, [])

  // Setup automatic token refresh
  useEffect(() => {
    if (authAPI.isAuthenticated()) {
      const cleanup = setupTokenRefresh(async () => {
        try {
          await authAPI.refreshToken()
          // Optionally refresh user info after token refresh
          await checkAuth()
        } catch (error) {
          console.error('Token refresh failed:', error)
          logout()
        }
      })
      refreshCleanupRef.current = cleanup

      return () => {
        if (refreshCleanupRef.current) {
          refreshCleanupRef.current()
        }
      }
    }
  }, [user]) // Re-setup when user changes

  const checkAuth = async () => {
    setIsLoading(true)
    try {
      if (authAPI.isAuthenticated()) {
        // Try to refresh token if access token is expired
        const token = localStorage.getItem('auth_token')
        if (token) {
          try {
            const payload = JSON.parse(atob(token.split('.')[1]))
            const exp = payload.exp * 1000
            // If token expires in less than 5 minutes, refresh it
            if (Date.now() >= exp - 5 * 60 * 1000) {
              try {
                await authAPI.refreshToken()
              } catch (refreshError) {
                console.warn('Token refresh failed:', refreshError)
              }
            }
          } catch (e) {
            // Token invalid, try to refresh
            try {
              await authAPI.refreshToken()
            } catch (refreshError) {
              console.warn('Token refresh failed:', refreshError)
            }
          }
        }

        // Try to get current user info from API
        try {
          const userData = await authAPI.getCurrentUser()
          setUser({
            id: userData.id,
            username: userData.username,
            email: userData.email,
            name: userData.name || userData.first_name || userData.username
          })
        } catch (apiError) {
          // If API call fails, try to decode token
          const currentToken = localStorage.getItem('auth_token')
          if (currentToken) {
            try {
              const payload = JSON.parse(atob(currentToken.split('.')[1]))
              setUser({
                id: payload.sub || payload.user_id || 0,
                username: payload.username || payload.sub || 'user',
                email: payload.email || '',
                name: payload.name || payload.username || 'User'
              })
            } catch (e) {
              // If token decode fails, try refresh or clear
              try {
                await authAPI.refreshToken()
                // Retry getting user after refresh
                const userData = await authAPI.getCurrentUser()
                setUser({
                  id: userData.id,
                  username: userData.username,
                  email: userData.email,
                  name: userData.name || userData.first_name || userData.username
                })
              } catch (refreshError) {
                await authAPI.logout()
                setUser(null)
              }
            }
          } else {
            setUser(null)
          }
        }
      } else {
        setUser(null)
      }
    } catch (error) {
      console.error('Auth check failed:', error)
      setUser(null)
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (username: string, password: string) => {
    try {
      const response = await authAPI.login(username, password)
      
      // Use user info from response if available, otherwise decode token
      if (response.user) {
        setUser({
          id: response.user.id,
          username: response.user.username,
          email: response.user.email,
          name: response.user.name || response.user.first_name || response.user.username
        })
      } else if (response.access_token) {
        try {
          const payload = JSON.parse(atob(response.access_token.split('.')[1]))
          setUser({
            id: payload.sub || payload.user_id || 0,
            username: payload.username || payload.sub || username,
            email: payload.email || '',
            name: payload.name || username
          })
        } catch (e) {
          // Fallback if token decode fails
          setUser({
            id: 0,
            username: username,
            email: '',
            name: username
          })
        }
      }
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }

  const logout = () => {
    // Cleanup token refresh interval immediately
    if (refreshCleanupRef.current) {
      refreshCleanupRef.current()
      refreshCleanupRef.current = null
    }
    
    // Clear user state immediately
    setUser(null)
    
    // Logout (clears tokens instantly, backend call is async)
    authAPI.logout()
  }

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user && authAPI.isAuthenticated(),
    isLoading,
    login,
    logout,
    checkAuth
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
