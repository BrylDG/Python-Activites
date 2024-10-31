import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from databasefunctions import add_record, getall_records, validate_record

class BooksGui():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Book Information")
        self.width = 900
        self.height = 300
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+{(self.screen_width-self.width)//2}+{(self.screen_height-self.height)//2}")

        self.inputs()
        self.load_data()
        self.root.mainloop()

    def inputs(self):
        self.left_frame = Frame(self.root, padx=10, pady=10)
        self.left_frame.grid(row=0, column=0, sticky="n")

        # Book fields
        self.label_isbn = Label(self.left_frame, text="ISBN")
        self.label_isbn.grid(row=0, column=0, sticky="w", pady=(0, 10))
        self.entry_isbn = Entry(self.left_frame, validate="key", validatecommand=(self.root.register(self.validate_int), '%P'))
        self.entry_isbn.grid(row=0, column=1, padx=(10, 0))

        self.label_title = Label(self.left_frame, text="Title")
        self.label_title.grid(row=1, column=0, sticky="w", pady=(0, 10))
        self.entry_title = Entry(self.left_frame)
        self.entry_title.grid(row=1, column=1, padx=(10, 0))

        self.label_author = Label(self.left_frame, text="Author")
        self.label_author.grid(row=2, column=0, sticky="w", pady=(0, 10))
        self.entry_author = Entry(self.left_frame)
        self.entry_author.grid(row=2, column=1, padx=(10, 0))

        self.label_copyright = Label(self.left_frame, text="Copyright")
        self.label_copyright.grid(row=3, column=0, sticky="w", pady=(0, 10))
        self.entry_copyright = Entry(self.left_frame)
        self.entry_copyright.grid(row=3, column=1, padx=(10, 0))

        self.label_edition = Label(self.left_frame, text="Edition")
        self.label_edition.grid(row=4, column=0, sticky="w", pady=(0, 10))
        self.entry_edition = Entry(self.left_frame)
        self.entry_edition.grid(row=4, column=1, padx=(10, 0))

        self.label_price = Label(self.left_frame, text="Price")
        self.label_price.grid(row=5, column=0, sticky="w", pady=(0, 10))
        self.entry_price = Entry(self.left_frame)
        self.entry_price.grid(row=5, column=1, padx=(10, 0))

        self.label_qty = Label(self.left_frame, text="Quantity")
        self.label_qty.grid(row=6, column=0, sticky="w", pady=(0, 10))
        self.entry_qty = Entry(self.left_frame)
        self.entry_qty.grid(row=6, column=1, padx=(10, 0))

        self.table_frame = Frame(self.root, padx=30, pady=10)
        self.table_frame.grid(row=0, column=1, sticky="n")

        self.table()
        self.buttons()

    def buttons(self):
        self.button_frame = Frame(self.left_frame)
        self.button_frame.grid(row=7, column=0, columnspan=2, pady=(20, 10))

        self.btn_save = Button(self.button_frame, text="SAVE", command=self.add_book, width=10)
        self.btn_save.grid(row=0, column=0, padx=(40, 10))

        self.btn_clear = Button(self.button_frame, text="CANCEL", command=self.clear_prompt, width=10)
        self.btn_clear.grid(row=0, column=1, padx=(10, 0))

    def table(self):
        self.tree = ttk.Treeview(self.table_frame, columns=("ISBN", "Title", "Author", "Edition", "Price", "Quantity"), show="headings")
        
        self.tree.heading("ISBN", text="ISBN", anchor='center')
        self.tree.heading("Title", text="Title", anchor='center')
        self.tree.heading("Author", text="Author", anchor='center')
        self.tree.heading("Edition", text="Edition", anchor='center')
        self.tree.heading("Price", text="Price", anchor='center')
        self.tree.heading("Quantity", text="Quantity", anchor='center')

        for col in ["ISBN", "Title", "Author", "Edition", "Price", "Quantity"]:
            self.tree.column(col, anchor='center', width=100)

        self.tree.pack()

    def load_data(self):
        books = getall_records('books')

        for row in self.tree.get_children():
            self.tree.delete(row)

        for book in books:
            values = (book['isbn'], book['title'], book['author'], book['edition'], book['price'], book['qty'])
            self.tree.insert('', 'end', values=values)

    def add_book(self):
        isbn = self.entry_isbn.get()
        title = self.entry_title.get()
        author = self.entry_author.get()
        copyright = self.entry_copyright.get()
        edition = self.entry_edition.get()
        price = self.entry_price.get()
        qty = self.entry_qty.get()

        if not (isbn and title and author and copyright and edition and price and qty):
            messagebox.showwarning("Input Error", "All fields must be filled out!")
            return

        result = add_record('books', isbn=isbn, title=title, author=author, copyright=copyright,
                            edition=edition, price=price, qty=qty)

        if result:
            messagebox.showinfo("Input Success", "Book added successfully.")
            self.clear_inputs()
            self.load_data()
        else:
            messagebox.showerror("Duplicate ISBN", "ISBN already exists!")

    def clear_prompt(self):
        if messagebox.askyesno("Confirmation", "Are you sure you want to clear everything?"):
            self.clear_inputs()

    def clear_inputs(self):
        self.entry_isbn.delete(0, END)
        self.entry_title.delete(0, END)
        self.entry_author.delete(0, END)
        self.entry_copyright.delete(0, END)
        self.entry_edition.delete(0, END)
        self.entry_price.delete(0, END)
        self.entry_qty.delete(0, END)

    def validate_int(self, id_input):
        return id_input.isdigit() or id_input == ""

def main():
    BooksGui()

if __name__ == "__main__":
    main()
