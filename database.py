"""
Database operations for the Football Field Management System
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from config import MONGO_URI, DB_NAME, COLLECTION_NAME
from bson.objectid import ObjectId

class Database:
    """Database class for MongoDB operations"""
    
    def __init__(self):
        """Initialize the database connection"""
        self.client = None
        self.db = None
        self.collection = None
        self.is_connected = False
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(MONGO_URI)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[DB_NAME]
            self.collection = self.db[COLLECTION_NAME]
            self.is_connected = True
            return True, "Connected to MongoDB successfully"
        except ConnectionFailure as e:
            self.is_connected = False
            return False, f"MongoDB connection failed: {str(e)}"
        except PyMongoError as e:
            self.is_connected = False
            return False, f"MongoDB error: {str(e)}"
    
    def create_field(self, field_data):
        """Create a new football field"""
        try:
            if not self.is_connected:
                success, message = self.connect()
                if not success:
                    return False, message
            
            result = self.collection.insert_one(field_data)
            return True, str(result.inserted_id)
        except PyMongoError as e:
            return False, f"Error creating field: {str(e)}"
    
    def get_all_fields(self):
        """Get all football fields"""
        try:
            if not self.is_connected:
                success, message = self.connect()
                if not success:
                    return False, message
            
            fields = list(self.collection.find())
            return True, fields
        except PyMongoError as e:
            return False, f"Error retrieving fields: {str(e)}"
    
    def get_field_by_id(self, field_id):
        """Get a football field by ID"""
        try:
            if not self.is_connected:
                success, message = self.connect()
                if not success:
                    return False, message
            
            field = self.collection.find_one({"_id": ObjectId(field_id)})
            if field:
                return True, field
            else:
                return False, "Field not found"
        except PyMongoError as e:
            return False, f"Error retrieving field: {str(e)}"
    
    def update_field(self, field_id, field_data):
        """Update a football field"""
        try:
            if not self.is_connected:
                success, message = self.connect()
                if not success:
                    return False, message
            
            result = self.collection.update_one(
                {"_id": ObjectId(field_id)},
                {"$set": field_data}
            )
            
            if result.matched_count > 0:
                return True, "Field updated successfully"
            else:
                return False, "Field not found"
        except PyMongoError as e:
            return False, f"Error updating field: {str(e)}"
    
    def delete_field(self, field_id):
        """Delete a football field"""
        try:
            if not self.is_connected:
                success, message = self.connect()
                if not success:
                    return False, message
            
            result = self.collection.delete_one({"_id": ObjectId(field_id)})
            
            if result.deleted_count > 0:
                return True, "Field deleted successfully"
            else:
                return False, "Field not found"
        except PyMongoError as e:
            return False, f"Error deleting field: {str(e)}"
    
    def search_fields(self, query):
        """Search for football fields"""
        try:
            if not self.is_connected:
                success, message = self.connect()
                if not success:
                    return False, message
            
            # Create a query that searches in name and location fields
            search_query = {
                "$or": [
                    {"name": {"$regex": query, "$options": "i"}},
                    {"location": {"$regex": query, "$options": "i"}}
                ]
            }
            
            fields = list(self.collection.find(search_query))
            return True, fields
        except PyMongoError as e:
            return False, f"Error searching fields: {str(e)}"
    
    def filter_fields_by_status(self, status):
        """Filter fields by status"""
        try:
            if not self.is_connected:
                success, message = self.connect()
                if not success:
                    return False, message
            
            fields = list(self.collection.find({"status": status}))
            return True, fields
        except PyMongoError as e:
            return False, f"Error filtering fields: {str(e)}"
    
    def close(self):
        """Close the database connection"""
        if self.client:
            self.client.close()
            self.is_connected = False