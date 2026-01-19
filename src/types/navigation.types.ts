export interface NavItem {
  id: string
  label: string
  href: string
  icon?: string
  badge?: string
  children?: NavItem[]
}

export interface UserProfile {
  name: string
  email: string
  avatar: string
  role?: string
}

export interface NavBarProps {
  logo?: string
  logoText?: string
  menuItems: NavItem[]
  userProfile?: UserProfile
  onSearch?: (query: string) => void
  onLogin?: () => void
  onLogout?: () => void
  showSearch?: boolean
  sticky?: boolean
  transparent?: boolean
}
