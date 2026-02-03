# System Architecture

## Overview

This document describes the architecture of the full-stack application deployed on Render.com, consisting of a React frontend, Flask API backend, PostgreSQL database, Redis cache, and Celery background workers.

## Architecture Diagram

![Architecture Diagram](./assets/886a7afe-aabb-4e47-a886-a9b6abbbf6f2.png)

## Component Layers

### 1. Frontend Layer (Client-Side)

**Technology:** React 18.2 + TypeScript + Vite

**Deployment:** Render.com Static Site

**Components:**
- **Dashboard** - Main user dashboard with analytics
- **Kanban Board** - Task management with drag-and-drop
- **Social Feed** - Blog posts and social interactions
- **Product Showcase** - E-commerce product catalog
- **Analytics** - Data visualization and reporting
- **User Profile** - User management and settings
- **Registration/Login** - Authentication UI

**Features:**
- Responsive design with Tailwind CSS
- Client-side routing
- JWT token management
- API integration via Axios/Fetch
- Real-time updates (via polling/WebSockets)

**Build Process:**
```bash
npm install && npm run build
```
- Output: Static files in `dist/` directory
- Environment: `VITE_API_URL` configured at build time

---

### 2. API Gateway / Load Balancer

**Technology:** Render.com Web Service Layer

**Features:**
- HTTPS/SSL termination (automatic)
- Request routing and load balancing
- Health checks and auto-scaling
- DDoS protection
- Geographic distribution (multi-region support)

**Port Configuration:**
- Render automatically sets `$PORT` environment variable
- Application binds to `0.0.0.0:$PORT`

---

### 3. Backend Services Layer

**Technology:** Flask 3.0 + Python 3.11 + Gunicorn

**Deployment:** Render.com Web Service

**WSGI Server:** Gunicorn
- Workers: 4
- Threads: 2 per worker
- Timeout: 120 seconds
- Access/Error logging to stdout

**Application Structure:**
```
flask_api/
├── app/
│   ├── __init__.py          # App factory
│   ├── models/              # SQLAlchemy models (15+ models)
│   ├── schemas/             # Marshmallow schemas
│   ├── auth/                # Authentication routes
│   ├── users/               # User management
│   ├── posts/               # Blog posts
│   ├── tickets/             # Support tickets
│   ├── tasks/               # Task management
│   ├── projects/            # Project management
│   ├── teams/               # Team collaboration
│   ├── products/            # E-commerce products
│   ├── cart/                # Shopping cart
│   ├── checkout/            # Checkout process
│   ├── orders/              # Order management
│   ├── categories/          # Product categories
│   ├── comments/            # Comments system
│   ├── notifications/       # Notifications
│   ├── admin/               # Admin panel
│   └── agents/              # Support agents
```

**API Modules:**

#### Authentication (`/api/auth`)
- User registration
- Login with JWT tokens
- Token refresh
- Current user endpoint
- Logout

#### User Management (`/api/users`)
- CRUD operations
- Profile management
- Role-based access (customer, agent, admin)

#### Blog/Posts (`/api/posts`)
- Create, read, update, delete posts
- Search and filtering
- Categories and tags
- Comments system

#### Support Tickets (`/api/tickets`)
- Ticket creation (public endpoint)
- Assignment and status tracking
- Priority management
- Comments and attachments
- SLA tracking

#### Task Management (`/api/tasks`)
- Kanban board tasks
- Task assignment
- Status tracking
- Comments and attachments

#### Projects & Teams (`/api/projects`, `/api/teams`)
- Project management
- Team collaboration
- Member management

#### E-commerce (`/api/products`, `/api/cart`, `/api/checkout`, `/api/orders`)
- Product catalog
- Shopping cart
- Checkout process
- Order management

**Security Features:**
- JWT authentication
- Password hashing (Werkzeug)
- CORS configuration
- Rate limiting (Flask-Limiter)
- Input sanitization (Bleach)
- SQL injection prevention (SQLAlchemy ORM)

