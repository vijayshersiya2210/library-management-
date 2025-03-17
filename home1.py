import os
import tkinter as tk
from tkinter import messagebox

# Function to Open Books Management
def open_books():
    os.system("python bookinventory1.py")  # Opens the Books Management file

# Function to Open Issue/Return Books
def open_issue_return():
    os.system("python newissuance1.py")  # Opens the Issue/Return Books file

# Function to Open Members Management
def open_members():
    os.system("python members1.py")  # Opens the Members Management file

# Main Home Page Window
root = tk.Tk()
root.title("Library Management System")
root.geometry("400x300")

# Header Label
tk.Label(root, text="Library Management System", font=("Arial", 14, "bold")).pack(pady=20)

# Navigation Buttons
tk.Button(root, text="Books Management", font=("Arial", 12), command=open_books, width=25,bg="lightblue").pack(pady=5)
root.configure(bg='#90ee90') 
tk.Button(root, text="Issue/Return Books", font=("Arial", 12), command=open_issue_return, width=25,bg="lightblue").pack(pady=5)
tk.Button(root, text="Members Management", font=("Arial", 12), command=open_members, width=25,bg="lightblue").pack(pady=5)

# Run Tkinter
root.mainloop()
