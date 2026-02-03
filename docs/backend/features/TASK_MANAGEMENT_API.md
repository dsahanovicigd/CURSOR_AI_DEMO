# Task Management System API

A comprehensive REST API for task management with user authentication, project management, team collaboration, and real-time notifications.

## 🚀 Features

- **User Authentication** - JWT-based authentication with refresh tokens
- **Task Management** - Full CRUD operations for tasks with status, priority, assignments
- **Project Management** - Create and manage projects with member collaboration
- **Team Collaboration** - Team creation and management with role-based access
- **Task Comments** - Comment threads on tasks for collaboration
- **Real-time Notifications** - Notification system for task assignments, completions, comments, and invites
- **Swagger Documentation** - Interactive API documentation

## 📋 API Endpoints

### Authentication (`/api/auth`)
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT tokens
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info

### Tasks (`/api/tasks`)
- `GET /api/tasks` - Get all tasks (with filters: project_id, assigned_to_id, status, priority)
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/<id>` - Get a specific task
- `PUT /api/tasks/<id>` - Update a task
- `DELETE /api/tasks/<id>` - Delete a task
- `POST /api/tasks/<id>/complete` - Mark task as completed

### Projects (`/api/projects`)
- `GET /api/projects` - Get all projects (user's projects)
- `POST /api/projects` - Create a new project
- `GET /api/projects/<id>` - Get a specific project
- `PUT /api/projects/<id>` - Update a project
- `DELETE /api/projects/<id>` - Delete a project
- `GET /api/projects/<id>/members` - Get project members
- `POST /api/projects/<id>/members` - Add member to project
- `DELETE /api/projects/<id>/members/<user_id>` - Remove member from project

### Teams (`/api/teams`)
- `GET /api/teams` - Get all teams (user's teams)
- `POST /api/teams` - Create a new team
- `GET /api/teams/<id>` - Get a specific team
- `PUT /api/teams/<id>` - Update a team
- `DELETE /api/teams/<id>` - Delete a team
- `GET /api/teams/<id>/members` - Get team members
- `POST /api/teams/<id>/members` - Add member to team
- `DELETE /api/teams/<id>/members/<user_id>` - Remove member from team

### Notifications (`/api/notifications`)
- `GET /api/notifications` - Get all notifications (with filters: is_read, type)
- `GET /api/notifications/<id>` - Get a specific notification
- `POST /api/notifications/<id>/read` - Mark notification as read
- `POST /api/notifications/read-all` - Mark all notifications as read
- `GET /api/notifications/unread-count` - Get unread notification count

### Task Comments (`/api/tasks/<task_id>/comments`)
- `GET /api/tasks/<task_id>/comments` - Get all comments for a task
- `POST /api/tasks/<task_id>/comments` - Create a comment on a task
- `PUT /api/comments/<comment_id>` - Update a comment
- `DELETE /api/comments/<comment_id>` - Delete a comment

## 🔐 Authentication

All endpoints (except auth endpoints) require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## 📊 Data Models

### Task
- `id` - Integer (primary key)
- `title` - String (required)
- `description` - Text (optional)
- `status` - Enum: pending, in_progress, completed, cancelled
- `priority` - Enum: low, medium, high, urgent
- `project_id` - Integer (foreign key, optional)
- `assigned_to_id` - Integer (foreign key, optional)
- `created_by_id` - Integer (foreign key, required)
- `due_date` - DateTime (optional)
- `completed_at` - DateTime (optional)
- `created_at` - DateTime
- `updated_at` - DateTime

### Project
- `id` - Integer (primary key)
- `name` - String (required)
- `description` - Text (optional)
- `status` - Enum: active, archived, completed
- `owner_id` - Integer (foreign key, required)
- `team_id` - Integer (foreign key, optional)
- `start_date` - DateTime (optional)
- `end_date` - DateTime (optional)
- `created_at` - DateTime
- `updated_at` - DateTime

### Team
- `id` - Integer (primary key)
- `name` - String (required)
- `description` - Text (optional)
- `owner_id` - Integer (foreign key, required)
- `created_at` - DateTime
- `updated_at` - DateTime

### Notification
- `id` - Integer (primary key)
- `type` - Enum: task_assigned, task_completed, task_comment, project_invite, team_invite, mention, due_date_reminder
- `title` - String (required)
- `message` - Text (required)
- `is_read` - Boolean
- `user_id` - Integer (foreign key, required)
- `related_task_id` - Integer (foreign key, optional)
- `related_project_id` - Integer (foreign key, optional)
- `related_team_id` - Integer (foreign key, optional)
- `meta_data` - JSON (optional)
- `created_at` - DateTime
- `read_at` - DateTime

## 🎯 Usage Examples

### 1. Register and Login
```bash
# Register
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Login
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepass123"
  }'
