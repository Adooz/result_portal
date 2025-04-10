import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')  # Default for development
    ACCESS_CODE_DB = 'data/access_codes.json'
    STUDENT_DB = 'data/students.json'
    RESULTS_FOLDER = 'results'
