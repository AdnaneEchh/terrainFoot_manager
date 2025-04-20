"""
Add/Edit form for the Football Field Management System
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.field import Field
from config import FIELD_STATUS

class AddEditFieldFrame(ttk.Frame):
    """Frame for adding or editing football fields"""
    
    def __init__(self, parent, save_callback=None, cancel_callback=None):
        """Initialize the add/edit field frame"""
        super().__init__(parent)
        self.parent = parent
        self.save_callback = save_callback
        self.cancel_callback = cancel_callback
        
        # Create UI components
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI widgets"""
        # Form title
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill=tk.X, pady=10)
        
        self.title_label = ttk.Label(
            self.title_frame, 
            text="Add New Field",
            font=('Helvetica', 14, 'bold')
        )
        self.title_label.pack(side=tk.LEFT)
        
        # Create a form frame
        self.form_frame = ttk.Frame(self)
        self.form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Field name
        self.name_label = ttk.Label(self.form_frame, text="Field Name:")
        self.name_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.form_frame, textvariable=self.name_var, width=40)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Field location
        self.location_label = ttk.Label(self.form_frame, text="Location:")
        self.location_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.location_var = tk.StringVar()
        self.location_entry = ttk.Entry(self.form_frame, textvariable=self.location_var, width=40)
        self.location_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Field capacity
        self.capacity_label = ttk.Label(self.form_frame, text="Capacity:")
        self.capacity_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.capacity_var = tk.IntVar(value=10)
        self.capacity_entry = ttk.Spinbox(
            self.form_frame, 
            textvariable=self.capacity_var,
            from_=1, 
            to=100, 
            width=10
        )
        self.capacity_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Field price per hour
        self.price_label = ttk.Label(self.form_frame, text="Price per Hour ($):")
        self.price_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.price_var = tk.DoubleVar(value=20.0)
        self.price_entry = ttk.Spinbox(
            self.form_frame, 
            textvariable=self.price_var,
            from_=0.0, 
            to=1000.0, 
            increment=5.0,
            width=10
        )
        self.price_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Field status
        self.status_label = ttk.Label(self.form_frame, text="Status:")
        self.status_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.status_var = tk.StringVar(value=FIELD_STATUS[0])
        self.status_combobox = ttk.Combobox(
            self.form_frame, 
            textvariable=self.status_var,
            values=FIELD_STATUS,
            state="readonly",
            width=20
        )
        self.status_combobox.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Field description
        self.description_label = ttk.Label(self.form_frame, text="Description:")
        self.description_label.grid(row=5, column=0, sticky=tk.NW, pady=5)
        
        self.description_text = tk.Text(self.form_frame, width=40, height=5)
        self.description_text.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Button frame
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        # Save button
        self.save_button = ttk.Button(
            self.button_frame, 
            text="Save",
            command=self.on_save
        )
        self.save_button.pack(side=tk.RIGHT, padx=5)
        
        # Cancel button
        self.cancel_button = ttk.Button(
            self.button_frame, 
            text="Cancel",
            command=self.on_cancel
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=5)
        
        # Clear button
        self.clear_button = ttk.Button(
            self.button_frame, 
            text="Clear",
            command=self.clear
        )
        self.clear_button.pack(side=tk.RIGHT, padx=5)
    
    def on_save(self):
        """Handle save button click"""
        # Get field data from form
        try:
            field = Field(
                name=self.name_var.get(),
                location=self.location_var.get(),
                capacity=self.capacity_var.get(),
                price_per_hour=self.price_var.get(),
                status=self.status_var.get(),
                description=self.description_text.get("1.0", tk.END).strip()
            )
            
            # Validate field data
            errors = field.validate()
            if errors:
                messagebox.showerror("Validation Error", "\n".join(errors))
                return
            
            # Call save callback with field data
            if self.save_callback:
                self.save_callback(field.to_dict())
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def on_cancel(self):
        """Handle cancel button click"""
        if self.cancel_callback:
            self.cancel_callback()
    
    def clear(self):
        """Clear the form"""
        self.name_var.set("")
        self.location_var.set("")
        self.capacity_var.set(10)
        self.price_var.set(20.0)
        self.status_var.set(FIELD_STATUS[0])
        self.description_text.delete("1.0", tk.END)
        self.title_label.config(text="Add New Field")
    
    def set_field_data(self, field):
        """Set form data from a field object"""
        self.clear()
        
        self.name_var.set(field.get("name", ""))
        self.location_var.set(field.get("location", ""))
        self.capacity_var.set(field.get("capacity", 10))
        self.price_var.set(field.get("price_per_hour", 20.0))
        self.status_var.set(field.get("status", FIELD_STATUS[0]))
        self.description_text.insert("1.0", field.get("description", ""))
        
        self.title_label.config(text="Edit Field")