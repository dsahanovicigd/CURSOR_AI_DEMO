import { useState, useEffect, useRef, useCallback } from 'react'
import { Post, User } from '../../types/social'
import PostCard from './PostCard'
import CreatePost from './CreatePost'

interface SocialFeedProps {
  currentUser: User
  initialPosts?: Post[]
  onLoadMore?: () => Promise<Post[]>
}

const SocialFeed = ({ currentUser, initialPosts = [], onLoadMore }: SocialFeedProps) => {
  const [posts, setPosts] = useState<Post[]>(initialPosts)
  const [isLoading, setIsLoading] = useState(false)
  const [hasMore, setHasMore] = useState(true)
  const observerTarget = useRef<HTMLDivElement>(null)

  // Infinite scroll observer
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !isLoading) {
          loadMorePosts()
        }
      },
      { threshold: 0.5 }
    )

    if (observerTarget.current) {
      observer.observe(observerTarget.current)
    }

    return () => observer.disconnect()
  }, [hasMore, isLoading, loadMorePosts])

  const loadMorePosts = useCallback(async () => {
    if (onLoadMore && !isLoading) {
      setIsLoading(true)
      try {
        const newPosts = await onLoadMore()
        if (newPosts.length === 0) {
          setHasMore(false)
        } else {
          setPosts((prev) => [...prev, ...newPosts])
        }
      } catch (error) {
        console.error('Failed to load more posts:', error)
      } finally {
        setIsLoading(false)
      }
    }
  }, [onLoadMore, isLoading])

  const handleCreatePost = (content: string, image?: File) => {
    const newPost: Post = {
      id: Date.now().toString(),
      user: currentUser,
      content,
      image: image ? URL.createObjectURL(image) : undefined,
      timestamp: 'Just now',
      likes: 0,
      comments: [],
      shares: 0,
      isLiked: false,
      isBookmarked: false,
    }
    setPosts([newPost, ...posts])
  }

  const handleLike = (postId: string) => {
    setPosts(posts.map(post =>
      post.id === postId
        ? { ...post, isLiked: !post.isLiked, likes: post.isLiked ? post.likes - 1 : post.likes + 1 }
        : post
    ))
  }

  const handleComment = (postId: string, commentText: string) => {
    setPosts(posts.map(post =>
      post.id === postId
        ? {
            ...post,
            comments: [
              ...post.comments,
              {
                id: Date.now().toString(),
                user: currentUser,
                content: commentText,
                timestamp: 'Just now',
                likes: 0,
              }
            ]
          }
        : post
    ))
  }

  const handleShare = (postId: string) => {
    setPosts(posts.map(post =>
      post.id === postId
        ? { ...post, shares: post.shares + 1 }
        : post
    ))
    // Show success notification
    console.log('Post shared:', postId)
  }

  const handleBookmark = (postId: string) => {
    setPosts(posts.map(post =>
      post.id === postId
        ? { ...post, isBookmarked: !post.isBookmarked }
        : post
    ))
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Create Post */}
      <CreatePost
        currentUser={currentUser}
        onPost={handleCreatePost}
      />

      {/* Posts Feed */}
      <div className="space-y-6">
        {posts.map((post) => (
          <PostCard
            key={post.id}
            post={post}
            onLike={handleLike}
            onComment={handleComment}
            onShare={handleShare}
            onBookmark={handleBookmark}
          />
        ))}
      </div>

      {/* Loading Indicator / Infinite Scroll Trigger */}
      <div ref={observerTarget} className="py-8">
        {isLoading && (
          <div className="flex flex-col items-center justify-center">
            <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Loading more posts...</p>
          </div>
        )}
        {!hasMore && posts.length > 0 && (
          <div className="text-center">
            <p className="text-sm text-gray-500 dark:text-gray-400">
              You've reached the end! 🎉
            </p>
          </div>
        )}
        {posts.length === 0 && !isLoading && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📝</div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
              No posts yet
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Be the first to share something!
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default SocialFeed
