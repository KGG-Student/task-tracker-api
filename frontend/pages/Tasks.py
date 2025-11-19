import streamlit as st
import requests

st.title("Assignment Task Manager")
st.markdown("### Manage your assignments and tasks efficiently")

# Check if user is logged in
if "token" not in st.session_state:
    st.error("Please login first.")
    st.stop()

token = st.session_state.token
headers = {"Authorization": f"Bearer {token}"}
base_url = "http://localhost:8000"

# Logout button
if st.button("Logout"):
    del st.session_state.token
    st.success("Logged out successfully!")
    st.switch_page("pages/Login.py")

st.header("Your Tasks")

# Function to fetch tasks
def fetch_tasks():
    try:
        response = requests.get(f"{base_url}/api/tasks/", headers=headers)
        if response.status_code == 200:
            return response.json().get("tasks", [])
        else:
            try:
                error_detail = response.json().get('detail', 'Unknown error')
                st.error(f"Failed to fetch tasks: {error_detail}")
            except:
                st.error(f"Failed to fetch tasks: Status code {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return []

# Fetch and display tasks
tasks = fetch_tasks()
if tasks:
    for task in tasks:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            with col1:
                st.subheader(task.get("title", "No title"))
                st.write(task.get("description", "No description"))
                st.write(f"Due: {task.get('due_date', 'No due date')}")
                st.write(f"Status: {'Completed' if task.get('completed') else 'Pending'}")
            with col2:
                # Update status
                if st.button(f"Mark {'Incomplete' if task.get('completed') else 'Complete'}", key=f"status_{task['id']}"):
                    update_data = {"completed": not task.get('completed')}
                    try:
                        response = requests.put(f"{base_url}/api/tasks/{task['id']}", json=update_data, headers=headers)
                        if response.status_code == 200:
                            st.success("Task status updated!")
                            st.rerun()
                        else:
                            try:
                                error_detail = response.json().get('detail', 'Unknown error')
                                st.error(f"Failed to update status: {error_detail}")
                            except:
                                st.error(f"Failed to update status: Status code {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error: {e}")
            with col3:
                # Edit button
                if st.button("Edit", key=f"edit_{task['id']}"):
                    st.session_state.edit_task = task
                    st.rerun()
            with col4:
                # Delete button
                if st.button("Delete", key=f"delete_{task['id']}"):
                    try:
                        response = requests.delete(f"{base_url}/api/tasks/{task['id']}", headers=headers)
                        if response.status_code == 204:
                            st.success("Task deleted!")
                            st.rerun()
                        else:
                            try:
                                error_detail = response.json().get('detail', 'Unknown error')
                                st.error(f"Failed to delete task: {error_detail}")
                            except:
                                st.error(f"Failed to delete task: Status code {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error: {e}")
        st.divider()
else:
    st.write("No tasks found.")

# Create new task
st.header("Create New Task")
with st.form("create_task"):
    title = st.text_input("Title")
    description = st.text_area("Description")
    due_date = st.date_input("Due Date")
    submitted = st.form_submit_button("Create Task")
    if submitted:
        if not title:
            st.error("Title is required.")
        else:
            task_data = {
                "title": title,
                "description": description,
                "completed": False,
                "due_date": due_date.strftime("%Y-%m-%d")
            }
            try:
                response = requests.post(f"{base_url}/api/tasks/", json=task_data, headers=headers)
                if response.status_code == 201:
                    st.success("Task created successfully!")
                    st.rerun()
                else:
                    try:
                        error_detail = response.json().get('detail', 'Unknown error')
                        st.error(f"Failed to create task: {error_detail}")
                    except:
                        st.error(f"Failed to create task: Status code {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")

# Edit task form
if "edit_task" in st.session_state:
    task = st.session_state.edit_task
    st.header(f"Edit Task: {task.get('title')}")
    with st.form("edit_task"):
        new_title = st.text_input("Title", value=task.get("title"))
        new_description = st.text_area("Description", value=task.get("description"))
        new_due_date = st.date_input("Due Date", value=task.get("due_date"))
        edit_submitted = st.form_submit_button("Update Task")
        if edit_submitted:
            if not new_title:
                st.error("Title is required.")
            else:
                update_data = {
                    "title": new_title,
                    "description": new_description,
                    "due_date": new_due_date.strftime("%Y-%m-%d")
                }
                try:
                    response = requests.put(f"{base_url}/api/tasks/{task['id']}", json=update_data, headers=headers)
                    if response.status_code == 200:
                        st.success("Task updated successfully!")
                        del st.session_state.edit_task
                        st.rerun()
                    else:
                        try:
                            error_detail = response.json().get('detail', 'Unknown error')
                            st.error(f"Failed to update task: {error_detail}")
                        except:
                            st.error(f"Failed to update task: Status code {response.status_code}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {e}")
    if st.button("Cancel Edit"):
        del st.session_state.edit_task
        st.rerun()
