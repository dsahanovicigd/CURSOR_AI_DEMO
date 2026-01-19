interface AvatarProps {
  src: string
  alt: string
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  className?: string
  verified?: boolean
}

const Avatar = ({ src, alt, size = 'md', className = '', verified = false }: AvatarProps) => {
  const sizeClasses = {
    sm: 'w-10 h-10',
    md: 'w-16 h-16',
    lg: 'w-24 h-24',
    xl: 'w-32 h-32',
    '2xl': 'w-40 h-40'
  }

  return (
    <div className="relative inline-block">
      <img
        src={src}
        alt={alt}
        className={`${sizeClasses[size]} rounded-full object-cover border-4 border-white shadow-lg ${className}`}
        loading="lazy"
      />
      {verified && (
        <div 
          className="absolute bottom-0 right-0 bg-blue-500 rounded-full p-1 border-2 border-white"
          aria-label="Verified user"
          role="img"
        >
          <svg 
            className="w-4 h-4 text-white" 
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
        </div>
      )}
    </div>
  )
}

export default Avatar
