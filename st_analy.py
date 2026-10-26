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

# -------------------- CUSTOM CSS (COLORS) --------------------
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f8fafc 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #1e3a8a, #2563eb, #3b82f6);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.25);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .main-header p {
        margin: 0.3rem 0 0 0;
        opacity: 0.9;
        font-size: 1rem;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.3);
        color: white !important;
        border-radius: 10px;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.25);
        border-color: white;
    }
    section[data-testid="stSidebar"] .stDownloadButton > button {
        background: #22c55e !important;
        border: none !important;
        color: white !important;
    }

    /* Form & Expander */
    .stExpander {
        border: 2px solid #bfdbfe;
        border-radius: 14px;
        background: white;
    }
    
    /* Success / Error boxes */
    .stSuccess {
        background-color: #dcfce7;
        border-left: 5px solid #22c55e;
    }
    .stError {
        background-color: #fee2e2;
        border-left: 5px solid #ef4444;
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: #e0f2fe;
        border-radius: 10px 10px 0 0;
        padding: 10px 18px;
        font-weight: 600;
        color: #1e40af;
    }
    .stTabs [aria-selected="true"] {
        background: #2563eb !important;
        color: white !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1.2rem;
    }
    
    /* Custom colored buttons via HTML classes */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------
if "students" not in st.session_state:
    st.session_state.students = []

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
st.sidebar.markdown("## ⚙️ Actions")
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
    st.sidebar.success(f"✅ Loaded {len(sample)} students!")
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
                st.sidebar.success(f"✅ Imported {len(new_students)} students!")
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
if st.sidebar.button("🗑️ Clear All Data", use_container_width=True):
    st.session_state.students = []
    st.rerun()

# -------------------- MAIN HEADER --------------------
st.markdown("""
<div class="main-header">
    <h1>📊 Smart Student Result Analyzer</h1>
    <p>Student Records  •  Result Analysis  •  Performance Reports</p>
</div>
""", unsafe_allow_html=True)

df = get_dataframe()
total, avg, topper, pass_rate = update_dashboard(df)

# -------------------- DASHBOARD CARDS --------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("👥 Total Students", total)
with c2:
    st.metric("📈 Class Average", f"{avg:.2f}%")
with c3:
    st.metric("🏆 Highest Result", f"{topper:.2f}%" if isinstance(topper, (int, float)) else topper)
with c4:
    st.metric("✅ Pass Rate", f"{pass_rate:.1f}%")

st.markdown("")

# -------------------- ADD STUDENT FORM --------------------
with st.expander("➕  Add New Student Result", expanded=True):
    with st.form("add_student_form", clear_on_submit=True):
        c1, c2, c3, c4, c5 = st.columns(5)
        roll = c1.text_input("Roll Number *", placeholder="e.g. 101")
        name = c2.text_input("Student Name *", placeholder="Full Name")
        python = c3.number_input("Python Marks", min_value=0.0, max_value=100.0, step=0.5, value=0.0)
        sub2 = c4.number_input("Subject 2 Marks", min_value=0.0, max_value=100.0, step=0.5, value=0.0)
        sub3 = c5.number_input("Subject 3 Marks", min_value=0.0, max_value=100.0, step=0.5, value=0.0)

        submitted = st.form_submit_button("✨ Add Student", use_container_width=True, type="primary")

        if submitted:
            if not roll.strip() or not name.strip():
                st.error("⚠️ Please enter both Roll Number and Student Name.")
            elif any(str(s["Roll No"]).lower() == roll.strip().lower() for s in st.session_state.students):
                st.error("🚫 This roll number already exists.")
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
                st.success(f"✅ Added **{name}** → {perc}% | Grade: **{grade}** | **{status}**")
                st.rerun()

# -------------------- SEARCH + TABLE --------------------
st.subheader("📋 Student Records")

search = st.text_input("🔍 Search by name or roll number", placeholder="Type to filter students...")

if search:
    mask = (
        df["Roll No"].astype(str).str.lower().str.contains(search.lower()) |
        df["Name"].astype(str).str.lower().str.contains(search.lower())
    )
    display_df = df[mask].copy()
else:
    display_df = df.copy()

def color_status(val):
    if val == "Pass":
        return "background-color: #dcfce7; color: #166534; font-weight: bold"
    return "background-color: #fee2e2; color: #991b1b; font-weight: bold"

