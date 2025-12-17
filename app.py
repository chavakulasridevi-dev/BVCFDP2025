import streamlit as st
def calculate_grade(percentage: float) -> str:
    """Return grade based on percentage."""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


st.set_page_config(page_title="Student Marks & Grade Calculator", page_icon=":mortar_board:")

st.title("Student Marks & Grade Calculator")
st.write("Enter the number of subjects and the marks for each subject to calculate the total, percentage and grade.")

# Inputs for number of subjects and maximum marks per subject
cols = st.columns(2)
with cols[0]:
    num_subjects = st.number_input("Number of subjects", min_value=1, max_value=30, value=5, step=1, key="num_subjects")
with cols[1]:
    max_mark_per_subject = st.number_input("Max marks per subject", min_value=1, value=100, step=1, key="max_mark")

# Initialize marks in session_state so values persist between reruns
if "marks" not in st.session_state:
    st.session_state["marks"] = [0.0] * int(num_subjects)

# Adjust list length if num_subjects changed
if len(st.session_state["marks"]) != int(num_subjects):
    if int(num_subjects) > len(st.session_state["marks"]):
        st.session_state["marks"].extend([0.0] * (int(num_subjects) - len(st.session_state["marks"])))
    else:
        st.session_state["marks"] = st.session_state["marks"][: int(num_subjects)]

with st.form("marks_form"):
    st.subheader("Enter marks for each subject")
    for i in range(int(num_subjects)):
        # Use session_state to prefill values and keep them after reruns
        default_val = float(st.session_state["marks"][i]) if i < len(st.session_state["marks"]) else 0.0
        st.session_state["marks"][i] = st.number_input(
            f"Marks for Subject {i+1}", min_value=0.0, max_value=float(max_mark_per_subject), step=0.5, value=default_val, key=f"m{i}"
        )

    submitted = st.form_submit_button("Calculate")

# Calculate and display results when the form is submitted
if submitted:
    marks = [float(st.session_state[f"m{i}"]) for i in range(int(num_subjects))]
    if any((m < 0 or m > float(max_mark_per_subject)) for m in marks):
        st.error(f"Please ensure all marks are between 0 and {max_mark_per_subject}.")
    else:
        total_obtained = sum(marks)
        total_max = int(num_subjects) * float(max_mark_per_subject)
        percentage = (total_obtained / total_max) * 100 if total_max > 0 else 0.0
        grade = calculate_grade(percentage)
        pass_status = "Pass" if percentage >= 35 else "Fail"

        st.success("Results")
        st.write(f"**Total:** {total_obtained} / {int(total_max)}")
        st.write(f"**Percentage:** {percentage:.2f}%")
        st.write(f"**Grade:** {grade}  •  **Overall Result:** {pass_status}")

        st.write("---")
        st.write("### Subject-wise details")
        for idx, m in enumerate(marks, start=1):
            subj_pct = (m / float(max_mark_per_subject)) * 100 if max_mark_per_subject > 0 else 0.0
            subj_status = "Pass" if subj_pct >= 35 else "Fail"
            st.write(f"- Subject {idx}: {m} / {max_mark_per_subject} — {subj_pct:.2f}% — {subj_status}")

# Reset button
if st.button("Reset"): 
    st.session_state["marks"] = [0.0] * int(num_subjects)
    for i in range(int(num_subjects)):
        # reset individual inputs keys so values clear
        st.session_state[f"m{i}"] = 0.0
    st.experimental_rerun()