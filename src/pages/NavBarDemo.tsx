import { useState } from 'react'
import { NavBar } from '../components'
import { sampleMenuItems, sampleUserProfile } from '../data/sampleNavigation'

const NavBarDemo = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  const handleSearch = (query: string) => {
    setSearchQuery(query)
    console.log('Searching for:', query)
  }

  const handleLogin = () => {
    setIsLoggedIn(true)
    console.log('Logged in')
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    console.log('Logged out')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50">
      {/* Navigation Bar */}
      <NavBar
        logoText="Component Showcase"
        menuItems={sampleMenuItems}
        userProfile={isLoggedIn ? sampleUserProfile : undefined}
        onSearch={handleSearch}
        onLogin={handleLogin}
        onLogout={handleLogout}
        showSearch={true}
        sticky={true}
      />

      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            Navigation Bar Component
          </h1>
          <p className="text-xl md:text-2xl text-blue-100 mb-8 max-w-3xl mx-auto">
            A fully responsive, accessible navigation bar with dropdown menus, search, 
            and user profile features
          </p>
          {searchQuery && (
            <div className="inline-block bg-white text-gray-900 px-6 py-3 rounded-lg shadow-lg">
              <p className="text-sm font-medium">
                Search results for: <span className="font-bold text-blue-600">{searchQuery}</span>
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Content Sections */}
      <div className="container mx-auto px-4 py-16 space-y-16">
        {/* Features Grid */}
        <section className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
            ✨ Navigation Bar Features
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-800 text-lg flex items-center gap-2">
                <span className="text-2xl">🎨</span>
                <span>Design Features</span>
              </h3>
              <ul className="space-y-2 text-gray-600 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Sticky navigation on scroll</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Shadow appears when scrolled</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Smooth animations and transitions</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Hover effects on menu items</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Underline animation on hover</span>
                </li>
              </ul>
            </div>
            
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-800 text-lg flex items-center gap-2">
                <span className="text-2xl">📱</span>
                <span>Responsive Design</span>
              </h3>
              <ul className="space-y-2 text-gray-600 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Desktop horizontal menu</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Mobile hamburger menu</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Full-screen mobile overlay</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Prevents body scroll when open</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Auto-close on window resize</span>
                </li>
              </ul>
            </div>
            
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-800 text-lg flex items-center gap-2">
                <span className="text-2xl">🔍</span>
                <span>Search Features</span>
              </h3>
              <ul className="space-y-2 text-gray-600 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Integrated search bar</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Keyboard shortcut (⌘K / Ctrl+K)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Clear button when typing</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Focus state with scale effect</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Search icon and visual feedback</span>
                </li>
              </ul>
            </div>
            
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-800 text-lg flex items-center gap-2">
                <span className="text-2xl">📋</span>
                <span>Menu System</span>
              </h3>
              <ul className="space-y-2 text-gray-600 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Multi-level dropdown menus</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Icons for menu items</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Badge support (New, Sale, etc.)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Hover delay for dropdowns</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Smooth slide-down animation</span>
                </li>
              </ul>
            </div>
            
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-800 text-lg flex items-center gap-2">
                <span className="text-2xl">👤</span>
                <span>User Profile</span>
              </h3>
              <ul className="space-y-2 text-gray-600 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Profile avatar and dropdown</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>User info display</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Profile, Settings, Sign Out</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Click outside to close</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Escape key to close</span>
                </li>
              </ul>
            </div>
            
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-800 text-lg flex items-center gap-2">
                <span className="text-2xl">♿</span>
                <span>Accessibility</span>
              </h3>
              <ul className="space-y-2 text-gray-600 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Semantic HTML navigation</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>ARIA labels and attributes</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Keyboard navigation support</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Focus indicators</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Screen reader friendly</span>
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Interactive Demo Controls */}
        <section className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">
            🎮 Interactive Demo Controls
          </h2>
          
          <div className="max-w-2xl mx-auto space-y-6">
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <h3 className="font-semibold text-gray-800">User Authentication</h3>
                <p className="text-sm text-gray-600">
                  {isLoggedIn ? 'You are logged in' : 'You are logged out'}
                </p>
              </div>
              <button
                onClick={() => setIsLoggedIn(!isLoggedIn)}
                className={`px-6 py-2 rounded-lg font-medium transition-all ${
                  isLoggedIn
                    ? 'bg-red-500 hover:bg-red-600 text-white'
                    : 'bg-blue-600 hover:bg-blue-700 text-white'
                }`}
              >
                {isLoggedIn ? 'Log Out' : 'Log In'}
              </button>
            </div>

            <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
              <h3 className="font-semibold text-blue-900 mb-2">💡 Try These:</h3>
              <ul className="space-y-1 text-sm text-blue-800">
                <li>• Hover over "Products" or "Features" to see dropdown menus</li>
                <li>• Press ⌘K (Mac) or Ctrl+K (Windows) to focus the search bar</li>
                <li>• Click the profile avatar to see the user menu</li>
                <li>• Scroll down to see the sticky navigation in action</li>
                <li>• Resize your browser to see the mobile menu</li>
                <li>• Try the hamburger menu on mobile devices</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Scroll Content */}
        <section className="space-y-8">
          {[1, 2, 3, 4].map((section) => (
            <div key={section} className="bg-white rounded-2xl shadow-xl p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Section {section}: Scroll to See Sticky Navigation
              </h2>
              <p className="text-gray-600 mb-4">
                This is demonstration content to show the sticky navigation behavior. 
                As you scroll down, notice how the navigation bar stays at the top of the page 
                and gains a shadow for better visibility.
              </p>
              <div className="grid md:grid-cols-3 gap-4">
                {[1, 2, 3].map((card) => (
                  <div key={card} className="p-6 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg">
                    <h3 className="font-semibold text-gray-800 mb-2">Feature {card}</h3>
                    <p className="text-sm text-gray-600">
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                      Sed do eiusmod tempor incididunt ut labore.
                    </p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </section>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-gray-600">
            <p className="mb-2">
              Built with React, TypeScript, Vite, and Tailwind CSS
            </p>
            <p className="text-sm text-gray-500">
              Fully responsive navigation with dropdown menus, search, and user profile
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default NavBarDemo
