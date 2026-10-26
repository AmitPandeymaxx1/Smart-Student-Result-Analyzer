import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt

# -------------------- DATA --------------------
students = []
columns = (
    "Roll No", "Name", "Python", "Subject 2",
    "Subject 3", "Percentage", "Grade", "Status"
)

# -------------------- MAIN WINDOW --------------------
root = tk.Tk()
root.title("Smart Student Result Analyzer")
root.geometry("1150x720")
root.minsize(950, 600)
root.configure(bg="#f1f5f9")

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    rowheight=30,
    font=("Segoe UI", 10),
    background="white",
    fieldbackground="white"
)
style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 10, "bold"),
    background="#dbeafe",
    foreground="#1e3a8a",
    padding=8
)
style.configure("TButton", font=("Segoe UI", 10), padding=7)

# -------------------- HEADER --------------------
header = tk.Frame(root, bg="#1e3a8a", height=85)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="SMART STUDENT RESULT ANALYZER",
    font=("Segoe UI", 21, "bold"),
    bg="#1e3a8a",
    fg="white"
).pack(pady=(12, 2))

tk.Label(
    header,
    text="Student Records  |  Result Analysis  |  Performance Reports",
    font=("Segoe UI", 10),
    bg="#1e3a8a",
    fg="#dbeafe"
).pack()

# -------------------- DASHBOARD --------------------
dashboard = tk.Frame(root, bg="#f1f5f9")
dashboard.pack(fill="x", padx=15, pady=12)

def create_card(parent, title, color):
    card = tk.Frame(parent, bg="white", bd=1, relief="solid")
    card.pack(side="left", fill="x", expand=True, padx=5)

    tk.Label(
        card, text=title, bg="white", fg="#64748b",
        font=("Segoe UI", 10)
    ).pack(pady=(10, 2))

    value = tk.Label(
        card, text="0", bg="white", fg=color,
        font=("Segoe UI", 19, "bold")
    )
    value.pack(pady=(0, 10))
    return value

total_label   = create_card(dashboard, "Total Students", "#2563eb")
average_label = create_card(dashboard, "Class Average",  "#7c3aed")
topper_label  = create_card(dashboard, "Highest Result", "#059669")
pass_label    = create_card(dashboard, "Pass Rate",      "#ea580c")

# -------------------- INPUT FORM --------------------
form = ttk.LabelFrame(root, text=" Add Student Result ", padding=12)
form.pack(fill="x", padx=20, pady=5)

fields = [
    ("Roll Number", 0),
    ("Student Name", 1),
    ("Python Marks", 2),
    ("Subject 2 Marks", 3),
    ("Subject 3 Marks", 4)
]

entries = {}
for label, col in fields:
    ttk.Label(form, text=label).grid(row=0, column=col, padx=7, pady=(0, 5), sticky="w")
    entry = ttk.Entry(form, width=19)
    entry.grid(row=1, column=col, padx=7, pady=3, sticky="ew")
    entries[label] = entry

form.columnconfigure(tuple(range(5)), weight=1)

roll_entry   = entries["Roll Number"]
name_entry   = entries["Student Name"]
mark_entries = [
    entries["Python Marks"],
    entries["Subject 2 Marks"],
    entries["Subject 3 Marks"]
]

# -------------------- STUDENT TABLE --------------------
table_frame = ttk.LabelFrame(root, text=" Student Records ", padding=10)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

search_frame = ttk.Frame(table_frame)
search_frame.pack(fill="x", pady=(0, 8))

ttk.Label(search_frame, text="Search by name or roll number:").pack(side="left", padx=(0, 8))
search_var = tk.StringVar()
search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30)
search_entry.pack(side="left", padx=5)

tree_frame = ttk.Frame(table_frame)
tree_frame.pack(fill="both", expand=True)

tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

yscroll = ttk.Scrollbar(tree_frame, orient="vertical",   command=tree.yview)
xscroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

yscroll.pack(side="right", fill="y")
xscroll.pack(side="bottom", fill="x")
tree.pack(fill="both", expand=True)

widths = [90, 150, 100, 110, 110, 110, 75, 85]
for col, width in zip(columns, widths):
    tree.heading(col, text=col, command=lambda c=col: sort_by(c))
    tree.column(col, width=width, minwidth=65, anchor="center")

tree.tag_configure("pass", foreground="#047857")
tree.tag_configure("fail", foreground="#dc2626")

