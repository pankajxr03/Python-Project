
from Daily_task_organizer.modules.database import get_connection

from tkinter import messagebox
from datetime import date

def export_tasks_to_file():
    """ Fetches all tasks and exports them to 'task_report.txt' """
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute("SELECT id, task, status, date FROM tasks ORDER BY id")
        rows = cur.fetchall()
        conn.close()

        if not rows:
            messagebox.showinfo("Export Info", "No tasks found to export.")
            return True

        file_name = "task_report.txt"
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write("--- Daily Task Organizer Report ---\n")
            f.write(f"Generated on: {date.today()} (System Date)\n\n")
            f.write(f"{'ID':<4} | {'Task':<30} | {'Status':<10} | {'Date Added':<10}\n")
            f.write("-" * 60 + "\n")

            for row in rows:
                f.write(f"{row[0]:<4} | {row[1]:<30} | {row[2]:<10} | {row[3]:<10}\n")

        return True

    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred during export: {e}")
        return False
    finally:
        if conn:
            conn.close()
