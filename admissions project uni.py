import random
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox, simpledialog
                                
                                #inheritance applied
class AbstractApplication(ABC): #abstract class (blueprint for concrete classes)
    def __init__(self, applicant_name, age, program, grades):
        self._application_id = self._generate_application_id() #encapsulation (protectod attributes)
        self._applicant_name = applicant_name 
        self._age = age
        self._program = program
        self._grades = grades
        self._status = "Pending"

    @abstractmethod
    def _generate_application_id(self): #abstract method
        pass

    def update_status(self, status):
        self._status = status

    def display(self):
        return (f"Application ID: {self._application_id}\n"
                f"Name: {self._applicant_name}\n"
                f"Age: {self._age}\n"
                f"Program: {self._program}\n"
                f"Grades: {', '.join(self._grades)}\n"
                f"Status: {self._status}")

    def get_application_id(self):
        return self._application_id

class Application(AbstractApplication):  #polymorphism applied (own implementation provided)
    def _generate_application_id(self):
        return random.randint(10000, 99999)

class AdmissionManagementSystem:
    def __init__(self):
        self.programs = ["Computer Science", "Business Administration", "Data Science", "Electrical Engineering", "Civil Engineering"]
        self.applications = []

    def list_programs(self): #explain code
        program_list = []
        for program in self.programs:
            program_list.append(f"{self.programs.index(program) + 1}. {program}")
        return "\n".join(program_list)

    def submit_application(self, applicant_name, age, program_choice, grades):
        if program_choice < 1 or program_choice > len(self.programs):
            return "Invalid program choice."
        program = self.programs[program_choice - 1]  # This part is correct
        new_application = Application(applicant_name, age, program, grades)
        self.applications.append(new_application)
        return f"Application submitted successfully! Your Application ID is: {new_application.get_application_id()}"

    def track_application(self, app_id):
        for application in self.applications:
            if application.get_application_id() == int(app_id):
                return application._status
        return "Application ID not found."

    def update_application_status(self, app_id, status):
        for application in self.applications:
            if application.get_application_id() == int(app_id):
                application.update_status(status)
                return "Status updated!"
        return "Application ID not found."

    def list_all_applications(self):
        if not self.applications:
            return "No applications submitted yet."
    
        application_details = []
        for app in self.applications:
            application_details.append(app.display() + "\n" + "-" * 40)

        return "\n".join(application_details)

# Tkinter GUI Implementation
#user window
def display_programs():
    allprograms = system.list_programs()
    messagebox.showinfo("Available Programs", allprograms)

def submit_application():
    name = simpledialog.askstring("Applicant Name", "Enter applicant's name:")
    if not name:
        return
    try:
        age = int(simpledialog.askstring("Applicant Age", "Enter applicant's age:"))
    except ValueError:
        messagebox.showerror("Error", "Age must be a number.")
        return
    programs = system.list_programs()
    program_choice = simpledialog.askinteger("Program Choice", f"Select a program number:\n\n{programs}")
    if not program_choice or program_choice < 1 or program_choice > len(system.programs):
        messagebox.showerror("Error", "Invalid program choice.")
        return
    grades = simpledialog.askstring("Grades", "Enter Grades (comma-separated):").split(", ")
    response = system.submit_application(name, age, program_choice, grades)
    messagebox.showinfo("Submission Status", response)  # Show the response with Application ID

def track_application():
    app_id = simpledialog.askstring("Track Application", "Enter Application ID:")
    if app_id:
        response = system.track_application(app_id.strip())  #strip to clean input
        messagebox.showinfo("Application Status", f"Status: {response}")  #display status
    else:
        messagebox.showerror("Error", "Please enter a valid Application ID.")  #handle empty input

def update_status():
    app_id = simpledialog.askstring("Update Application Status", "Enter Application ID:")
    if not app_id:
        return
    status = simpledialog.askstring("Status", "Enter new status (Pending/Under Review/Accepted/Rejected):")
    if status:
        response = system.update_application_status(app_id.strip(), status.strip())
        messagebox.showinfo("Update Status", response)  # Show the response with status update

def list_applications():
    response = system.list_all_applications()
    messagebox.showinfo("All Applications", response)


#admin window
def open_admin_window():
    admin_pin = simpledialog.askstring("Admin Login", "Enter admin pin: ", show='*')
    if admin_pin == "2001":
        admin_root = tk.Toplevel()  
        admin_root.title("Admin Dashboard")
        
        admin_button_frame = tk.Frame(admin_root, padx=20, pady=20)
        admin_button_frame.pack(pady=10)

        def admin_button(text, command):
            return tk.Button(admin_button_frame, text=text, command=command, width=40, bg="sea green", fg="black", font=("Open Sans", 10), borderwidth=2, relief="raised")

        admin_button("Update Application Status", update_status).pack(pady=8)
        admin_button("List All Applications", list_applications).pack(pady=8)
        admin_button("Close", admin_root.destroy).pack(pady=8)
        
        admin_root.mainloop()  
    else:
        messagebox.showerror("Access Denied", "Incorrect pin.")


system = AdmissionManagementSystem()

root = tk.Tk()
root.title("Admission Management System")

button_frame = tk.Frame(root, padx=20, pady=20)
button_frame.pack(pady=10)

def create_button(text, command):
    return tk.Button(button_frame, text=text, command=command, width=40, bg="sea green", fg="black", font=("Helvetica", 10),
                      borderwidth=2, relief="groove")

create_button("List Available Programs", display_programs).pack(pady=8)
create_button("Submit Application", submit_application).pack(pady=8)
create_button("Track Application", track_application).pack(pady=8)
create_button("Admin Login", open_admin_window).pack(pady=8)
create_button("Exit", root.quit).pack(pady=8)

root.mainloop()