# -------------------- SORTING --------------------
sort_directions = {}

def sort_by(column):
    reverse = sort_directions.get(column, False)

    if column in ("Percentage", "Python", "Subject 2", "Subject 3"):
        key_func = lambda s: float(s[columns.index(column)])
    else:
        key_func = lambda s: str(s[columns.index(column)]).lower()

    students.sort(key=key_func, reverse=reverse)
    sort_directions[column] = not reverse
    refresh_table()

# -------------------- DASHBOARD UPDATE --------------------
def update_dashboard():
    total = len(students)
    total_label.config(text=str(total))

    if total == 0:
        average_label.config(text="0.00%")
        topper_label.config(text="N/A")
        pass_label.config(text="0%")
        return

    avg    = sum(s[5] for s in students) / total
    topper = max(students, key=lambda s: s[5])
    passed = sum(1 for s in students if s[7] == "Pass")

    average_label.config(text=f"{avg:.2f}%")
    topper_label.config(text=f"{topper[5]:.2f}%")
    pass_label.config(text=f"{passed / total * 100:.1f}%")

# -------------------- TABLE REFRESH --------------------
def refresh_table(*args):
    query = search_var.get().strip().lower()

    for item in tree.get_children():
        tree.delete(item)

    for student in students:
        if query and query not in str(student[0]).lower() and query not in str(student[1]).lower():
            continue

        tag = "pass" if student[7] == "Pass" else "fail"
        display_values = list(student)
        display_values[5] = f"{student[5]:.2f}%"

        tree.insert("", "end", values=display_values, tags=(tag,))

    update_dashboard()

search_var.trace_add("write", refresh_table)

# -------------------- ADD STUDENT --------------------
def add_student():
    roll = roll_entry.get().strip()
    name = name_entry.get().strip()

    if not roll or not name:
        messagebox.showwarning("Missing Information", "Please enter both roll number and student name.")
        return

    if any(s[0].lower() == roll.lower() for s in students):
        messagebox.showerror("Duplicate Roll Number", "This roll number already exists.")
        return

    try:
        marks = [float(entry.get()) for entry in mark_entries]
    except ValueError:
        messagebox.showerror("Invalid Marks", "Enter a valid number for all three subjects.")
        return

    if any(mark < 0 or mark > 100 for mark in marks):
        messagebox.showerror("Marks Out of Range", "Marks must be between 0 and 100.")
        return

    percentage = sum(marks) / len(marks)

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"

    # Must score at least 33 in every subject to pass
    status = "Pass" if all(m >= 33 for m in marks) else "Fail"

    student = [roll, name, marks[0], marks[1], marks[2], percentage, grade, status]
    students.append(student)
    refresh_table()
    clear_fields()

    messagebox.showinfo(
        "Result Added",
        f"Student: {name}\nPercentage: {percentage:.2f}%\nGrade: {grade}\nStatus: {status}"
    )

