interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

interface NavItem {
  id: string
  label: string
  icon: string
  href: string
  badge?: number
}

const Sidebar = ({ isOpen, onClose }: SidebarProps) => {
  const navItems: NavItem[] = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊', href: '#dashboard' },
    { id: 'tasks', label: 'My Tasks', icon: '✓', href: '#tasks', badge: 12 },
    { id: 'projects', label: 'Projects', icon: '📁', href: '#projects', badge: 3 },
    { id: 'calendar', label: 'Calendar', icon: '📅', href: '#calendar' },
    { id: 'team', label: 'Team', icon: '👥', href: '#team' },
    { id: 'reports', label: 'Reports', icon: '📈', href: '#reports' },
    { id: 'settings', label: 'Settings', icon: '⚙️', href: '#settings' }
  ]

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:static inset-y-0 left-0 z-50
          w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700
          transform transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
          flex flex-col
        `}
        role="navigation"
        aria-label="Sidebar navigation"
      >
        {/* Sidebar Header */}
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">T</span>
              </div>
              <div>
                <h2 className="text-lg font-bold text-gray-900 dark:text-white">
                  TaskFlow
                </h2>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Manage your work
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="lg:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              aria-label="Close sidebar"
            >
              <svg className="w-5 h-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 p-4 overflow-y-auto">
          <div className="space-y-1">
            {navItems.map((item, index) => (
              <a
                key={item.id}
                href={item.href}
                className={`
                  flex items-center justify-between px-4 py-3 rounded-lg
                  text-gray-700 dark:text-gray-300
                  hover:bg-gray-100 dark:hover:bg-gray-800
                  transition-colors group
                  ${index === 0 ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400' : ''}
                `}
                onClick={onClose}
              >
                <div className="flex items-center gap-3">
                  <span className="text-xl">{item.icon}</span>
                  <span className="font-medium">{item.label}</span>
                </div>
                {item.badge !== undefined && (
                  <span className="px-2 py-1 text-xs font-bold bg-blue-600 text-white rounded-full">
                    {item.badge}
                  </span>
                )}
              </a>
            ))}
          </div>

          {/* Quick Actions */}
          <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
            <h3 className="px-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">
              Quick Actions
            </h3>
            <button
              className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-lg
                bg-gradient-to-r from-blue-600 to-purple-600 text-white
                hover:from-blue-700 hover:to-purple-700 transition-all shadow-md"
            >
              <span className="text-xl">➕</span>
              <span className="font-medium">New Task</span>
            </button>
          </div>
        </nav>

        {/* Sidebar Footer */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <div className="p-4 bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg">
            <p className="text-sm font-semibold text-gray-900 dark:text-white mb-1">
              Pro Plan
            </p>
            <p className="text-xs text-gray-600 dark:text-gray-400 mb-3">
              23 days remaining
            </p>
            <button className="w-full px-3 py-2 text-xs font-medium bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all">
              Upgrade Now
            </button>
          </div>
        </div>
      </aside>
    </>
  )
}

export default Sidebar
