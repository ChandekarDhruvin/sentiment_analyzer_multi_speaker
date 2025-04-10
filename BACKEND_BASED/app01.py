# import streamlit as st
# from sqlalchemy import create_engine, and_
# from sqlalchemy.orm import sessionmaker
# from models import Base, Employee, EmployeeSkills, SkillRecommendation, TaskRecommendation, RollingSentiment
# import pandas as pd
# import json
# from datetime import datetime

# # Database setup
# DATABASE_URL = "postgresql://postgres:root@localhost:5432/test_sentiment_analysis"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Initialize session state
# if 'authenticated' not in st.session_state:
#     st.session_state.authenticated = False
# if 'user_role' not in st.session_state:
#     st.session_state.user_role = None
# if 'user_name' not in st.session_state:
#     st.session_state.user_name = None
# if 'user_email' not in st.session_state:
#     st.session_state.user_email = None

# # Page config
# st.set_page_config(page_title="Employee Dashboard", layout="wide")

# # Helper functions
# def get_employee_by_email(email):
#     db = SessionLocal()
#     try:
#         employee = db.query(Employee).filter(Employee.email == email).first()
#         return employee
#     finally:
#         db.close()

# def get_skills_for_employee(name, meeting_id=None):
#     db = SessionLocal()
#     try:
#         query = db.query(SkillRecommendation).filter(SkillRecommendation.name == name)
#         if meeting_id:
#             query = query.filter(SkillRecommendation.meeting_id == meeting_id)
#         skills = query.all()
#         return [{"skill": skill.skill_recommendation, "meeting_id": skill.meeting_id} for skill in skills]
#     finally:
#         db.close()

# def get_tasks_for_employee(name, meeting_id=None):
#     db = SessionLocal()
#     try:
#         query = db.query(TaskRecommendation).filter(
#             (TaskRecommendation.assigned_to == name) | 
#             (TaskRecommendation.assigned_by == name)
#         )
#         if meeting_id:
#             query = query.filter(TaskRecommendation.meeting_id == meeting_id)
#         tasks = query.all()
#         return tasks
#     finally:
#         db.close()

# def get_sentiment_data(name, meeting_id=None):
#     db = SessionLocal()
#     try:
#         query = db.query(EmployeeSkills).filter(EmployeeSkills.employee_name == name)
#         if meeting_id:
#             query = query.filter(EmployeeSkills.meeting_id == meeting_id)
#         sentiments = query.all()
#         return sentiments
#     finally:
#         db.close()

# def get_rolling_sentiment(name, meeting_id=None):
#     db = SessionLocal()
#     try:
#         query = db.query(RollingSentiment).filter(RollingSentiment.name == name)
#         if meeting_id:
#             query = query.filter(RollingSentiment.meeting_id == meeting_id)
#         rolling = query.first()
#         if rolling:
#             return json.loads(rolling.rolling_sentiment)
#         return None
#     finally:
#         db.close()

# def get_all_employees(role_filter=None):
#     db = SessionLocal()
#     try:
#         query = db.query(Employee)
#         if role_filter:
#             query = query.filter(Employee.role == role_filter)
#         return query.all()
#     finally:
#         db.close()

# def get_employee_meetings(name):
#     db = SessionLocal()
#     try:
#         meetings = db.query(EmployeeSkills.meeting_id)\
#                    .filter(EmployeeSkills.employee_name == name)\
#                    .distinct()\
#                    .order_by(EmployeeSkills.meeting_id.desc())\
#                    .all()
#         return [m[0] for m in meetings]
#     finally:
#         db.close()

# # Login page
# def login_page():
#     st.title("Employee Dashboard Login")
#     with st.form("login_form"):
#         email = st.text_input("Email")
#         submitted = st.form_submit_button("Login")
#         if submitted:
#             employee = get_employee_by_email(email)
#             if employee:
#                 st.session_state.authenticated = True
#                 st.session_state.user_role = employee.role
#                 st.session_state.user_name = employee.name
#                 st.session_state.user_email = employee.email
#                 st.rerun()
#             else:
#                 st.error("Invalid email or employee not found")

