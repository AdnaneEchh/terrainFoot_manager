import tkinter as tk
from tkinter import ttk
from gui.main_window import MainWindow
from config import APP_TITLE, APP_SIZE

def main():
    """Main application entry point"""
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}")
    root.minsize(800, 600)
    
    # Use ttk theme
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure styles
    style.configure("TFrame", background="#f5f5f5")
    style.configure("TButton", padding=6, relief="flat", background="#3498db", foreground="white")
    style.configure("TLabel", background="#f5f5f5", font=('Helvetica', 10))
    style.configure("TEntry", padding=5)
    style.configure("Heading.TLabel", font=('Helvetica', 12, 'bold'))
    
    # Initialize main window
    app = MainWindow(root)
    app.pack(fill=tk.BOTH, expand=True)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()