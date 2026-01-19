import { UserStats } from '../../types/user.types'

interface ProfileStatsProps {
  stats: UserStats
  className?: string
}

const ProfileStats = ({ stats, className = '' }: ProfileStatsProps) => {
  const formatNumber = (num: number): string => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`
    }
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`
    }
    return num.toString()
  }

  const statItems = [
    { label: 'Posts', value: stats.posts, id: 'posts' },
    { label: 'Followers', value: stats.followers, id: 'followers' },
    { label: 'Following', value: stats.following, id: 'following' }
  ]

  return (
    <div 
      className={`flex justify-around items-center gap-4 ${className}`}
      role="group"
      aria-label="Profile statistics"
    >
      {statItems.map((stat) => (
        <button
          key={stat.id}
          className="flex flex-col items-center hover:bg-gray-50 rounded-lg p-3 transition-colors cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500"
          aria-label={`${formatNumber(stat.value)} ${stat.label}`}
        >
          <span 
            className="text-xl md:text-2xl font-bold text-gray-800"
            aria-hidden="true"
          >
            {formatNumber(stat.value)}
          </span>
          <span 
            className="text-sm text-gray-600"
            aria-hidden="true"
          >
            {stat.label}
          </span>
        </button>
      ))}
    </div>
  )
}

export default ProfileStats
