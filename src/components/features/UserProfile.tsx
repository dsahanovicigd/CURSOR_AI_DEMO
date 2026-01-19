import { UserProfileProps } from '../../types/user.types'
import Avatar from '../common/Avatar'
import ProfileStats from '../common/ProfileStats'
import Button from '../common/Button'

const UserProfile = ({ user, onFollow, onMessage, onEditProfile }: UserProfileProps) => {
  const handleFollow = () => {
    if (onFollow) {
      onFollow()
    }
  }

  const handleMessage = () => {
    if (onMessage) {
      onMessage()
    }
  }

  const handleEditProfile = () => {
    if (onEditProfile) {
      onEditProfile()
    }
  }

  return (
    <div 
      className="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden"
      role="article"
      aria-label={`Profile of ${user.name}`}
    >
      {/* Cover Image / Header Background */}
      <div className="h-32 md:h-48 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500"></div>
      
      {/* Profile Content */}
      <div className="px-4 md:px-8 pb-8">
        {/* Avatar & Action Buttons Row */}
        <div className="flex flex-col md:flex-row md:items-end md:justify-between -mt-16 md:-mt-20 mb-4">
          {/* Avatar */}
          <div className="mb-4 md:mb-0">
            <Avatar
              src={user.avatar}
              alt={`${user.name}'s profile picture`}
              size="2xl"
              verified={user.verified}
            />
          </div>
          
          {/* Action Buttons */}
          <div className="flex gap-2 md:gap-3 flex-wrap">
            {user.isOwnProfile ? (
              <Button
                onClick={handleEditProfile}
                variant="secondary"
                className="flex-1 md:flex-initial"
                aria-label="Edit your profile"
              >
                <span className="flex items-center gap-2">
                  <svg 
                    className="w-4 h-4" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path 
                      strokeLinecap="round" 
                      strokeLinejoin="round" 
                      strokeWidth={2} 
                      d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" 
                    />
                  </svg>
                  Edit Profile
                </span>
              </Button>
            ) : (
              <>
                <Button
                  onClick={handleFollow}
                  variant={user.isFollowing ? "secondary" : "primary"}
                  className="flex-1 md:flex-initial"
                  aria-label={user.isFollowing ? `Unfollow ${user.name}` : `Follow ${user.name}`}
                  aria-pressed={user.isFollowing}
                >
                  <span className="flex items-center gap-2">
                    {user.isFollowing ? (
                      <>
                        <svg 
                          className="w-4 h-4" 
                          fill="currentColor" 
                          viewBox="0 0 20 20"
                          aria-hidden="true"
                        >
                          <path 
                            fillRule="evenodd" 
                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" 
                            clipRule="evenodd" 
                          />
                        </svg>
                        Following
                      </>
                    ) : (
                      <>
                        <svg 
                          className="w-4 h-4" 
                          fill="none" 
                          stroke="currentColor" 
                          viewBox="0 0 24 24"
                          aria-hidden="true"
                        >
                          <path 
                            strokeLinecap="round" 
                            strokeLinejoin="round" 
                            strokeWidth={2} 
                            d="M12 4v16m8-8H4" 
                          />
                        </svg>
                        Follow
                      </>
                    )}
                  </span>
                </Button>
                
                <Button
                  onClick={handleMessage}
                  variant="secondary"
                  className="flex-1 md:flex-initial"
                  aria-label={`Send message to ${user.name}`}
                >
                  <span className="flex items-center gap-2">
                    <svg 
                      className="w-4 h-4" 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                      aria-hidden="true"
                    >
                      <path 
                        strokeLinecap="round" 
                        strokeLinejoin="round" 
                        strokeWidth={2} 
                        d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" 
                      />
                    </svg>
                    Message
                  </span>
                </Button>
              </>
            )}
          </div>
        </div>
        
        {/* User Info */}
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl md:text-3xl font-bold text-gray-900">
              {user.name}
            </h1>
            {user.verified && (
              <span className="sr-only">Verified user</span>
            )}
          </div>
          <p className="text-gray-600 mb-3">@{user.username}</p>
          
          {user.bio && (
            <p className="text-gray-800 text-base md:text-lg leading-relaxed mb-4">
              {user.bio}
            </p>
          )}
          
          {/* Additional Info */}
          <div className="flex flex-wrap gap-4 text-sm text-gray-600">
            {user.location && (
              <div className="flex items-center gap-1">
                <svg 
                  className="w-4 h-4" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" 
                  />
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" 
                  />
                </svg>
                <span>{user.location}</span>
              </div>
            )}
            
            {user.website && (
              <a 
                href={user.website}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1 text-blue-600 hover:underline focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
              >
                <svg 
                  className="w-4 h-4" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" 
                  />
                </svg>
                <span>{user.website.replace(/^https?:\/\//, '')}</span>
              </a>
            )}
            
            {user.joinedDate && (
              <div className="flex items-center gap-1">
                <svg 
                  className="w-4 h-4" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" 
                  />
                </svg>
                <span>Joined {user.joinedDate}</span>
              </div>
            )}
          </div>
        </div>
        
        {/* Stats */}
        <div className="border-t pt-4">
          <ProfileStats stats={user.stats} />
        </div>
      </div>
    </div>
  )
}

export default UserProfile
