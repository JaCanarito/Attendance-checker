import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3, csv, os, math
from datetime import datetime


class AttendanceApp:
    def __init__(self, root):
        self.root = root
        root.title("Attendance Control - Course Report")
        root.geometry("1000x700")
        root.configure(bg="#F3F6FC")
        folder = os.path.dirname(os.path.abspath(__file__))
        self.db = os.path.join(folder, "asistencia.db")
        self.report = None
        try:
            self.logo = tk.PhotoImage(file=os.path.join(folder, "logotype.png"))
            root.iconphoto(True, self.logo)
        except tk.TclError:
            self.logo = None
            messagebox.showwarning("Logo Not Found", "Place logotype.png next to the program.")
        self.database("init")
        self.build()
      
