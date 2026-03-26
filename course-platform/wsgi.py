"""WSGI entry point for production deployment."""
from app import app, init_database

with app.app_context():
    init_database()

if __name__ == "__main__":
    app.run()
