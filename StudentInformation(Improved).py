import os
from tkinter import *
import pandas as pd
from tkinter import ttk, filedialog
from tkinter import messagebox
import csv
from collections import defaultdict

class Student_Information():

    def __init__(self, root):
        self.root = root
        self.root.title('Student Information System')
        self.root.geometry('1010x600')
        self.root.resizable(False,False)

        self.ID_Number = StringVar()
        self.Full_Name = StringVar()
        self.Year_Level = StringVar()
        self.Gender = StringVar()
        self.Course = StringVar()
        self.Search = StringVar()
        self.selections = defaultdict(list)
        self.last_lookup = ""

        #==============Menu============
        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)
        self.file_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Open", menu=self.file_menu)
        self.file_menu.add_command(label="Open a CSV file", command=self.file_open)

        self.save_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Save", menu=self.save_menu)
        self.save_menu.add_command(label="Save as CSV file", command=self.save_info)

        #==============Frame============
        self.First_Frame = Frame(self.root, bd=8, relief=FLAT, bg='#fb8263')
        self.First_Frame.place(y=0, width=1366, height=53)

        self.Search_entry = Entry(self.First_Frame, relief=FLAT, bg='white', font=('Lato', 12), width=20)
        self.Search_entry.grid(padx=5,ipady=3, row=0, column=0)
        self.Search_entry.insert(0, "Search by ID Number")
        self.Search_entry.config(state=DISABLED)
        self.Search_entry.bind("<Button-1>", self.search_click)

        self.Search_button = Button(self.First_Frame, text='Search',command=self.search, font=('Century Gothic', 10), bg='#ffffff', relief=GROOVE)
        self.Search_button.grid(padx=5,pady=0, ipady=2, row=0, column=1)

        self.Add_Student = Button(self.First_Frame, text='Add Student',command=self.add_student, font=('Century Gothic', 10), bg='#ffffff', relief=GROOVE)
        self.Add_Student.grid(padx=5, pady=0, ipady=2, row=0, column=2)

        self.Update_Student = Button(self.First_Frame, text='Update Student',command=self.update_student, font=('Century Gothic', 10), bg='#ffffff',relief=GROOVE)
        self.Update_Student.grid(padx=5, pady=0, ipady=2, row=0, column=3)

        self.Delete_Student = Button(self.First_Frame, text='Delete Student',command=self.delete, font=('Century Gothic', 10), bg='#ffffff',relief=GROOVE)
        self.Delete_Student.grid(padx=5, pady=0, ipady=2, row=0, column=4)

        self.Title = Label(self.First_Frame, text='STUDENT INFORMATION SYSTEM', font=('Century Gothic', 17,'bold'),bg='#fb8263', fg='white', justify=RIGHT)
        self.Title.grid(padx=40, pady=0, ipady=2, row=0, column=5)

        self.Below_Frame = Frame(self.root, bd=5, relief=RIDGE, bg='#fb8263')
        self.Below_Frame.place(y=550, width=1366, height=53)

        self.List = Label(self.Below_Frame, text='NUMBER OF STUDENTS:', font=('Century Gothic', 17,'bold'), fg='#fefefe',
                          bg='#fb8263')
        self.List.grid(row=0, column=3, padx=655,pady=6, sticky='w')
        self.List_entry = Entry(self.Below_Frame, font=('Lato', 12), bd=2, relief=RIDGE, width=8)
        self.List_entry.grid(row=0, column=3, padx=910, sticky='w')

        self.Details_Frame = Frame(self.root, bd=2, relief=FLAT, bg='white')
        self.Details_Frame.place(x=0, y=53, width=1010, height=500)

        # ============Scroll Bar and Treeview=========
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                             background="#f1e2df",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="#f1e2df"
                             )
        self.style.map("Treeview",
                       background=[('selected', '#f56f4c')])

        self.Student_Record = ttk.Treeview(self.Details_Frame, selectmode='browse')
        self.Student_Record["columns"] = ("ID Number", "Full Name", "Course", "Year Level", "Gender")

        self.scroll_horizontal = Scrollbar(self.Details_Frame, orient=HORIZONTAL)
        self.scroll_horizontal.pack(side=BOTTOM, fill=X)
        self.scroll_vertical = Scrollbar(self.Details_Frame, orient=VERTICAL)
        self.scroll_vertical.pack(side=RIGHT, fill=Y)

        self.Student_Record.config(yscrollcommand=self.scroll_vertical.set)
        self.Student_Record.config(xscrollcommand=self.scroll_horizontal.set)

        self.scroll_horizontal.config(command=self.Student_Record.xview)
        self.scroll_vertical.config(command=self.Student_Record.yview)

        self.Student_Record['show'] = 'headings'
        self.Student_Record.column("ID Number",anchor=CENTER, stretch=NO, width=200)
        self.Student_Record.column("Full Name", anchor=CENTER, stretch=NO, width=200)
        self.Student_Record.column("Course",anchor=CENTER, stretch=NO, width=200)
        self.Student_Record.column("Year Level", anchor=CENTER, stretch=NO, width=200)
        self.Student_Record.column("Gender", anchor=CENTER, stretch=NO, width=200)

        self.Student_Record.heading("ID Number", text="ID Number")
        self.Student_Record.heading("Full Name", text="Full Name")
        self.Student_Record.heading("Course", text="Course")
        self.Student_Record.heading("Year Level", text="Year Level")
        self.Student_Record.heading("Gender", text="Gender")

        self.Student_Record.pack(fill=BOTH, expand=1)
        self.Student_Record.bind('<Button-1>', self.handle_click)

    def search_click(self, a):
        self.Search_entry.config(state=NORMAL)
        self.Search_entry.delete(0, END)

    def course_click(self, a):
        self.Label_course_entry.config(state=NORMAL)
        self.Label_course_entry.delete(0, END)

    def name_click(self, a):
        self.Label_name_entry.config(state=NORMAL)
        self.Label_name_entry.delete(0, END)

    def handle_click(self, event):
        if self.Student_Record.identify_region(event.x, event.y) == "separator":
            return "break"

     # Open A File Function
    def file_open(self):
        file_name = filedialog.askopenfilename(initialdir="C:/Users/", title="Open a File",
                                                   filetypes=(("csv files", "*.csv"), ("All Files", "*.*")))
        if file_name:
            try:
                filename = r"{}".format(file_name)
                data = pd.read_csv(filename)
            except ValueError:
                messagebox.showerror("Error", "File Could Not Be Opened")
            except FileNotFoundError:
                messagebox.showerror("Error", "File Could Not Be Found")

        self.clear_tree()

        self.Student_Record.bind('<Button-1>', self.handle_click)

        self.Student_Record["column"] = list(data.columns)
        self.Student_Record["show"] = "headings"

        for column in self.Student_Record["column"]:
            self.Student_Record.column(column, anchor='center')
            self.Student_Record.heading(column, text=column)

        data_rows = data.to_numpy().tolist()
        for row in data_rows:
            self.Student_Record.insert("", "end", values=row)

        self.update_list()

        self.Student_Record.pack()

    # Clear Current Tree
    def clear_tree(self):
        self.Student_Record.delete(*self.Student_Record.get_children())

    def save_info(self):
        if len(self.Student_Record.get_children()) < 1:
            messagebox.showinfo("No Data", "No data available to export")
            return False

        file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title='Save CSV',
                                                filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
        with open(file, 'w', newline='') as output:
            output_data = csv.writer(output, delimiter=',')
            csv_writer = csv.writer(output, delimiter=',')
            csv_writer.writerow(['ID Number', 'Full Name', 'Course', 'Year Level', 'Gender'])
            for x in self.Student_Record.get_children():
                row = self.Student_Record.item(x)['values']
                output_data.writerow(row)
        messagebox.showinfo("File Saved", "Data exported successfully!")

    def add_student(self):
        self.student_add()
        self.window = Toplevel(root)
        self.window.title("Adding...")
        self.window.resizable(False, False)
        self.window.geometry('380x610')

        self.First_Frame = Frame(self.window, bd=2, relief=RIDGE, bg='#f1e2df')
        self.First_Frame.place(y=0, width=380, height=100)

        self.title = Label(self.First_Frame, text='STUDENT DATA', font=('Century Gothic', 25, 'bold'), fg='#fb8263',
                           bg='#f1e2df', justify=CENTER)
        self.title.grid(row=0, columnspan=2, ipady=5, padx=80)
        self.title1 = Label(self.First_Frame, text='Hello. We are glad to see you!',
                            font=('Century Gothic', 12, 'italic'),
                            fg='#fb8263', bg='#f1e2df', justify=CENTER)
        self.title1.grid(row=1, columnspan=2, padx=0)

        self.Second_Frame = Frame(self.window, bd=2, relief=RIDGE, bg='white')
        self.Second_Frame.place(y=100, width=380, height=510)

        self.Label_id = Label(self.Second_Frame, text='ID Number:', font=('Lato', 15), fg='#333438', bg='white')
        self.Label_id.grid(row=2, column=0, pady=10, padx=20, sticky='w')
        self.Label_id_entry = Entry(self.Second_Frame, textvariable=self.ID_Number, font=('Lato', 12), bd=2,
                                    relief=GROOVE)
        self.Label_id_entry.grid(row=2, column=1, ipady=3, pady=30, padx=20, sticky='w')

        self.Label_name = Label(self.Second_Frame, text='Full Name:', font=('Lato', 15), fg='#333438', bg='white')
        self.Label_name.grid(row=3, column=0, pady=10, padx=20, sticky='w')
        self.Label_name_entry = Entry(self.Second_Frame, textvariable=self.Full_Name, font=('Lato', 12), bd=2,
                                      relief=GROOVE)
        self.Label_name_entry.grid(row=3, column=1, ipady=3, pady=30, padx=20, sticky='w')
        self.Label_name_entry.insert(0, "First Name, M.I, Surname")
        self.Label_name_entry.config(state=DISABLED)
        self.Label_name_entry.bind("<Button-1>", self.name_click)

        self.Label_course = Label(self.Second_Frame, text='Course:', font=('Lato', 15), fg='#333438', bg='white')
        self.Label_course.grid(row=4, column=0, pady=10, padx=20, sticky='w')
        self.Label_course_entry = Entry(self.Second_Frame, textvariable=self.Course, font=('Lato', 12), bd=2,
                                        relief=GROOVE)
        self.Label_course_entry.grid(row=4, column=1, ipady=3, pady=30, padx=20, sticky='w')
        self.Label_course_entry.insert(0, "Course Acronym")
        self.Label_course_entry.config(state=DISABLED)
        self.Label_course_entry.bind("<Button-1>", self.course_click)

        self.Label_year = Label(self.Second_Frame, text='Year Level:', font=('Lato', 15), fg='#333438', bg='white')
        self.Label_year.grid(row=5, column=0, pady=10, padx=20, sticky='w')
        self.Label_year_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Year_Level, font=('Lato', 12),
                                             state='readonly', values=['1st Year', '2nd Year', '3rd Year', '4th Year', '5th Year', 'Other'], width=18)
        self.Label_year_entry.grid(row=5, column=1, ipady=3, pady=30, padx=20, sticky='w')

        self.Label_gender = Label(self.Second_Frame, text='Gender:', font=('Lato', 15), fg='#333438', bg='white')
        self.Label_gender.grid(row=6, column=0, pady=10, padx=20, sticky='w')
        self.Label_gender_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Gender, font=('Lato', 12),
                                               state='readonly', values=['Male', 'Female'], width=18)
        self.Label_gender_entry.grid(row=6, column=1, ipady=3, pady=30, padx=20, sticky='w')

        self.Add_Button = Button(self.Second_Frame, text='Add', font=('Century Gothic', 13), command=self.add,
                             bg='#ffffff', relief=GROOVE)
        self.Add_Button.place(x=220, y=450)

        self.Clear = Button(self.Second_Frame, text='Clear', font=('Century Gothic', 13), command=self.clear,
                            bg='#ffffff', relief=GROOVE)
        self.Clear.place(x=290, y=450)

    def student_add(self):
        self.ID_Number.set('')
        self.Full_Name.set('')
        self.Year_Level.set('')
        self.Gender.set('')
        self.Course.set('')

    def add(self):
        if (len(self.ID_Number.get()) == 0 or len(self.Full_Name.get()) == 0 or len(
                self.Year_Level.get()) == 0 or len(self.Gender.get()) == '' or len(self.Course.get()) == 0):
            messagebox.showerror("Error", "All fields should be filled!")
        else:
            self.Student_Record.insert("", "end", text="", values=(self.ID_Number.get(),
                                                                    self.Full_Name.get(),
                                                                    self.Course.get(),
                                                                    self.Year_Level.get(),
                                                                    self.Gender.get()
                                                                       ))
            for column in self.Student_Record["column"]:
                self.Student_Record.column(column, anchor='center')
            messagebox.showinfo("Successful", "Student is added in the class")

            self.Label_id_entry.delete(0, END)
            self.Label_name_entry.delete(0, END)
            self.Label_year_entry.set('')
            self.Label_gender_entry.set('')
            self.Label_course_entry.delete(0, END)

            self.update_list()
            self.window.destroy()

    def update_student(self):
        answer = messagebox.askyesno("Update Student Data", "Do you want to update data?")
        if not answer:
            pass
        else:
            self.second_window =Toplevel(root)
            self.second_window.title("Updating...")
            self.second_window.resizable(False, False)
            self.second_window.geometry('380x610')

            self.First_Frame = Frame(self.second_window, bd=2, relief=RIDGE, bg='#f1e2df')
            self.First_Frame.place(y=0, width=380, height=100)

            self.title = Label(self.First_Frame, text='STUDENT DATA', font=('Century Gothic', 25, 'bold'), fg='#fb8263',
                               bg='#f1e2df',justify=CENTER)
            self.title.grid(row=0, columnspan=2, ipady=5, padx=80)
            self.title1 = Label(self.First_Frame, text='Hello. We are glad to see you!', font=('Century Gothic', 12, 'italic'),
                                fg='#fb8263',bg='#f1e2df', justify=CENTER)
            self.title1.grid(row=1, columnspan=2, padx=0)

            self.Second_Frame = Frame(self.second_window, bd=2, relief=RIDGE, bg='white')
            self.Second_Frame.place(y=100, width=380, height=510)

            self.Label_id = Label(self.Second_Frame, text='ID Number:', font=('Lato', 15), fg='#333438', bg='white')
            self.Label_id.grid(row=2, column=0, pady=10, padx=20, sticky='w')
            self.Label_id_entry = Entry(self.Second_Frame, textvariable=self.ID_Number, font=('Lato', 12), bd=2, relief=GROOVE)
            self.Label_id_entry.grid(row=2, column=1, ipady=3, pady=30, padx=20, sticky='w')

            self.Label_name = Label(self.Second_Frame, text='Full Name:', font=('Lato', 15), fg='#333438', bg='white')
            self.Label_name.grid(row=3, column=0, pady=10, padx=20, sticky='w')
            self.Label_name_entry = Entry(self.Second_Frame, textvariable=self.Full_Name, font=('Lato', 12), bd=2, relief=GROOVE)
            self.Label_name_entry.grid(row=3, column=1, ipady=3, pady=30, padx=20, sticky='w')

            self.Label_course = Label(self.Second_Frame, text='Course:', font=('Lato', 15), fg='#333438', bg='white')
            self.Label_course.grid(row=4, column=0, pady=10, padx=20, sticky='w')
            self.Label_course_entry = Entry(self.Second_Frame, textvariable=self.Course, font=('Lato', 12), bd=2, relief=GROOVE)
            self.Label_course_entry.grid(row=4, column=1, ipady=3, pady=30, padx=20, sticky='w')
            self.Label_course_entry.grid(row=4, column=1, ipady=3, pady=30, padx=20, sticky='w')

            self.Label_year = Label(self.Second_Frame, text='Year Level:', font=('Lato', 15), fg='#333438', bg='white')
            self.Label_year.grid(row=5, column=0, pady=10, padx=20, sticky='w')
            self.Label_year_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Year_Level, font=('Lato', 12),state='readonly',
                                                 values=['1st Year', '2nd Year', '3rd Year', '4th Year', '5th Year', 'Other'], width=18)
            self.Label_year_entry.grid(row=5, column=1, ipady=3, pady=30, padx=20, sticky='w')

            self.Label_gender = Label(self.Second_Frame, text='Gender:', font=('Lato', 15), fg='#333438', bg='white')
            self.Label_gender.grid(row=6, column=0, pady=10, padx=20, sticky='w')
            self.Label_gender_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Gender, font=('Lato', 12),state='readonly', values=['Male', 'Female'], width=18)
            self.Label_gender_entry.grid(row=6, column=1, ipady=3, pady=30, padx=20, sticky='w')

            self.Update = Button(self.Second_Frame, text='Update', font=('Century Gothic', 13), command=self.update,
                                     bg='#ffffff', relief=GROOVE)
            self.Update.place(x=190, y=450)

            self.Clear = Button(self.Second_Frame, text='Clear', font=('Century Gothic', 13), command=self.clear,
                                 bg='#ffffff', relief=GROOVE)
            self.Clear.place(x=290, y=450)

            self.student_update()

    def student_update(self):
        self.ID_Number.set('')
        self.Full_Name.set('')
        self.Year_Level.set('')
        self.Gender.set('')
        self.Course.set('')

        selected = self.Student_Record.focus()
        values = self.Student_Record.item(selected, 'values')

        self.Label_id_entry.insert(0, values[0])
        self.Label_name_entry.insert(0, values[1])
        self.Label_course_entry.insert(0, values[2])
        self.Label_year_entry.set(values[3])
        self.Label_gender_entry.set(values[4])

    def update(self):
        if (len(self.ID_Number.get()) == 0 or len(self.Full_Name.get()) == 0 or len(
                self.Year_Level.get()) == 0 or len(self.Gender.get()) == '' or len(self.Course.get()) == 0):
            messagebox.showerror("Error", "All fields should be filled!")
        else:
            selected = self.Student_Record.focus()
            self.Student_Record.item(selected, text='', values=(self.ID_Number.get(),
                                                            self.Full_Name.get(),
                                                            self.Course.get(),
                                                            self.Year_Level.get(),
                                                            self.Gender.get(),
                                                                ))
            self.Label_id_entry.delete(0, END)
            self.Label_name_entry.delete(0, END)
            self.Label_year_entry.delete(0, END)
            self.Label_gender_entry.delete(0, END)
            self.Label_course_entry.delete(0, END)

            messagebox.showinfo("Update Student", "Successfully updated!")

            self.second_window.destroy()

    def delete(self):
        response = messagebox.askyesno("Delete Student", "Delete student from the list?")
        if not response:
            pass
        else:
            x = self.Student_Record.selection()[0]
            self.Student_Record.delete(x)

        self.update_list()

    def clear(self):
        self.Label_id_entry.delete(0, END)
        self.Label_name_entry.delete(0, END)
        self.Label_year_entry.set('')
        self.Label_gender_entry.set('')
        self.Label_course_entry.delete(0, END)

    def search(self):
        query = str(self.Search_entry.get())
        if not query:
            pass
        children = self.Student_Record.get_children()
        for child in children:
            curr = self.Student_Record.item(child)["values"][0]
            if query in curr and child not in self.selections[query]:
                self.selections[query].append(child)
                self.Student_Record.selection_set(child)
                self.Student_Record.focus(child)
                self.Student_Record.see(child)
                self.last_lookup = query

                self.ID_Number.set('')
                self.Full_Name.set('')
                self.Year_Level.set('')
                self.Gender.set('')
                self.Course.set('')
                self.Search_entry.delete(0, END)

                return
            elif query != self.last_lookup:
                self.selections = defaultdict(list)
                self.Search_entry.delete(0, END)
        messagebox.showerror('Error', 'Student is not in the list')

    def select_item(self, a):
        self.ID_Number.set('')
        self.Full_Name.set('')
        self.Year_Level.set('')
        self.Gender.set('')
        self.Course.set('')

        selected = self.Student_Record.focus()
        values = self.Student_Record.item(selected, 'values')

        self.Label_id_entry.insert(0, values[0])
        self.Label_name_entry.insert(0, values[1])
        self.Label_course_entry.insert(0, values[2])
        self.Label_year_entry.insert(0, values[3])
        self.Label_gender_entry.insert(0, values[4])

    def update_list(self):
        self.List_entry.delete(0, END)
        self.List_entry.insert(0, str(len(self.Student_Record.get_children())))

root = Tk()
ob = Student_Information(root)
root.mainloop()