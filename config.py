import os

class Config:
    """
    General configuration settings for the Flask app.
    """
    # Secret key for session management (use a more secure key for production)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key') 

    # Enable/disable Flask debugging
    DEBUG = os.environ.get('FLASK_DEBUG', True)  # Set to False in production

    # Database URI (SQLite in this case)
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'result_portal.db')
    #DB_PATH = DATABASE
    DB_PATH = os.path.join(os.getcwd(), 'result_portal.db')  # SQLite database location
    RESULTS_FOLDER = os.path.join(os.getcwd(), 'results')  # Path to results folder
    ACCESS_CODE_DB = 'access_codes'
    STUDENT_DB = 'students'

    # Set to the URI for your SQLite database
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE}"
    
    # To track database modifications (set to False to silence warnings)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Folder to store results as PDFs
    #RESULTS_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'results')
    
    # Path for access codes database
    #ACCESS_CODE_DB = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'access_codes.json')
    
    # Path for student database (JSON format)
    #STUDENT_DB = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'students.json')

    # Mail configuration (if you're using Flask-Mail)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.example.com')  # e.g. 'smtp.gmail.com'
    MAIL_PORT = os.environ.get('MAIL_PORT', 587)  # Typically 587 for TLS
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'your-email@example.com')

    # Session configuration (if you need more custom session behavior)
    SESSION_TYPE = 'filesystem'  # Options: 'filesystem', 'redis', etc.
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_NAME = 'result_portal_session'
    SESSION_COOKIE_SECURE = True  # Only set to True if using HTTPS

    # Caching (optional)
    CACHE_TYPE = "simple"  # Options: 'simple', 'redis', 'memcached', etc.
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes

    # Other optional configurations
    LANGUAGES = ['en', 'fr']  # List of supported languages for internationalization (i18n)
    TIMEZONE = 'UTC'  # Default timezone for the application (can be set to your local timezone)
