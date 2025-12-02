# Added these imports - Nick
import os
import sys
import re

import tkinter as tk
from tkinter import ttk, messagebox


class MainWindowUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Assets")
        self.root.geometry("1400x650")
        
        # Real user data - modified to use username and status passed from LOGIN - Nick
        self.current_user = user_name
        if user_status == "ADMIN":
            self.is_admin = True
        else:
            self.is_admin = False          
        
        self.create_widgets()
        self.load_sample_data()
        
    def create_widgets(self):
        """Create the main Assets window UI"""
        
        # Top frame for user info and logout
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=5)
        
        # Modified to use passed user_status - Nick
        role = "Administrator" if self.is_admin else "USER"
        tk.Label(top_frame, text=f"Logged in as: {self.current_user} ({role})", 
                font=('Arial', 10)).pack(side='left')
        
        tk.Button(top_frame, text="Logout", command=self.logout, width=10).pack(side='right')
        
        # Admin menu access
        if self.is_admin:
            tk.Button(top_frame, text="Manage Users", command=self.manage_users, 
                     width=12).pack(side='right', padx=5)
        
        # Button bar
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        self.search_btn = tk.Button(btn_frame, text="Search", width=12, command=self.search_assets)
        self.search_btn.pack(side='left', padx=2)
        
        self.checkout_btn = tk.Button(btn_frame, text="Check-out", width=12, command=self.checkout_asset)
        self.checkout_btn.pack(side='left', padx=2)
        
        self.checkin_btn = tk.Button(btn_frame, text="Check-in", width=12, command=self.checkin_asset)
        self.checkin_btn.pack(side='left', padx=2)
        
        self.edit_btn = tk.Button(btn_frame, text="Edit", width=12, command=self.edit_asset)
        self.edit_btn.pack(side='left', padx=2)
        
        self.add_btn = tk.Button(btn_frame, text="Add", width=12, command=self.add_asset)
        self.add_btn.pack(side='left', padx=2)
        
        self.delete_btn = tk.Button(btn_frame, text="Delete", width=12, command=self.delete_asset)
        self.delete_btn.pack(side='left', padx=2)
        
        # Admin-only buttons grayed out for regular users
        if not self.is_admin:
            self.edit_btn.config(state='disabled', bg='lightgray')
            self.add_btn.config(state='disabled', bg='lightgray')
            self.delete_btn.config(state='disabled', bg='lightgray')
            
            note_label = tk.Label(self.root, text="Greyed out buttons are only available to the Administrator", 
                                 font=('Arial', 9, 'italic'), fg='gray')
            note_label.pack()
        
        # Frame for table
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for assets
        columns = ('Asset ID', 'Asset Name', 'Manufacturer', 'Serial Number', 'Purchase Date', 
                  'Initial Cost', 'Depreciation', 'Location', 'Condition', 'Maintenance', 'Check Out Status')
        
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == 'Asset ID':
                self.tree.column(col, width=80)
            elif col in ['Initial Cost', 'Depreciation']:
                self.tree.column(col, width=100)
            elif col == 'Maintenance':
                self.tree.column(col, width=90)
            else:
                self.tree.column(col, width=120)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def load_sample_data(self):
        """Load sample asset data for demo"""
        sample_assets = [
            ('ASSET-0001', 'Scalpel Handle #3', 'Medline', 'SN123456789', '2023-01-15', 
             '25.00', '15.00', 'Nursing Skills Lab', 'Good', 'No', 'Available'),
            ('ASSET-0002', 'Disposable Syringe 10ml', 'BD', 'SN987654321', '2022-06-20', 
             '2.00', '1.00', 'Classroom Supply Cabinet', 'Fair', 'Yes', 'Available'),
            ('ASSET-0003', 'Suture Kit – Absorbable', 'Ethicon', 'SN555666777', '2023-09-10', 
             '45.00', '35.00', 'Simulation Lab', 'Excellent', 'No', 'Checked Out'),
            ('ASSET-0004', 'Surgical Forceps', 'Sklar', 'SN111222333', '2021-03-05', 
             '60.00', '30.00', 'Sterile Practice Station', 'Good', 'No', 'Available'),
            ('ASSET-0005', 'IV Start Kit', 'Cardinal Health', 'SN444555666', '2024-01-20', 
             '75.00', '65.00', 'Skills Practice Cart', 'Excellent', 'No', 'Available'),
            ('ASSET-0006', 'Needle Holder', 'Aesculap', 'SN777888999', '2022-11-12', 
             '40.00', '20.00', 'Lab Storage Room', 'Poor', 'Yes', 'Available'),
            ('ASSET-0007', 'Surgical Scissors', 'Miltex', 'SN000111222', '2020-08-15', 
             '55.00', '25.00', 'Nursing Classroom 102', 'Good', 'No', 'Checked Out'),
            ('ASSET-0008', 'Disposable Scalpel Blades', 'Feather', 'SN333444555', '2023-05-08', 
             '15.00', '10.00', 'Supply Prep Area', 'Excellent', 'No', 'Available'),
        ]
        
        for asset in sample_assets:
            self.tree.insert('', 'end', values=asset)
    
    def on_select(self, event):
        """Handle item selection"""
        selected = self.tree.selection()
        if selected:
            print(f"Selected: {self.tree.item(selected[0])['values'][0]}")
    
    # Button command handlers (demo only)
    def search_assets(self):
        messagebox.showinfo("Search", "Search functionality - opens search dialog")
    
    def checkout_asset(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an asset to check out")
            return
        asset_id = self.tree.item(selected[0])['values'][0]
        messagebox.showinfo("Check-out", f"Checked out asset: {asset_id}")
    
    def checkin_asset(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an asset to check in")
            return
        asset_id = self.tree.item(selected[0])['values'][0]
        messagebox.showinfo("Check-in", f"Checked in asset: {asset_id}")
    
    def edit_asset(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an asset to edit")
            return
        messagebox.showinfo("Edit", "Edit functionality - opens edit form")
    
    def add_asset(self):
        messagebox.showinfo("Add", "Add functionality - opens add form")
    
    def delete_asset(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an asset to delete")
            return
        if messagebox.askyesno("Confirm", "Delete selected asset?"):
            self.tree.delete(selected[0])
            messagebox.showinfo("Success", "Asset deleted")
    
    def manage_users(self):
        messagebox.showinfo("Users", "User management - opens users window")
        # Modified to call the userview UI - Nick
        os.system("userview.py")
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Main entry point
if __name__ == "__main__":

    # Added this to read the passed current username and status (USER or ADMIN) from the login process - Nick
    if len(sys.argv) > 1:
        user_name = sys.argv[1]
        user_status = sys.argv[2]

    app = MainWindowUI()
    app.run()