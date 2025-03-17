import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="librarydb",
    charset="utf8"
)
cursor = conn.cursor()

# Function to add a placeholder to an entry widget
def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.bind("<FocusIn>", lambda event: remove_placeholder(event, placeholder))
    entry.bind("<FocusOut>", lambda event: restore_placeholder(event, placeholder))

# Function to remove the placeholder when typing
def remove_placeholder(event, placeholder):
    if event.widget.get() == placeholder:
        event.widget.delete(0, tk.END)

# Function to restore the placeholder if the field is left empty
def restore_placeholder(event, placeholder):
    if event.widget.get() == "":
        event.widget.insert(0, placeholder)

# Function to add a new member
def add_member():
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()

    if name == "Enter Name" or email == "Enter Email" or phone == "Enter Phone Number":
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    if name and email and phone:
        try:
            query = "INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, phone))
            conn.commit()
            messagebox.showinfo("Success", "Member added successfully!")
            display_members()
            name_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            add_placeholder(name_entry, "Enter Name")
            add_placeholder(email_entry, "Enter Email")
            add_placeholder(phone_entry, "Enter Phone Number")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

# Function to display members in the table
def display_members():
    for row in tree.get_children():
        tree.delete(row)
    
    cursor.execute("SELECT * FROM members")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

# Function to search members by email
def search_member():
    email = search_entry.get().strip()
    if email == "Search by Email":
        messagebox.showwarning("Input Error", "Please enter an email to search.")
        return
    
    for row in tree.get_children():
        tree.delete(row)

    query = "SELECT * FROM members WHERE email LIKE %s"
    cursor.execute(query, (f"%{email}%",))
    rows = cursor.fetchall()

    if not rows:
        messagebox.showinfo("No Results", "No member found with this email.")
    else:
        for row in rows:
            tree.insert("", tk.END, values=row)

# Function to delete a member
def delete_member():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a member to delete.")
        return
    
    member_id = tree.item(selected_item)['values'][0]
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this member?")
    if confirm:
        try:
            query = "DELETE FROM members WHERE id = %s"
            cursor.execute(query, (member_id,))
            conn.commit()
            messagebox.showinfo("Success", "Member deleted successfully!")
            display_members()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

# GUI Setup
root = tk.Tk()
root.title("Library Management - Members")
root.geometry("750x500")

# Custom Colors
bg_color = "#ffcccb"
frame_bg = "#ffb6c1"
btn_color = "#ff4081"
text_color = "#2d2d2d"

# Background
root.configure(bg=bg_color)

# Frame for Input Fields
frame = tk.Frame(root, bg=frame_bg, padx=20, pady=5)
frame.pack(pady=10, fill="x")

tk.Label(frame, text="Name:", bg=frame_bg).grid(row=0, column=0, padx=3, sticky="e")
name_entry = ttk.Entry(frame, width=30)
name_entry.grid(row=0, column=1, padx=3)
add_placeholder(name_entry, "Enter Name")

tk.Label(frame, text="Email:", bg=frame_bg).grid(row=1, column=0, padx=3, sticky="e")
email_entry = ttk.Entry(frame, width=30)
email_entry.grid(row=1, column=1,  padx=3)
add_placeholder(email_entry, "Enter Email")

tk.Label(frame, text="Phone:", bg=frame_bg).grid(row=2, column=0, padx=3, sticky="e")
phone_entry = ttk.Entry(frame, width=30)
phone_entry.grid(row=2, column=1, padx=3)
add_placeholder(phone_entry, "Enter Phone Number")

# Buttons
btn_frame = tk.Frame(root, bg=bg_color)
btn_frame.pack(pady=5)

add_btn = ttk.Button(btn_frame, text="Add Member", command=add_member)
add_btn.pack()

delete_btn = ttk.Button(btn_frame, text="Delete Member", command=delete_member)
delete_btn.pack()

# Search Bar
search_frame = tk.Frame(root, bg=bg_color)
search_frame.pack(pady=5)

tk.Label(search_frame, text="Search by Email:", bg=bg_color).grid(row=0, column=0, padx=5)
search_entry = ttk.Entry(search_frame, width=30)
search_entry.grid(row=0, column=1, padx=5)
search_btn = ttk.Button(search_frame, text="Search", command=search_member)
search_btn.grid(row=0, column=2, padx=5)
add_placeholder(search_entry, "Search by Email")

# Table for displaying members
table_frame = tk.Frame(root, bg=bg_color)
table_frame.pack(pady=5)

tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Email", "Phone"), show="headings", height=10)
tree.heading("ID", text="Member ID")
tree.heading("Name", text="Name")
tree.heading("Email", text="Email")
tree.heading("Phone", text="Phone")

# Add scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack()

display_members()
root.mainloop()