**API Documentation:**
- Swagger UI at `/api/docs`
- Interactive API testing
- JWT token support

---

### 4. Background Workers

**Technology:** Celery 5.3 + Redis

**Deployment:** Separate Render.com Web Service (optional)

**Tasks:**
- Email notifications
- Scheduled jobs
- Background processing
- Task queue management

**Configuration:**
- Broker: Redis
- Result Backend: Redis
- Task Serialization: JSON

---

### 5. Data Layer

#### PostgreSQL Database

**Technology:** PostgreSQL 15

**Deployment:** Render.com Managed PostgreSQL

**Models (15+):**
- Users (with roles: customer, agent, admin)
- Posts (blog content)
- Comments
- Categories
- Tickets (support system)
- Ticket Comments
- Ticket Attachments
- Ticket Assignments
- Ticket Status History
- Tasks
- Task Comments
- Task Attachments
- Projects
- Teams
- Products
- Cart Items
- Orders
- Notifications

**Features:**
- Database migrations (Flask-Migrate)
- Connection pooling
- Indexes for performance
- Foreign key relationships
- Timestamps (created_at, updated_at)

**Connection:**
- Auto-configured via `DATABASE_URL`
- Connection pooling: 10 pool size, 20 max overflow
- Pool recycling: 3600 seconds

#### Redis Cache

**Technology:** Redis

**Deployment:** Render.com Managed Redis

**Usage:**
- API response caching
- Session storage
- Celery broker
- Celery result backend
- Rate limiting storage

**Configuration:**
- Memory policy: allkeys-lru
- Connection via `REDIS_URL`

---

### 6. External Services

**Email Service:**
- Notification emails
- Transactional emails
- SMTP configuration

**File Storage:**
- Ticket attachments
- Task attachments
- User avatars
- Product images

---

## Data Flow

### Request Flow (User → Backend)

1. **User Request**
   - User interacts with React frontend
   - Frontend makes API call to backend

2. **API Gateway**
   - Request routed through Render load balancer
   - HTTPS termination
   - Request forwarded to Flask API

3. **Flask API**
   - Gunicorn receives request
   - Flask app processes request
   - Authentication check (JWT)
   - Rate limiting check
   - Business logic execution

4. **Data Access**
   - Check Redis cache (if applicable)
   - Query PostgreSQL database
   - Update cache (if applicable)

5. **Response**
   - JSON response returned
   - CORS headers added
   - Response sent to frontend

### Background Task Flow

1. **Task Creation**
   - Flask API creates Celery task
   - Task sent to Redis broker

2. **Task Processing**
   - Celery worker picks up task
   - Task executed
   - Results stored in Redis

3. **Notification**
   - Email sent (if applicable)
   - Database updated
   - Frontend notified (via polling/WebSocket)

---

## Deployment Architecture

### Render.com Services

1. **react-frontend** (Static Site)
   - Type: Static Site
   - Build: `npm install && npm run build`
   - Publish: `./dist`
   - Environment: `VITE_API_URL`

2. **flask-api** (Web Service)
   - Type: Web Service (Python)
   - Root Directory: `flask_api`
   - Build: `pip install -r requirements.txt && flask db upgrade`
   - Start: `gunicorn --bind 0.0.0.0:$PORT ... run:app`
   - Environment: Multiple variables (see render.yaml)

3. **postgres-db** (Database)
   - Type: PostgreSQL
   - Version: PostgreSQL 15
   - Plan: Starter/Standard/Pro
   - Auto-backups enabled

4. **redis-cache** (Cache)
   - Type: Redis
   - Plan: Starter/Standard/Pro
   - Memory policy: allkeys-lru

---

## Environment Variables

### Frontend
- `VITE_API_URL` - Backend API URL

### Backend
- `FLASK_ENV` - Environment (production)
- `FLASK_APP` - App entry point
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `CELERY_BROKER_URL` - Celery broker URL
- `CELERY_RESULT_BACKEND` - Celery result backend
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT signing key
- `CORS_ORIGINS` - Allowed CORS origins

