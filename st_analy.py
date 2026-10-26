import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Smart Student Result Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- SESSION STATE --------------------
if "students" not in st.session_state:
    st.session_state.students = []   # list of dicts

# -------------------- HELPER FUNCTIONS --------------------
def calculate_result(marks):
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
    status = "Pass" if all(m >= 33 for m in marks) else "Fail"
    return round(percentage, 2), grade, status

def get_dataframe():
    if not st.session_state.students:
        return pd.DataFrame(columns=[
            "Roll No", "Name", "Python", "Subject 2", "Subject 3",
            "Percentage", "Grade", "Status"
        ])
    return pd.DataFrame(st.session_state.students)

def update_dashboard(df):
    total = len(df)
    if total == 0:
        return 0, 0.0, "N/A", 0.0
    avg = df["Percentage"].mean()
    topper = df["Percentage"].max()
    pass_rate = (df["Status"] == "Pass").mean() * 100
    return total, avg, topper, pass_rate

# -------------------- SIDEBAR --------------------
st.sidebar.title("⚙️ Actions")
st.sidebar.markdown("---")

# Load Sample Data
if st.sidebar.button("📥 Load Sample Data", use_container_width=True):
    sample = [
        ["101", "Aarav", 89, 78, 91],
        ["102", "Diya", 76, 82, 79],
        ["103", "Rohan", 92, 88, 94],
        ["104", "Ananya", 68, 75, 72],
        ["105", "Vivaan", 95, 91, 97],
        ["151", "Rahul Mehra", 88, 84, 90],
        ["152", "Sneha Arora", 76, 79, 81],
        ["153", "Akash Sharma", 65, 72, 68],
        ["154", "Neha Gupta", 93, 91, 95],
        ["155", "Karan Singh", 58, 62, 60],
        ["156", "Priya Verma", 85, 87, 89],
        ["157", "Aman Kumar", 71, 74, 69],
        ["158", "Simran Kaur", 96, 98, 97],
        ["159", "Rajat Jain", 49, 52, 55],
        ["160", "Pooja Patel", 80, 82, 84],
        ["161", "Mohit Yadav", 67, 64, 70],
        ["162", "Riya Kapoor", 91, 89, 93],
        ["163", "Sachin Das", 54, 58, 56],
        ["164", "Anjali Shah", 87, 85, 88],
        ["165", "Rohit Soni", 73, 76, 74],
        ["166", "Kajal Mishra", 94, 92, 96],
        ["167", "Varun Malhotra", 61, 65, 63],
        ["168", "Tanya Agarwal", 82, 84, 80],
        ["169", "Nitin Arora", 45, 38, 50],
        ["170", "Muskan Sharma", 89, 91, 87],
    ]
    st.session_state.students = []
    for row in sample:
        perc, grade, status = calculate_result(row[2:])
        st.session_state.students.append({
            "Roll No": row[0],
            "Name": row[1],
            "Python": row[2],
            "Subject 2": row[3],
            "Subject 3": row[4],
            "Percentage": perc,
            "Grade": grade,
            "Status": status
        })
    st.sidebar.success(f"Loaded {len(sample)} students!")
    st.rerun()

# Import CSV
uploaded_file = st.sidebar.file_uploader("📂 Import CSV", type=["csv"])
if uploaded_file is not None:
    try:
        df_up = pd.read_csv(uploaded_file)
        required = ["Roll No", "Name", "Python", "Subject 2", "Subject 3"]
        if not all(col in df_up.columns for col in required):
            st.sidebar.error("CSV must contain: " + ", ".join(required))
        else:
            df_up = df_up[required].copy()
            df_up["Roll No"] = df_up["Roll No"].astype(str).str.strip()
            df_up["Name"] = df_up["Name"].astype(str).str.strip()

            if df_up["Roll No"].duplicated().any():
                st.sidebar.error("Duplicate roll numbers in CSV.")
            else:
                existing = {str(s["Roll No"]).lower() for s in st.session_state.students}
                new_students = []
                for _, row in df_up.iterrows():
                    if str(row["Roll No"]).lower() in existing:
                        continue
                    marks = [float(row["Python"]), float(row["Subject 2"]), float(row["Subject 3"])]
                    if any(m < 0 or m > 100 for m in marks):
                        continue
                    perc, grade, status = calculate_result(marks)
                    new_students.append({
                        "Roll No": str(row["Roll No"]),
                        "Name": str(row["Name"]),
                        "Python": marks[0],
                        "Subject 2": marks[1],
                        "Subject 3": marks[2],
                        "Percentage": perc,
                        "Grade": grade,
                        "Status": status
                    })
                st.session_state.students.extend(new_students)
                st.sidebar.success(f"Imported {len(new_students)} students!")
                st.rerun()
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

