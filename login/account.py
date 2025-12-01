import os
import re
import tkinter
import sqlite3
from tkinter import INSERT, messagebox

window = tkinter.Tk()
window.title("Account Request form")
window.geometry('540x440')
window.configure(bg = 'lightgray')


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
    if row:
        # If this username and password already exist in login.db, then you can't creat another account
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
                            create_user(user_input, pass_input, firstname_input, middleinitial_input, lastname_input, email_input)
                            messagebox.showinfo(title="Account creation", message="Account will be requested. You will not be able to login until Admin approves the account request")
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

def create_user (uname, pword, fname, midi, lname, emailadd):

    # Method to enter a new user requesting an account

    # connect to login.db
    conn=sqlite3.connect('login.db')
    database_file = "login.db"
    # commit
    conn.commit()
    # create a cursor
    cursor=conn.cursor()
    # SQL insert query string
    sql_insert_query = "INSERT INTO login(username, password, firstname, mi, lastname, email, status) VALUES (?, ?, ?, ?, ?, ?, ?)"
    # Cursor Execute for new user record
    cursor.execute(sql_insert_query, (uname.get(), pword.get(), fname.get(), midi.get(), lname.get(), emailadd.get(), 'NEW'))
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
    regex = r'^[a-z]+\.[a-z]+\.[a-z]+@[a-z]+\.[a-z]+$'

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

# Create frame
#root = tkinter.Tk()
frame = tkinter.Frame(bg = 'lightgray')

# Create string variables
user_input=tkinter.StringVar()
pass_input=tkinter.StringVar()
firstname_input=tkinter.StringVar()
middleinitial_input=tkinter.StringVar()
lastname_input=tkinter.StringVar()
email_input=tkinter.StringVar()

# Create integer valiable
pass_hide= tkinter.IntVar()

# Creating Widgets for labels, entry fields, and buttons
account_label = tkinter.Label(frame, text="Request An Account", font=("arial", 25, "bold"), bg = 'lightgray', fg = "#000000")
username_label = tkinter.Label(frame, text="Username", font=("arial", 14), bg = 'lightgray', fg = "#000000")
username_entry = tkinter.Entry(frame, textvariable=user_input, font=("arial", 14))
password_label = tkinter.Label(frame, text="Password", font=("arial", 14), bg = 'lightgray', fg = "#000000")
password_entry = tkinter.Entry(frame, textvariable=pass_input, show="*", font=("arial", 14))
firstname_label = tkinter.Label(frame, text="First Name", font=("arial", 14), bg = 'lightgray', fg = "#000000")
firstname_entry = tkinter.Entry(frame, textvariable=firstname_input, font=("arial", 14))
middleinitial_label = tkinter.Label(frame, text="Middle Initial", font=("arial", 14), bg = 'lightgray', fg = "#000000")
middleinitial_entry = tkinter.Entry(frame, textvariable=middleinitial_input, font=("arial", 14))
lastname_label = tkinter.Label(frame, text="Last Name", font=("arial", 14), bg = 'lightgray', fg = "#000000")
lastname_entry = tkinter.Entry(frame, textvariable=lastname_input, font=("arial", 14))
email_label = tkinter.Label(frame, text="Email Address", font=("arial", 14), bg = 'lightgray', fg = "#000000")
email_entry = tkinter.Entry(frame, textvariable=email_input, font=("arial", 14))
hide_button = tkinter.Checkbutton(frame, text="Show Password", variable=pass_hide, command=unhide, bg = 'lightgray', font=("arial", 14))
request_button = tkinter.Button(frame, text="Request Account", font=("arial", 14), command=account, bg = "#023508", fg = "#F5F0F0")

# Place widgets on the screen using columns and rows
account_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=20)
username_label.grid(row=1, column=0, sticky=tkinter.E)
username_entry.grid(row=1, column=1, pady=5, padx=15)
password_label.grid(row=2, column=0, sticky=tkinter.E, padx=5)
password_entry.grid(row=2, column=1, pady=5, padx=15)
firstname_label.grid(row=3, column=0, sticky=tkinter.E, padx=5)
firstname_entry.grid(row=3, column=1, pady=5, padx=15)
middleinitial_label.grid(row=4, column=0, sticky=tkinter.E, padx=5)
middleinitial_entry.grid(row=4, column=1, pady=5, padx=15)
lastname_label.grid(row=5, column=0, sticky=tkinter.E, padx=5)
lastname_entry.grid(row=5, column=1, pady=5, padx=15)
email_label.grid(row=6, column=0, sticky=tkinter.E, padx=5)
email_entry.grid(row=6, column=1, pady=5, padx=15)
hide_button.grid(row=7, column=1, sticky=tkinter.W)
request_button.grid(row=8, column=0, columnspan=2, sticky="news", pady=20, padx=5)

frame.pack()

window.mainloop()
