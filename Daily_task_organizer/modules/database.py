
import sqlite3
import os
from tkinter import messagebox

DATABASE_NAME = "tasks.db"

def get_connection():
    """
    Establishes a connection to the SQLite database.
    Initializes the database structure if it doesn't exist.
    """
    try:
        # Connect to the database file. It will be created if it doesn't exist.
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Create the 'tasks' table if it doesn't already exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                date TEXT NOT NULL
            )
        """)
        conn.commit()
        return conn
    except sqlite3.Error as e:
        # In a GUI, showing a message box
        messagebox.showerror("Database Error", f"Failed to connect to or initialize database: {e}")
        return None