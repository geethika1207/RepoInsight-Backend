import streamlit as st
import requests

# --- HELPER FUNCTION ---
# This converts the raw dictionary into clean, readable Markdown bullet points
def json_to_markdown(data, indent_level=0):
    markdown_text = ""
    indent = "    " * indent_level  # 4 spaces for proper markdown nesting
    
    if isinstance(data, dict):
        for key, value in data.items():
            # Clean up keys: "technology_stack" -> "Technology Stack"
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

# Set user expectations right on the dashboard!
st.info(
    "👋 **Welcome to RepoInsight!** \n\n"
    "To guarantee the highest quality AI analysis, our engine is currently optimized "
    "for **small to medium-sized repositories** (up to ~350,000 characters). "
    "Support for massive codebases is coming soon!"
)

# Live Render backend URL
API_URL = "https://repoinsight-backend-1.onrender.com"

# 2. Sidebar Setup
with st.sidebar:
    st.header("Authentication")
    auth_token = st.text_input("Access Token / JWT", type="password", help="Enter your auth token from login")
    
    st.divider()
    
    st.header("Configuration")
    repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/user/repo")
    report_type = st.selectbox("Select Report Type", ["Security Analysis", "Code Quality", "Full Summary"])
    generate_btn = st.button("Generate Report", type="primary")

# 3. Handle Action
if generate_btn:
    if not auth_token:
        st.error("Please enter your Access Token in the sidebar first!")
    elif not repo_url:
        st.warning("Please enter a repository URL!")
    else:
        with st.spinner("Cloning repository, embedding chunks, and generating report...\n\n⏳ *This process typically takes up to 1m 50s with a stable internet connection. Please wait...*"):
            try:
                # 4. Prepare Headers with Authentication
                headers = {
                    "Authorization": f"Bearer {auth_token}"
                }
                
                # 5. Make Call to Backend
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
                    
                    # Dynamically loop through the exact keys your backend returned
                    for section_key, section_content in report_data.items():
                        display_title = section_key.replace("_", " ").title()
                        
                        # The Dropdown Expander you liked!
                        with st.expander(f"📁 {display_title}", expanded=True):
                            
                            if isinstance(section_content, (dict, list)):
                                # USE THE HELPER FUNCTION HERE INSTEAD OF st.json()
                                formatted_markdown = json_to_markdown(section_content)
                                st.markdown(formatted_markdown)
                            else:
                                st.markdown(section_content)
                                
                elif response.status_code == 413:
                    # Safely extract the exact custom message from the backend JSON
                    try:
                        error_detail = response.json().get("detail", "Repository is too large.")
                    except ValueError:
                        error_detail = "The repository exceeded the maximum allowed size."
                    
                    # Display a friendly UI instead of a harsh red error
                    st.warning("🧱 **Repository Size Limit Exceeded**", icon="⚠️")
                    st.info(f"**Backend Message:** {error_detail}", icon="ℹ️")
                    st.markdown(
                        "*💡 **Tip:** Try running RepoInsight on a smaller microservice or a specific module rather than a massive monorepo!*"
                    )
                    
                elif response.status_code == 401:
                    st.error("🔒 Unauthorized (401): Invalid or expired access token.")
                else:
                    st.error(f"🚨 Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("The request timed out. The repository processing took longer than expected.")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend: {e}")