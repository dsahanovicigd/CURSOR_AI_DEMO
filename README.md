# React + TypeScript + Vite + Tailwind CSS Project

A modern, comprehensive React application showcasing enterprise-level components and features built with TypeScript, Vite, and Tailwind CSS.

## 🚀 Features

- ⚡️ **Vite** - Lightning fast development server and build tool
- ⚛️ **React 18** - Latest version of React with TypeScript
- 🎨 **Tailwind CSS** - Utility-first CSS framework with dark mode
- 📦 **Component Library** - Extensive collection of reusable components
- 🔍 **ESLint** - Code linting configured
- 🎯 **TypeScript** - Full type safety across the application
- 🌙 **Dark Mode** - Complete dark mode support with persistence
- 📱 **Responsive Design** - Mobile-first responsive layouts
- ♿ **Accessibility** - WCAG 2.0 AA compliant components
- 🧪 **E2E Testing** - Comprehensive Playwright test suite

## 🎨 Application Pages

### 👤 **Profile Demo**
Social media-style user profiles with stats, badges, and actions
- User avatars with verification badges
- Follower/following statistics
- Bio and location information
- Action buttons (Follow, Message, Edit)

### 🛍️ **Product Showcase**
E-commerce product cards with advanced features
- Product images with hover effects
- Star ratings and reviews
- Price display with discounts
- Wishlist functionality
- Add to cart interactions

### 🧭 **Navigation Bar**
Responsive navigation with modern features
- Multi-level dropdown menus
- Search bar with keyboard shortcuts
- User profile dropdown
- Mobile hamburger menu
- Sticky header on scroll

### 📊 **Dashboard**
Task management dashboard
- Task cards with progress tracking
- Status-based organization
- Statistics widgets
- Sidebar navigation
- Team member assignments

### 📈 **Analytics Dashboard**
Data visualization and analytics
- KPI cards with trends
- Interactive charts (line, bar, pie, donut)
- Sortable data tables
- Filter controls
- Date range selectors
- Export functionality

### 📝 **Registration Form**
Multi-step registration with validation
- Step-by-step form wizard
- Field validation
- Password strength meter
- Terms acceptance
- Success confirmation

### 👥 **Team Collaboration Dashboard** ⭐ NEW!
Complete team management and project tracking
- Project overview with key metrics
- Team member avatars with tooltips
- Interactive task progress charts
- Real-time activity feed
- Priority breakdown visualization
- Team performance metrics
- Upcoming deadlines tracker
- Workload distribution analysis
- Quick action buttons
- Fully responsive with dark mode

## 📁 Project Structure

```
src/
├── components/
│   ├── common/          # Reusable UI components
│   │   ├── Avatar.tsx
│   │   ├── Button.tsx
│   │   ├── StarRating.tsx
│   │   └── ProfileStats.tsx
│   ├── layout/          # Layout components
│   │   ├── Card.tsx
│   │   ├── Header.tsx
│   │   ├── NavBar.tsx
│   │   ├── SearchBar.tsx
│   │   └── UserProfileDropdown.tsx
│   ├── features/        # Feature-specific components
│   │   ├── UserProfile.tsx
│   │   └── ProductCard.tsx
│   ├── dashboard/       # Dashboard components
│   │   ├── Sidebar.tsx
│   │   ├── DashboardHeader.tsx
│   │   ├── TaskCard.tsx
│   │   └── StatWidget.tsx
│   ├── analytics/       # Analytics components
│   │   ├── KPICard.tsx
│   │   ├── ChartPlaceholder.tsx
│   │   ├── DataTable.tsx
│   │   └── FilterControls.tsx
│   └── index.ts         # Central export point
├── pages/               # Page components
│   ├── ProfileDemo.tsx
│   ├── ProductShowcase.tsx
│   ├── NavBarDemo.tsx
│   ├── Dashboard.tsx
│   ├── AnalyticsDashboard.tsx
│   ├── RegistrationForm.tsx
│   └── TeamDashboard.tsx  ⭐ NEW!
├── data/                # Sample data
│   ├── sampleUsers.ts
│   ├── sampleProducts.ts
│   ├── sampleTasks.ts
│   ├── sampleAnalytics.ts
│   └── sampleNavigation.ts
├── types/               # TypeScript type definitions
│   ├── user.types.ts
│   ├── product.types.ts
│   ├── task.types.ts
│   ├── analytics.types.ts
│   └── navigation.types.ts
├── hooks/               # Custom React hooks
│   └── useDarkMode.ts
├── App.tsx              # Main application with routing
├── main.tsx             # Application entry point
├── index.css            # Global styles with Tailwind directives
└── vite-env.d.ts        # Vite type definitions

tests/                   # E2E tests
├── accessibility.spec.ts
├── auth.spec.ts
├── error-handling.spec.ts
├── navigation.spec.ts
├── product-search.spec.ts
├── registration.spec.ts
├── responsive.spec.ts
└── task-management.spec.ts
```

## 🛠️ Installation

Install dependencies:

```bash
npm install
```

