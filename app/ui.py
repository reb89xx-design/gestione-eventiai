import streamlit as st

def page_header(title, subtitle=None):
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(f"_{subtitle}_")

def small_card(title, subtitle=""):
    st.markdown(f"**{title}**  \\n{subtitle}")
