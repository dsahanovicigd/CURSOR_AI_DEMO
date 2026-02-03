# Flask REST API

A production-ready Flask REST API with SQLAlchemy, Marshmallow, JWT authentication, and Swagger UI documentation.

## 🚀 Features

- **Flask** - Modern web framework
- **SQLAlchemy** - ORM for database operations
- **Marshmallow** - Serialization and validation
- **JWT Authentication** - Secure token-based authentication
- **Swagger UI** - Interactive API documentation
- **Flask-Migrate** - Database migrations
- **CORS Support** - Cross-origin resource sharing
- **Blueprint Architecture** - Modular route organization

## 📁 Project Structure

```
flask_api/
├── app/
│   ├── __init__.py          # App factory
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── post.py          # Post model
│   ├── schemas/             # Marshmallow schemas
│   │   ├── __init__.py
│   │   ├── user.py          # User schemas
│   │   └── post.py          # Post schemas
│   ├── auth/                # Authentication routes
│   │   ├── __init__.py
│   │   └── routes.py        # Auth endpoints
│   ├── users/               # User routes
│   │   ├── __init__.py
│   │   └── routes.py        # User CRUD endpoints
│   └── posts/               # Post routes
│       ├── __init__.py
│       └── routes.py        # Post CRUD endpoints
├── config.py                # Configuration classes
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🛠️ Installation

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Initialize Database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 🚀 Running the Application

### Development Mode

```bash
python run.py
```

Or using Flask CLI:

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```

The API will be available at: `http://localhost:5001` (port 5001 to avoid conflict with macOS AirPlay Receiver)

## 📚 API Documentation

Once the server is running, access Swagger UI at:

**http://localhost:5001/api/docs**

## 🔐 Authentication

### Register a User

```bash
POST http://localhost:5001/api/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Login

```bash
POST http://localhost:5001/api/auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepassword123"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

### Using JWT Token

Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get tokens
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user

### Users
- `GET http://localhost:5001/api/users` - List all users (paginated)
- `GET http://localhost:5001/api/users/<id>` - Get user by ID
- `PUT http://localhost:5001/api/users/<id>` - Update user
- `DELETE http://localhost:5001/api/users/<id>` - Delete user

### Posts
- `GET http://localhost:5001/api/posts` - List all posts (paginated)
- `GET http://localhost:5001/api/posts/<id>` - Get post by ID
- `POST http://localhost:5001/api/posts` - Create new post (requires auth)
- `PUT http://localhost:5001/api/posts/<id>` - Update post (requires auth)
- `DELETE http://localhost:5001/api/posts/<id>` - Delete post (requires auth)

### Health Check
- `GET http://localhost:5001/api/health` - API health status

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app
```

## 🔧 Configuration

The application uses environment-based configuration:

- **Development** - SQLite database, debug mode
- **Production** - PostgreSQL recommended, debug off
- **Testing** - In-memory database

Set `FLASK_ENV` environment variable to switch modes.

## 📝 Database Migrations

```bash
# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

## 🔒 Security Best Practices

1. **Change Secret Keys** - Update `SECRET_KEY` and `JWT_SECRET_KEY` in production
2. **Use HTTPS** - Always use HTTPS in production
3. **Environment Variables** - Never commit `.env` file
4. **Password Hashing** - Passwords are automatically hashed using Werkzeug
5. **CORS Configuration** - Configure allowed origins in production

## 🚀 Production Deployment

1. Set `FLASK_ENV=production`
2. Use PostgreSQL database
3. Set strong secret keys
4. Configure CORS origins
5. Use a production WSGI server (Gunicorn, uWSGI)
6. Set up reverse proxy (Nginx)

### Example with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 📦 Dependencies

- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM
- **Flask-Migrate** - Database migrations
- **Flask-JWT-Extended** - JWT authentication
- **Marshmallow** - Serialization/validation
- **Flasgger** - Swagger UI integration
- **Flask-CORS** - CORS support

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Add tests
4. Submit a pull request

## 📄 License

MIT License

## 🆘 Support

For issues and questions, please open an issue on GitHub.

---

**Happy Coding! 🚀**
