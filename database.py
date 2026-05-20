import os
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Brukermodell med autentisering og datalagrting"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Fleksibel JSON-lagring for brukerdata
    user_data = db.Column(db.Text, default='{}')
    
    def set_password(self, password):
        """Hash og lagre passord"""
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Sjekk om passord matcher"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def get_data(self, key=None):
        """Hent brukerdata fra JSON-lagring"""
        try:
            data = json.loads(self.user_data or '{}')
            if key:
                return data.get(key)
            return data
        except:
            return {} if key is None else None
    
    def set_data(self, key, value):
        """Sett brukerdata i JSON-lagring"""
        try:
            data = json.loads(self.user_data or '{}')
            data[key] = value
            self.user_data = json.dumps(data)
        except:
            self.user_data = json.dumps({key: value})

def init_db(app):
    """Initialisер databasen"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
