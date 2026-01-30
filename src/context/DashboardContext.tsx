import { createContext, useContext, ReactNode } from 'react'

interface DashboardContextType {
  isDarkMode: boolean
  toggleDarkMode: () => void
  user: {
    id: string
    name: string
    email: string
    avatar: string
  } | null
}

const DashboardContext = createContext<DashboardContextType | undefined>(undefined)

// eslint-disable-next-line react-refresh/only-export-components
export const useDashboardContext = () => {
  const context = useContext(DashboardContext)
  if (!context) {
    throw new Error('useDashboardContext must be used within DashboardProvider')
  }
  return context
}

interface DashboardProviderProps {
  children: ReactNode
  value: DashboardContextType
}

export const DashboardProvider = ({ children, value }: DashboardProviderProps) => {
  return (
    <DashboardContext.Provider value={value}>
      {children}
    </DashboardContext.Provider>
  )
}

export default DashboardContext