```

### 2. Create a Project
```bash
curl -X POST http://localhost:5001/api/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "Website Redesign",
    "description": "Redesign company website",
    "status": "active"
  }'
```

### 3. Create a Task
```bash
curl -X POST http://localhost:5001/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "title": "Design homepage mockup",
    "description": "Create initial design mockup for homepage",
    "status": "pending",
    "priority": "high",
    "project_id": 1,
    "assigned_to_id": 2,
    "due_date": "2026-02-01T00:00:00Z"
  }'
```

### 4. Get Tasks
```bash
# Get all tasks
curl http://localhost:5001/api/tasks \
  -H "Authorization: Bearer <token>"

# Get tasks for a project
curl "http://localhost:5001/api/tasks?project_id=1" \
  -H "Authorization: Bearer <token>"

# Get tasks by status
curl "http://localhost:5001/api/tasks?status=pending" \
  -H "Authorization: Bearer <token>"
```

### 5. Add Comment to Task
```bash
curl -X POST http://localhost:5001/api/tasks/1/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "content": "This looks great! Let me know if you need any changes."
  }'
```

### 6. Get Notifications
```bash
# Get all notifications
curl http://localhost:5001/api/notifications \
  -H "Authorization: Bearer <token>"

# Get unread notifications
curl "http://localhost:5001/api/notifications?is_read=false" \
  -H "Authorization: Bearer <token>"

# Get unread count
curl http://localhost:5001/api/notifications/unread-count \
  -H "Authorization: Bearer <token>"
```

## 📚 Swagger Documentation

Access interactive API documentation at:
**http://localhost:5001/api/docs**

## 🔧 Setup

1. **Install Dependencies**
```bash
cd flask_api
source venv/bin/activate
pip install -r requirements.txt
```

2. **Initialize Database**
```bash
python3 -c "from app import create_app, db; from app.models import *; app = create_app(); app.app_context().push(); db.create_all()"
```

3. **Start Server**
```bash
./start.sh
# or
python run.py
```

## 🎨 Features in Detail

### Task Management
- Create, read, update, delete tasks
- Assign tasks to users
- Set task priority and status
- Add due dates
- Filter tasks by project, assignee, status, priority
- Mark tasks as completed

### Project Management
- Create projects with teams
- Add/remove project members
- Role-based access (owner, admin, member)
- Project status tracking (active, archived, completed)

### Team Collaboration
- Create teams
- Add/remove team members
- Role-based access control
- Teams can have multiple projects

### Notifications
- Automatic notifications for:
  - Task assignments
  - Task completions
  - Task comments
  - Project invites
  - Team invites
- Mark notifications as read
- Filter by type and read status
- Get unread count

### Comments
- Add comments to tasks
- Edit and delete own comments
- Automatic notifications to task assignee and project members

## 🔒 Security

- JWT-based authentication
- Password hashing with Werkzeug
- Role-based access control
- Project/team membership validation
- CORS configuration

## 📝 Error Handling

All endpoints return appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `204` - No Content (deleted)
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (missing/invalid token)
- `403` - Forbidden (access denied)
- `404` - Not Found
- `500` - Internal Server Error

Error responses follow this format:
```json
{
  "error": "Error message"
}
```
