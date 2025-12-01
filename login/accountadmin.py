import os
import sys
import re
import tkinter
import sqlite3
from tkinter import INSERT, messagebox

#window = tkinter.Tk()
#window.title("Account Request Form")
#window.geometry('540x440')
#window.configure(bg = 'lightgray')

# Create root and frame
root = tkinter.Tk()
root.title("Account Request form")
root.geometry('400x440')
frame = tkinter.Frame(root, bg = 'lightgray')
frame.pack(fill=tkinter.BOTH, expand=True)

def account():

    # Acccount method:  Validates new account request

    # connect to login.db
    conn=sqlite3.connect('login.db')
    database_file = "login.db"
    # if the file exists, show a message
    if os.path.isfile(database_file):
        print(f"The SQLite database '{database_file}' exists.")
    # if the file does not exist, create it and commit an admin record
    else:
        print(f"The SQLite database '{database_file}' does not exist.")
        conn.execute('CREATE TABLE IF NOT EXISTS login(username TEXT, password TEXT, firstname TEXT, mi TEXT, lastname TEXT, email TEXT, status TEXT)')
        conn.execute("INSERT INTO login(username, password, firstname, mi, lastname, email, status) VALUES('admin','admin','John', 'A', 'Smith', 'john.a.smith@gmail.com', 'ADMIN')")
    # commit
    conn.commit()
    # create a cursor
    cursor=conn.cursor()
    # see if user_input and pass_input are in the db
    cursor.execute("SELECT * FROM login where username=? AND password = ?", ( user_input.get(), pass_input.get()))
    # fetch a row
    row=cursor.fetchone()
    # if the row exist for this user/password you already have an account
    # this is where you will call another py to run
    # else create an account
    if row and len(sys.argv) < 1:
        # If this username and password already exist in login.db, then you can't create another account
        messagebox.showinfo(title="Account Exists", message="This user name already exists!")
        conn.close()
    else:
        # Check password strength, first, mi, last only contain letters, and valid e-mail format
        if check_password_strength(pass_input.get()):
            if is_valid_name(firstname_input.get()):
                if is_valid_name(middleinitial_input.get()):
                    if is_valid_name(lastname_input.get()):
                        if is_valid_email(email_input.get()):
                            # create a new user in login.db.  
                            # Status set to NEW. 
                            # Can't login until the admin sets the status to USER
                            create_user(user_input, pass_input, firstname_input, middleinitial_input, lastname_input, email_input, status_var)
                            conn.close()
                        else:
                            # Email address is not valid
                            messagebox.showinfo(title="Email address is invalid", message="Email address is not the correct format")
                            conn.close()
                    else:
                        # Last name has something other than letters
                        messagebox.showinfo(title="Last Name is invalid", message="Last names can only contain letters.")
                        conn.close()
                else:
                    # Middle initial is not a letter
                    messagebox.showinfo(title="Middle Initial is invalid", message="Middle initials can only contain letters.")
                    conn.close()
            else:
                # First name has something other than letters 
                messagebox.showinfo(title="First Name is invalid", message="First names can only contain letters.")
                conn.close()        
        else:
            # Password is not strong enough
            messagebox.showinfo(title="Password is invalid", message="Passwords must be 8 characters long with at least one upper case, one lower case, one number, and one special character.")

def create_user (uname, pword, fname, midi, lname, emailadd, statusvar):

    # Method to enter a new user requesting an account

    # connect to login.db
    conn=sqlite3.connect('login.db')
    database_file = "login.db"
    # commit
    conn.commit()
    # create a cursor
    cursor=conn.cursor()

    # SQL insert and update query strings
    sql_insert_query = "INSERT INTO login(username, password, firstname, mi, lastname, email, status) VALUES (?, ?, ?, ?, ?, ?, ?)"
    sql_update_query = "UPDATE login SET password = ?, firstname = ?, mi = ?, lastname = ?, email = ?, status = ? WHERE username = ?"

    # Cursor Execute for updated or new user record
    if len(sys.argv) > 1:
        cursor.execute(sql_update_query, (pword.get(), fname.get(), midi.get(), lname.get(), emailadd.get(), statusvar.get(), uname.get()))
        messagebox.showinfo(title="Account Update", message="Account has been updated.")
    else:
        cursor.execute(sql_insert_query, (uname.get(), pword.get(), fname.get(), midi.get(), lname.get(), emailadd.get(), statusvar.get()))
        messagebox.showinfo(title="Account Creation", message="Account has been created.")

    conn.commit()
    conn.close()

def check_password_strength(password):

    # Checks the strength of a password based on several criteria.
    # Returns True if the password meets all criteria, False otherwise.

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

def is_valid_name(name):
  
  # Checks if a given string contains only alphabetical characters.
  # name: The string to be checked (e.g., a first name, mi, or lastname).
  # Returns: True if the string contains only letters, False otherwise.

  return name.isalpha()

def is_valid_email(email):
    # Check if the email is a valid format.

    # Regular expression for validating an Email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # If the string matches the regex, it is a valid email
    if re.match(regex, email):
        return True
    else:
        return False
    
def unhide():

    # method for hiding and showing the password

    if pass_hide.get() == 1:
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# Create string variables
user_input=tkinter.StringVar()
pass_input=tkinter.StringVar()
firstname_input=tkinter.StringVar()
middleinitial_input=tkinter.StringVar()
lastname_input=tkinter.StringVar()
email_input=tkinter.StringVar()

# Create integer valiable
pass_hide= tkinter.IntVar()
    
if len(sys.argv) > 1:
    function_name = "Edit an Account"
else:
    function_name = "Add an Account"

