"""
Fields list display for the Football Field Management System
"""
import tkinter as tk
from tkinter import ttk
from config import COLORS

class FieldsListFrame(ttk.Frame):
    """Frame for displaying the list of football fields"""
    
    def __init__(self, parent, edit_callback=None, delete_callback=None):
        """Initialize the fields list frame"""
        super().__init__(parent)
        self.parent = parent
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback
        
        # Store the fields data
        self.fields = []
        
        # Create the UI components
        self.create_widgets()
    
    def create_widgets(self):
        """Create the UI widgets"""
        # Create the treeview for displaying fields
        columns = ("name", "location", "capacity", "price", "status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        # Configure the columns
        self.tree.heading("name", text="Name", command=lambda: self.sort_by_column("name", False))
        self.tree.heading("location", text="Location", command=lambda: self.sort_by_column("location", False))
        self.tree.heading("capacity", text="Capacity", command=lambda: self.sort_by_column("capacity", False))
        self.tree.heading("price", text="Price/Hour", command=lambda: self.sort_by_column("price", False))
        self.tree.heading("status", text="Status", command=lambda: self.sort_by_column("status", False))
        
        # Configure column widths
        self.tree.column("name", width=150, minwidth=100)
        self.tree.column("location", width=150, minwidth=100)
        self.tree.column("capacity", width=100, minwidth=80)
        self.tree.column("price", width=100, minwidth=80)
        self.tree.column("status", width=120, minwidth=100)
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<ButtonRelease-1>", self.on_select)
        
        # Add a context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_selected)
        self.context_menu.add_command(label="Delete", command=self.delete_selected)
        
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        # Add a toolbar frame for actions
        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        # Add buttons
        self.refresh_button = ttk.Button(self.toolbar, text="Refresh", command=self.refresh)
        self.refresh_button.pack(side=tk.LEFT, padx=5)
        
        self.edit_button = ttk.Button(self.toolbar, text="Edit", command=self.edit_selected, state=tk.DISABLED)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(self.toolbar, text="Delete", command=self.delete_selected, state=tk.DISABLED)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # Selected item ID
        self.selected_id = None
    
    def load_fields(self, fields):
        """Load fields into the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Store the fields data
        self.fields = fields
        
        # Add fields to the treeview
        for field in fields:
            # Set tag based on status for color coding
            status = field.get("status", "Available")
            tag = status.lower().replace(" ", "_")
            
            self.tree.insert(
                "",
                tk.END,
                values=(
                    field.get("name", ""),
                    field.get("location", ""),
                    field.get("capacity", ""),
                    f"${field.get('price_per_hour', 0):.2f}",
                    status
                ),
                tags=(tag, str(field["_id"]))
            )
        
        # Configure tags for color coding
        self.tree.tag_configure("available", background=COLORS["available"])
        self.tree.tag_configure("under_maintenance", background=COLORS["maintenance"])
        self.tree.tag_configure("booked", background=COLORS["booked"])
    
    def on_select(self, event):
        """Handle selection event"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            item_tags = self.tree.item(item, "tags")
            if len(item_tags) > 1:  # The second tag is the ID
                self.selected_id = item_tags[1]
                # Enable buttons
                self.edit_button.config(state=tk.NORMAL)
                self.delete_button.config(state=tk.NORMAL)
            else:
                self.selected_id = None
                # Disable buttons
                self.edit_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.DISABLED)
        else:
            self.selected_id = None
            # Disable buttons
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
    
    def on_double_click(self, event):
        """Handle double-click event"""
        self.edit_selected()
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        # Select the item under the mouse
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            item_tags = self.tree.item(item, "tags")
            if len(item_tags) > 1:  # The second tag is the ID
                self.selected_id = item_tags[1]
                # Show context menu
                self.context_menu.post(event.x_root, event.y_root)
    
    def edit_selected(self):
        """Edit the selected field"""
        if self.selected_id and self.edit_callback:
            self.edit_callback(self.selected_id)
    
    def delete_selected(self):
        """Delete the selected field"""
        if self.selected_id and self.delete_callback:
            self.delete_callback(self.selected_id)
    
    def refresh(self):
        """Refresh the fields list"""
        # This will be implemented by the parent
        pass
    
    def sort_by_column(self, column, reverse):
        """Sort treeview by column"""
        # Get column index
        column_index = {
            "name": 0,
            "location": 1,
            "capacity": 2,
            "price": 3,
            "status": 4
        }.get(column, 0)
        
        # Get all items with their values
        l = [(self.tree.set(k, column), k) for k in self.tree.get_children('')]
        
        # Special handling for capacity and price (numeric values)
        if column in ["capacity", "price"]:
            # Extract numeric value for sorting
            l = [(float(v.replace('$', '')) if v else 0, k) for v, k in l]
        
        # Sort the list
        l.sort(reverse=reverse)
        
        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        
        # Reverse sort next time
        self.tree.heading(column, command=lambda: self.sort_by_column(column, not reverse))