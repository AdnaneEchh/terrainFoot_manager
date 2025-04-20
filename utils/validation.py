"""
Input validation utilities for the Football Field Management System
"""

def validate_required(value, field_name):
    """Validate that a field is not empty"""
    if not value:
        return f"{field_name} is required"
    return None

def validate_integer(value, field_name, min_value=None, max_value=None):
    """Validate that a field is an integer within an optional range"""
    try:
        int_value = int(value)
        
        if min_value is not None and int_value < min_value:
            return f"{field_name} must be at least {min_value}"
        
        if max_value is not None and int_value > max_value:
            return f"{field_name} must be at most {max_value}"
        
        return None
    except ValueError:
        return f"{field_name} must be an integer"

def validate_float(value, field_name, min_value=None, max_value=None):
    """Validate that a field is a float within an optional range"""
    try:
        float_value = float(value)
        
        if min_value is not None and float_value < min_value:
            return f"{field_name} must be at least {min_value}"
        
        if max_value is not None and float_value > max_value:
            return f"{field_name} must be at most {max_value}"
        
        return None
    except ValueError:
        return f"{field_name} must be a number"

def validate_in_list(value, field_name, valid_values):
    """Validate that a field's value is in a list of valid values"""
    if value not in valid_values:
        return f"{field_name} must be one of: {', '.join(valid_values)}"
    return None

def validate_field_form(name, location, capacity, price_per_hour, status, valid_statuses):
    """Validate the football field form data"""
    errors = []
    
    # Validate required fields
    name_error = validate_required(name, "Field name")
    if name_error:
        errors.append(name_error)
    
    location_error = validate_required(location, "Location")
    if location_error:
        errors.append(location_error)
    
    # Validate numeric fields
    capacity_error = validate_integer(capacity, "Capacity", min_value=1)
    if capacity_error:
        errors.append(capacity_error)
    
    price_error = validate_float(price_per_hour, "Price per hour", min_value=0)
    if price_error:
        errors.append(price_error)
    
    # Validate status
    status_error = validate_in_list(status, "Status", valid_statuses)
    if status_error:
        errors.append(status_error)
    
    return errors