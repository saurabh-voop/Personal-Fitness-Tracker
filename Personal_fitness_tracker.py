import streamlit as st
from datetime import datetime

# Define the Workout class
class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

    def __str__(self):
        return f"{self.date}: {self.exercise_type} for {self.duration} minutes, {self.calories_burned} calories burned"

# Define the User class
class User:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def view_workouts(self):
        return "\n".join(str(workout) for workout in self.workouts) if self.workouts else "No workouts recorded yet."

    def save_data(self, filename):
        try:
            with open(filename, "w") as file:
                for workout in self.workouts:
                    file.write(f"{workout.date},{workout.exercise_type},{workout.duration},{workout.calories_burned}\n")
            return "Data saved successfully!"
        except Exception as e:
            return f"Error saving data: {e}"

    def load_data(self, filename):
        try:
            self.workouts = []
            with open(filename, "r") as file:
                for line in file:
                    date, exercise_type, duration, calories_burned = line.strip().split(",")
                    self.workouts.append(Workout(date, exercise_type, int(duration), int(calories_burned)))
            return "Data loaded successfully!"
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"Error loading data: {e}"

# Streamlit UI
st.set_page_config(page_title="Workout Tracker", layout="wide")
st.title("🏋️‍♂️ Workout Tracker")

# Sidebar for User Profile
st.sidebar.header("User Profile")
name = st.sidebar.text_input("Name", "John Doe")
age = st.sidebar.number_input("Age", min_value=1, step=1)
weight = st.sidebar.number_input("Weight (kg)", min_value=1.0, step=0.1)

if "user" not in st.session_state:
    st.session_state.user = User(name, age, weight)

# Tabs for navigation
tab1, tab2, tab3, tab4 = st.tabs(["Add Workout", "View Workouts", "Save Data", "Load Data"])

# Add Workout Tab
with tab1:
    st.subheader("Add a New Workout")
    date = st.date_input("Workout Date", datetime.today())
    exercise_type = st.text_input("Exercise Type", "Running")
    duration = st.number_input("Duration (minutes)", min_value=1, step=1)
    calories_burned = st.number_input("Calories Burned", min_value=1, step=1)
    if st.button("➕ Add Workout"):
        workout = Workout(date, exercise_type, duration, calories_burned)
        st.session_state.user.add_workout(workout)
        st.success("Workout added successfully!")

# View Workouts Tab
with tab2:
    st.subheader("📋 Workout History")
    if st.button("🔍 View Workouts"):
        workouts_text = st.session_state.user.view_workouts()
        st.text_area("Your Workouts:", workouts_text, height=200)

# Save Data Tab
with tab3:
    st.subheader("💾 Save Your Workouts")
    filename = st.text_input("Filename to Save", "workouts.txt")
    if st.button("💾 Save Data"):
        status = st.session_state.user.save_data(filename)
        st.success(status)

# Load Data Tab
with tab4:
    st.subheader("📂 Load Saved Workouts")
    load_filename = st.text_input("Filename to Load", "workouts.txt")
    if st.button("📂 Load Data"):
        status = st.session_state.user.load_data(load_filename)
        st.success(status)
