import tkinter as tk
from tkinter import ttk, messagebox
from database import TaskDatabase
from datetime import datetime

class TaskManager:
    def __init__(self, root, db_name="data/task_manager.db"):
        self.db = TaskDatabase(db_name)
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("800x600")  # Window size

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Input Frame
        self.input_frame = ttk.Frame(self.root, padding="10")
        self.input_frame.grid(row=0, column=0, sticky="ew")

        # Labels and Entries
        ttk.Label(self.input_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(self.input_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(self.input_frame)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        self.due_date_entry = ttk.Entry(self.input_frame)
        self.due_date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Category:").grid(row=3, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(self.input_frame)
        self.category_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Task ID (for update/delete):").grid(row=4, column=0, padx=5, pady=5)
        self.id_entry = ttk.Entry(self.input_frame)
        self.id_entry.grid(row=4, column=1, padx=5, pady=5)

        # Button Frame
        self.button_frame = ttk.Frame(self.root, padding="10")
        self.button_frame.grid(row=1, column=0, sticky="ew")

        ttk.Button(self.button_frame, text="Add Task", command=self.add_task).grid(row=0, column=0, padx=5)
        ttk.Button(self.button_frame, text="View All Tasks", command=self.view_all_tasks).grid(row=0, column=1, padx=5)
        ttk.Button(self.button_frame, text="View by Category", command=self.view_by_category).grid(row=0, column=2, padx=5)
        ttk.Button(self.button_frame, text="Update Task", command=self.update_task).grid(row=0, column=3, padx=5)
        ttk.Button(self.button_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=4, padx=5)
        ttk.Button(self.button_frame, text="Clear Fields", command=self.clear_fields).grid(row=0, column=5, padx=5)

        # Table Frame
        self.table_frame = ttk.Frame(self.root, padding="10")
        self.table_frame.grid(row=2, column=0, sticky="nsew")

        self.tree = ttk.Treeview(self.table_frame, columns=("ID", "Title", "Description", "Due Date", "Category"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Category", text="Category")
        self.tree.column("ID", width=50)
        self.tree.column("Title", width=150)
        self.tree.column("Description", width=200)
        self.tree.column("Due Date", width=100)
        self.tree.column("Category", width=100)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Styling
        self.root.style = ttk.Style()
        self.root.style.theme_use("clam")
        self.root.option_add("*Font", "Arial 12")

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.rowconfigure(0, weight=1)

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_task(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Title cannot be empty.")
            return
        desc = self.desc_entry.get().strip() or None
        due_date = self.due_date_entry.get().strip()
        if not due_date:
            messagebox.showerror("Error", "Due date cannot be empty.")
            return
        if not self.validate_date(due_date):
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return
        category = self.category_entry.get().strip()
        if not category:
            messagebox.showerror("Error", "Category cannot be empty.")
            return
        if self.db.add_task(title, desc, due_date, category):
            messagebox.showinfo("Success", "Task added successfully")
            self.clear_fields()
            self.view_all_tasks()
        else:
            messagebox.showerror("Error", "Failed to add task.")

    def view_all_tasks(self):
        self.tree.delete(*self.tree.get_children())
        tasks = self.db.view_tasks()
        for task in tasks:
            self.tree.insert("", "end", values=(task[0], task[1], task[2] or "None", task[3], task[4]))

    def view_by_category(self):
        from tkinter import simpledialog
        category = simpledialog.askstring("Input", "Enter category:")
        if category:
            self.tree.delete(*self.tree.get_children())
            tasks = self.db.view_tasks(category)
            for task in tasks:
                self.tree.insert("", "end", values=(task[0], task[1], task[2] or "None", task[3], task[4]))
        else:
            messagebox.showerror("Error", "Category cannot be empty.")

    def update_task(self):
        try:
            task_id = int(self.id_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Invalid Task ID.")
            return
        title = self.title_entry.get().strip() or None
        desc = self.desc_entry.get().strip() or None
        due_date = self.due_date_entry.get().strip() or None
        if due_date and not self.validate_date(due_date):
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return
        category = self.category_entry.get().strip() or None
        if self.db.update_task(task_id, title, desc, due_date, category):
            messagebox.showinfo("Success", "Task updated successfully")
            self.clear_fields()
            self.view_all_tasks()
        else:
            messagebox.showerror("Error", "Failed to update task. Task ID may not exist.")

    def delete_task(self):
        try:
            task_id = int(self.id_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Invalid Task ID.")
            return
        if self.db.delete_task(task_id):
            messagebox.showinfo("Success", "Task deleted successfully")
            self.clear_fields()
            self.view_all_tasks()
        else:
            messagebox.showerror("Error", "Failed to delete task. Task ID may not exist.")

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()