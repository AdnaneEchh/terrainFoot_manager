"""
Main window for the Football Field Management System
"""
import tkinter as tk
from tkinter import ttk, messagebox
from gui.fields_list import FieldsListFrame
from gui.form import AddEditFieldFrame
from gui.search import SearchFilterFrame
from database import Database

class MainWindow(ttk.Frame):
    """Main application window"""
    
    def __init__(self, parent):
        """Initialize the main window"""
        super().__init__(parent)
        self.parent = parent
        
        # Initialize database
        self.db = Database()
        success, message = self.db.connect()
        if not success:
            messagebox.showerror("Database Error", message)
        
        # Create UI components
        self.create_widgets()
        
        # Default state - no selected field
        self.selected_field_id = None
        
        # When the window is closed, close the database connection
        self.parent.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_widgets(self):
        """Create UI widgets"""
        # Main title
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.title_label = ttk.Label(
            self.title_frame, 
            text="Football Field Management System",
            font=('Helvetica', 16, 'bold')
        )
        self.title_label.pack(side=tk.LEFT)
        
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tab 1: Fields List
        self.fields_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.fields_tab, text="Fields")
        
        # Search and filter frame
        self.search_filter_frame = SearchFilterFrame(
            self.fields_tab,
            search_callback=self.search_fields,
            filter_callback=self.filter_fields,
            reset_callback=self.reset_fields
        )
        self.search_filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Fields list frame
        self.fields_list_frame = FieldsListFrame(
            self.fields_tab,
            edit_callback=self.edit_field,
            delete_callback=self.confirm_delete_field
        )
        self.fields_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tab 2: Add/Edit Field
        self.add_edit_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_edit_tab, text="Add/Edit Field")
        
        # Add/Edit form
        self.add_edit_form = AddEditFieldFrame(
            self.add_edit_tab,
            save_callback=self.save_field,
            cancel_callback=self.cancel_edit
        )
        self.add_edit_form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status bar
        self.status_bar = ttk.Label(
            self,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)
        
        # Load fields on startup
        self.load_fields()
    
    def load_fields(self):
        """Load all fields from the database"""
        success, result = self.db.get_all_fields()
        if success:
            self.fields_list_frame.load_fields(result)
            self.status_bar.config(text=f"Loaded {len(result)} fields")
        else:
            messagebox.showerror("Error", result)
            self.status_bar.config(text="Error loading fields")
    
    def search_fields(self, query):
        """Search fields by query"""
        if not query:
            self.load_fields()
            return
        
        success, result = self.db.search_fields(query)
        if success:
            self.fields_list_frame.load_fields(result)
            self.status_bar.config(text=f"Found {len(result)} fields matching '{query}'")
        else:
            messagebox.showerror("Error", result)
            self.status_bar.config(text="Error searching fields")
    
    def filter_fields(self, status):
        """Filter fields by status"""
        success, result = self.db.filter_fields_by_status(status)
        if success:
            self.fields_list_frame.load_fields(result)
            self.status_bar.config(text=f"Found {len(result)} fields with status '{status}'")
        else:
            messagebox.showerror("Error", result)
            self.status_bar.config(text="Error filtering fields")
    
    def reset_fields(self):
        """Reset fields to show all"""
        self.load_fields()
        self.search_filter_frame.reset()
    
    def edit_field(self, field_id):
        """Edit a field"""
        success, field = self.db.get_field_by_id(field_id)
        if success:
            self.selected_field_id = field_id
            self.add_edit_form.set_field_data(field)
            self.notebook.select(1)  # Switch to Add/Edit tab
            self.status_bar.config(text=f"Editing field: {field['name']}")
        else:
            messagebox.showerror("Error", field)
            self.status_bar.config(text="Error loading field for editing")
    
    def save_field(self, field_data):
        """Save a field (create or update)"""
        if self.selected_field_id:  # Update existing field
            success, message = self.db.update_field(self.selected_field_id, field_data)
            if success:
                messagebox.showinfo("Success", "Field updated successfully")
                self.selected_field_id = None
                self.add_edit_form.clear()
                self.notebook.select(0)  # Switch to Fields tab
                self.load_fields()
                self.status_bar.config(text="Field updated successfully")
            else:
                messagebox.showerror("Error", message)
                self.status_bar.config(text="Error updating field")
        else:  # Create new field
            success, message = self.db.create_field(field_data)
            if success:
                messagebox.showinfo("Success", "Field created successfully")
                self.add_edit_form.clear()
                self.notebook.select(0)  # Switch to Fields tab
                self.load_fields()
                self.status_bar.config(text="Field created successfully")
            else:
                messagebox.showerror("Error", message)
                self.status_bar.config(text="Error creating field")
    
    def confirm_delete_field(self, field_id):
        """Confirm field deletion"""
        success, field = self.db.get_field_by_id(field_id)
        if success:
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete the field '{field['name']}'?"
            )
            if confirm:
                self.delete_field(field_id)
        else:
            messagebox.showerror("Error", field)
    
    def delete_field(self, field_id):
        """Delete a field"""
        success, message = self.db.delete_field(field_id)
        if success:
            messagebox.showinfo("Success", "Field deleted successfully")
            self.load_fields()
            self.status_bar.config(text="Field deleted successfully")
        else:
            messagebox.showerror("Error", message)
            self.status_bar.config(text="Error deleting field")
    
    def cancel_edit(self):
        """Cancel field editing"""
        self.selected_field_id = None
        self.add_edit_form.clear()
        self.notebook.select(0)  # Switch to Fields tab
        self.status_bar.config(text="Edit cancelled")
    
    def on_close(self):
        """Handle window close event"""
        # Close database connection
        if self.db:
            self.db.close()
        
        # Destroy the window
        self.parent.destroy()