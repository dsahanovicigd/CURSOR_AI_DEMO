export interface User {
  id: string
  name: string
  username: string
  avatar: string
  verified?: boolean
}

export interface Comment {
  id: string
  user: User
  content: string
  timestamp: string
  likes: number
  replies?: Comment[]
}

export interface Post {
  id: string
  user: User
  content: string
  image?: string
  timestamp: string
  likes: number
  comments: Comment[]
  shares: number
  isLiked?: boolean
  isBookmarked?: boolean
}

export interface PostCardProps {
  post: Post
  onLike?: (postId: string) => void
  onComment?: (postId: string, comment: string) => void
  onShare?: (postId: string) => void
  onBookmark?: (postId: string) => void
}

export interface CreatePostProps {
  onPost: (content: string, image?: File) => void
  currentUser: User
}