# -------------------- LOAD DATASET --------------------
def load_dataset():
    path = filedialog.askopenfilename(
        title="Select Student Dataset",
        filetypes=[("CSV Files", "*.csv")]
    )
    if not path:
        return

    try:
        df = pd.read_csv(path)

        required = ["Roll No", "Name", "Python", "Subject 2", "Subject 3"]
        if not all(col in df.columns for col in required):
            messagebox.showerror("Invalid Dataset", "CSV must contain: " + ", ".join(required))
            return

        df = df[required].copy()
        df["Roll No"] = df["Roll No"].astype("string").str.strip()
        df["Name"]    = df["Name"].astype("string").str.strip()

        if (df["Roll No"].isna().any() or df["Name"].isna().any() or
                df["Roll No"].eq("").any() or df["Name"].eq("").any()):
            messagebox.showerror("Invalid Data", "Roll numbers and names cannot be empty.")
            return

        if df["Roll No"].duplicated().any():
            messagebox.showerror("Duplicate Data", "The dataset contains duplicate roll numbers.")
            return

        for col in ["Python", "Subject 2", "Subject 3"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        marks = df[["Python", "Subject 2", "Subject 3"]]
        if marks.isna().any().any() or ((marks < 0) | (marks > 100)).any().any():
            messagebox.showerror("Invalid Marks", "All marks must be numbers between 0 and 100.")
            return

        existing_rolls = {str(s[0]).lower() for s in students}
        if any(str(roll).lower() in existing_rolls for roll in df["Roll No"].tolist()):
            messagebox.showerror("Duplicate Roll Number", "Some roll numbers already exist in the app.")
            return

        imported = []
        for _, row in df.iterrows():
            m1 = float(row["Python"])
            m2 = float(row["Subject 2"])
            m3 = float(row["Subject 3"])

            percentage = (m1 + m2 + m3) / 3

            if percentage >= 90:   grade = "A+"
            elif percentage >= 80: grade = "A"
            elif percentage >= 70: grade = "B"
            elif percentage >= 60: grade = "C"
            elif percentage >= 40: grade = "D"
            else:                  grade = "F"

            status = "Pass" if all(m >= 33 for m in [m1, m2, m3]) else "Fail"

            imported.append([
                str(row["Roll No"]), str(row["Name"]),
                m1, m2, m3, percentage, grade, status
            ])

        students.extend(imported)
        refresh_table()
        messagebox.showinfo("Import Successful", f"Imported {len(imported)} students successfully!")

    except Exception as error:
        messagebox.showerror("Import Error", str(error))

# -------------------- CLEAR INPUTS --------------------
def clear_fields():
    for entry in entries.values():
        entry.delete(0, tk.END)
    roll_entry.focus_set()

# -------------------- DELETE STUDENT --------------------
def delete_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Select a student record to delete.")
        return

    values = tree.item(selected[0], "values")
    roll = str(values[0])

    if not messagebox.askyesno("Confirm Delete", f"Delete the record for {values[1]} ({roll})?"):
        return

    students[:] = [s for s in students if str(s[0]) != roll]
    refresh_table()

# -------------------- SHOW TOPPER --------------------
def show_topper():
    if not students:
        messagebox.showinfo("Topper", "No student records available.")
        return

    topper = max(students, key=lambda s: s[5])
    messagebox.showinfo(
        "Top Performer",
        f"Name: {topper[1]}\nRoll Number: {topper[0]}\n"
        f"Percentage: {topper[5]:.2f}%\nGrade: {topper[6]}\nStatus: {topper[7]}"
    )

# -------------------- SAVE CSV --------------------
def save_csv():
    if not students:
        messagebox.showwarning("No Data", "Add students before exporting.")
        return

    path = filedialog.asksaveasfilename(
        title="Export Student Results",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="student_results.csv"
    )
    if not path:
        return

    try:
        df = pd.DataFrame(students, columns=columns)
        df["Percentage"] = df["Percentage"].round(2)
        df.to_csv(path, index=False)
        messagebox.showinfo("Export Successful", f"Results saved successfully:\n{path}")
    except Exception as error:
        messagebox.showerror("Export Error", str(error))

# -------------------- PERFORMANCE CHART --------------------
def show_chart():
    if not students:
        messagebox.showwarning("No Data", "Add students to view the performance chart.")
        return

    ranked = sorted(students, key=lambda s: s[5], reverse=True)
    names = [s[1] for s in ranked]
    percentages = [s[5] for s in ranked]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(names, percentages, color="#3b82f6")

    ax.set_title("Student Performance Comparison", fontsize=14, fontweight="bold")
    ax.set_xlabel("Students")
    ax.set_ylabel("Percentage (%)")
    ax.set_ylim(0, 110)
    ax.tick_params(axis="x", rotation=35)

    for bar, percentage in zip(bars, percentages):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.5,
            f"{percentage:.1f}%",
            ha="center", fontsize=9
        )

    fig.tight_layout()
    plt.show()
# PASTE NEW CHART FUNCTIONS HERE
def show_pie_chart():
    if not students:
        return

    passed = sum(1 for s in students if s[7] == "Pass")
    failed = len(students) - passed

    plt.figure(figsize=(6,6))
    plt.pie(
        [passed, failed],
        labels=["Pass", "Fail"],
        autopct="%1.1f%%",
        colors=["green", "red"]
    )
    plt.title("Pass vs Fail Analysis")
    plt.show()
def show_grade_chart():
    grades = {}

    for s in students:
        grade = s[6]
        grades[grade] = grades.get(grade, 0) + 1

    plt.figure(figsize=(8,5))
    plt.bar(grades.keys(), grades.values(), color="orange")

    plt.title("Grade Distribution")
    plt.xlabel("Grade")
    plt.ylabel("Number of Students")

    plt.show()