# def display_meeting_data(name, meeting_id=None):
#     # Get all meetings for this employee
#     meetings = get_employee_meetings(name)
    
#     if meetings:
#         selected_meeting = st.selectbox(
#             "Select Meeting",
#             options=meetings,
#             format_func=lambda x: f"Meeting {x}",
#             index=0
#         )
        
#         # Display data for selected meeting
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.subheader("Skill Recommendations")
#             skills = get_skills_for_employee(name, selected_meeting)
#             if skills:
#                 for skill in skills:
#                     st.info(f"📚 {skill['skill']} (Meeting {skill['meeting_id']})")
#             else:
#                 st.warning("No skill recommendations found for this meeting")
        
#         with col2:
#             st.subheader("Tasks")
#             tasks = get_tasks_for_employee(name, selected_meeting)
#             if tasks:
#                 for task in tasks:
#                     status_emoji = "✅" if task.status.lower() == "completed" else "🔄"
#                     st.write(f"{status_emoji} {task.task} (Assigned by: {task.assigned_by}, Deadline: {task.deadline})")
#             else:
#                 st.warning("No tasks found for this meeting")
        
#         st.subheader("Sentiment Analysis")
#         sentiment_data = get_sentiment_data(name, selected_meeting)
#         if sentiment_data:
#             for data in sentiment_data:
#                 st.metric("Overall Sentiment Score", f"{data.overall_sentiment_score:.2f}")
                
#                 # Show rolling sentiment
#                 rolling = get_rolling_sentiment(name, selected_meeting)
#                 if rolling:
#                     st.line_chart(pd.DataFrame(rolling['scores']).set_index('Index'))
#         else:
#             st.warning("No sentiment data available for this meeting")
#     else:
#         st.warning("No meeting data available")

# # Dashboard pages
# def employee_dashboard():
#     st.title(f"Welcome, {st.session_state.user_name} ({st.session_state.user_role})")
#     display_meeting_data(st.session_state.user_name)

# def manager_dashboard():
#     st.title(f"Welcome, {st.session_state.user_name} ({st.session_state.user_role})")
    
#     # Show manager's own data
#     st.header("Your Data")
#     display_meeting_data(st.session_state.user_name)
    
#     # Team management section
#     st.header("Team Management")
#     employees = get_all_employees(role_filter="Employee")
#     employee_names = [emp.name for emp in employees]
    
#     selected_employee = st.selectbox("Select an employee to view", employee_names)
#     if selected_employee:
#         display_meeting_data(selected_employee)

# def hr_dashboard():
#     st.title(f"Welcome, {st.session_state.user_name} ({st.session_state.user_role})")
    
#     # Show HR's own data
#     st.header("Your Data")
#     display_meeting_data(st.session_state.user_name)
    
#     # HR analytics section
#     st.header("HR Analytics")
#     all_employees = get_all_employees()
#     non_hr_employees = [emp for emp in all_employees if emp.role != 'HR']
#     employee_names = [emp.name for emp in non_hr_employees]
    
#     selected_employee = st.selectbox("Select an employee/manager to view", employee_names)
#     if selected_employee:
#         display_meeting_data(selected_employee)
    
#     # Organization-wide analytics
#     st.header("Organization Overview")
#     all_employees = get_all_employees()
    
#     # Sentiment by role
#     st.subheader("Average Sentiment by Role")
#     sentiment_by_role = {}
#     for emp in all_employees:
#         data = get_sentiment_data(emp.name)
#         if data:
#             avg_sentiment = sum([d.overall_sentiment_score for d in data]) / len(data)
#             if emp.role not in sentiment_by_role:
#                 sentiment_by_role[emp.role] = []
#             sentiment_by_role[emp.role].append(avg_sentiment)
    
#     if sentiment_by_role:
#         role_avg = {role: sum(scores)/len(scores) for role, scores in sentiment_by_role.items()}
#         st.bar_chart(pd.DataFrame.from_dict(role_avg, orient='index', columns=['Average Sentiment']))

