import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox
from datetime import date

# Database Connection
def db_connect():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="librarydb",
            charset="utf8"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

conn = db_connect()
cursor = conn.cursor() if conn else None

# Create Tkinter Window
root = Tk()
root.title("Library Management - Issue & Return Books")
root.geometry("800x500")
root.configure(bg="#FFB6C1")  # Light Pink Background

# Function to center the window
def center_window(win, width=800, height=500):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

center_window(root, 800, 500)

# Main Frame to Center Everything
main_frame = Frame(root, bg="#FFB6C1")
main_frame.pack(expand=True)

# Labels and Inputs
Label(main_frame, text="Member ID:", bg="#FFB6C1", fg="#FF69B4", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="e")
member_entry = Entry(main_frame, font=("Arial", 12))
member_entry.grid(row=0, column=1, padx=10, pady=5)

Label(main_frame, text="Book ID:", bg="#FFB6C1", fg="#FF69B4", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="e")
book_entry = Entry(main_frame, font=("Arial", 12))
book_entry.grid(row=1, column=1, padx=10, pady=5)

# Buttons
button_frame = Frame(main_frame, bg="#FFB6C1")
button_frame.grid(row=2, column=0, columnspan=2, pady=10)

issue_btn = Button(button_frame, text="Issue Book", command=lambda: issue_book(), bg="#FF69B4", fg="white", font=("Arial", 10, "bold"), width=12)
issue_btn.pack(side=LEFT, padx=5)

return_btn = Button(button_frame, text="Return Book", command=lambda: return_book(), bg="#FF69B4", fg="white", font=("Arial", 10, "bold"), width=12)
return_btn.pack(side=LEFT, padx=5)

# Treeview (Table)
columns = ("Issue ID", "Member ID", "Book ID", "Issue Date", "Return Date", "Status")
tree = ttk.Treeview(main_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=110)

tree.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

# Apply Treeview Styling
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="white", foreground="black")
style.configure("Treeview", background="white", foreground="black", rowheight=25)
style.map("Treeview", background=[("selected", "#F08080")])  # Light Coral when selected

# Function to Load Data
def load_data():
    if not cursor:
        return

    tree.delete(*tree.get_children())  # Clear Table
    cursor.execute("SELECT issue_id, member_id, book_id, issue_date, return_date, is_returned FROM book_issuance")
    for row in cursor.fetchall():
        status = "Returned" if row[5] else "Issued"
        tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], status))

# Function to Issue Book
def issue_book():
    if not cursor or not conn:
        messagebox.showerror("Database Error", "No Database Connection!")
        return

    member_id = member_entry.get()
    book_id = book_entry.get()

    if not member_id or not book_id:
        messagebox.showwarning("Error", "Member ID and Book ID are required!")
        return

    # Check if the book is available
    cursor.execute("SELECT available FROM Books WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()

    if not book:
        messagebox.showwarning("Error", "Book not found!")
        return

    if book[0] <= 0:  # No copies available
        messagebox.showwarning("Error", "Book is not available!")
        return

    issue_date = date.today()

    # Issue the book
    cursor.execute("INSERT INTO book_issuance (member_id, book_id, issue_date) VALUES (%s, %s, %s)", 
                   (member_id, book_id, issue_date))

    # Reduce available count in Books table
    cursor.execute("UPDATE Books SET available = available - 1 WHERE book_id = %s", (book_id,))

    conn.commit()
    load_data()
    messagebox.showinfo("Success", "Book issued successfully!")

# Function to Return Book
def return_book():
    if not cursor or not conn:
        messagebox.showerror("Database Error", "No Database Connection!")
        return

    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)["values"]
        issue_id = item[0]
        book_id = item[2]
        return_date = date.today()

        # Update `return_date` and mark as returned
        cursor.execute("UPDATE book_issuance SET return_date = %s, is_returned = TRUE WHERE issue_id = %s", 
                       (return_date, issue_id))

        # Increase available count in Books table
        cursor.execute("UPDATE Books SET available = available + 1 WHERE book_id = %s", (book_id,))

        conn.commit()
        load_data()
        messagebox.showinfo("Success", f"Book returned on {return_date}!")
    else:
        messagebox.showwarning("Error", "Please select a book to return!")

# Load Initial Data
load_data()

# Run Tkinter
root.mainloop()
