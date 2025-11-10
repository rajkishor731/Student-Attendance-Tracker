import streamlit as st
import pandas as pd

st.title("📊 Student Attendance Tracker (with Data Wrangling)")

# --- Input Section ---
st.sidebar.header("Add Student Details")
num_students = st.sidebar.number_input("Number of Students", min_value=1, step=1)

student_data = []

for i in range(num_students):
    st.subheader(f"🧑‍🎓 Student {i+1}")
    student_id = st.text_input(f"Student ID (Student {i+1})", key=f"id_{i}")
    name = st.text_input(f"Name (Student {i+1})", key=f"name_{i}")
    total_classes = st.number_input(f"Total Classes (Student {i+1})", min_value=0, step=1, key=f"total_{i}")
    attended_classes = st.number_input(f"Attended Classes (Student {i+1})", min_value=0, step=1, key=f"attended_{i}")
    
    if student_id and name:
        student_data.append({
            "Student ID": student_id,
            "Name": name.strip().title(),
            "Total Class": total_classes,
            "Attended Class": attended_classes
        })

# --- Process Data ---
if st.button("📋 Generate Attendance Report"):
    if student_data:
        df = pd.DataFrame(student_data)

        st.subheader("🧹 Data Wrangling Steps")

        # --- Step 1: Handle Missing Data ---
        st.write("✅ Handling Missing or Invalid Data...")
        df["Total Class"].replace(0, None, inplace=True)  # Avoid divide-by-zero
        df["Total Class"].fillna(df["Total Class"].mean(), inplace=True)

        # --- Step 2: Remove Duplicates (if any) ---
        before = len(df)
        df.drop_duplicates(subset=["Student ID"], inplace=True)
        after = len(df)
        if before != after:
            st.warning(f"Removed {before - after} duplicate entries based on Student ID")

        # --- Step 3: Data Type Conversion ---
        st.write("✅ Ensuring correct data types...")
        df["Total Class"] = df["Total Class"].astype(int)
        df["Attended Class"] = df["Attended Class"].astype(int)

        # --- Step 4: Feature Engineering (Attendance %) ---
        df["Attendance"] = (df["Attended Class"] * 100 / df["Total Class"]).round(2)
        df["Attendance Status"] = df["Attendance"].apply(lambda x: "Low" if x < 75 else "Good")

        st.success("🎯 Data Wrangling Completed Successfully!")

        # --- Display Results ---
        st.subheader("📄 Cleaned Attendance Data")
        st.dataframe(df, use_container_width=True)

        st.markdown(f"**📈 Average Attendance:** {df['Attendance'].mean():.2f}%")

        st.subheader("⚠️ Students Below 75% Attendance")
        st.dataframe(df[df["Attendance"] < 75])

        # --- Download Option ---
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Attendance Report", data=csv, file_name="attendance_report.csv", mime="text/csv")
    else:
        st.warning("Please fill in all student details before generating the report.")

# --- Footer ---
st.markdown("---")
st.markdown("### 👨‍💻 Made by **Raj Kishor**")