# # Main app flow
# def main():
#     if not st.session_state.authenticated:
#         login_page()
#     else:
#         # Sidebar with user info and logout
#         st.sidebar.title(f"User Info")
#         st.sidebar.write(f"Name: {st.session_state.user_name}")
#         st.sidebar.write(f"Role: {st.session_state.user_role}")
#         st.sidebar.write(f"Email: {st.session_state.user_email}")
        
#         if st.sidebar.button("Logout"):
#             st.session_state.authenticated = False
#             st.session_state.user_role = None
#             st.session_state.user_name = None
#             st.session_state.user_email = None
#             st.rerun()
        
#         # Role-based routing
#         if st.session_state.user_role == "HR":
#             hr_dashboard()
#         elif st.session_state.user_role == "Manager":
#             manager_dashboard()
#         else:
#             employee_dashboard()

# if __name__ == "__main__":
#     main()


import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Employee, EmployeeSkills, SkillRecommendation, TaskRecommendation, RollingSentiment
import pandas as pd
import json

# Database setup
DATABASE_URL = "postgresql://postgres:root@localhost:5432/test_sentiment_analysis"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize session state
for key in ['authenticated', 'user_role', 'user_name', 'user_email']:
    if key not in st.session_state:
        st.session_state[key] = False if key == 'authenticated' else None

st.set_page_config(page_title="Employee Dashboard", layout="wide")

# -------------------- Helper Functions --------------------

def get_employee_by_email(email):
    with SessionLocal() as db:
        return db.query(Employee).filter(Employee.email == email).first()

def get_skills_for_employee(name, meeting_id=None):
    with SessionLocal() as db:
        query = db.query(SkillRecommendation).filter(SkillRecommendation.name == name)
        if meeting_id:
            query = query.filter(SkillRecommendation.meeting_id == meeting_id)
        return [{"skill": s.skill_recommendation, "meeting_id": s.meeting_id} for s in query.all()]

def get_tasks_for_employee(name, meeting_id=None):
    with SessionLocal() as db:
        query = db.query(TaskRecommendation).filter(
            (TaskRecommendation.assigned_to == name) | 
            (TaskRecommendation.assigned_by == name)
        )
        if meeting_id:
            query = query.filter(TaskRecommendation.meeting_id == meeting_id)
        return query.all()

def get_sentiment_data(name, meeting_id=None):
    with SessionLocal() as db:
        query = db.query(EmployeeSkills).filter(EmployeeSkills.employee_name == name)
        if meeting_id:
            query = query.filter(EmployeeSkills.meeting_id == meeting_id)
        return query.all()

def get_rolling_sentiment(name, meeting_id=None):
    with SessionLocal() as db:
        query = db.query(RollingSentiment).filter(RollingSentiment.name == name)
        if meeting_id:
            query = query.filter(RollingSentiment.meeting_id == meeting_id)
        rolling = query.first()
        return json.loads(rolling.rolling_sentiment) if rolling else None

def get_all_employees(role_filter=None):
    with SessionLocal() as db:
        query = db.query(Employee)
        if role_filter:
            query = query.filter(Employee.role == role_filter)
        return query.all()

def get_employee_meetings(name):
    with SessionLocal() as db:
        meetings = db.query(EmployeeSkills.meeting_id).filter(
            EmployeeSkills.employee_name == name).distinct().order_by(
            EmployeeSkills.meeting_id.desc()).all()
        return [m[0] for m in meetings]

# -------------------- UI Pages --------------------

def login_page():
    st.markdown("<h1 style='text-align:center;'>🔐 Employee Dashboard Login</h1>", unsafe_allow_html=True)
    with st.form("login_form", clear_on_submit=True):
        st.text_input("📧 Enter your email", key="login_email")
        if st.form_submit_button("Login"):
            emp = get_employee_by_email(st.session_state.login_email)
            if emp:
                st.session_state.authenticated = True
                st.session_state.user_role = emp.role
                st.session_state.user_name = emp.name
                st.session_state.user_email = emp.email
                st.rerun()
            else:
                st.error("🚫 Invalid email or employee not found")

