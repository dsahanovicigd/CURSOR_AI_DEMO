import os
from app import create_app

# Get environment or default to development
config_name = os.environ.get('FLASK_ENV', 'development')

app = create_app(config_name)

if __name__ == '__main__':
    # Use port 5001 by default to avoid conflict with macOS AirPlay Receiver on port 5000
    # Force port 5001 unless explicitly set in environment
    port = int(os.environ.get('FLASK_PORT', 5001))
    if port == 5000:
        print("⚠️  Port 5000 conflicts with macOS AirPlay Receiver. Using port 5001 instead.")
        port = 5001
    
    app.run(
        host=os.environ.get('FLASK_HOST', '0.0.0.0'),
        port=port,
        debug=os.environ.get('FLASK_DEBUG', 'True') == 'True'
    )
