export interface User {
  id: string
  name: string
  username: string
  avatar: string
  bio: string
  stats: UserStats
  isFollowing?: boolean
  isOwnProfile?: boolean
  verified?: boolean
  location?: string
  website?: string
  joinedDate?: string
}

export interface UserStats {
  followers: number
  following: number
  posts: number
}

export interface UserProfileProps {
  user: User
  onFollow?: () => void
  onMessage?: () => void
  onEditProfile?: () => void
}
