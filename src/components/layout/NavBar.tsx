import { useState, useEffect, useRef } from 'react'
import { NavBarProps } from '../../types/navigation.types'
import SearchBar from './SearchBar'
import UserProfileDropdown from './UserProfileDropdown'
import Button from '../common/Button'

const NavBar = ({
  logo,
  logoText = 'Brand',
  menuItems,
  userProfile,
  onSearch,
  onLogin,
  onLogout,
  showSearch = true,
  sticky = true,
  transparent = false
}: NavBarProps) => {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null)
  const dropdownTimeoutRef = useRef<NodeJS.Timeout>()

  // Handle scroll for sticky behavior
  useEffect(() => {
    if (!sticky) return

    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [sticky])

  // Close mobile menu on window resize
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768 && isMobileMenuOpen) {
        setIsMobileMenuOpen(false)
      }
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [isMobileMenuOpen])

  // Prevent body scroll when mobile menu is open
  useEffect(() => {
    if (isMobileMenuOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }

    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isMobileMenuOpen])

  const handleDropdownEnter = (itemId: string) => {
    if (dropdownTimeoutRef.current) {
      clearTimeout(dropdownTimeoutRef.current)
    }
    setActiveDropdown(itemId)
  }

  const handleDropdownLeave = () => {
    dropdownTimeoutRef.current = setTimeout(() => {
      setActiveDropdown(null)
    }, 200)
  }

  const handleSearch = (query: string) => {
    if (onSearch) {
      onSearch(query)
      console.log('Searching for:', query)
    }
  }

  const navClasses = `
    ${sticky ? 'sticky top-0' : 'relative'}
    z-50 transition-all duration-300
    ${isScrolled || !transparent
      ? 'bg-white shadow-md'
      : 'bg-transparent'
    }
  `

  return (
    <nav className={navClasses} role="navigation" aria-label="Main navigation">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-3 flex-shrink-0">
            {logo ? (
              <img src={logo} alt={logoText} className="h-8 w-auto" />
            ) : (
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-xl">🎨</span>
                </div>
                <span className="text-xl font-bold text-gray-900">{logoText}</span>
              </div>
            )}
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-6 flex-1 justify-center">
            {menuItems.map((item) => (
              <div
                key={item.id}
                className="relative"
                onMouseEnter={() => item.children && handleDropdownEnter(item.id)}
                onMouseLeave={() => item.children && handleDropdownLeave()}
              >
                <a
                  href={item.href}
                  className="flex items-center gap-1 px-3 py-2 text-gray-700 hover:text-blue-600 font-medium transition-colors relative group"
                  aria-haspopup={item.children ? 'true' : 'false'}
                  aria-expanded={activeDropdown === item.id}
                >
                  {item.icon && <span>{item.icon}</span>}
                  <span>{item.label}</span>
                  {item.badge && (
                    <span className="ml-1 px-1.5 py-0.5 text-xs font-bold bg-red-500 text-white rounded-full">
                      {item.badge}
                    </span>
                  )}
                  {item.children && (
                    <svg
                      className={`w-4 h-4 transition-transform duration-200 ${
                        activeDropdown === item.id ? 'rotate-180' : 'rotate-0'
                      }`}
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  )}
                  <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-blue-600 transition-all duration-300 group-hover:w-full" />
                </a>

                {/* Dropdown Menu */}
                {item.children && activeDropdown === item.id && (
                  <div className="absolute top-full left-0 mt-2 w-56 bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden animate-slideDown">
                    {item.children.map((child) => (
                      <a
                        key={child.id}
                        href={child.href}
                        className="flex items-center gap-2 px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                      >
                        {child.icon && <span>{child.icon}</span>}
                        <span>{child.label}</span>
                        {child.badge && (
                          <span className="ml-auto px-2 py-0.5 text-xs font-bold bg-blue-100 text-blue-700 rounded-full">
                            {child.badge}
                          </span>
                        )}
                      </a>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Search and Actions */}
          <div className="hidden md:flex items-center gap-3">
            {showSearch && (
              <div className="w-64">
                <SearchBar onSearch={handleSearch} placeholder="Search..." />
              </div>
            )}

            {userProfile ? (
              <UserProfileDropdown
                user={userProfile}
                onLogout={onLogout}
                onProfile={() => console.log('View profile')}
                onSettings={() => console.log('Settings')}
              />
            ) : (
              <Button onClick={onLogin} variant="primary">
                Sign In
              </Button>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
            aria-label="Toggle mobile menu"
            aria-expanded={isMobileMenuOpen}
          >
            <svg
              className="w-6 h-6 text-gray-700"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {isMobileMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden animate-fadeIn"
            onClick={() => setIsMobileMenuOpen(false)}
            aria-hidden="true"
          />

          {/* Mobile Menu Panel */}
          <div className="fixed top-16 left-0 right-0 bottom-0 bg-white z-50 md:hidden overflow-y-auto animate-slideInRight">
            <div className="p-4 space-y-4">
              {/* Mobile Search */}
              {showSearch && (
                <div className="pb-4 border-b border-gray-200">
                  <SearchBar onSearch={handleSearch} placeholder="Search..." />
                </div>
              )}

              {/* User Profile Mobile */}
              {userProfile && (
                <div className="pb-4 border-b border-gray-200">
                  <div className="flex items-center gap-3 p-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
                    <img
                      src={userProfile.avatar}
                      alt={userProfile.name}
                      className="w-12 h-12 rounded-full object-cover border-2 border-white shadow-md"
                    />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-semibold text-gray-900 truncate">
                        {userProfile.name}
                      </p>
                      <p className="text-xs text-gray-600 truncate">
                        {userProfile.email}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Mobile Menu Items */}
              <div className="space-y-1">
                {menuItems.map((item) => (
                  <div key={item.id}>
                    <a
                      href={item.href}
                      className="flex items-center justify-between px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors font-medium"
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      <span className="flex items-center gap-2">
                        {item.icon && <span>{item.icon}</span>}
                        <span>{item.label}</span>
                      </span>
                      {item.badge && (
                        <span className="px-2 py-0.5 text-xs font-bold bg-red-500 text-white rounded-full">
                          {item.badge}
                        </span>
                      )}
                    </a>

                    {/* Mobile Submenu */}
                    {item.children && (
                      <div className="ml-8 mt-1 space-y-1">
                        {item.children.map((child) => (
                          <a
                            key={child.id}
                            href={child.href}
                            className="flex items-center gap-2 px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded-lg transition-colors"
                            onClick={() => setIsMobileMenuOpen(false)}
                          >
                            {child.icon && <span>{child.icon}</span>}
                            <span>{child.label}</span>
                            {child.badge && (
                              <span className="ml-auto px-2 py-0.5 text-xs font-bold bg-blue-100 text-blue-700 rounded-full">
                                {child.badge}
                              </span>
                            )}
                          </a>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Mobile Actions */}
              {userProfile ? (
                <div className="pt-4 border-t border-gray-200 space-y-2">
                  <button
                    onClick={() => {
                      console.log('View profile')
                      setIsMobileMenuOpen(false)
                    }}
                    className="w-full flex items-center gap-3 px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
                  >
                    <span>👤</span>
                    <span>Your Profile</span>
                  </button>
                  <button
                    onClick={() => {
                      console.log('Settings')
                      setIsMobileMenuOpen(false)
                    }}
                    className="w-full flex items-center gap-3 px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
                  >
                    <span>⚙️</span>
                    <span>Settings</span>
                  </button>
                  <button
                    onClick={() => {
                      onLogout?.()
                      setIsMobileMenuOpen(false)
                    }}
                    className="w-full flex items-center gap-3 px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    <span>🚪</span>
                    <span>Sign Out</span>
                  </button>
                </div>
              ) : (
                <div className="pt-4 border-t border-gray-200">
                  <Button
                    onClick={() => {
                      onLogin?.()
                      setIsMobileMenuOpen(false)
                    }}
                    variant="primary"
                    className="w-full"
                  >
                    Sign In
                  </Button>
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </nav>
  )
}

export default NavBar
