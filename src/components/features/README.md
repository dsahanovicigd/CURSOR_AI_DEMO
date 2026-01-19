# UserProfile Component

A comprehensive, accessible user profile component for social media applications.

## Features

### 🎨 Design
- **Responsive Layout**: Adapts beautifully from mobile to desktop
- **Gradient Header**: Eye-catching gradient background
- **Professional Avatar**: Large, circular profile picture with verification badge
- **Clean Typography**: Clear hierarchy with well-structured content
- **Smooth Interactions**: Hover effects and transitions throughout

### ♿ Accessibility
- **Semantic HTML**: Uses proper HTML5 semantic elements
- **ARIA Labels**: Comprehensive ARIA attributes for screen readers
- **Keyboard Navigation**: Full keyboard support with visible focus indicators
- **Color Contrast**: WCAG AA compliant color combinations
- **Screen Reader Friendly**: Descriptive labels and proper roles

### 🔧 Functionality
- **Dynamic Stats**: Followers, following, and posts with smart number formatting
- **Conditional Actions**: Shows different buttons based on profile ownership
- **Follow/Unfollow**: Toggle following status with visual feedback
- **Messaging**: Quick access to message the user
- **Edit Profile**: For viewing your own profile
- **Optional Fields**: Location, website, join date (shown only if provided)
- **Verified Badge**: Visual indicator for verified users

## Usage

### Basic Usage

```tsx
import { UserProfile } from './components'
import { User } from './types/user.types'

const user: User = {
  id: '1',
  name: 'Jane Doe',
  username: 'janedoe',
  avatar: 'https://example.com/avatar.jpg',
  bio: 'Software engineer and open source contributor',
  stats: {
    followers: 1250,
    following: 340,
    posts: 89
  },
  verified: true,
  location: 'New York, NY',
  website: 'https://janedoe.com',
  joinedDate: 'January 2021'
}

function App() {
  const handleFollow = () => {
    console.log('Follow clicked')
  }

  const handleMessage = () => {
    console.log('Message clicked')
  }

  return (
    <UserProfile
      user={user}
      onFollow={handleFollow}
      onMessage={handleMessage}
    />
  )
}
```

### Own Profile View

```tsx
const ownUser: User = {
  // ... user data
  isOwnProfile: true
}

<UserProfile
  user={ownUser}
  onEditProfile={() => console.log('Edit profile')}
/>
```

### Following State

```tsx
const followedUser: User = {
  // ... user data
  isFollowing: true
}

<UserProfile
  user={followedUser}
  onFollow={() => console.log('Unfollow')}
  onMessage={() => console.log('Message')}
/>
```

## Type Definitions

### User Interface

```typescript
interface User {
  id: string                    // Unique user identifier
  name: string                  // Display name
  username: string              // Username/handle
  avatar: string                // Avatar image URL
  bio: string                   // User biography
  stats: UserStats              // User statistics
  isFollowing?: boolean         // Current user is following (optional)
  isOwnProfile?: boolean        // Is this the current user's profile (optional)
  verified?: boolean            // Verified badge (optional)
  location?: string             // User location (optional)
  website?: string              // User website (optional)
  joinedDate?: string           // Member since date (optional)
}
```

### UserStats Interface

```typescript
interface UserStats {
  followers: number   // Number of followers
  following: number   // Number of following
  posts: number       // Number of posts
}
```

### UserProfileProps Interface

```typescript
interface UserProfileProps {
  user: User                     // User data
  onFollow?: () => void          // Follow/unfollow callback
  onMessage?: () => void         // Message callback
  onEditProfile?: () => void     // Edit profile callback
}
```

## Component Structure

The UserProfile component is composed of several sub-components:

### Avatar Component
- Displays circular profile picture
- Shows verification badge if user is verified
- Supports multiple sizes (sm, md, lg, xl, 2xl)
- Accessible with proper alt text

### ProfileStats Component
- Displays follower, following, and post counts
- Formats large numbers (1K, 1M, etc.)
- Interactive buttons for each stat
- Keyboard accessible

## Styling

All styling is done with Tailwind CSS utility classes:

- **Colors**: Blue/purple gradient scheme
- **Shadows**: Layered shadows for depth
- **Borders**: Rounded corners throughout
- **Spacing**: Consistent padding and margins
- **Typography**: Clear hierarchy with bold headings

### Responsive Breakpoints

- **Mobile**: < 768px
  - Stacked layout
  - Full-width buttons
  - Smaller avatar
  
- **Tablet/Desktop**: ≥ 768px
  - Horizontal layout
  - Side-by-side buttons
  - Larger avatar

## Accessibility Features

1. **Semantic HTML**
   - `<article>` for profile container
   - `<nav>` for action buttons
   - Proper heading hierarchy

2. **ARIA Attributes**
   - `aria-label` for descriptive labels
   - `aria-pressed` for toggle buttons
   - `role="img"` for icon indicators

3. **Keyboard Navigation**
   - All interactive elements are focusable
   - Visible focus indicators
   - Logical tab order

4. **Screen Readers**
   - Hidden decorative elements
   - Descriptive button labels
   - Status announcements

## Customization

### Changing Colors

Modify the Tailwind classes in the component:

```tsx
// Gradient header
<div className="h-32 md:h-48 bg-gradient-to-r from-pink-400 via-red-500 to-orange-500">
```

### Custom Button Variants

The component uses the shared Button component which supports:
- `primary`: Blue background
- `secondary`: Gray background
- `danger`: Red background

### Stats Formatting

Number formatting is handled in ProfileStats:
- 1,000+ → "1K"
- 1,000,000+ → "1M"

## Best Practices

1. **Image Optimization**: Use optimized images for avatars (256x256px recommended)
2. **Loading States**: Implement skeleton loaders while fetching user data
3. **Error Handling**: Show error messages if data fails to load
4. **Performance**: Memoize callbacks to prevent unnecessary re-renders
5. **Security**: Validate and sanitize user input (bio, website, etc.)

## Examples

See `App.tsx` for a complete working example with:
- View mode switcher (other user, following, own profile)
- Follow/unfollow functionality
- Dynamic stat updates
- Event handlers

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome)
