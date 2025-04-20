"""
Configuration settings for the Football Field Management System
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Application settings
APP_TITLE = "Football Field Management System"
APP_SIZE = (1024, 768)

# MongoDB settings
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "football_field_management")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "fields")

# Field status options
FIELD_STATUS = ["Available", "Under Maintenance", "Booked"]

# Default field values
DEFAULT_FIELD = {
    "name": "",
    "location": "",
    "capacity": 10,
    "price_per_hour": 20.0,
    "is_available": True,
    "status": "Available",
    "description": ""
}

# Color settings
COLORS = {
    "primary": "#3498db",    # Blue
    "secondary": "#2ecc71",  # Green
    "accent": "#e74c3c",     # Red
    "bg_light": "#f5f5f5",   # Light gray
    "bg_dark": "#34495e",    # Dark blue/gray
    "text_primary": "#2c3e50", # Dark blue/gray
    "text_secondary": "#7f8c8d", # Gray
    "available": "#2ecc71",  # Green
    "maintenance": "#f39c12", # Yellow
    "booked": "#e74c3c"      # Red
}