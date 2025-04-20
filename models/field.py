"""
Field data model for Football Field Management System
"""
from datetime import datetime

class Field:
    """Football Field data model"""
    
    def __init__(self, 
                 name, 
                 location, 
                 capacity=10, 
                 price_per_hour=20.0, 
                 status="Available", 
                 description="",
                 _id=None):
        """Initialize a new football field"""
        self._id = _id
        self.name = name
        self.location = location
        self.capacity = capacity
        self.price_per_hour = price_per_hour
        self.status = status
        self.description = description
        self.created_at = datetime.now().isoformat() if not _id else None
        self.updated_at = None
    
    def to_dict(self):
        """Convert the field to a dictionary for MongoDB"""
        field_dict = {
            "name": self.name,
            "location": self.location,
            "capacity": self.capacity,
            "price_per_hour": self.price_per_hour,
            "status": self.status,
            "description": self.description,
            "updated_at": datetime.now().isoformat()
        }
        
        # Include created_at only for new fields
        if self.created_at:
            field_dict["created_at"] = self.created_at
            
        return field_dict
    
    @classmethod
    def from_dict(cls, field_dict):
        """Create a Field object from a dictionary from MongoDB"""
        return cls(
            _id=field_dict.get("_id"),
            name=field_dict.get("name", ""),
            location=field_dict.get("location", ""),
            capacity=field_dict.get("capacity", 10),
            price_per_hour=field_dict.get("price_per_hour", 20.0),
            status=field_dict.get("status", "Available"),
            description=field_dict.get("description", "")
        )
    
    def validate(self):
        """Validate the field data"""
        errors = []
        
        if not self.name:
            errors.append("Name is required")
        
        if not self.location:
            errors.append("Location is required")
        
        if not isinstance(self.capacity, int) or self.capacity <= 0:
            errors.append("Capacity must be a positive integer")
        
        if not isinstance(self.price_per_hour, (int, float)) or self.price_per_hour < 0:
            errors.append("Price per hour must be a non-negative number")
        
        if not self.status in ["Available", "Under Maintenance", "Booked"]:
            errors.append("Status must be 'Available', 'Under Maintenance', or 'Booked'")
        
        return errors