def color_grade(val):
    colors = {
        "A+": "background-color: #dbeafe; color: #1e40af; font-weight: bold",
        "A":  "background-color: #e0e7ff; color: #3730a3; font-weight: bold",
        "B":  "background-color: #fef3c7; color: #92400e; font-weight: bold",
        "C":  "background-color: #ffedd5; color: #9a3412; font-weight: bold",
        "D":  "background-color: #fce7f3; color: #9d174d; font-weight: bold",
        "F":  "background-color: #fee2e2; color: #991b1b; font-weight: bold",
    }
    return colors.get(val, "")

if not display_df.empty:
    styled = (display_df.style
              .format({
                  "Python": "{:.1f}",
                  "Subject 2": "{:.1f}",
                  "Subject 3": "{:.1f}",
                  "Percentage": "{:.2f}%"
              })
              .map(color_status, subset=["Status"])
              .map(color_grade, subset=["Grade"]))
    st.dataframe(styled, use_container_width=True, height=420)
else:
    st.info("📭 No student records yet. Add some students or load the sample data from the sidebar.")

# Delete selected
if not display_df.empty:
    st.markdown("#### 🗑️ Delete a student")
    options = [f"{row['Roll No']} - {row['Name']}" for _, row in display_df.iterrows()]
    col_del1, col_del2 = st.columns([3, 1])
    with col_del1:
        to_delete = st.selectbox("Select student to delete", [""] + options, label_visibility="collapsed")
    with col_del2:
        if to_delete and st.button("Delete", type="primary", use_container_width=True):
            roll_to_del = to_delete.split(" - ")[0]
            st.session_state.students = [
                s for s in st.session_state.students if str(s["Roll No"]) != roll_to_del
            ]
            st.success("Student deleted successfully.")
            st.rerun()

# -------------------- TOPPER --------------------
if st.session_state.students:
    topper_row = max(st.session_state.students, key=lambda x: x["Percentage"])
    with st.expander("🏆  View Class Topper"):
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #fef3c7, #fde68a); 
                    padding: 1.2rem 1.5rem; border-radius: 12px; 
                    border-left: 6px solid #f59e0b;">
            <h3 style="margin:0; color:#92400e;">🥇 {topper_row['Name']}</h3>
            <p style="margin:0.4rem 0 0 0; color:#78350f; font-size:1.05rem;">
                Roll No: <b>{topper_row['Roll No']}</b> &nbsp;|&nbsp; 
                Percentage: <b>{topper_row['Percentage']:.2f}%</b> &nbsp;|&nbsp; 
                Grade: <b>{topper_row['Grade']}</b> &nbsp;|&nbsp; 
                Status: <b>{topper_row['Status']}</b>
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# -------------------- CHARTS --------------------
st.subheader("📈 Performance Charts")

if not st.session_state.students:
    st.info("Add students to unlock beautiful performance charts.")
