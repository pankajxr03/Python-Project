
import datetime
from tkinter import *
from tkinter import messagebox, ttk
from .database import get_connection
from .file_utils import export_tasks_to_file


class TaskManager:
    """Main class for managing tasks using OOP structure."""

    def __init__(self, root):
        self.root = root
        self.root.title("🗂️ Daily Task Organizer")
        self.root.geometry("600x500")
        self.root.config(bg="#F5F5F5")

        self.task_input = StringVar()

        Label(root, text="🗓️ Daily Task Organizer", font=("Arial", 18, "bold"),
              bg="#F5F5F5", fg="#333").pack(pady=10)

        self.time_label = Label(root, text=self.get_time(), font=("Arial", 10),
                                bg="#F5F5F5", fg="#666")
        self.time_label.pack(pady=2)

        self.create_input_section()
        self.create_task_table()
        self.create_buttons()
        self.view_tasks()

    # -------------------------
    # Helper Methods
    # -------------------------
    def get_time(self):
        return datetime.datetime.now().strftime("%A, %d %B %Y %I:%M %p")

    def create_input_section(self):
        frame = Frame(self.root, bg="#F5F5F5")
        frame.pack(pady=10)
        Entry(frame, textvariable=self.task_input, width=40,
              font=("Arial", 12)).grid(row=0, column=0, padx=5)
        Button(frame, text="Add Task", command=self.add_task,
               bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)

    def create_task_table(self):
        self.tree = ttk.Treeview(self.root, columns=("ID", "Task", "Status", "Date"), show="headings", height=10)
        for col, width in [("ID", 40), ("Task", 250), ("Status", 100), ("Date", 120)]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=CENTER)
        self.tree.pack(pady=10)

    def create_buttons(self):
        frame = Frame(self.root, bg="#F5F5F5")
        frame.pack(pady=5)
        Button(frame, text="✅ Mark Completed", command=self.mark_done, bg="#2196F3", fg="white", width=15).grid(row=0, column=0, padx=5)
        Button(frame, text="❌ Delete Task", command=self.delete_task, bg="#F44336", fg="white", width=12).grid(row=0, column=1, padx=5)
        Button(frame, text="📂 Export Tasks", command=self.export_tasks, bg="#9C27B0", fg="white", width=13).grid(row=0, column=2, padx=5)
        Button(frame, text="🔄 Refresh", command=self.view_tasks, bg="#FF9800", fg="white", width=10).grid(row=0, column=3, padx=5)

    # -------------------------
    # CRUD Functions
    # -------------------------
    def add_task(self):
        task = self.task_input.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Please enter a task!")
            return
        try:
            conn = get_connection()
            if not conn: return
            cur = conn.cursor()
            cur.execute("INSERT INTO tasks (task, date) VALUES (?, ?)", (task, str(datetime.date.today())))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Task '{task}' added successfully!")
            self.task_input.set("")
            self.view_tasks()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = get_connection()
            if not conn: return
            cur = conn.cursor()
            cur.execute("SELECT * FROM tasks")
            rows = cur.fetchall()
            conn.close()
            for row in rows:
                self.tree.insert("", END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mark_done(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Task", "Please select a task to mark as completed.")
            return
        try:
            task_id = self.tree.item(selected[0])['values'][0]
            conn = get_connection()
            if not conn: return
            cur = conn.cursor()
            cur.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Updated", "Task marked as completed!")
            self.view_tasks()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Task", "Please select a task to delete.")
            return
        try:
            task_id = self.tree.item(selected[0])['values'][0]
            conn = get_connection()
            if not conn: return
            cur = conn.cursor()
            cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Task deleted successfully!")
            self.view_tasks()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_tasks(self):
        # export_tasks_to_file is imported from .file_utils
        if export_tasks_to_file():
            messagebox.showinfo("Exported", "Tasks exported to 'task_report.txt'")
        else:
            # If get_connection fails inside export_tasks_to_file, it will show an error there
            pass