# Export CSV
if st.session_state.students:
    df_export = get_dataframe()
    csv = df_export.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button(
        label="💾 Export Results (CSV)",
        data=csv,
        file_name="student_results.csv",
        mime="text/csv",
        use_container_width=True
    )

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear All Data", use_container_width=True, type="secondary"):
    st.session_state.students = []
    st.rerun()

# -------------------- MAIN UI --------------------
st.title("📊 Smart Student Result Analyzer")
st.caption("Student Records  |  Result Analysis  |  Performance Reports")

df = get_dataframe()
total, avg, topper, pass_rate = update_dashboard(df)

# Dashboard cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", total)
col2.metric("Class Average", f"{avg:.2f}%")
col3.metric("Highest Result", f"{topper:.2f}%" if isinstance(topper, float) else topper)
col4.metric("Pass Rate", f"{pass_rate:.1f}%")

st.markdown("---")

# -------------------- ADD STUDENT FORM --------------------
with st.expander("➕ Add Student Result", expanded=True):
    with st.form("add_student_form", clear_on_submit=True):
        c1, c2, c3, c4, c5 = st.columns(5)
        roll = c1.text_input("Roll Number *")
        name = c2.text_input("Student Name *")
        python = c3.number_input("Python Marks", min_value=0.0, max_value=100.0, step=0.5, value=0.0)
        sub2 = c4.number_input("Subject 2 Marks", min_value=0.0, max_value=100.0, step=0.5, value=0.0)
        sub3 = c5.number_input("Subject 3 Marks", min_value=0.0, max_value=100.0, step=0.5, value=0.0)

        submitted = st.form_submit_button("Add Student", use_container_width=True)

        if submitted:
            if not roll.strip() or not name.strip():
                st.error("Please enter both Roll Number and Student Name.")
            elif any(str(s["Roll No"]).lower() == roll.strip().lower() for s in st.session_state.students):
                st.error("This roll number already exists.")
            else:
                marks = [python, sub2, sub3]
                perc, grade, status = calculate_result(marks)
                st.session_state.students.append({
                    "Roll No": roll.strip(),
                    "Name": name.strip(),
                    "Python": python,
                    "Subject 2": sub2,
                    "Subject 3": sub3,
                    "Percentage": perc,
                    "Grade": grade,
                    "Status": status
                })
                st.success(f"Added **{name}** | {perc}% | Grade: {grade} | {status}")
                st.rerun()

# -------------------- SEARCH + TABLE --------------------
st.subheader("📋 Student Records")

search = st.text_input("🔍 Search by name or roll number", placeholder="Type to filter...")

if search:
    mask = (
        df["Roll No"].astype(str).str.lower().str.contains(search.lower()) |
        df["Name"].astype(str).str.lower().str.contains(search.lower())
    )
    display_df = df[mask].copy()
else:
    display_df = df.copy()

# Color status
def color_status(val):
    color = "green" if val == "Pass" else "red"
    return f"color: {color}; font-weight: bold"

if not display_df.empty:
    styled = display_df.style.format({
        "Python": "{:.1f}",
        "Subject 2": "{:.1f}",
        "Subject 3": "{:.1f}",
        "Percentage": "{:.2f}%"
    }).map(color_status, subset=["Status"])
    st.dataframe(styled, use_container_width=True, height=400)
else:
    st.info("No student records yet. Add some or load sample data.")

# Delete selected
if not display_df.empty:
    st.markdown("#### Delete a student")
    options = [f"{row['Roll No']} - {row['Name']}" for _, row in display_df.iterrows()]
    to_delete = st.selectbox("Select student to delete", [""] + options)
    if to_delete and st.button("🗑️ Delete Selected", type="primary"):
        roll_to_del = to_delete.split(" - ")[0]
        st.session_state.students = [
            s for s in st.session_state.students if str(s["Roll No"]) != roll_to_del
        ]
        st.success("Student deleted.")
        st.rerun()