else:
    chart_tabs = st.tabs([
        "📊 Performance Comparison",
        "🟢 Pass / Fail",
        "🏅 Grade Distribution",
        "📚 Subject Averages",
        "📉 Percentage Histogram",
        "🥇 Top 10 Students"
    ])

    # 1. Performance bar
    with chart_tabs[0]:
        ranked = sorted(st.session_state.students, key=lambda x: x["Percentage"], reverse=True)
        names = [s["Name"] for s in ranked]
        percs = [s["Percentage"] for s in ranked]
        
        fig, ax = plt.subplots(figsize=(12, 5.5))
        colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(names)))
        bars = ax.bar(names, percs, color=colors, edgecolor="white", linewidth=0.7)
        ax.set_title("Student Performance Comparison", fontsize=15, fontweight="bold", color="#1e3a8a", pad=15)
        ax.set_ylabel("Percentage (%)", fontsize=11)
        ax.set_ylim(0, 112)
        ax.tick_params(axis="x", rotation=45)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3)
        for bar, p in zip(bars, percs):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.8,
                    f"{p:.1f}%", ha="center", fontsize=8, fontweight="bold", color="#1e40af")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)

    # 2. Pass / Fail pie
    with chart_tabs[1]:
        passed = sum(1 for s in st.session_state.students if s["Status"] == "Pass")
        failed = len(st.session_state.students) - passed
        
        fig, ax = plt.subplots(figsize=(7, 6))
        wedges, texts, autotexts = ax.pie(
            [passed, failed],
            labels=["Pass", "Fail"],
            autopct="%1.1f%%",
            colors=["#22c55e", "#ef4444"],
            startangle=90,
            explode=(0.03, 0.03),
            shadow=True,
            textprops={'fontsize': 12, 'fontweight': 'bold'}
        )
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(13)
        ax.set_title("Pass vs Fail Analysis", fontsize=15, fontweight="bold", color="#1e3a8a", pad=12)
        st.pyplot(fig, use_container_width=True)

    # 3. Grade distribution
    with chart_tabs[2]:
        grades = {}
        for s in st.session_state.students:
            grades[s["Grade"]] = grades.get(s["Grade"], 0) + 1
        
        # Sort grades logically
        order = ["A+", "A", "B", "C", "D", "F"]
        sorted_grades = {k: grades[k] for k in order if k in grades}
        
        grade_colors = {
            "A+": "#3b82f6", "A": "#6366f1", "B": "#f59e0b",
            "C": "#f97316", "D": "#ec4899", "F": "#ef4444"
        }
        colors = [grade_colors.get(g, "#94a3b8") for g in sorted_grades.keys()]
        
        fig, ax = plt.subplots(figsize=(9, 5.5))
        bars = ax.bar(sorted_grades.keys(), sorted_grades.values(), color=colors, edgecolor="white", linewidth=1.2)
        ax.set_title("Grade Distribution", fontsize=15, fontweight="bold", color="#1e3a8a", pad=12)
        ax.set_xlabel("Grade", fontsize=11)
        ax.set_ylabel("Number of Students", fontsize=11)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.15, f"{int(height)}",
                    ha="center", va="bottom", fontweight="bold", color="#1e40af")
        st.pyplot(fig, use_container_width=True)

    # 4. Subject averages
    with chart_tabs[3]:
        py_avg = np.mean([s["Python"] for s in st.session_state.students])
        s2_avg = np.mean([s["Subject 2"] for s in st.session_state.students])
        s3_avg = np.mean([s["Subject 3"] for s in st.session_state.students])
        
        subjects = ["Python", "Subject 2", "Subject 3"]
        averages = [py_avg, s2_avg, s3_avg]
        colors = ["#3b82f6", "#22c55e", "#ef4444"]
        
        fig, ax = plt.subplots(figsize=(8, 5.5))
        bars = ax.bar(subjects, averages, color=colors, edgecolor="white", linewidth=1.5, width=0.6)
        ax.set_title("Subject-wise Average Marks", fontsize=15, fontweight="bold", color="#1e3a8a", pad=12)
        ax.set_ylabel("Average Marks", fontsize=11)
        ax.set_ylim(0, 105)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3)
        for bar, avg in zip(bars, averages):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                    f"{avg:.1f}", ha="center", fontweight="bold", fontsize=12, color="#1e40af")
        st.pyplot(fig, use_container_width=True)

    # 5. Histogram
    with chart_tabs[4]:
        percs = [s["Percentage"] for s in st.session_state.students]
        fig, ax = plt.subplots(figsize=(9, 5.5))
        n, bins, patches = ax.hist(percs, bins=10, edgecolor="white", linewidth=1.2)
        
        # Color the bars with a purple gradient
        for i, patch in enumerate(patches):
            patch.set_facecolor(plt.cm.Purples(0.35 + i * 0.06))
        
        ax.set_title("Percentage Distribution", fontsize=15, fontweight="bold", color="#1e3a8a", pad=12)
        ax.set_xlabel("Percentage", fontsize=11)
        ax.set_ylabel("Number of Students", fontsize=11)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig, use_container_width=True)

    # 6. Top 10
    with chart_tabs[5]:
        top = sorted(st.session_state.students, key=lambda x: x["Percentage"], reverse=True)[:10]
        names = [s["Name"] for s in top]
        percs = [s["Percentage"] for s in top]
        
        fig, ax = plt.subplots(figsize=(11, 5.5))
        colors = plt.cm.YlOrRd(np.linspace(0.35, 0.85, len(names)))
        bars = ax.bar(names, percs, color=colors, edgecolor="white", linewidth=0.8)
        ax.set_title("Top 10 Students", fontsize=15, fontweight="bold", color="#1e3a8a", pad=12)
        ax.set_ylabel("Percentage (%)", fontsize=11)
        ax.set_ylim(0, 112)
        ax.tick_params(axis="x", rotation=40)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3)
        for bar, p in zip(bars, percs):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                    f"{p:.1f}%", ha="center", fontsize=9, fontweight="bold")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#64748b; font-size:0.9rem;'>"
    "Built with ❤️ using Streamlit &nbsp;•&nbsp; Pass Rule: ≥ 33 marks in every subject"
    "</p>",
    unsafe_allow_html=True
)
