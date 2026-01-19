import { NavItem, UserProfile } from '../types/navigation.types'

export const sampleMenuItems: NavItem[] = [
  {
    id: 'home',
    label: 'Home',
    href: '#home',
    icon: '🏠'
  },
  {
    id: 'products',
    label: 'Products',
    href: '#products',
    icon: '🛍️',
    badge: 'New',
    children: [
      {
        id: 'electronics',
        label: 'Electronics',
        href: '#electronics',
        icon: '📱'
      },
      {
        id: 'clothing',
        label: 'Clothing',
        href: '#clothing',
        icon: '👕'
      },
      {
        id: 'accessories',
        label: 'Accessories',
        href: '#accessories',
        icon: '⌚'
      },
      {
        id: 'sale',
        label: 'Sale',
        href: '#sale',
        icon: '🏷️',
        badge: '50%'
      }
    ]
  },
  {
    id: 'features',
    label: 'Features',
    href: '#features',
    icon: '✨',
    children: [
      {
        id: 'components',
        label: 'Components',
        href: '#components',
        icon: '🧩'
      },
      {
        id: 'templates',
        label: 'Templates',
        href: '#templates',
        icon: '📄'
      },
      {
        id: 'integrations',
        label: 'Integrations',
        href: '#integrations',
        icon: '🔗'
      }
    ]
  },
  {
    id: 'docs',
    label: 'Documentation',
    href: '#docs',
    icon: '📚'
  },
  {
    id: 'pricing',
    label: 'Pricing',
    href: '#pricing',
    icon: '💰'
  },
  {
    id: 'about',
    label: 'About',
    href: '#about',
    icon: 'ℹ️'
  }
]

export const sampleUserProfile: UserProfile = {
  name: 'Alex Johnson',
  email: 'alex.johnson@example.com',
  avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80',
  role: 'Premium'
}

export const sampleUserProfile2: UserProfile = {
  name: 'Sarah Chen',
  email: 'sarah.chen@example.com',
  avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80',
  role: 'Admin'
}
