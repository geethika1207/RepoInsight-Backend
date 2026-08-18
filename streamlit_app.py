import streamlit as st
import requests

# --- HELPER FUNCTION ---
def json_to_markdown(data, indent_level=0):
    markdown_text = ""
    indent = "    " * indent_level  # 4 spaces for proper markdown nesting
    
    if isinstance(data, dict):
        for key, value in data.items():
            clean_key = key.replace("_", " ").title()
            if isinstance(value, (dict, list)):
                markdown_text += f"{indent}- **{clean_key}**\n"
                markdown_text += json_to_markdown(value, indent_level + 1)
            else:
                markdown_text += f"{indent}- **{clean_key}:** {value}\n"
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                markdown_text += json_to_markdown(item, indent_level + 1)
            else:
                markdown_text += f"{indent}- {item}\n"
    else:
        markdown_text += f"{indent}- {data}\n"
        
    return markdown_text
# -----------------------

# 1. Page Configuration
st.set_page_config(page_title="RepoInsight", page_icon="🔍", layout="wide")
st.title("🔍 RepoInsight Dashboard")
st.write("Generate intelligent reports from your codebase.")

st.info(
    "👋 **Welcome to RepoInsight!**\n\n"
    "To guarantee the highest quality AI analysis, our engine is currently optimized for "
    "small to medium-sized repositories (up to **~400,000 characters**, or roughly **~10,000 lines of code**). "
    "Support for massive codebases is coming soon!"
)

# Live Render backend URL
API_URL = "https://repoinsight-backend-1.onrender.com"

# --- INIT SESSION STATE ---
# This keeps the user logged in across button clicks
if "auth_token" not in st.session_state:
    st.session_state.auth_token = None

# 2. Sidebar Setup
with st.sidebar:
    st.header("Authentication")
    
    # If the user is already logged in, show a success message and a Logout button
    if st.session_state.auth_token:
        st.success("✅ You are securely logged in.")
        if st.button("Logout"):
            st.session_state.auth_token = None
            st.rerun() # Refresh the app to clear state
            
    # If the user is NOT logged in, show the Login/Register UI
    else:
        auth_mode = st.radio("Select Action", ["Log In", "Register", "Manual Token"])
        
        if auth_mode == "Log In":
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Log In")
                
                if submit_login:
                    with st.spinner("Logging in..."):
                        # OAuth2PasswordRequestForm expects 'username' and 'password' as form data
                        login_res = requests.post(
                            f"{API_URL}/login", 
                            data={"username": email, "password": password}
                        )
                        if login_res.status_code in [200, 201]:
                            # Save the token to session state
                            st.session_state.auth_token = login_res.json().get("access_token")
                            st.success("Logged in successfully!")
                            st.rerun() # Refresh the UI to hide the login form
                        else:
                            st.error(f"Login failed: {login_res.json().get('detail', 'Invalid credentials')}")
                            
        elif auth_mode == "Register":
            with st.form("register_form"):
                reg_email = st.text_input("Email")
                reg_password = st.text_input("Password", type="password")
                submit_register = st.form_submit_button("Register")
                
                if submit_register:
                    with st.spinner("Creating account..."):
                        # Registration expects standard JSON
                        reg_res = requests.post(
                            f"{API_URL}/user", 
                            json={"email": reg_email, "password": reg_password}
                        )
                        if reg_res.status_code == 201:
                            st.success("✅ Account created! Please select 'Log In' above to authenticate.")
                        else:
                            st.error(f"Registration failed: {reg_res.json().get('detail', 'Error')}")
                            
        elif auth_mode == "Manual Token":
            manual_token = st.text_input("Access Token / JWT", type="password")
            if st.button("Set Token"):
                if manual_token:
                    st.session_state.auth_token = manual_token
                    st.success("Token set!")
                    st.rerun()
                else:
                    st.warning("Please enter a token.")

    st.divider()
    
    st.header("Configuration")
    repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/user/repo")
    report_type = st.selectbox("Select Report Type", ["Security Analysis", "Code Quality", "Full Summary"])
    generate_btn = st.button("Generate Report", type="primary")

# 3. Handle Action
if generate_btn:
    # Use the token from session state!
    if not st.session_state.auth_token:
        st.error("Please log in or provide an Access Token in the sidebar first!")
    elif not repo_url:
        st.warning("Please enter a repository URL!")
    else:
        with st.spinner(
            "Cloning repository, embedding chunks, and generating report...\n\n"
            "⏳ *Most reports finish in under 45 seconds, but repositories near the size limit may take up to a maximum of 1m 15s. Please wait...*"
        ):
            try:
                headers = {
                    "Authorization": f"Bearer {st.session_state.auth_token}"
                }
                
                response = requests.post(
                    f"{API_URL}/repository_analysis", 
                    json={
                        "url": repo_url, 
                    },
                    headers=headers,
                    timeout=180
                )
                
                if response.status_code == 200:
                    st.success("✅ Report Generated Successfully!")
                    
                    report_data = response.json()
                    
                    for section_key, section_content in report_data.items():
                        display_title = section_key.replace("_", " ").title()
                        
                        with st.expander(f"📁 {display_title}", expanded=True):
                            if isinstance(section_content, (dict, list)):
                                formatted_markdown = json_to_markdown(section_content)
                                st.markdown(formatted_markdown)
                            else:
                                st.markdown(section_content)
                                
                elif response.status_code == 413:
                    try:
                        error_detail = response.json().get("detail", "Repository is too large.")
                    except ValueError:
                        error_detail = "The repository exceeded the maximum allowed size."
                    
                    st.warning("🧱 **Repository Size Limit Exceeded**", icon="⚠️")
                    st.info(f"**Backend Message:** {error_detail}", icon="ℹ️")
                    st.markdown(
                        "*💡 **Tip:** Try running RepoInsight on a smaller microservice or a specific module rather than a massive monorepo!*"
                    )
                    
                elif response.status_code == 401:
                    st.error("🔒 Unauthorized (401): Invalid or expired access token. Please log out and log back in.")
                else:
                    st.error(f"🚨 Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("The request timed out. The repository processing took longer than expected.")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend: {e}")