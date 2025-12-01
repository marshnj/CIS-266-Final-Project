import os
import tkinter
import sqlite3
from tkinter import INSERT, messagebox

window = tkinter.Tk()
window.title("Password Reset form")
window.geometry('540x440')
window.configure(bg = 'lightgray')

# Reset method:  Checks the username and password against the login.db
def reset():
    # connect to login.db
    conn=sqlite3.connect('login.db')
    database_file = "login.db"
    # commit
    conn.commit()
    # create a cursor
    cursor=conn.cursor()
    # see if user_input and pass_input are in the db
    cursor.execute("SELECT * FROM login where username=? AND password = ?", ( user_input.get(), old_pass_input.get()))
    # fetch a row
    row=cursor.fetchone()
    # if the row exist for this use you can continue to check the password reset
    if row:
        # 
        if new_pass_input.get() == verify_pass_input.get():
            messagebox.showinfo(title="New and Verify Passwords Match", message="New Password and Verify Password match.")
            password_input = new_pass_input.get()
            if check_password_strength(password_input):
                messagebox.showinfo(title="Reset success!", message="Password is valid.")
                # here is where you call a dev to update the password for user_input
                update_password ()
            else:
                messagebox.showinfo(title="Reset failed!", message="Passwords must be 8 characters long with at least one upper case, one lower case, one number, and one special character.")
                print("Password is not valid.")
        else:
            messagebox.showinfo(title="Reset failed", message="New Password and Verify Password do not match.")
        conn.close()
    else:
    # if the row not exist for this user/password you can continue to check the password reset
        messagebox.showinfo(title="Reset failed", message="Username or old password are not valid.")
        conn.close()
    
def check_password_strength(password):
    """
    Checks the strength of a password based on several criteria.
    Returns True if the password meets all criteria, False otherwise.
    """
    min_length = 8
    has_uppercase = False
    has_lowercase = False
    has_digit = False
    has_special_char = False
    special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?/"

    # Check password length
    if len(password) < min_length:
        print(f"Password must be at least {min_length} characters long.")
        return False

    # Check for character types
    for char in password:
        if char.isupper():
            has_uppercase = True
        elif char.islower():
            has_lowercase = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special_char = True

    # Evaluate all criteria
    if not has_uppercase:
        messagebox.showinfo(title="Reset Error", message="Password must contain at least one uppercase letter.")
        return False
    if not has_lowercase:
        messagebox.showinfo(title="Reset Error", message="Password must contain at least one lowercase letter.")
        print("Password must contain at least one lowercase letter.")
        return False
    if not has_digit:
        messagebox.showinfo(title="Reset Error", message="Password must contain at least one digit.")
        print("Password must contain at least one digit.")
        return False
    if not has_special_char:
        messagebox.showinfo(title="Reset Error", message="Password must contain at least one special character.")       
        print("Password must contain at least one special character.")
        return False
        messagebox.showinfo(title="Reset Approved", message="Password meets all strength requirements.")       
    return True

def update_password ():
    # connect to login.db
    conn=sqlite3.connect('login.db')
    database_file = "login.db"
    # commit
    conn.commit()
    # create a cursor
    cursor=conn.cursor()
    cursor.execute("Update login SET password = ? WHERE username = ?", ( verify_pass_input.get(), user_input.get()))
    conn.commit()
    conn.close()

# method for hiding and showing the password
def unhide():
    if pass_hide.get() == 1:
        old_password_entry.config(show="")
        new_password_entry.config(show="")
        verify_password_entry.config(show="")
    else:
        old_password_entry.config(show="*")
        new_password_entry.config(show="*")
        verify_password_entry.config(show="*")

# Create string variables
user_input=tkinter.StringVar()
old_pass_input=tkinter.StringVar()
new_pass_input=tkinter.StringVar()
verify_pass_input=tkinter.StringVar()

# Create integer valiable
pass_hide= tkinter.IntVar()

# Create the frame
frame = tkinter.Frame(bg = 'lightgray')

# Creating Widgets for labels, entry fields, and buttons
# Place widgets on the screen using columns and rows

# Row 00 - Reset Password window label
reset_label = tkinter.Label(frame, text="Reset Password", font=("arial", 25, "bold"), bg = 'lightgray', fg = "#000000")
reset_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=20)

# Row 01 - Username label and entry field
username_label = tkinter.Label(frame, text="Username", font=("arial", 14), bg = 'lightgray', fg = "#000000")
username_label.grid(row=1, column=0, sticky=tkinter.E)
username_entry = tkinter.Entry(frame, textvariable=user_input, font=("arial", 14))
username_entry.grid(row=1, column=1, pady=5)

# Row 02 - Old password label and entry field
old_password_label = tkinter.Label(frame, text="Old Password", font=("arial", 14), bg = 'lightgray', fg = "#000000")
old_password_label.grid(row=2, column=0, sticky=tkinter.E, padx=5)
old_password_entry = tkinter.Entry(frame, textvariable=old_pass_input, show="*", font=("arial", 14))
old_password_entry.grid(row=2, column=1, pady=5)

# Row 03 - New password label and entry field
new_password_label = tkinter.Label(frame, text="New Password", font=("arial", 14), bg = 'lightgray', fg = "#000000")
new_password_label.grid(row=3, column=0, sticky=tkinter.E, padx=5)
new_password_entry = tkinter.Entry(frame, textvariable=new_pass_input, show="*", font=("arial", 14))
new_password_entry.grid(row=3, column=1, pady=5)

# Row 04 - Verify new password label and entry field
verify_password_entry = tkinter.Entry(frame, textvariable=verify_pass_input, show="*", font=("arial", 14))
verify_password_entry.grid(row=4, column=1, pady=5)
verify_password_label = tkinter.Label(frame, text="Verify Password", font=("arial", 14), bg = 'lightgray', fg = "#000000")
verify_password_label.grid(row=4, column=0, sticky=tkinter.E, padx=5)

# Row 05 - - Show/Hide Password checkbutton
hide_button = tkinter.Checkbutton(frame, text="Show Passwords", variable=pass_hide, command=unhide, bg = 'lightgray', font=("arial", 14))
hide_button.grid(row=5, column=1)

# Row 06 - Reset Password commit button
reset_button = tkinter.Button(frame, text="Reset", width=(25), font=("arial", 14), command=reset, bg = "#1820F2", fg = "#F5F0F0")
reset_button.grid(row=6, column=0, columnspan=2, pady=15)

frame.pack()

window.mainloop()