# Creating Widgets for labels, entry fields, and buttons
# Place widgets on the screen using columns and rows
# 4 columns are needed for this UI

# Row 00 - Create an Account Window label
account_label = tkinter.Label(frame, text=function_name, font=("arial", 20, "bold"), bg = 'lightgray', fg = "#000000")
account_label.grid(row=0, column=0, columnspan=4, sticky=tkinter.EW, pady=25)

# Row 01 - Username label and entry field
username_label = tkinter.Label(frame, text="Username", font=("arial", 14), bg = 'lightgray', fg = "#000000")
username_label.grid(row=1, column=0, sticky=tkinter.E, padx=5)
username_entry = tkinter.Entry(frame, textvariable=user_input, font=("arial", 14))
username_entry.grid(row=1, column=1, columnspan=3, sticky=tkinter.EW, pady=5)

# Row 02 - Password label and entry field
password_label = tkinter.Label(frame, text="Password", font=("arial", 14), bg = 'lightgray', fg = "#000000")
password_label.grid(row=2, column=0, sticky=tkinter.E, padx=5)
password_entry = tkinter.Entry(frame, textvariable=pass_input, show="*", font=("arial", 14))
password_entry.grid(row=2, column=1, columnspan=3, sticky=tkinter.EW, pady=5)

# Row 03 - Firstname label and entry field
firstname_label = tkinter.Label(frame, text="First Name", font=("arial", 14), bg = 'lightgray', fg = "#000000")
firstname_label.grid(row=3, column=0, sticky=tkinter.E, padx=5)
firstname_entry = tkinter.Entry(frame, textvariable=firstname_input, font=("arial", 14))
firstname_entry.grid(row=3, column=1, columnspan=3, sticky=tkinter.EW, pady=5)

# Row 04 - Middle Initial label and entry field
middleinitial_label = tkinter.Label(frame, text="Middle Initial", font=("arial", 14), bg = 'lightgray', fg = "#000000")
middleinitial_label.grid(row=4, column=0, sticky=tkinter.E, padx=5)
middleinitial_entry = tkinter.Entry(frame, textvariable=middleinitial_input, font=("arial", 14))
middleinitial_entry.grid(row=4, column=1, columnspan=3, sticky=tkinter.EW, pady=5)

# Row 05 - Lastname label and entry field
lastname_label = tkinter.Label(frame, text="Last Name", font=("arial", 14), bg = 'lightgray', fg = "#000000")
lastname_label.grid(row=5, column=0, sticky=tkinter.E, padx=5)
lastname_entry = tkinter.Entry(frame, textvariable=lastname_input, font=("arial", 14))
lastname_entry.grid(row=5, column=1, columnspan=3, sticky=tkinter.EW, pady=5)

# Row 06 - Email label and entry field
email_label = tkinter.Label(frame, text="Email Address", font=("arial", 14), bg = 'lightgray', fg = "#000000")
email_label.grid(row=6, column=0, sticky=tkinter.E, padx=5)
email_entry = tkinter.Entry(frame, textvariable=email_input, font=("arial", 14))
email_entry.grid(row=6, column=1, columnspan=3, sticky=tkinter.EW, pady=5)

# Row 07: Radio Buttons for user status
status_label = tkinter.Label(frame, text="Status", font=("arial", 14), bg = 'lightgray', fg = "#000000")
status_label.grid(row=7, column=0, sticky=tkinter.E, padx=5)
status_var = tkinter.StringVar(value="NEW") # Default value
tkinter.Radiobutton(frame, text="New", variable=status_var, value="NEW", font=("arial", 14), bg = 'lightgray', fg = "#000000").grid(row=7, column=1, sticky=tkinter.EW, pady=2)
tkinter.Radiobutton(frame, text="User", variable=status_var, value="USER", font=("arial", 14), bg = 'lightgray', fg = "#000000").grid(row=7, column=2, sticky=tkinter.EW, pady=2)
tkinter.Radiobutton(frame, text="Admin", variable=status_var, value="ADMIN", font=("arial", 14), bg = 'lightgray', fg = "#000000").grid(row=7, column=3, sticky=tkinter.EW, pady=2)

# Row 08 - Show/Hide Password checkbutton
hide_button = tkinter.Checkbutton(frame, text="Show Password", variable=pass_hide, command=unhide, bg = 'lightgray', font=("arial", 14))
hide_button.grid(row=8, column=1, columnspan=3, sticky=tkinter.EW)

# Row 09: Request account commit button
request_button = tkinter.Button(frame, text=function_name, font=("arial", 14), command=account, bg = "#023508", fg = "#F5F0F0")
request_button.grid(row=9, column=1, columnspan=4, sticky=tkinter.EW, pady=20, padx=20) 

if len(sys.argv) > 1:
        #print(f"Parameter 0: {sys.argv[0]}")
        #print(f"Parameter 1: {sys.argv[1]}")
        #print(f"Parameter 2: {sys.argv[2]}")
        #print(f"Parameter 3: {sys.argv[3]}")
        #print(f"Parameter 4: {sys.argv[4]}")
        #print(f"Parameter 5: {sys.argv[5]}")
        #print(f"Parameter 6: {sys.argv[6]}")
        #print(f"Parameter 7: {sys.argv[7]}")
        user_input.set(sys.argv[1])
        pass_input.set(sys.argv[2])
        firstname_input.set(sys.argv[3])
        middleinitial_input.set(sys.argv[4])
        lastname_input.set(sys.argv[5])
        email_input.set(sys.argv[6])
        status_var.set(sys.argv[7])

frame.pack()

root.mainloop()