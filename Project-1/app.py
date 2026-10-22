
import csv
import io

import pandas as pd
import streamlit as st

from backend import (
    add_student,
    build_student_table,
    delete_student,
    get_all_students,
    get_performance_summary,
    get_result,
    get_student,
    update_student
)
from result_calculator import SUBJECTS
from storage import initialize_storage


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Student Result Management",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_storage()

st.markdown(
    """
    <style>
    .stApp {
        background: #F5F7FB;
    }

    [data-testid="stSidebar"] {
        background: #202B3C;
    }

    [data-testid="stSidebar"] * {
        color: #F5F7FB;
    }

    .main-title {
        font-size: 2rem;
        font-weight: 750;
        color: #202B3C;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        color: #657187;
        margin-bottom: 1.3rem;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #E1E6EF;
        padding: 15px;
        border-radius: 12px;
    }

    div[data-testid="stForm"] {
        background: white;
        padding: 20px;
        border: 1px solid #E1E6EF;
        border-radius: 12px;
    }

    div.stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] button {
        background: #7655A6;
        border-color: #7655A6;
        color: white;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# REUSABLE FUNCTIONS
# --------------------------------------------------

def show_heading(title, subtitle):
    st.markdown(
        f'<div class="main-title">{title}</div>'
        f'<div class="sub-title">{subtitle}</div>',
        unsafe_allow_html=True
    )


def marks_input(prefix, defaults=None):
    """Create validated marks inputs for all subjects."""
    marks = {}

    defaults = defaults or {}

    columns = st.columns(2)

    for index, subject in enumerate(SUBJECTS):
        with columns[index % 2]:
            marks[subject] = st.number_input(
                subject,
                min_value=0,
                max_value=100,
                value=int(defaults.get(subject, 0)),
                step=1,
                key=f"{prefix}_{subject}"
            )

    return marks


def show_student_result(student):
    result = get_result(student)

    st.subheader(f"Result: {student['name']}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Marks", f"{result['total']} / {result['maximum']}")
    col2.metric("Percentage", f"{result['percentage']:.2f}%")
    col3.metric("Grade", result["grade"])

    if result["status"] == "PASS":
        st.success("Result: PASS")
    else:
        st.error("Result: FAIL — at least one subject is below 35.")

    result_df = pd.DataFrame([
        {"Subject": subject, "Marks": student["marks"][subject]}
        for subject in SUBJECTS
    ])

    st.dataframe(result_df, use_container_width=True, hide_index=True)


def student_options():
    """Build a select list using student IDs."""
    return {
        student["student_id"]: (
            f"{student['student_id']} — {student['name']}"
        )
        for student in get_all_students()
    }


def make_csv(rows):
    """Generate a downloadable CSV in memory."""
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=list(rows[0].keys()) if rows else [
            "Student ID", "Name", "Class", "Total",
            "Percentage", "Grade", "Status"
        ]
    )

    writer.writeheader()
    writer.writerows(rows)

    return output.getvalue().encode("utf-8-sig")


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:
    st.title(" Student Portal")
    st.caption("Result & Grade Management")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Add Student",
            "All Students",
            "Search Student",
            "Update Student",
            "Delete Student",
            "Performance Analytics"
        ],
        key="navigation"
    )

    st.divider()
    st.caption("Academic Results")
    st.caption("Students Grade Management System")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":
    show_heading(
        "Dashboard",
        "Overview of student records and academic performance."
    )

    summary = get_performance_summary()
    students = get_all_students()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", summary["total_students"])
    col2.metric("Class Average", f"{summary['average_percentage']:.2f}%")
    col3.metric("Pass Rate", f"{summary['pass_percentage']:.1f}%")
    col4.metric("Students Failed", summary["fail_count"])

    st.divider()

    left, right = st.columns([1.3, 1])

    with left:
        st.subheader("Recent Student Records")

        rows = build_student_table()

        if rows:
            st.dataframe(
                pd.DataFrame(rows).tail(8),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No student records yet. Add your first student.")

    with right:
        st.subheader("Grade Distribution")

        distribution = summary["grade_distribution"]

        if distribution:
            grade_df = pd.DataFrame({
                "Grade": list(distribution.keys()),
                "Students": list(distribution.values())
            }).set_index("Grade")

            st.bar_chart(grade_df)
        else:
            st.info("Grade analytics will appear after records are added.")

    top_student = summary["top_student"]

    st.subheader("Top Performer")

    if top_student:
        st.success(
            f"🏆 {top_student['name']} "
            f"({top_student['student_id']}) — "
            f"{top_student['percentage']:.2f}% "
            f"(Grade {top_student['grade']})"
        )
    else:
        st.info("Add student records to identify the top performer.")


# --------------------------------------------------
# ADD STUDENT
# --------------------------------------------------

elif page == "Add Student":
    show_heading(
        "Add Student",
        "Register a student and enter their academic marks."
    )

    with st.form("add_student_form"):
        student_id = st.text_input("Student ID", max_chars=30)
        name = st.text_input("Full Name", max_chars=100)
        student_class = st.text_input("Class / Section", max_chars=50)

        st.subheader("Subject Marks")
        marks = marks_input("add")

        submitted = st.form_submit_button(
            "Add Student Record",
            type="primary",
            use_container_width=True
        )

    if submitted:
        try:
            add_student(student_id, name, student_class, marks)
            st.success("Student added successfully.")
            st.rerun()
        except ValueError as error:
            st.error(str(error))


# --------------------------------------------------
# ALL STUDENTS
# --------------------------------------------------

elif page == "All Students":
    show_heading(
        "All Students",
        "View and export all student records."
    )

    rows = build_student_table()

    if rows:
        df = pd.DataFrame(rows)

        search_text = st.text_input(
            "Filter by ID, name, or class",
            placeholder="Type to filter records..."
        )

        if search_text:
            mask = df.astype(str).apply(
                lambda column: column.str.contains(
                    search_text, case=False, na=False
                )
            ).any(axis=1)

            df = df[mask]

        st.dataframe(df, use_container_width=True, hide_index=True)

        st.download_button(
            "Download Student Records (CSV)",
            data=make_csv(df.to_dict(orient="records")),
            file_name="student_results.csv",
            mime="text/csv"
        )

        st.caption(f"{len(df)} record(s) displayed.")
    else:
        st.info("No student records are available.")


# --------------------------------------------------
# SEARCH STUDENT
# --------------------------------------------------

elif page == "Search Student":
    show_heading(
        "Search Student",
        "Find a student using their unique ID."
    )

    search_id = st.text_input("Enter Student ID")

    if st.button("Search", type="primary"):
        if not search_id.strip():
            st.warning("Enter a student ID.")
        else:
            student = get_student(search_id)

            if student:
                st.success("Student record found.")
                st.write(f"**Name:** {student['name']}")
                st.write(f"**Class:** {student['class']}")
                show_student_result(student)
            else:
                st.error("No student found with that ID.")


# --------------------------------------------------
# UPDATE STUDENT
# --------------------------------------------------

elif page == "Update Student":
    show_heading(
        "Update Student",
        "Edit student details and marks."
    )

    options = student_options()

    if not options:
        st.info("Add a student before trying to update a record.")
    else:
        selected_id = st.selectbox(
            "Select Student",
            options=list(options.keys()),
            format_func=lambda student_id: options[student_id]
        )

        student = get_student(selected_id)

        with st.form("update_student_form"):
            name = st.text_input("Full Name", value=student["name"])
            student_class = st.text_input(
                "Class / Section", value=student["class"]
            )

            st.subheader("Update Subject Marks")
            marks = marks_input(
                f"update_{selected_id}",
                defaults=student["marks"]
            )

            submitted = st.form_submit_button(
                "Save Changes",
                type="primary",
                use_container_width=True
            )

        if submitted:
            try:
                update_student(
                    selected_id, name, student_class, marks
                )
                st.success("Student record updated successfully.")
                st.rerun()
            except ValueError as error:
                st.error(str(error))


# --------------------------------------------------
# DELETE STUDENT
# --------------------------------------------------

elif page == "Delete Student":
    show_heading(
        "Delete Student",
        "Remove a student record after confirmation."
    )

    options = student_options()

    if not options:
        st.info("No student records are available to delete.")
    else:
        selected_id = st.selectbox(
            "Select Student to Delete",
            options=list(options.keys()),
            format_func=lambda student_id: options[student_id]
        )

        student = get_student(selected_id)

        st.warning(
            f"You selected **{student['name']}** "
            f"({student['student_id']}). "
            "Deleting this record cannot be undone from the application."
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this student."
        )

        if st.button("Delete Student", type="primary"):
            if not confirm:
                st.error("Please confirm the deletion first.")
            else:
                try:
                    delete_student(selected_id)
                    st.success("Student record deleted.")
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))


# --------------------------------------------------
# PERFORMANCE ANALYTICS
# --------------------------------------------------

elif page == "Performance Analytics":
    show_heading(
        "Performance Analytics",
        "Explore class results, subject marks, and grade distribution."
    )

    students = get_all_students()
    rows = build_student_table()
    summary = get_performance_summary()

    if not students:
        st.info("Add student records to view analytics.")
    else:
        col1, col2, col3 = st.columns(3)

        col1.metric("Students", summary["total_students"])
        col2.metric("Class Average", f"{summary['average_percentage']:.2f}%")
        col3.metric("Pass Percentage", f"{summary['pass_percentage']:.2f}%")

        df = pd.DataFrame(rows)

        st.subheader("Student Percentage Comparison")
        st.bar_chart(
            df.set_index("Name")[["Percentage"]]
        )

        st.subheader("Grade Distribution")

        grade_df = pd.DataFrame({
            "Grade": list(summary["grade_distribution"].keys()),
            "Count": list(summary["grade_distribution"].values())
        }).set_index("Grade")

        st.bar_chart(grade_df)

        st.subheader("Average Marks by Subject")

        subject_averages = {
            subject: round(
                sum(student["marks"][subject] for student in students)
                / len(students),
                2
            )
            for subject in SUBJECTS
        }

        subject_df = pd.DataFrame({
            "Subject": list(subject_averages.keys()),
            "Average Marks": list(subject_averages.values())
        }).set_index("Subject")

        st.bar_chart(subject_df)

        st.subheader("Download Report")

        st.download_button(
            "Export Results as CSV",
            data=make_csv(rows),
            file_name="student_performance_report.csv",
            mime="text/csv"
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Student Result & Grade Management System | "
    "Built with Python and Streamlit"
)
