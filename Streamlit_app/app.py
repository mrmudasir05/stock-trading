import streamlit as st

st.set_page_config(page_title="Crypto Trading App", page_icon="💹", layout="wide")

st.title("💹 Crypto Trading Platform")
st.sidebar.success("Select a page above 👆")

# Initialize session state for JWT token
if "token" not in st.session_state:
    st.session_state["token"] = None
