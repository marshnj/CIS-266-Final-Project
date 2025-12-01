import os
import sys
import re
import tkinter
import sqlite3
from tkinter import INSERT, messagebox

window = tkinter.Tk()
window.title("Administrator Switch")
window.geometry('540x200')
window.configure(bg = 'lightgray')

def accounts():

    # Go to the userview UI
    script_name = "userview.py"
    command = f"python {script_name} {user_status}"
    os.system(command)

def assets():

    # Go to the assets UI
    script_name = "assets.py"
    command = f"python {script_name} {user_status}"
    os.system(command)


# Create the frame
frame = tkinter.Frame(bg = 'lightgray')

# Creating Widgets for labels, entry fields, and buttons
# Place widgets on the screen using columns and rows

# Row 00 - Switch Screen Window label
switch_label = tkinter.Label(frame, text="Administator Switch Screen", font=("arial", 25, "bold"), bg = 'lightgray', fg = "#000000")
switch_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=20)

# Row 01 - Account button and Emily's table button called assets for now
login_button = tkinter.Button(frame, text="User Account Management", font=("arial", 14), command=accounts, bg = "#044D07", fg = "#FFFFFF")
login_button.grid(row=1, column=0, pady=15, padx=5)
reset_button = tkinter.Button(frame, text="Asset Management", font=("arial", 14), command=assets, bg = "#2B07F8", fg = "#FFFFFF")
reset_button.grid(row=1, column=1, pady=15, padx=5)

if len(sys.argv) > 1:
        print(f"Parameter 0: {sys.argv[0]}")
        print(f"Parameter 1: {sys.argv[1]}")
        user_status = {sys.argv[1]}
        
frame.pack()

window.mainloop()