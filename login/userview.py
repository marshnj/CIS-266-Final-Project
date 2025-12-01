import sqlite3
import os
import tkinter as tk
from tkinter import ttk, messagebox
root = tk.Tk()
root.title("SQLite User Data Viewer")
root.geometry("1400x350")

conn = sqlite3.connect('login.db')
cursor = conn.cursor()

# Create a Treeview widget
tree = ttk.Treeview(root, columns=("Username", "Password", "First Name", "Middle Initial", "Last Name", "Email", "Status"), show="headings")
tree.heading("Username", text="Username")
tree.heading("Password", text="Password")
tree.heading("First Name", text="First Name")
tree.heading("Middle Initial", text="Middle Initial")
tree.heading("Last Name", text="Last Name")
tree.heading("Email", text="Email")
tree.heading("Status", text="Status")
tree.pack(pady=10)

# Switch to Assets UI
def access_assets():
    messagebox.showinfo(title="Asset Management", message="You are switching to the Asset Management UI.")
    script_name = "assets.py"
    current_user_status = "ADMIN"
    command = f"python {script_name} {""} {""} {""} {""} {""} {""} {""} {current_user_status}"
    os.system(command)
    conn.close() 
    sys.exit()  

# Function to load data into the Treeview
def load_data():
    for item in tree.get_children():
        tree.delete(item)  # Clear existing data
    cursor.execute("SELECT * FROM login")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def edit_selected_user():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select one or more rows to edit.")
        return
    
    # messagebox.showinfo("Edit", "Edit functionality - opens edit form")
    # Extract Usernames of selected rows
    for item in selected_item:
        username = tree.item(item, "values")[0]  # Get the username from the Treeview
        password = tree.item(item, "values")[1]  # Get the password from the Treeview 
        firstname = tree.item(item, "values")[2]  # Get the firstname from the Treeview
        mi = tree.item(item, "values")[3]  # Get the mi from the Treeview
        lastname = tree.item(item, "values")[4]  # Get the Lastname from the Treeview
        email = tree.item(item, "values")[5]  # Get the email from the Treeview
        status = tree.item(item, "values")[6]  # Get the status from the Treeview

    # messagebox.showinfo("Info", f"Current selection, {username}, {password}, {firstname}, {mi}, {lastname}, {email}, {status}")
    script_name = "accountadmin.py"
    command = f"python {script_name} {username} \"{password}\" {firstname} \"{mi}\" {lastname} \"{email}\" {status}"

    os.system(command)
    load_data()

def add_new_user():
    # messagebox.showinfo("Add", "Add functionality - opens add form")
    os.system("accountadmin.py")
    load_data()

# Function to delete selected rows
def delete_selected_rows():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("No Selection", "Please select one or more rows to delete.")
        return

    # Extract Usernames of selected rows
    uns_to_delete = []
    for item in selected_items:
        db_un = tree.item(item, "values")[0]  # Get the Username from the Treeview
        uns_to_delete.append(db_un)

    # Delete from the database
    try:
        # Use executemany for deleting multiple rows efficiently
        cursor.executemany("DELETE FROM login WHERE username = ?", [(username,) for username in uns_to_delete])
        conn.commit()
        messagebox.showinfo("Success", f"{len(uns_to_delete)} row(s) deleted successfully.")
        load_data()  # Refresh the Treeview
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error deleting rows: {e}")

# Button bar
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Edit button
edit_btn = tk.Button(button_frame, text="Edit", width=12, command=edit_selected_user)
edit_btn.pack(side='left', padx=2, pady=20)

# Add button       
add_btn = tk.Button(button_frame, text="Add", width=12, command=add_new_user)
add_btn.pack(side='left', padx=2, pady=20)

# Delete button 
delete_button = tk.Button(button_frame, text="Delete Rows", width=12, command=delete_selected_rows)
delete_button.pack(side='left', padx=2, pady=20)

# Delete button 
delete_button = tk.Button(button_frame, text="Manage Assets", width=12, command=access_assets)
delete_button.pack(side='left', padx=2, pady=20)

# Initial data load
load_data()

root.mainloop()

# Close the database connection when the application exits
conn.close()