def display_meeting_data(name, meeting_id=None):
    meetings = get_employee_meetings(name)
    if not meetings:
        st.warning("No meeting data available for this employee.")
        return

    st.markdown("### 📅 Select a Meeting")
    selected_meeting = st.selectbox("Meeting List", options=meetings, format_func=lambda x: f"📝 Meeting {x}")

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("📚 Skill Recommendations", expanded=True):
            skills = get_skills_for_employee(name, selected_meeting)
            if skills:
                for skill in skills:
                    st.success(f"✅ {skill['skill']} (Meeting {skill['meeting_id']})")
            else:
                st.info("No skill recommendations for this meeting.")

    with col2:
        with st.expander("🛠️ Task Recommendations", expanded=True):
            tasks = get_tasks_for_employee(name, selected_meeting)
            if tasks:
                for task in tasks:
                    status = "✅" if task.status.lower() == "completed" else "⏳"
                    st.markdown(f"**{status} {task.task}**  \nAssigned by: `{task.assigned_by}` | Deadline: `{task.deadline}`")
            else:
                st.info("No tasks found for this meeting.")

    st.markdown("### 📊 Sentiment Analysis")
    sentiments = get_sentiment_data(name, selected_meeting)
    if sentiments:
        for data in sentiments:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric("Overall Sentiment", f"{data.overall_sentiment_score:.2f}")
            with col2:
                rolling = get_rolling_sentiment(name, selected_meeting)
                if rolling:
                    df = pd.DataFrame(rolling['scores']).set_index('Index')
                    st.line_chart(df)
    else:
        st.warning("No sentiment data found for this meeting.")

def employee_dashboard():
    st.markdown(f"## 👋 Welcome, **{st.session_state.user_name}** ({st.session_state.user_role})")
    st.divider()
    display_meeting_data(st.session_state.user_name)
    
def manager_dashboard():
    st.markdown(f"## 👋 Welcome, **{st.session_state.user_name}** ({st.session_state.user_role})")
    st.divider()

    # ✅ Removed outer expander to avoid nesting
    st.markdown("### 📈 Your Data")
    display_meeting_data(st.session_state.user_name)

    st.markdown("### 👥 Team Overview")
    employee_names = [e.name for e in get_all_employees(role_filter="Employee")]
    selected = st.selectbox("🔍 Select an employee", employee_names)
    if selected:
        display_meeting_data(selected)

def hr_dashboard():
    st.markdown(f"## 👋 Welcome, **{st.session_state.user_name}** ({st.session_state.user_role})")
    st.divider()

    # ✅ Removed outer expander to avoid nesting
    st.markdown("### 📈 Your Data")
    display_meeting_data(st.session_state.user_name)

    st.markdown("### 🧑‍💼 View Employee/Manager Data")
    all_emps = get_all_employees()
    names = [emp.name for emp in all_emps if emp.role != 'HR']
    selected = st.selectbox("🔍 Select a member", names)
    if selected:
        display_meeting_data(selected)

    st.markdown("### 🌐 Organization Overview")
    total_emps = sum(1 for e in all_emps if e.role == 'Employee')
    total_mgrs = sum(1 for e in all_emps if e.role == 'Manager')
    total_hr = sum(1 for e in all_emps if e.role == 'HR')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👨‍💼 Employees", total_emps)
    col2.metric("👩‍💼 Managers", total_mgrs)
    col3.metric("🧑‍💼 HRs", total_hr)
    col4.metric("🌐 Total Users", len(all_emps))

# -------------------- Main App --------------------

def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        with st.sidebar:
            st.image("https://cdn-icons-png.flaticon.com/512/2922/2922510.png", width=80)
            st.markdown(f"### 👤 {st.session_state.user_name}")
            st.caption(f"📧 {st.session_state.user_email}")
            st.caption(f"🧾 Role: `{st.session_state.user_role}`")
            st.markdown("---")
            if st.button("🚪 Logout"):
                for key in ['authenticated', 'user_role', 'user_name', 'user_email']:
                    st.session_state[key] = False if key == 'authenticated' else None
                st.rerun()

        if st.session_state.user_role == "HR":
            hr_dashboard()
        elif st.session_state.user_role == "Manager":
            manager_dashboard()
        else:
            employee_dashboard()

if __name__ == "__main__":
    main()
