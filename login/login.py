import os
import sys
import tkinter
import sqlite3
from tkinter import INSERT, messagebox

window = tkinter.Tk()
window.title("Login form")
window.geometry('540x440')
window.configure(bg = 'lightgray')

# Login method:  Checks the username and password against the login.db
def login():
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

    # if a login.db row exists for this user/password 
    # check the username/password status
    # get the username and status to pass to either SWITCH (for ADMIN) or ASSETS (for USERS)
    if row:
        target_column_1 = 'username'
        target_column_6 = 'status'
        condition_column_1 = 'username'
        condition_value_1 = user_input.get()
        condition_column_2 = 'password'
        condition_value_2 = pass_input.get()

        cursor.execute(f"SELECT {target_column_1}, {target_column_6} FROM login WHERE {condition_column_1} = ? AND {condition_column_2} = ?",
                   (condition_value_1, condition_value_2))
        result = cursor.fetchone()
        current_user_name = result[0]
        current_user_status = result[1]
        print(f"The username of this user is: {current_user_name}")
        print(f"The status of this user is: {current_user_status}")

        # if status is NEW, deny login - administrator has not approved the account yet.
        if current_user_status == "NEW":
            messagebox.showinfo(title="Login failed", message="Your account is not approved as yet.")
            conn.close() 

        # if status is USER, allow login and go to Emily's asset UI.        
        elif current_user_status == "USER":
            messagebox.showinfo(title="Successfull Log in", message="You have successfully logged in.")
            script_name = "assets.py"
            command = f"python {script_name} {current_user_name} {""} {""} {""} {""} {""} {""} {current_user_status}"
            conn.close() 
            os.system(command)
            sys.exit()  

        # if status is ADMIN, allow login and go the switch UI
        elif current_user_status == "ADMIN":
            messagebox.showinfo(title="Successfull Log in", message="You have successfully logged in.")
            script_name = "switch.py"
            command = f"python {script_name} {current_user_name} {""} {""} {""} {""} {""} {""} {current_user_status}"
            conn.close()
            os.system(command)
            sys.exit()   

    # login failed because no login.db row exists for this user/password 
    else:
        messagebox.showinfo(title="Login failed", message="Invalid log in, username and/or password are incorrect.")
        conn.close()
    
# method for resetting your password
def reset():
    os.system("reset.py")
    
# method for requesting an account
def account():
    os.system("account.py")

# method for hiding and showing the password
def unhide():
    if pass_hide.get() == 1:
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# Create the frame
frame = tkinter.Frame(bg = 'lightgray')

# Create string variables
user_input=tkinter.StringVar()
pass_input=tkinter.StringVar()

# Create integer valiable
pass_hide= tkinter.IntVar()

# Creating Widgets for labels, entry fields, and buttons
# Place widgets on the screen using columns and rows
# 3 columns are needed for this UI

# Row 00 - Login Screen Window label
login_label = tkinter.Label(frame, text="Login Screen", font=("arial", 25, "bold"), bg = 'lightgray', fg = "#000000")
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=20)

# Row 01 - Button to request a new account
account_button = tkinter.Button(frame, text="Request an Account", font=("arial", 14), command=account, bg = "#023508", fg = "#F5F0F0")
account_button.grid(row=1, column=0, columnspan=3, pady=20)

# Row 02 - Username label and entry field
username_label = tkinter.Label(frame, text="Username", font=("arial", 14), bg = 'lightgray', fg = "#000000")
username_label.grid(row=2, column=0)
username_entry = tkinter.Entry(frame, textvariable=user_input, font=("arial", 14))
username_entry.grid(row=2, column=1, pady=5)

# Row 03 - Password label and entry field
password_label = tkinter.Label(frame, text="Password", font=("arial", 14), bg = 'lightgray', fg = "#000000")
password_label.grid(row=3, column=0)
password_entry = tkinter.Entry(frame, textvariable=pass_input, show="*", font=("arial", 14))
password_entry.grid(row=3, column=1, pady=5)

# Row 04 - Show/Hide Password checkbutton
hide_button = tkinter.Checkbutton(frame, text="Show Password", variable=pass_hide, command=unhide, bg = 'lightgray', font=("arial", 14))
hide_button.grid(row=4, column=1)

# Row 05 - Login button and Reset Password button
login_button = tkinter.Button(frame, text="Login", font=("arial", 14), command=login, bg = "#1820F2", fg = "#F5F0F0")
login_button.grid(row=5, column=0, pady=15)
reset_button = tkinter.Button(frame, text="Reset Password", font=("arial", 14), command=reset, bg = "#CCF807", fg = "#1820F2")
reset_button.grid(row=5, column=1, pady=15)

frame.pack()

window.mainloop()
