import streamlit as st
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_conn

def get_user(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,username,password_hash,display_name FROM users WHERE username= ?", (username,))
    r = cur.fetchone()
    conn.close()
    if r:
        return {"id": r[0], "username": r[1], "password_hash": r[2], "display_name": r[3]}
    return None

def login_widget():
    st.sidebar.markdown("## Login")
    if "user" in st.session_state and st.session_state["user"]:
        st.sidebar.success(f"Connesso come {st.session_state['user']['display_name']}")
        if st.sidebar.button("Logout"):
            st.session_state.pop("user")
            st.experimental_rerun()
        return True
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        user = get_user(username)
        if user and check_password_hash(user["password_hash"], password):
            st.session_state["user"] = user
            st.sidebar.success(f"Benvenuto {user['display_name']}")
            st.experimental_rerun()
        else:
            st.sidebar.error("Credenziali errate.")
            return False
    return False
