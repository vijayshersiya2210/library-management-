import os
import tkinter as tk

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
root.geometry("500x400")
root.configure(bg='#FFB0B0')  # Light green background

# Header Label (Increased Size)
header = tk.Label(root, text="Library Management System", font=("Arial", 20, "bold"), fg="#2c3e50", bg="#FFB0B0")
header.pack(pady=20)

# Button Style with Hover Effect
def on_enter(e):
    e.widget.config(bg="#5dade2")

def on_leave(e):
    e.widget.config(bg="#DA498D")

def create_button(text, command):
    btn = tk.Button(root, text=text, font=("Arial", 12, "bold"), command=command, width=25, 
                    bg="#DA498D", fg="white", bd=3, relief="raised", cursor="hand2")
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

# Navigation Buttons
btn_books = create_button("Books Management", open_books)
btn_books.pack(pady=10)

btn_issue_return = create_button("Issue/Return Books", open_issue_return)
btn_issue_return.pack(pady=10)

btn_members = create_button("Members Management", open_members)
btn_members.pack(pady=10)

# Run Tkinter
root.mainloop()
