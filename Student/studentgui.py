import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from dbfunctions import add_record, getall_records


class StudentGui():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student Manager")
        self.width = 600
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

        self.label_id = Label(self.left_frame, text="IDNO")
        self.label_id.grid(row=0, column=0, sticky="w", pady=(0, 10))
        self.entry_id = Entry(self.left_frame, validate="key", validatecommand=(self.root.register(self.validate_idno), '%P'))
        self.entry_id.grid(row=0, column=1, pady=(0, 0), padx=(10, 0))

        self.label_lastname = Label(self.left_frame, text="LAST NAME")
        self.label_lastname.grid(row=1, column=0, sticky="w", pady=(0, 10))
        self.entry_lastname = Entry(self.left_frame, validate="key", validatecommand=(self.root.register(self.validate_names), '%P'))
        self.entry_lastname.grid(row=1, column=1, pady=(0, 10), padx=(10, 0))

        self.label_firstname = Label(self.left_frame, text="FIRST NAME")
        self.label_firstname.grid(row=2, column=0, sticky="w", pady=(0, 10))
        self.entry_firstname = Entry(self.left_frame, validate="key", validatecommand=(self.root.register(self.validate_names), '%P'))
        self.entry_firstname.grid(row=2, column=1, pady=(0, 10), padx=(10, 0))

        self.label_course = Label(self.left_frame, text="COURSE")
        self.label_course.grid(row=3, column=0, sticky="w", pady=(0, 10))
        self.course_options = ['BSIT', 'BSCS', 'BSCPE', 'BSCJ', 'BSHM', 'BSE', 'BEED']
        self.combo_course = ttk.Combobox(self.left_frame, values=self.course_options, width=17, state="readonly")
        self.combo_course.grid(row=3, column=1, pady=(0, 10), padx=(10, 0))

        self.label_level = Label(self.left_frame, text="LEVEL")
        self.label_level.grid(row=4, column=0, sticky="w", pady=(0, 10))
        self.level_options = ['1', '2', '3', '4']
        self.combo_level = ttk.Combobox(self.left_frame, values=self.level_options, width=17, state="readonly")
        self.combo_level.grid(row=4, column=1, pady=(0, 10), padx=(10,0))

        self.table_frame = Frame(self.root, padx=30, pady=10)
        self.table_frame.grid(row=0, column=1, sticky="n")

        self.table()
        self.buttons()
        
    def buttons(self):
        self.button_frame = Frame(self.left_frame)
        self.button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 10))

        self.btn_save = Button(self.button_frame, text="SAVE", command=self.add_student, width=10)
        self.btn_save.grid(row=0, column=0, padx=(40, 10))

        self.btn_clear = Button(self.button_frame, text="CANCEL", command=self.clear_prompt, width=10)
        self.btn_clear.grid(row=0, column=1, padx=(10, 0))
        
    def table(self):
        self.tree = ttk.Treeview(self.table_frame, columns=("ID", "Name", "Course-Level"), show="headings")
        
        self.tree.heading("ID", text="IDNO", anchor='center')
        self.tree.heading("Name", text="NAME", anchor='center')
        self.tree.heading("Course-Level", text="COURSE-LEVEL", anchor='center')

        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("Name", width=150, anchor='center')
        self.tree.column("Course-Level", width=100, anchor='center')
        
        self.tree.pack()

    def load_data(self):
        students = getall_records('students')

        for row in self.tree.get_children():
            self.tree.delete(row)

        for student in students:
            student_id = student['idno']
            full_name = f"{student['lastname']},{student['firstname']}"
            course_level = f"{student['course']}-{student['level']}"
            self.tree.insert('', 'end', values=(student_id, full_name, course_level))

    def add_student(self):
        student_id = self.entry_id.get()
        first_name = self.entry_firstname.get()
        last_name = self.entry_lastname.get()
        course = self.combo_course.get()
        year_level = self.combo_level.get()

        if not (student_id and first_name and last_name and course and year_level):
            messagebox.showwarning("Input Error", "All fields must be filled out!")
            return

        result = add_record('students', idno=student_id, firstname=first_name, lastname=last_name, course=course, level=year_level)

        if result:
            messagebox.showinfo("Input Success", "Student record has been added successfully.")
            self.clear_inputs()
            self.load_data()
        else:
            messagebox.showerror("Input Error", "Failed to add student record.")
    
    def clear_prompt(self):
        if messagebox.askyesno("Confirmation", "Are you sure you want to clear all fields?"):
            self.clear_inputs()
            
    def clear_inputs(self):
            self.entry_id.delete(0, END)
            self.entry_firstname.delete(0, END)
            self.entry_lastname.delete(0, END)
            self.combo_course.set('')
            self.combo_level.set('')
            
    def validate_idno(self, id_input):
        return id_input.isdigit() or id_input == ""

    def validate_names(self, name_input):
        return name_input.isalpha() or name_input == ""

           
def main() -> None:
    StudentGui()


if __name__ == "__main__":
    main()
