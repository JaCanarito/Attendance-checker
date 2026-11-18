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
      
    # Database: initialize, save, clear and export all records.
    def database(self, task, data=None):
        with sqlite3.connect(self.db) as con:
            if task == "init":
                con.execute("""CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY, student_id TEXT, course TEXT, total INTEGER,
                    attended INTEGER, excused INTEGER, unexcused INTEGER, percentage REAL,
                    minimum REAL, remaining INTEGER, status TEXT, date TEXT,
                    UNIQUE(student_id, course))""")
            elif task == "save":
                con.execute("""INSERT INTO students VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)
                    ON CONFLICT(student_id,course) DO UPDATE SET
                    total=excluded.total, attended=excluded.attended, excused=excluded.excused,
                    unexcused=excluded.unexcused, percentage=excluded.percentage,
                    minimum=excluded.minimum, remaining=excluded.remaining,
                    status=excluded.status, date=excluded.date""",
                    (data["DNI"], data["Course"], data["Total"], data["Attended"],
                     data["Excused"], data["Unexcused"], data["Percentage"],
                     data["Minimum"], data["Remaining"], data["Status"],
                     datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            elif task == "clear":
                if messagebox.askyesno("Clear Database", "Delete all saved student records?"):
                    con.execute("DELETE FROM students")
                    messagebox.showinfo("Database", "Database cleared.")
            elif task == "export":
                rows = con.execute("SELECT student_id,course,total,attended,excused,unexcused,percentage,minimum,remaining,status,date FROM students ORDER BY course,student_id").fetchall()
                if not rows:
                    messagebox.showinfo("Database", "There are no saved records.")
                    return
                path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="Attendance_Database.csv", filetypes=[("CSV", "*.csv")])
                if path:
                    with open(path, "w", newline="", encoding="utf-8-sig") as f:
                        w = csv.writer(f, delimiter=";")
                        w.writerow(["Student ID", "Course", "Total Classes", "Attended", "Excused", "Unexcused", "Percentage", "Minimum", "Remaining", "Status", "Date"])
                        w.writerows(rows)
                    messagebox.showinfo("Export", f"Exported {len(rows)} records.")
