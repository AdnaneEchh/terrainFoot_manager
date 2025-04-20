"""
Export utilities for the Football Field Management System
"""
import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def export_to_csv(fields, default_filename="football_fields.csv"):
    """Export fields data to CSV file"""
    if not fields:
        messagebox.showerror("Export Error", "No data to export")
        return False
    
    # Ask for file location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        initialfile=default_filename
    )
    
    if not file_path:  # User cancelled
        return False
    
    try:
        with open(file_path, 'w', newline='') as csvfile:
            # Get field keys from first record (assuming all records have same structure)
            fieldnames = list(fields[0].keys())
            
            # Remove MongoDB ObjectId from fieldnames
            if '_id' in fieldnames:
                fieldnames.remove('_id')
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for field in fields:
                # Create a new dict without _id
                field_data = {k: v for k, v in field.items() if k != '_id'}
                writer.writerow(field_data)
        
        messagebox.showinfo("Export Successful", f"Data exported to {os.path.basename(file_path)}")
        return True
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred: {str(e)}")
        return False

def generate_report(fields, report_type="summary"):
    """Generate a report about the fields"""
    if not fields:
        return "No data available for report"
    
    if report_type == "summary":
        # Count by status
        status_counts = {}
        for field in fields:
            status = field.get("status", "Unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Calculate average price
        total_price = sum(field.get("price_per_hour", 0) for field in fields)
        avg_price = total_price / len(fields) if fields else 0
        
        # Calculate total capacity
        total_capacity = sum(field.get("capacity", 0) for field in fields)
        
        # Generate report
        report = [
            "Football Fields Summary Report",
            "==============================",
            f"Total fields: {len(fields)}",
            f"Average price per hour: ${avg_price:.2f}",
            f"Total capacity: {total_capacity}",
            "\nStatus Distribution:",
        ]
        
        for status, count in status_counts.items():
            report.append(f"- {status}: {count}")
        
        return "\n".join(report)
    
    return "Unknown report type"