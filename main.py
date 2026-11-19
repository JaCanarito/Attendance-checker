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

    # Build the window and all controls.
    def build(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=9)
        header = tk.Frame(self.root, bg="#08294D", height=115)
        header.pack(fill="x")
        if self.logo:
            self.logo_small = self.logo.subsample(2, 2)
            tk.Label(header, image=self.logo_small, bg="#08294D").pack(side="left", padx=25, pady=10)
        tk.Label(header, text="Attendance Report", bg="#08294D", fg="white", font=("Segoe UI", 27, "bold")).pack(side="left")

        body = tk.Frame(self.root, bg="#F3F6FC", padx=25, pady=20)
        body.pack(fill="both", expand=True)
        form = tk.LabelFrame(body, text=" Course and Attendance Information ", bg="white", padx=18, pady=15, font=("Segoe UI", 12, "bold"))
        form.pack(side="left", fill="both", expand=True, padx=(0, 18))
        result = tk.LabelFrame(body, text=" Result ", bg="#E8F0FC", padx=15, pady=15, font=("Segoe UI", 12, "bold"))
        result.pack(side="right", fill="both", expand=True)

        names = [("Course Name", "course", ""), ("Student ID", "dni", ""),
                 ("Total Classes Held", "total", ""), ("Classes Attended", "attended", ""),
                 ("Excused Absences", "excused", "0"), ("Minimum Required (%)", "minimum", "80")]
        self.fields = {}
        for r, (label, key, default) in enumerate(names):
            tk.Label(form, text=label, bg="white", fg="#102A43", font=("Segoe UI", 11)).grid(row=r, column=0, sticky="w", pady=10)
            entry = ttk.Entry(form, width=28, font=("Segoe UI", 11))
            entry.grid(row=r, column=1, sticky="ew", padx=12, pady=10)
            entry.insert(0, default)
            self.fields[key] = entry
        form.columnconfigure(1, weight=1)
    
        self.gauge = tk.Canvas(result, width=230, height=220, bg="#E8F0FC", highlightthickness=0)
        self.gauge.pack(pady=8)
        self.state = tk.Label(result, text="PENDING", bg="#C9D6E8", fg="#173B63", font=("Segoe UI", 18, "bold"), pady=10)
        self.state.pack(fill="x", pady=10)
        self.details = tk.Label(result, text="Enter the details and calculate attendance.", bg="#E8F0FC", fg="#173B63", font=("Segoe UI", 11), wraplength=300, justify="center")
        self.details.pack(fill="x", pady=10)
        self.action("gauge", 0, "#9AAAC0")

        buttons = tk.Frame(self.root, bg="#F3F6FC", padx=18, pady=12)
        buttons.pack(fill="x")
        for label, command in [("Calculate Attendance", self.calculate),
                               ("Export Report", lambda: self.action("report")),
                               ("Clear Fields", lambda: self.action("clear")),
                               ("Export Database", lambda: self.database("export")),
                               ("Clear Database", lambda: self.database("clear"))]:
            ttk.Button(buttons, text=label, command=command).pack(side="left", expand=True, fill="x", padx=4)
