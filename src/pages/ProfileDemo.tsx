import { useState } from 'react'
import { UserProfile } from '../components'
import { User } from '../types/user.types'
import { sampleUsers } from '../data/sampleUsers'

type FilterType = 'all' | 'verified' | 'following' | 'own'

const ProfileDemo = () => {
  const [users, setUsers] = useState<User[]>(sampleUsers)
  const [filter, setFilter] = useState<FilterType>('all')

  const handleFollow = (userId: string) => {
    setUsers(prevUsers =>
      prevUsers.map(user =>
        user.id === userId
          ? {
              ...user,
              isFollowing: !user.isFollowing,
              stats: {
                ...user.stats,
                followers: user.isFollowing
                  ? user.stats.followers - 1
                  : user.stats.followers + 1
              }
            }
          : user
      )
    )
  }

  const handleMessage = (user: User) => {
    alert(`Opening chat with ${user.name}...`)
  }

  const handleEditProfile = () => {
    alert('Opening profile editor...')
  }

  const filteredUsers = users.filter(user => {
    switch (filter) {
      case 'verified':
        return user.verified
      case 'following':
        return user.isFollowing
      case 'own':
        return user.isOwnProfile
      default:
        return true
    }
  })

  const filterButtons: { type: FilterType; label: string; icon: string }[] = [
    { type: 'all', label: 'All Profiles', icon: '👥' },
    { type: 'verified', label: 'Verified', icon: '✅' },
    { type: 'following', label: 'Following', icon: '💙' },
    { type: 'own', label: 'My Profile', icon: '👤' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Hero Section */}
      <div className="bg-white shadow-md border-b border-gray-200">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              User Profile Component Demo
            </h1>
            <p className="text-lg text-gray-600 mb-6">
              Explore different user profiles showcasing various features, states, and configurations.
            </p>
            
            {/* Filter Buttons */}
            <div className="flex flex-wrap justify-center gap-3">
              {filterButtons.map(({ type, label, icon }) => (
                <button
                  key={type}
                  onClick={() => setFilter(type)}
                  className={`px-6 py-3 rounded-xl font-medium transition-all duration-200 ${
                    filter === type
                      ? 'bg-blue-600 text-white shadow-lg scale-105'
                      : 'bg-white text-gray-700 border-2 border-gray-200 hover:border-blue-300 hover:shadow-md'
                  }`}
                  aria-pressed={filter === type}
                >
                  <span className="flex items-center gap-2">
                    <span>{icon}</span>
                    <span>{label}</span>
                    {filter === type && (
                      <span className="bg-white text-blue-600 rounded-full px-2 py-0.5 text-sm font-bold">
                        {filteredUsers.length}
                      </span>
                    )}
                  </span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Profiles Grid */}
      <main className="container mx-auto px-4 py-12">
        <div className="space-y-8">
          {filteredUsers.map((user) => (
            <div
              key={user.id}
              className="transform transition-all duration-300 hover:scale-[1.02]"
            >
              <UserProfile
                user={user}
                onFollow={() => handleFollow(user.id)}
                onMessage={() => handleMessage(user)}
                onEditProfile={handleEditProfile}
              />
            </div>
          ))}

          {filteredUsers.length === 0 && (
            <div className="text-center py-16">
              <div className="text-6xl mb-4">🔍</div>
              <h3 className="text-2xl font-semibold text-gray-700 mb-2">
                No profiles found
              </h3>
              <p className="text-gray-500">
                Try selecting a different filter
              </p>
            </div>
          )}
        </div>

        {/* Stats Summary */}
        <div className="mt-16 max-w-4xl mx-auto">
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
              📊 Demo Statistics
            </h2>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-4 text-center">
                <div className="text-3xl font-bold text-blue-600">
                  {users.length}
                </div>
                <div className="text-sm text-blue-800 mt-1">Total Users</div>
              </div>
              
              <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-4 text-center">
                <div className="text-3xl font-bold text-green-600">
                  {users.filter(u => u.verified).length}
                </div>
                <div className="text-sm text-green-800 mt-1">Verified</div>
              </div>
              
              <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-4 text-center">
                <div className="text-3xl font-bold text-purple-600">
                  {users.filter(u => u.isFollowing).length}
                </div>
                <div className="text-sm text-purple-800 mt-1">Following</div>
              </div>
              
              <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl p-4 text-center">
                <div className="text-3xl font-bold text-orange-600">
                  {users.reduce((sum, u) => sum + u.stats.followers, 0).toLocaleString()}
                </div>
                <div className="text-sm text-orange-800 mt-1">Total Followers</div>
              </div>
            </div>
          </div>
        </div>

        {/* Component Features */}
        <div className="mt-12 max-w-4xl mx-auto bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            ✨ Component Features Demonstrated
          </h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span className="text-2xl">🎨</span>
                <span>Visual Features</span>
              </h3>
              <ul className="space-y-2 text-gray-600">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Gradient header backgrounds</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Verified badges for authenticated users</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Responsive design (mobile, tablet, desktop)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Smooth hover effects and transitions</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Large number formatting (K, M notation)</span>
                </li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span className="text-2xl">⚡</span>
                <span>Interactive Features</span>
              </h3>
              <ul className="space-y-2 text-gray-600">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Follow/Unfollow with live counter updates</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Message functionality</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Edit profile for own profile view</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Clickable stats for navigation</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Optional profile fields display</span>
                </li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span className="text-2xl">♿</span>
                <span>Accessibility</span>
              </h3>
              <ul className="space-y-2 text-gray-600">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Semantic HTML structure</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>ARIA labels and roles</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Keyboard navigation support</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Screen reader friendly</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Focus indicators on interactive elements</span>
                </li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span className="text-2xl">🔧</span>
                <span>Technical</span>
              </h3>
              <ul className="space-y-2 text-gray-600">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Full TypeScript support</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Type-safe props and interfaces</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Modular component architecture</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>Tailwind CSS utility classes</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>No linter errors or warnings</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto text-center text-gray-600">
            <p className="mb-2">
              Built with React, TypeScript, Vite, and Tailwind CSS
            </p>
            <p className="text-sm text-gray-500">
              Try interacting with the profiles: follow/unfollow, filter by category, and explore different states!
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default ProfileDemo
