"""
Search and filter functionality for the Football Field Management System
"""
import tkinter as tk
from tkinter import ttk
from config import FIELD_STATUS

class SearchFilterFrame(ttk.Frame):
    """Frame for search and filter functionality"""
    
    def __init__(self, parent, search_callback=None, filter_callback=None, reset_callback=None):
        """Initialize the search and filter frame"""
        super().__init__(parent)
        self.parent = parent
        self.search_callback = search_callback
        self.filter_callback = filter_callback
        self.reset_callback = reset_callback
        
        # Create UI components
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI widgets"""
        # Search frame
        self.search_frame = ttk.Frame(self)
        self.search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        # Search label
        self.search_label = ttk.Label(self.search_frame, text="Search:")
        self.search_label.pack(side=tk.LEFT, padx=5)
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        # Search button
        self.search_button = ttk.Button(
            self.search_frame, 
            text="Search",
            command=self.on_search
        )
        self.search_button.pack(side=tk.LEFT, padx=5)
        
        # Filter frame
        self.filter_frame = ttk.Frame(self)
        self.filter_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        # Filter label
        self.filter_label = ttk.Label(self.filter_frame, text="Filter by Status:")
        self.filter_label.pack(side=tk.LEFT, padx=5)
        
        # Filter combobox
        self.filter_var = tk.StringVar()
        self.filter_combobox = ttk.Combobox(
            self.filter_frame, 
            textvariable=self.filter_var,
            values=FIELD_STATUS,
            state="readonly",
            width=20
        )
        self.filter_combobox.pack(side=tk.LEFT, padx=5)
        
        # Filter button
        self.filter_button = ttk.Button(
            self.filter_frame, 
            text="Filter",
            command=self.on_filter
        )
        self.filter_button.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        self.reset_button = ttk.Button(
            self.filter_frame, 
            text="Reset",
            command=self.on_reset
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Bind events
        self.search_entry.bind("<Return>", lambda event: self.on_search())
    
    def on_search(self):
        """Handle search button click"""
        query = self.search_var.get().strip()
        if self.search_callback:
            self.search_callback(query)
    
    def on_filter(self):
        """Handle filter button click"""
        status = self.filter_var.get()
        if status and self.filter_callback:
            self.filter_callback(status)
    
    def on_reset(self):
        """Handle reset button click"""
        self.reset()
        if self.reset_callback:
            self.reset_callback()
    
    def reset(self):
        """Reset search and filter fields"""
        self.search_var.set("")
        self.filter_var.set("")