import streamlit as st
import requests

# Point this to your live Render backend
API_URL = "https://repoinsight-backend-1.onrender.com"

st.title("RepoInsight Dashboard")

# Example of how Streamlit will talk to your backend
if st.button("Generate Report"):
    response = requests.post(f"{API_URL}/your-endpoint", json={"query": "test"})
    st.write(response.json())