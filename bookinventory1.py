import mysql.connector
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd

# Connecting to MySQL Database
connector = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="librarydb",
    charset="utf8"
)
cursor = connector.cursor()

def issuer_card():
    Cid = sd.askstring('Issuer Card ID', 'What is the Issuer\'s Card ID?')
    if not Cid:
        mb.showerror('Error', 'Issuer ID cannot be empty')
    return Cid

def display_records():
    tree.delete(*tree.get_children())  # Clear the tree first
    cursor.execute('SELECT * FROM books')
    data = cursor.fetchall()
    for record in data:
        tree.insert('', END, values=record)

def clear_fields():
    bk_name.set("")
    author_name.set("")
    genre.set("")
    available.set(0)  # Default to 0 (unavailable)

def add_record():
    try:
        cursor.execute(
            'INSERT INTO books (title, author, genre, available) VALUES (%s, %s, %s, %s)',
            (bk_name.get(), author_name.get(), genre.get(), available.get())
        )
        connector.commit()
        display_records()
        mb.showinfo('Success', 'Book added successfully')
    except mysql.connector.Error as err:
        mb.showerror('Error', f'Database error: {err}')

def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select a book to delete')
        return
    current_item = tree.focus()
    values = tree.item(current_item)['values']
    cursor.execute('DELETE FROM books WHERE book_id=%s', (values[0],))
    connector.commit()
    tree.delete(current_item)
    mb.showinfo('Success', 'Book deleted')
    display_records()

def change_availability():
    if not tree.selection():
        mb.showerror('Error!', 'Please select a book')
        return
    
    current_item = tree.focus()
    values = tree.item(current_item)['values']
    
    new_status = sd.askinteger("Change Availability", f"Current stock: {values[4]}\nEnter new stock quantity:", minvalue=0)
    
    if new_status is not None:
        cursor.execute('UPDATE books SET available=%s WHERE book_id=%s', (new_status, values[0]))
        connector.commit()
        clear_and_display()
def clear_and_display():
    clear_fields()
    display_records()



# GUI Setup
root = Tk()
root.title('Library Management System')
root.geometry('1010x530')

root.configure(bg="#FFC0CB")  # Pink background

bk_name = StringVar()
author_name = StringVar()
genre = StringVar()
available = IntVar(value=0)  # Default to 0 (unavailable)

# Apply ttk styles
style = ttk.Style()
style.configure("TButton", font=("Arial", 10, "bold"), padding=5, background="#FF69B4")  # Hot Pink Buttons
style.configure("Treeview", font=("Arial", 10), rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="white", foreground="black")  # Hot Pink Headers

# Left Section (Form)
left_frame = Frame(root, bg="#F08080", padx=10, pady=10)  # Light Coral
left_frame.place(x=0, y=30, relwidth=0.3, relheight=0.96)

Label(left_frame, text='Book Name', bg="#F08080", fg="white", font=("Arial", 12, "bold")).place(x=50, y=10)
Entry(left_frame, textvariable=bk_name, font=("Arial", 12)).place(x=20, y=40, width=200, height=25)

Label(left_frame, text='Author Name', bg="#F08080", fg="white", font=("Arial", 12, "bold")).place(x=50, y=80)
Entry(left_frame, textvariable=author_name, font=("Arial", 12)).place(x=20, y=110, width=200, height=25)

Label(left_frame, text='Genre', bg="#F08080", fg="white", font=("Arial", 12, "bold")).place(x=50, y=150)
Entry(left_frame, textvariable=genre, font=("Arial", 12)).place(x=20, y=180, width=200, height=25)

Label(left_frame, text='Available', bg="#F08080", fg="white", font=("Arial", 12, "bold")).place(x=50, y=220)
Entry(left_frame, textvariable=available, font=("Arial", 12)).place(x=20, y=250, width=200, height=25)

ttk.Button(left_frame, text='Add Book', command=add_record).place(x=50, y=290, width=150)
ttk.Button(left_frame, text='Delete Book', command=remove_record).place(x=50, y=330, width=150)
ttk.Button(left_frame, text='Change Availability', command=change_availability).place(x=50, y=370, width=150)

# Right Section (Table)
RB_frame = Frame(root, bg="#FFC0CB")  # Pink
RB_frame.place(relx=0.3, rely=0.24, relheight=0.785, relwidth=0.7)

Label(RB_frame, text='BOOK INVENTORY', font=("Arial", 14, "bold"), bg="#FF69B4", fg="white").pack(side=TOP, fill=X)  # Hot Pink Header

tree = ttk.Treeview(RB_frame, columns=('Book ID', 'Title', 'Author', 'Genre', 'Available'), show="headings")

tree.heading('Book ID', text='Book ID')
tree.heading('Title', text='Title')
tree.heading('Author', text='Author')
tree.heading('Genre', text='Genre')
tree.heading('Available', text='Available')

tree.column('Book ID', width=80, anchor=CENTER)
tree.column('Title', width=180, anchor=W)
tree.column('Author', width=150, anchor=W)
tree.column('Genre', width=120, anchor=W)
tree.column('Available', width=100, anchor=CENTER)  # Adjust width for visibility

tree.column('#0', width=0, stretch=NO)  # Hide the default first column
tree.place(y=30, x=10, relheight=0.9, relwidth=0.96)

# Display Data
display_records()

# Run Application
root.mainloop()
