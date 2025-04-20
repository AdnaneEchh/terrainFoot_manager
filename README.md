# Football Field Management System

A desktop application built with Python, Flask, and Tkinter for managing football fields with MongoDB as the database.

## Features

- **CRUD Operations**: Create, read, update, and delete football fields
- **Search & Filter**: Find fields by name, location, or status
- **Data Validation**: Prevent input errors with comprehensive validation
- **Visual Status Indicators**: Color-coded status for quick visual reference
- **Intuitive UI**: Well-organized tabbed interface and context menus

## Requirements

- Python 3.6+
- MongoDB (local or MongoDB Atlas)
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Configure MongoDB connection:
   - Create a `.env` file with the following variables:
     ```
     MONGO_URI=mongodb://localhost:27017/
     DB_NAME=football_field_management
     COLLECTION_NAME=fields
     ```
   - Or modify these settings directly in `config.py`

## Usage

Run the application:
```
python app.py
```

### Adding a Field

1. Navigate to the "Add/Edit Field" tab
2. Fill in the required information
3. Click "Save"

### Editing a Field

1. In the "Fields" tab, double-click on any field
2. Modify the information in the form
3. Click "Save"

### Deleting a Field

1. In the "Fields" tab, select a field
2. Right-click and select "Delete" or click the "Delete" button
3. Confirm the deletion

### Searching and Filtering

- Use the search box to find fields by name or location
- Use the status filter to view fields with a specific status

## Project Structure

- `app.py`: Main application entry point
- `config.py`: Configuration settings
- `database.py`: MongoDB connection and operations
- `models/`: Data models
- `gui/`: Tkinter GUI components
- `utils/`: Utility functions

## License

This project is licensed under the MIT License.

## Future Enhancements

- Booking/reservation functionality
- Field image support
- Data export to CSV/PDF

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.