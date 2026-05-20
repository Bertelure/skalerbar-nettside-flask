import os

class Config:
    """Grunnleggende konfigurasjonsinnstillinger"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # Relativ sti til database
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db', 'database.db').replace('\\', '/')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = False  # Sett til True i produksjon med HTTPS
    SESSION_COOKIE_HTTPONLY = True

class DevelopmentConfig(Config):
    """Utviklingsmiljø"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Produksjonsmiljø"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testmiljø"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Menysystem - enkelt å utvide
MENU_ITEMS = [
    {'name': 'Hjem', 'url': '/', 'icon': '🏠'},
    {'name': 'Om oss', 'url': '/about', 'icon': 'ℹ️'},
    {'name': 'Kontakt', 'url': '/contact', 'icon': '📧'},
]
