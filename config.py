"""
Enhanced Application Configuration
Provides robust configuration management with environment-specific settings
"""
import os
from pathlib import Path


class Config:
    """Base configuration with sensible defaults and environment variable support"""
    
    # Application Settings
    APP_NAME = 'Poetry Vault'
    APP_VERSION = '1.0.0'
    
    # Security Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-PLEASE'
    
    # Warn if using default secret key in production
    if SECRET_KEY == 'dev-secret-key-change-in-production-PLEASE' and os.environ.get('FLASK_ENV') == 'production':
        import warnings
        warnings.warn(
            "WARNING: Using default SECRET_KEY in production! "
            "Set SECRET_KEY environment variable for security.",
            RuntimeWarning
        )
    
    # Database Settings
    DATABASE_URL = os.environ.get('DATABASE_URL', '')
    
    # Fix postgres:// to postgresql:// for SQLAlchemy compatibility
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    # Default to SQLite if no DATABASE_URL provided
    if not DATABASE_URL:
        # Ensure instance directory exists
        instance_path = Path('instance')
        instance_path.mkdir(exist_ok=True)
        DATABASE_URL = 'sqlite:///poetry_app.db'
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    
    # Connection pool settings for production
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.environ.get('DB_POOL_SIZE', 10)),
        'pool_recycle': int(os.environ.get('DB_POOL_RECYCLE', 3600)),
        'pool_pre_ping': True,  # Verify connections before using
        'max_overflow': int(os.environ.get('DB_MAX_OVERFLOW', 20))
    }
    
    # Session Settings
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = int(os.environ.get('SESSION_LIFETIME', 86400))  # 24 hours default
    
    # Flask-Login Settings
    REMEMBER_COOKIE_DURATION = int(os.environ.get('REMEMBER_COOKIE_DURATION', 2592000))  # 30 days
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE
    REMEMBER_COOKIE_HTTPONLY = True
    
    # File Upload Settings (for future features)
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB default
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'instance/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # API Keys
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    OLLAMA_API_URL = os.environ.get('OLLAMA_API_URL', 'http://localhost:11434')
    
    # Rate Limiting (for future implementation)
    RATELIMIT_ENABLED = os.environ.get('RATELIMIT_ENABLED', 'False').lower() == 'true'
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '200 per day, 50 per hour')
    
    # Backup Settings
    BACKUP_ENABLED = os.environ.get('BACKUP_ENABLED', 'True').lower() == 'true'
    BACKUP_INTERVAL_HOURS = int(os.environ.get('BACKUP_INTERVAL_HOURS', 6))
    BACKUP_MAX_COUNT = int(os.environ.get('BACKUP_MAX_COUNT', 10))
    
    # Analytics Settings
    ANALYTICS_ENABLED = os.environ.get('ANALYTICS_ENABLED', 'True').lower() == 'true'
    TRACK_VISITORS = os.environ.get('TRACK_VISITORS', 'True').lower() == 'true'
    
    # Email Settings (for future password reset feature)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@poetryvault.com')
    
    # Admin Settings
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', '')
    ADMIN_SECRET_CODE = os.environ.get('ADMIN_SECRET_CODE', 'P0.1')
    
    # Feature Flags
    ENABLE_REGISTRATION = os.environ.get('ENABLE_REGISTRATION', 'True').lower() == 'true'
    ENABLE_COMMENTS = os.environ.get('ENABLE_COMMENTS', 'True').lower() == 'true'
    ENABLE_LIKES = os.environ.get('ENABLE_LIKES', 'True').lower() == 'true'
    ENABLE_FOLLOWS = os.environ.get('ENABLE_FOLLOWS', 'True').lower() == 'true'
    ENABLE_AI_CHAT = os.environ.get('ENABLE_AI_CHAT', 'True').lower() == 'true'
    
    # Pagination
    POEMS_PER_PAGE = int(os.environ.get('POEMS_PER_PAGE', 20))
    USERS_PER_PAGE = int(os.environ.get('USERS_PER_PAGE', 20))
    COMMENTS_PER_PAGE = int(os.environ.get('COMMENTS_PER_PAGE', 10))
    
    # Content Limits
    MAX_POEM_TITLE_LENGTH = int(os.environ.get('MAX_POEM_TITLE_LENGTH', 200))
    MAX_POEM_CONTENT_LENGTH = int(os.environ.get('MAX_POEM_CONTENT_LENGTH', 10000))
    MAX_COMMENT_LENGTH = int(os.environ.get('MAX_COMMENT_LENGTH', 500))
    MAX_USERNAME_LENGTH = int(os.environ.get('MAX_USERNAME_LENGTH', 80))
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'instance/poetry_vault.log')
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # Ensure required directories exist
        Path('instance').mkdir(exist_ok=True)
        Path('instance/backups').mkdir(exist_ok=True)
        Path('instance/uploads').mkdir(exist_ok=True)
        
        # Setup logging
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug:
            # Create logs directory
            log_dir = Path(Config.LOG_FILE).parent
            log_dir.mkdir(exist_ok=True)
            
            # Setup file handler
            file_handler = RotatingFileHandler(
                Config.LOG_FILE,
                maxBytes=10240000,  # 10MB
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
            app.logger.addHandler(file_handler)
            
            app.logger.setLevel(getattr(logging, Config.LOG_LEVEL))
            app.logger.info(f'{Config.APP_NAME} startup')


class DevelopmentConfig(Config):
    """Development-specific configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True  # Log all SQL queries


class ProductionConfig(Config):
    """Production-specific configuration"""
    DEBUG = False
    TESTING = False
    
    # Force secure cookies in production
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    
    # Stricter security settings
    SESSION_COOKIE_SAMESITE = 'Strict'


class TestingConfig(Config):
    """Testing-specific configuration"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