---

## Security Architecture

### Authentication & Authorization
- JWT-based authentication
- Token expiration (1 hour access, 30 days refresh)
- Role-based access control (RBAC)
- Protected routes with `@jwt_required()`

### Data Protection
- Password hashing (bcrypt)
- SQL injection prevention (ORM)
- XSS protection (input sanitization)
- CSRF protection (CORS configuration)

### Network Security
- HTTPS/SSL (automatic on Render)
- Rate limiting (100 requests/minute default)
- CORS restrictions
- Input validation (Marshmallow schemas)

---

## Scalability

### Horizontal Scaling
- Gunicorn workers (4 workers, 2 threads each)
- Multiple Flask API instances (Render auto-scaling)
- Load balancing (Render load balancer)
- Database connection pooling

### Caching Strategy
- Redis for API response caching
- Cache invalidation on updates
- Cache TTL configuration

### Database Optimization
- Indexes on frequently queried columns
- Connection pooling
- Query optimization
- Pagination for large datasets

---

## Monitoring & Logging

### Application Logs
- Gunicorn access logs (stdout)
- Gunicorn error logs (stderr)
- Flask application logs
- Available in Render dashboard

### Metrics
- Request count
- Response times
- Error rates
- CPU/Memory usage
- Database connections

### Health Checks
- `/api/health` endpoint
- Render automatic health checks
- Database connectivity checks

---

## Disaster Recovery

### Database Backups
- Automatic daily backups (Render managed)
- Point-in-time recovery
- Backup retention policy

### High Availability
- Multi-region deployment (optional)
- Database replication (Pro plan)
- Redis persistence

---

## Development vs Production

### Development
- SQLite database
- In-memory cache
- Debug mode enabled
- Local development server

### Production
- PostgreSQL database
- Redis cache
- Debug mode disabled
- Gunicorn WSGI server
- HTTPS enforced
- Environment-specific configuration

---

## Technology Stack Summary

### Frontend
- React 18.2
- TypeScript 5.2
- Vite 5.0
- Tailwind CSS 3.3
- React Router
- Axios/Fetch

### Backend
- Python 3.11
- Flask 3.0
- SQLAlchemy 2.0
- Marshmallow 3.20
- Gunicorn 21.2
- Celery 5.3

### Database
- PostgreSQL 15
- Redis (latest)

### Infrastructure
- Render.com
- Git (GitHub/GitLab/Bitbucket)

---

## API Endpoints Overview

### Authentication
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `GET /api/auth/me`

### Users
- `GET /api/users`
- `GET /api/users/<id>`
- `PUT /api/users/<id>`
- `DELETE /api/users/<id>`

### Posts
- `GET /api/posts`
- `GET /api/posts/<id>`
- `POST /api/posts`
- `PUT /api/posts/<id>`
- `DELETE /api/posts/<id>`

### Tickets
- `GET /api/tickets`
- `POST /api/tickets`
- `GET /api/tickets/<id>`
- `PUT /api/tickets/<id>`

### Tasks
- `GET /api/tasks`
- `POST /api/tasks`
- `GET /api/tasks/<id>`
- `PUT /api/tasks/<id>`

### Products
- `GET /api/products`
- `GET /api/products/<id>`

### Cart & Orders
- `GET /api/cart`
- `POST /api/cart`
- `POST /api/checkout`
- `GET /api/orders`

### Health
- `GET /api/health`

*See Swagger UI at `/api/docs` for complete API documentation*

---

## Future Enhancements

### Planned Features
- WebSocket support for real-time updates
- GraphQL API option
- Microservices architecture (if needed)
- CDN integration for static assets
- Advanced caching strategies
- Message queue (RabbitMQ) for high-volume tasks
- Elasticsearch for advanced search
- Docker containerization
- Kubernetes deployment option

---

## References

- [Render.com Documentation](https://render.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/docs/)

---

*Last Updated: January 2026*
