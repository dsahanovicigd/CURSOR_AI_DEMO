# Playwright E2E Tests

Comprehensive end-to-end testing suite for the task management application.

## Quick Start

```bash
# Install dependencies
npm install

# Install Playwright browsers
npx playwright install

# Run all tests
npm test

# Run tests with UI
npm run test:ui

# View test report
npm run test:report
```

## Test Files

### `navigation.spec.ts` - Navigation Tests ✨ NEW!
- Navigate between pages
- Breadcrumb navigation
- Back/forward button functionality
- Keyboard navigation
- State persistence
- Error handling
- Accessibility

### `auth.spec.ts` - Authentication Tests ✨ ENHANCED!
- **User Registration**
  - Registration form validation
  - Duplicate email handling
  - Password strength requirements
  - Email format validation
- **Login**
  - Valid credentials
  - Invalid credentials
  - Case-sensitive passwords
  - Loading states
- **Logout**
  - Desktop logout
  - Mobile logout
- **Session Persistence**
  - Page reload persistence
  - Cross-tab sessions
  - Session expiration
  - User preferences restoration

### `task-management.spec.ts` - Task Management ✨ ENHANCED!
- **Display & View**
  - Dashboard, cards, details
  - Filtering by status
  - Progress bars & assignees
- **Create Task**
  - Creation buttons
  - Form validation
- **Edit Task**
  - Title, description, priority
  - Due date, assignee
  - Cancel & validation
- **Complete Task**
  - Mark complete/incomplete
  - Completion animations
  - Statistics updates
- **Delete Task**
  - Confirmation dialogs
  - Single & bulk delete
  - Statistics updates
- **Search & Filter**
  - Search by title/description
  - Filter by priority/assignee/date
  - Combined filters
  - Filter persistence

### `accessibility.spec.ts` - Accessibility
- WCAG 2.0 AA compliance
- ARIA labels and roles
- Keyboard navigation
- Screen reader support
- Color contrast
- Form accessibility
- Heading hierarchy

### `responsive.spec.ts` - Responsive Design ✨ ENHANCED!
- **Mobile** viewport (375x667)
  - Hamburger menu
  - Sidebar drawer
  - Mobile-friendly layouts
- **Tablet** viewport (768x1024)
  - 2-column grids
  - Visible sidebar
- **Desktop** viewport (1920x1080)
  - Persistent sidebar
  - 4-column layouts
- **Orientation Changes** ✨ NEW!
  - Portrait ↔ Landscape
  - Layout adjustments
  - State persistence
  - Rapid changes

### `error-handling.spec.ts` - Error Handling
- Network errors
- Missing/malformed data
- Console errors
- Navigation errors
- UI component errors
- Form validation errors
- Rapid interactions

### `registration.spec.ts` - Multi-Step Registration Form ✨ NEW!
- **Initial State** (4 tests)
  - Form display
  - Progress bar
  - Step indicators
- **Field Validation** (28 tests)
  - Personal information (Step 1)
  - Account details (Step 2)
  - Preferences (Step 3)
  - Terms & review (Step 4)
- **Navigation** (9 tests)
  - Forward/backward navigation
  - Step indicators
  - Data persistence
- **Form Submission** (7 tests)
  - Loading states
  - Success message
  - Next steps
- **Error Handling** (10 tests)
  - Error messages
  - ARIA associations
  - Screen reader announcements
- **Accessibility** (4 tests)
  - WCAG 2.0 AA compliance
  - Keyboard navigation
  - Form labels

### `product-search.spec.ts` - Product Search & Filter
- **Initial Page Load**
  - Product display
  - Filter options
  - Sort dropdown
- **Category Filtering**
  - Filter by sale, bestsellers, new arrivals
  - Filter by stock status
  - Multiple filter combinations
- **Sort Functionality**
  - Sort by price (low to high, high to low)
  - Sort by rating
  - Sort persistence with filters
- **Product Interactions**
  - Add to cart
  - Favorite/wishlist toggle
  - Quick view
  - Loading states
- **Empty Results**
  - No matches handling
  - Reset filters
- **Responsive Product Grid**
  - Desktop multi-column
  - Tablet grid
  - Mobile single column
- **Performance**
  - Load times
  - No-reload filtering
- **Error Handling**
  - Rapid filter changes
  - Missing images
  - Simultaneous operations
- **Accessibility**
  - Keyboard navigation
  - Screen reader support

## Running Specific Tests

```bash
# Run one file
npx playwright test auth.spec.ts
npx playwright test registration.spec.ts
npx playwright test navigation.spec.ts
npx playwright test task-management.spec.ts
npx playwright test product-search.spec.ts

# Run specific test group
npx playwright test registration.spec.ts -g "Field Validation"
npx playwright test registration.spec.ts -g "Navigation"
npx playwright test product-search.spec.ts -g "Category Filtering"

# Run one test
npx playwright test -g "should logout successfully"

# Run for specific browser
npx playwright test --project=chromium

# Run for mobile
npx playwright test --project="Mobile Chrome"
```

## Debugging

```bash
# Debug mode
npm run test:debug

# Headed mode (see browser)
npm run test:headed

# Interactive UI mode
npm run test:ui
```

## Test Coverage

- ✅ **260+ total tests**
- ✅ 7 browser configurations
- ✅ 3 viewport sizes + orientation testing
- ✅ WCAG 2.0 AA compliance
- ✅ Complete CRUD operations
- ✅ Full navigation testing
- ✅ Session management
- ✅ Product search & filtering
- ✅ E-commerce functionality
- ✅ Error scenarios
- ✅ Responsive design
- ✅ Accessibility

### Test Count by File
- `registration.spec.ts`: **60+ tests** ✨ NEW!
- `product-search.spec.ts`: **48 tests**
- `navigation.spec.ts`: **19 tests**
- `auth.spec.ts`: **28 tests**
- `task-management.spec.ts`: **52 tests**
- `accessibility.spec.ts`: **15 tests**
- `responsive.spec.ts`: **31 tests**
- `error-handling.spec.ts`: **35 tests**

## CI/CD

Tests are configured to run in GitHub Actions with automatic retries and detailed reporting.

See `playwright.config.ts` for full configuration.
