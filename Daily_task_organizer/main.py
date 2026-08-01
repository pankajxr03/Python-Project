
from tkinter import Tk
# Import TaskManager from the 'modules' package
from modules.task_manager import TaskManager


if __name__ == '__main__':
    root = Tk()
    # Create the TaskManager instance
    app = TaskManager(root)
    # Start the Tkinter event loop
    root.mainloop()