def show_subject_chart():
    if not students:
        return

    python_avg = sum(s[2] for s in students) / len(students)
    sub2_avg = sum(s[3] for s in students) / len(students)
    sub3_avg = sum(s[4] for s in students) / len(students)

    subjects = ["Python", "Subject 2", "Subject 3"]
    averages = [python_avg, sub2_avg, sub3_avg]

    plt.figure(figsize=(7,5))
    plt.bar(subjects, averages,
            color=["blue", "green", "red"])

    plt.title("Subject-wise Average Marks")
    plt.ylabel("Average Marks")
    plt.show()
def show_histogram():
    if not students:
        return

    percentages = [s[5] for s in students]

    plt.figure(figsize=(8,5))
    plt.hist(
        percentages,
        bins=10,
        color="purple",
        edgecolor="black"
    )

    plt.title("Percentage Distribution")
    plt.xlabel("Percentage")
    plt.ylabel("Students")
    plt.show()
def show_top10():
    if not students:
        return

    top = sorted(
        students,
        key=lambda s: s[5],
        reverse=True
    )[:10]

    names = [s[1] for s in top]
    percentages = [s[5] for s in top]

    plt.figure(figsize=(10,5))
    plt.bar(names, percentages, color="gold")

    plt.title("Top 10 Students")
    plt.xticks(rotation=45)
    plt.show()  
# -------------------- BUTTONS --------------------
def load_sample_data():
    sample = [
    ["101","Aarav",89,78,91],
    ["102","Diya",76,82,79],
    ["103","Rohan",92,88,94],
    ["104","Ananya",68,75,72],
    ["105","Vivaan",95,91,97],

    ["151","Rahul Mehra",88,84,90],
    ["152","Sneha Arora",76,79,81],
    ["153","Akash Sharma",65,72,68],
    ["154","Neha Gupta",93,91,95],
    ["155","Karan Singh",58,62,60],
    ["156","Priya Verma",85,87,89],
    ["157","Aman Kumar",71,74,69],
    ["158","Simran Kaur",96,98,97],
    ["159","Rajat Jain",49,52,55],
    ["160","Pooja Patel",80,82,84],
    ["161","Mohit Yadav",67,64,70],
    ["162","Riya Kapoor",91,89,93],
    ["163","Sachin Das",54,58,56],
    ["164","Anjali Shah",87,85,88],
    ["165","Rohit Soni",73,76,74],
    ["166","Kajal Mishra",94,92,96],
    ["167","Varun Malhotra",61,65,63],
    ["168","Tanya Agarwal",82,84,80],
    ["169","Nitin Arora",45,38,50],
    ["170","Muskan Sharma",89,91,87]
]

    for row in sample:
        percentage = sum(row[2:]) / 3

        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 40:
            grade = "D"
        else:
            grade = "F"

        status = "Pass" if all(m >= 33 for m in row[2:]) else "Fail"

        students.append([
            row[0], row[1],
            row[2], row[3], row[4],
            percentage,
            grade,
            status
        ])

    refresh_table()

# -------------------- BUTTONS --------------------

button_frame = ttk.Frame(root)
button_frame.pack(fill="x", padx=20, pady=(0, 15))

ttk.Button(button_frame, text="Add Student",
           command=add_student).pack(side="left", padx=4)

ttk.Button(button_frame, text="Clear Form",
           command=clear_fields).pack(side="left", padx=4)

ttk.Button(button_frame, text="Delete Selected",
           command=delete_student).pack(side="left", padx=4)

ttk.Button(button_frame, text="Show Topper",
           command=show_topper).pack(side="left", padx=4)

ttk.Button(button_frame, text="Performance Chart",
           command=show_chart).pack(side="left", padx=4)

ttk.Button(button_frame, text="Pass/Fail Pie",
           command=show_pie_chart).pack(side="left", padx=4)

ttk.Button(button_frame, text="Grade Analysis",
           command=show_grade_chart).pack(side="left", padx=4)

ttk.Button(button_frame, text="Subject Average",
           command=show_subject_chart).pack(side="left", padx=4)

ttk.Button(button_frame, text="Histogram",
           command=show_histogram).pack(side="left", padx=4)

ttk.Button(button_frame, text="Top 10 Students",
           command=show_top10).pack(side="left", padx=4)
ttk.Button(
    button_frame,
    text="Load Sample Data",
    command=load_sample_data
).pack(side="left", padx=4)

# -------------------- START --------------------
root.mainloop()