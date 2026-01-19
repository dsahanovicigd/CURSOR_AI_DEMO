interface StarRatingProps {
  rating: number // 0-5, supports decimals
  totalStars?: number
  size?: 'sm' | 'md' | 'lg'
  showNumber?: boolean
  reviewCount?: number
  className?: string
}

const StarRating = ({
  rating,
  totalStars = 5,
  size = 'md',
  showNumber = true,
  reviewCount,
  className = ''
}: StarRatingProps) => {
  const sizeClasses = {
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
    lg: 'w-5 h-5'
  }

  const textSizeClasses = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base'
  }

  // Calculate filled, half-filled, and empty stars
  const fullStars = Math.floor(rating)
  const hasHalfStar = rating % 1 >= 0.5
  const emptyStars = totalStars - fullStars - (hasHalfStar ? 1 : 0)

  const StarIcon = ({ type }: { type: 'full' | 'half' | 'empty' }) => {
    if (type === 'full') {
      return (
        <svg
          className={`${sizeClasses[size]} text-yellow-400 fill-current`}
          viewBox="0 0 20 20"
          aria-hidden="true"
        >
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      )
    }

    if (type === 'half') {
      return (
        <div className={`${sizeClasses[size]} relative`}>
          <svg
            className={`${sizeClasses[size]} text-gray-300 fill-current absolute`}
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
          <svg
            className={`${sizeClasses[size]} text-yellow-400 fill-current absolute`}
            viewBox="0 0 20 20"
            style={{ clipPath: 'inset(0 50% 0 0)' }}
            aria-hidden="true"
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        </div>
      )
    }

    return (
      <svg
        className={`${sizeClasses[size]} text-gray-300 fill-current`}
        viewBox="0 0 20 20"
        aria-hidden="true"
      >
        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
      </svg>
    )
  }

  return (
    <div 
      className={`flex items-center gap-1 ${className}`}
      role="img"
      aria-label={`Rating: ${rating.toFixed(1)} out of ${totalStars} stars${reviewCount ? `, ${reviewCount} reviews` : ''}`}
    >
      {/* Stars */}
      <div className="flex items-center gap-0.5">
        {[...Array(fullStars)].map((_, i) => (
          <StarIcon key={`full-${i}`} type="full" />
        ))}
        {hasHalfStar && <StarIcon type="half" />}
        {[...Array(emptyStars)].map((_, i) => (
          <StarIcon key={`empty-${i}`} type="empty" />
        ))}
      </div>

      {/* Rating number and review count */}
      {showNumber && (
        <span className={`${textSizeClasses[size]} text-gray-700 font-medium`}>
          {rating.toFixed(1)}
        </span>
      )}

      {reviewCount !== undefined && (
        <span className={`${textSizeClasses[size]} text-gray-500`}>
          ({reviewCount.toLocaleString()})
        </span>
      )}
    </div>
  )
}

export default StarRating
