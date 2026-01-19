import { Post, User } from '../types/social'

export const currentUser: User = {
  id: 'current-user',
  name: 'John Doe',
  username: 'johndoe',
  avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80',
  verified: true
}

export const samplePosts: Post[] = [
  {
    id: '1',
    user: {
      id: '1',
      name: 'Sarah Chen',
      username: 'sarahchen',
      avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80',
      verified: true
    },
    content: 'Just finished building an amazing dashboard with React and Tailwind CSS! 🚀✨\n\nThe combination of TypeScript for type safety and Tailwind for styling makes development so much faster. Can\'t wait to share it with the team!',
    image: 'https://images.unsplash.com/photo-1551650975-87deedd944c3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
    timestamp: '2 hours ago',
    likes: 156,
    shares: 23,
    isLiked: false,
    isBookmarked: false,
    comments: [
      {
        id: 'c1',
        user: {
          id: '2',
          name: 'Alex Johnson',
          username: 'alexj',
          avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
        },
        content: 'This looks incredible! Would love to see a tutorial on this 👏',
        timestamp: '1 hour ago',
        likes: 12
      },
      {
        id: 'c2',
        user: {
          id: '3',
          name: 'Emma Wilson',
          username: 'emmaw',
          avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
        },
        content: 'Great work! The color scheme is perfect 🎨',
        timestamp: '45 minutes ago',
        likes: 8
      }
    ]
  },
  {
    id: '2',
    user: {
      id: '4',
      name: 'Michael Brown',
      username: 'mikeb',
      avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80',
      verified: false
    },
    content: '💡 Pro tip for developers:\n\nAlways write tests before refactoring. It saves so much time and prevents bugs from creeping in!\n\n#coding #bestpractices',
    timestamp: '5 hours ago',
    likes: 89,
    shares: 34,
    isLiked: true,
    isBookmarked: false,
    comments: [
      {
        id: 'c3',
        user: {
          id: '5',
          name: 'Lisa Anderson',
          username: 'lisaa',
          avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
        },
        content: 'Absolutely! TDD has changed my development workflow completely',
        timestamp: '3 hours ago',
        likes: 5
      }
    ]
  },
  {
    id: '3',
    user: {
      id: '6',
      name: 'David Lee',
      username: 'davidlee',
      avatar: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80',
      verified: true
    },
    content: 'Excited to announce that our team just launched the new feature! 🎉\n\nThank you to everyone who provided feedback during the beta. Your input was invaluable!',
    image: 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
    timestamp: '1 day ago',
    likes: 342,
    shares: 67,
    isLiked: false,
    isBookmarked: true,
    comments: [
      {
        id: 'c4',
        user: {
          id: '7',
          name: 'Rachel Green',
          username: 'rachelg',
          avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
        },
        content: 'Congratulations! Can\'t wait to try it out 🚀',
        timestamp: '20 hours ago',
        likes: 15
      },
      {
        id: 'c5',
        user: {
          id: '8',
          name: 'Tom Harris',
          username: 'tomh',
          avatar: 'https://images.unsplash.com/photo-1519345182560-3f2917c472ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
        },
        content: 'Amazing work team! This is going to be huge 💪',
        timestamp: '18 hours ago',
        likes: 9
      }
    ]
  },
  {
    id: '4',
    user: {
      id: '9',
      name: 'Jessica Martinez',
      username: 'jessicam',
      avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80',
      verified: true
    },
    content: 'Morning coffee and code ☕️💻\n\nStarting the day with some clean architecture refactoring. There\'s something satisfying about organizing code properly!',
    image: 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
    timestamp: '2 days ago',
    likes: 198,
    shares: 12,
    isLiked: false,
    isBookmarked: false,
    comments: []
  }
]

// Simulate loading more posts
export const generateMorePosts = (page: number): Post[] => {
  const basePosts: Post[] = [
    {
      id: `gen-${page}-1`,
      user: {
        id: 'user-gen-1',
        name: 'Chris Wilson',
        username: 'chrisw',
        avatar: 'https://images.unsplash.com/photo-1527980965255-d3b416303d12?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80',
        verified: false
      },
      content: `Just discovered this amazing feature in TypeScript! 🤯\n\nPage ${page} content here...`,
      timestamp: `${page * 2} days ago`,
      likes: Math.floor(Math.random() * 200),
      shares: Math.floor(Math.random() * 50),
      isLiked: false,
      isBookmarked: false,
      comments: []
    },
    {
      id: `gen-${page}-2`,
      user: {
        id: 'user-gen-2',
        name: 'Nina Patel',
        username: 'ninap',
        avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80',
        verified: true
      },
      content: `Working on an exciting new project! Stay tuned for updates 🚀`,
      image: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
      timestamp: `${page * 2 + 1} days ago`,
      likes: Math.floor(Math.random() * 300),
      shares: Math.floor(Math.random() * 40),
      isLiked: false,
      isBookmarked: false,
      comments: [
        {
          id: `gen-c-${page}`,
          user: {
            id: 'user-gen-3',
            name: 'Mike Johnson',
            username: 'mikej',
            avatar: 'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
          },
          content: 'Looks great! Can\'t wait to see the final result 👍',
          timestamp: `${page * 2} days ago`,
          likes: Math.floor(Math.random() * 20)
        }
      ]
    }
  ]

  return basePosts
}
