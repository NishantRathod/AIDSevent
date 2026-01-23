"""
Configuration settings for KnowledgeShare application
"""

# Application Settings
SECRET_KEY = "secret123"  # Change this to a random secret key in production
DEBUG_MODE = True
HOST = "127.0.0.1"
PORT = 5000

# Token Economics
TOKENS = {
    'REGISTRATION_BONUS': 50,
    'UPLOAD_REWARD': 10,
    'VIEW_COST': 5,
    'DOWNLOAD_COST': 3
}

# File Upload Settings
UPLOAD_FOLDER = "uploads/pdfs"
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Database Settings
DATABASE_PATH = "database.db"

# Subject Categories
SUBJECTS = [
    "Computer Science",
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Engineering",
    "Business",
    "Economics",
    "Literature",
    "History",
    "Other"
]

# Pagination Settings
PDFS_PER_PAGE = 20
LEADERBOARD_SIZE = 20
RECENT_UPLOADS_LIMIT = 5