## 🏃‍♂️ Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## 🏗️ Build

Build for production:

```bash
npm run build
```

Preview production build:

```bash
npm run preview
```

## 🧹 Linting

Run ESLint:

```bash
npm run lint
```

## 🎯 Quick Start

1. **Start Development Server**
   ```bash
   npm run dev
   ```

2. **Open Browser**
   Navigate to: http://localhost:5173

3. **Explore Features**
   - Click navigation buttons to view different pages
   - Toggle dark mode with ☀️/🌙 button
   - Try the new **Team Dashboard** (👥 Team button)

## 🧪 Testing

Run E2E tests with Playwright:

```bash
# Run all tests
npm run test

# Run specific test file
npm run test tests/registration.spec.ts

# Run tests in UI mode
npm run test:ui

# View test report
npm run test:report
```

## 📝 Component Usage Examples

### Avatar Component

```tsx
import { Avatar } from './components/common'

<Avatar
  src="https://example.com/avatar.jpg"
  alt="John Doe"
  size="md"
  isVerified={true}
/>
```

### ProductCard Component

```tsx
import { ProductCard } from './components/features'

<ProductCard
  product={{
    id: '1',
    name: 'Product Name',
    price: 99.99,
    rating: { average: 4.5, count: 120 },
    image: 'product.jpg'
  }}
/>
```

### KPICard Component (Analytics)

```tsx
import { KPICard } from './components/analytics'

<KPICard
  title="Total Revenue"
  value="$45,231"
  change={12.5}
  isPositive={true}
  icon={<DollarIcon />}
/>
```

## 🎨 Styling with Tailwind CSS

All components use Tailwind CSS utility classes with full dark mode support:

```tsx
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white p-4 rounded-lg shadow-lg hover:shadow-xl transition-all">
  Responsive, accessible, and beautiful!
</div>
```

## 🌙 Dark Mode

Dark mode is implemented using a custom hook:

```tsx
import { useDarkMode } from './hooks/useDarkMode'

const { isDarkMode, toggleDarkMode } = useDarkMode()
```

Features:
- System preference detection
- User preference persistence (localStorage)
- Smooth transitions
- All components support dark mode

## 📚 Documentation

### Main Guides
- **`DEMO_GUIDE.md`** - Complete demo walkthrough
- **`PROJECT_SUMMARY.md`** - Project overview and features
- **`TESTING_GUIDE.md`** - Testing documentation

### Component Documentation
- **`NAVBAR_SUMMARY.md`** - Navigation bar features
- **`PRODUCTCARD_SUMMARY.md`** - Product card component
- **`DASHBOARD_SUMMARY.md`** - Dashboard features
- **`ANALYTICS_SUMMARY.md`** - Analytics dashboard
- **`REGISTRATION_SUMMARY.md`** - Registration form

### Team Dashboard Documentation ⭐ NEW!
- **`TEAM_DASHBOARD_QUICKSTART.md`** - Quick start guide
- **`TEAM_DASHBOARD.md`** - Complete feature documentation
- **`TEAM_DASHBOARD_VISUAL_GUIDE.md`** - Visual layouts and specs

### Testing Documentation
- **`PRODUCT_SEARCH_TESTS.md`** - Product search tests
- **`REGISTRATION_TESTS.md`** - Registration form tests
- **`TEST_SCENARIOS_COVERAGE.md`** - Test coverage overview

## 🎯 Key Technologies

### Core Stack
- **React 18** - Modern React with hooks and concurrent features
- **TypeScript** - Type safety and enhanced developer experience
- **Vite** - Next-generation frontend tooling
- **Tailwind CSS** - Utility-first CSS framework

### Testing
- **Playwright** - End-to-end testing framework
- **@axe-core/playwright** - Accessibility testing

### Additional Libraries
- **Lucide React** - Modern icon library
- **Date-fns** - Date utility library
- **ESLint** - Code quality and consistency

## 🚀 Features Showcase

### State Management
- Custom hooks (useDarkMode)
- React useState and useMemo
- Efficient re-rendering strategies

### Responsive Design
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Touch-friendly interactions

### Accessibility
- ARIA labels and roles
- Keyboard navigation
- Screen reader support
- Color contrast compliance
- Focus management

### Performance
- Lazy loading ready
- Optimized re-renders with useMemo
- Efficient component structure
- Tree-shaking enabled

## 📊 Project Statistics

- **Components**: 30+ reusable components
- **Pages**: 7 complete page implementations
- **Test Suites**: 8 comprehensive test files
- **Test Cases**: 200+ E2E test scenarios
- **Lines of Code**: ~5000+ LOC
- **Type Coverage**: 100% TypeScript

## 🤝 Contributing

This is a demo project showcasing modern React development practices. Feel free to:
- Explore the codebase
- Learn from the implementations
- Use components in your projects
- Extend features
- Add new components

## 📝 License

MIT License - feel free to use this code for learning and development.

## 📚 Learn More

- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Playwright Documentation](https://playwright.dev/)

---

**Made with ❤️ using React, TypeScript, Vite, and Tailwind CSS**