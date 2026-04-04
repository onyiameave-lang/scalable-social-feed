import os

class Config:
    # Use Render's DB if available, otherwise use local
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Render uses 'postgres://', but SQLAlchemy needs 'postgresql://'
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    # If no environment variable, use your local Termux DB
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres@localhost/scalable_social_feed"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'another-secret-key'

