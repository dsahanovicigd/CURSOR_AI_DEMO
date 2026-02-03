# Documentation Structure

This document provides an overview of the organized documentation structure.

## 📁 Directory Structure

```
docs/
├── README.md                          # Main documentation index
├── DOCUMENTATION_STRUCTURE.md         # This file
│
├── architecture/                       # System architecture
│   ├── README.md
│   └── ARCHITECTURE.md
│
├── deployment/                         # Deployment guides
│   ├── README.md
│   ├── RENDER_DEPLOYMENT_GUIDE.md
│   ├── RENDER_QUICK_START.md
│   ├── VERCEL_DEPLOYMENT_GUIDE.md
│   ├── VERCEL_QUICK_START.md
│   └── VERCEL_SETUP_COMPLETE.md
│
├── development/                       # Development guides
│   ├── README.md
│   ├── START_ALL_SERVICES.md
│   ├── CELERY_WORKER_USAGE.md
│   ├── REDIS_CLIENTS_GUIDE.md
│   └── ...
│
├── features/                          # Feature documentation
│   ├── README.md
│   ├── ANALYTICS_SUMMARY.md
│   ├── AUTH_INTEGRATION_SUMMARY.md
│   ├── KANBAN_BOARD_SUMMARY.md
│   ├── SOCIAL_FEED_SUMMARY.md
│   └── ...
│
├── ci-cd/                            # CI/CD documentation
│   ├── README.md
│   ├── CI_CD_FIXES_APPLIED.md
│   ├── GITHUB_ACTIONS_SETUP.md
│   └── ...
│
├── testing/                          # Testing documentation
│   ├── README.md
│   ├── TESTING_GUIDE.md
│   ├── TEST_RESULTS_AFTER_FIXES.md
│   └── ...
│
├── api/                              # API documentation
│   ├── README.md
│   ├── FLASK_API_SUMMARY.md
│   ├── SWAGGER_AUTH_GUIDE.md
│   └── ...
│
├── troubleshooting/                  # Troubleshooting guides
│   ├── README.md
│   ├── API_CONNECTION_TROUBLESHOOTING.md
│   ├── CELERY_FIX.md
│   └── ...
│
├── project-management/               # Project management docs
│   ├── README.md
│   ├── PRD_Customer_Support_System.md
│   ├── PROJECT_SUMMARY.md
│   └── ...
│
├── backend/                          # Backend-specific docs
│   ├── README.md
│   ├── api/                          # Backend API docs
│   ├── guides/                       # Backend guides
│   ├── testing/                     # Backend testing
│   ├── features/                    # Backend features
│   └── troubleshooting/            # Backend troubleshooting
│
├── frontend/                         # Frontend-specific docs
│   └── (to be populated)
│
└── qa/                               # QA documentation
    ├── README.md
    ├── QA_SYSTEM_DOCUMENTATION.md
    ├── PYLINT_FIXES_SUMMARY.md
    └── ...
```

## 📊 Statistics

- **Total Documentation Files**: 141+
- **Main Categories**: 12
- **Subcategories**: Multiple

## 🔍 Quick Navigation

### Getting Started
- Start with [docs/README.md](./README.md)
- Check [Architecture](./architecture/ARCHITECTURE.md)
- Review [Deployment Guides](./deployment/)

### By Topic
- **Architecture**: [architecture/](./architecture/)
- **Deployment**: [deployment/](./deployment/)
- **Features**: [features/](./features/)
- **API**: [api/](./api/)
- **Testing**: [testing/](./testing/)
- **Troubleshooting**: [troubleshooting/](./troubleshooting/)

## 📝 Adding New Documentation

When adding new documentation:

1. **Choose the right category** based on content:
   - Architecture/system design → `architecture/`
   - Deployment guides → `deployment/`
   - Feature docs → `features/`
   - API docs → `api/`
   - Testing → `testing/`
   - Troubleshooting → `troubleshooting/`
   - CI/CD → `ci-cd/`
   - Development guides → `development/`
   - Project management → `project-management/`

2. **Update the relevant README.md** in that directory

3. **Update [docs/README.md](./README.md)** if adding a new category

## 🔄 Maintenance

- Keep README files updated
- Remove outdated documentation
- Organize new files immediately
- Use consistent naming conventions

---

*Last Updated: January 2026*