# -------------------- TOPPER --------------------
if st.session_state.students:
    topper_row = max(st.session_state.students, key=lambda x: x["Percentage"])
    with st.expander("🏆 Show Topper"):
        st.success(
            f"**Name:** {topper_row['Name']}  \n"
            f"**Roll No:** {topper_row['Roll No']}  \n"
            f"**Percentage:** {topper_row['Percentage']:.2f}%  \n"
            f"**Grade:** {topper_row['Grade']}  \n"
            f"**Status:** {topper_row['Status']}"
        )

st.markdown("---")

# -------------------- CHARTS --------------------
st.subheader("📈 Performance Charts")

if not st.session_state.students:
    st.info("Add students to see charts.")
else:
    chart_tabs = st.tabs([
        "Performance Comparison",
        "Pass / Fail",
        "Grade Distribution",
        "Subject Averages",
        "Percentage Histogram",
        "Top 10 Students"
    ])

    # 1. Performance bar
    with chart_tabs[0]:
        ranked = sorted(st.session_state.students, key=lambda x: x["Percentage"], reverse=True)
        names = [s["Name"] for s in ranked]
        percs = [s["Percentage"] for s in ranked]
        fig, ax = plt.subplots(figsize=(12, 5))
        bars = ax.bar(names, percs, color="#3b82f6")
        ax.set_title("Student Performance Comparison", fontsize=14, fontweight="bold")
        ax.set_ylabel("Percentage (%)")
        ax.set_ylim(0, 110)
        ax.tick_params(axis="x", rotation=45)
        for bar, p in zip(bars, percs):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                    f"{p:.1f}%", ha="center", fontsize=8)
        fig.tight_layout()
        st.pyplot(fig)

    # 2. Pass / Fail pie
    with chart_tabs[1]:
        passed = sum(1 for s in st.session_state.students if s["Status"] == "Pass")
        failed = len(st.session_state.students) - passed
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie([passed, failed], labels=["Pass", "Fail"], autopct="%1.1f%%",
               colors=["#22c55e", "#ef4444"], startangle=90)
        ax.set_title("Pass vs Fail Analysis")
        st.pyplot(fig)

    # 3. Grade distribution
    with chart_tabs[2]:
        grades = {}
        for s in st.session_state.students:
            grades[s["Grade"]] = grades.get(s["Grade"], 0) + 1
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(grades.keys(), grades.values(), color="#f97316")
        ax.set_title("Grade Distribution")
        ax.set_xlabel("Grade")
        ax.set_ylabel("Number of Students")
        st.pyplot(fig)

    # 4. Subject averages
    with chart_tabs[3]:
        py_avg = np.mean([s["Python"] for s in st.session_state.students])
        s2_avg = np.mean([s["Subject 2"] for s in st.session_state.students])
        s3_avg = np.mean([s["Subject 3"] for s in st.session_state.students])
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(["Python", "Subject 2", "Subject 3"], [py_avg, s2_avg, s3_avg],
               color=["#3b82f6", "#22c55e", "#ef4444"])
        ax.set_title("Subject-wise Average Marks")
        ax.set_ylabel("Average Marks")
        ax.set_ylim(0, 100)
        st.pyplot(fig)

    # 5. Histogram
    with chart_tabs[4]:
        percs = [s["Percentage"] for s in st.session_state.students]
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(percs, bins=10, color="#8b5cf6", edgecolor="black")
        ax.set_title("Percentage Distribution")
        ax.set_xlabel("Percentage")
        ax.set_ylabel("Number of Students")
        st.pyplot(fig)

    # 6. Top 10
    with chart_tabs[5]:
        top = sorted(st.session_state.students, key=lambda x: x["Percentage"], reverse=True)[:10]
        names = [s["Name"] for s in top]
        percs = [s["Percentage"] for s in top]
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(names, percs, color="#eab308")
        ax.set_title("Top 10 Students")
        ax.set_ylabel("Percentage (%)")
        ax.tick_params(axis="x", rotation=45)
        ax.set_ylim(0, 110)
        fig.tight_layout()
        st.pyplot(fig)

st.markdown("---")
st.caption("Built with Streamlit • Pass rule: ≥ 33 in every subject")
