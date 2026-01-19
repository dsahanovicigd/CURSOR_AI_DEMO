import { User } from '../types/user.types'

export const sampleUsers: User[] = [
  {
    id: '1',
    name: 'Sarah Anderson',
    username: 'sarah.codes',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=256&h=256&q=80',
    bio: '✨ Full-stack developer | Tech enthusiast | Coffee lover ☕ | Building amazing things with React & TypeScript | Open source contributor 🚀',
    stats: {
      followers: 12847,
      following: 523,
      posts: 342
    },
    isFollowing: false,
    isOwnProfile: false,
    verified: true,
    location: 'San Francisco, CA',
    website: 'https://sarah-anderson.dev',
    joinedDate: 'March 2020'
  },
  {
    id: '2',
    name: 'Marcus Chen',
    username: 'marcus_tech',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=256&h=256&q=80',
    bio: 'Product Designer × UI/UX Expert | Creating delightful user experiences | Former @Google @Airbnb | Mentor | Design systems enthusiast',
    stats: {
      followers: 8234,
      following: 892,
      posts: 156
    },
    isFollowing: true,
    isOwnProfile: false,
    verified: true,
    location: 'Seattle, WA',
    website: 'https://marcuschen.design',
    joinedDate: 'July 2019'
  },
  {
    id: '3',
    name: 'Emily Rodriguez',
    username: 'emily_creates',
    avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=256&h=256&q=80',
    bio: '🎨 Digital artist & illustrator | NFT creator | Teaching art online | Spreading creativity one pixel at a time',
    stats: {
      followers: 45621,
      following: 234,
      posts: 1289
    },
    isFollowing: false,
    isOwnProfile: false,
    verified: true,
    location: 'Austin, TX',
    website: 'https://emilyrodriguez.art',
    joinedDate: 'January 2018'
  },
  {
    id: '4',
    name: 'Alex Thompson',
    username: 'alex_dev',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=256&h=256&q=80',
    bio: 'Software Engineer | Blockchain enthusiast | Building the future of Web3 | Passionate about decentralization',
    stats: {
      followers: 3421,
      following: 678,
      posts: 89
    },
    isFollowing: false,
    isOwnProfile: false,
    verified: false,
    location: 'Miami, FL',
    website: 'https://alexthompson.io',
    joinedDate: 'September 2021'
  },
  {
    id: '5',
    name: 'Priya Patel',
    username: 'priya.builds',
    avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=256&h=256&q=80',
    bio: 'Mobile App Developer 📱 | iOS & Android | Tech speaker | Founder of @DevTalks | Empowering women in tech 💪',
    stats: {
      followers: 18956,
      following: 445,
      posts: 567
    },
    isFollowing: true,
    isOwnProfile: false,
    verified: true,
    location: 'Boston, MA',
    website: 'https://priyapatel.dev',
    joinedDate: 'May 2019'
  },
  {
    id: '6',
    name: 'James Wilson',
    username: 'jwilson',
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=256&h=256&q=80',
    bio: 'Data Scientist | ML Engineer | AI Researcher | Python enthusiast 🐍 | Sharing insights about machine learning',
    stats: {
      followers: 2156789,
      following: 1234,
      posts: 2341
    },
    isFollowing: true,
    isOwnProfile: false,
    verified: true,
    location: 'London, UK',
    website: 'https://jameswilson.ml',
    joinedDate: 'February 2017'
  },
  {
    id: '7',
    name: 'You',
    username: 'your_username',
    avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=256&h=256&q=80',
    bio: 'This is your profile! 🎉 You can edit your bio, add your interests, and share what makes you unique. The world is waiting to hear your story!',
    stats: {
      followers: 532,
      following: 189,
      posts: 47
    },
    isFollowing: false,
    isOwnProfile: true,
    verified: false,
    location: 'Your City',
    website: 'https://yourwebsite.com',
    joinedDate: 'December 2022'
  },
  {
    id: '8',
    name: 'Luna Martinez',
    username: 'luna_creative',
    avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=256&h=256&q=80',
    bio: 'Content Creator | Photographer 📸 | Travel blogger | Capturing moments around the world 🌍',
    stats: {
      followers: 67823,
      following: 891,
      posts: 1456
    },
    isFollowing: false,
    isOwnProfile: false,
    verified: true,
    location: 'Barcelona, Spain',
    joinedDate: 'April 2019'
  }
]

export const getCurrentUser = () => sampleUsers.find(user => user.isOwnProfile)

export const getVerifiedUsers = () => sampleUsers.filter(user => user.verified)

export const getFollowingUsers = () => sampleUsers.filter(user => user.isFollowing)
