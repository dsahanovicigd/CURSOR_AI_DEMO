#!/bin/bash

# Flask API Setup Script

echo "🚀 Setting up Flask REST API..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
JWT_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
DATABASE_URL=sqlite:///flask_api_dev.db
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
EOF
    echo "✅ .env file created with secure keys"
else
    echo "ℹ️  .env file already exists"
fi

# Initialize database
echo "🗄️  Initializing database..."
flask db init || echo "Database already initialized"
flask db migrate -m "Initial migration" || echo "Migration already exists"
flask db upgrade

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the server:"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo "API will be available at: http://localhost:5001"
echo "Swagger UI: http://localhost:5001/api/docs"
