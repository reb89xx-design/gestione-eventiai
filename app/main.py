import streamlit as st
from .db import init_db
from .auth import login_widget
from .views import calendar, events, structure, artists, formats, people

def main():
    st.set_page_config(page_title="Agenzia Eventi", layout="wide")
    init_db()
    st.sidebar.title("Agenzia — Menu")
    if not login_widget():
        st.title("Benvenuto — Agenzia Eventi")
        st.info("Accedi per iniziare.")
        return
    if 'nav_to' in st.session_state:
        nav_default = st.session_state.pop('nav_to')
    else:
        nav_default = "Calendario"
    options = ["Calendario", "Crea Evento", "Artisti", "Format", "Persone", "Struttura"]
    nav = st.sidebar.radio("Sezioni", options, index=options.index(nav_default) if nav_default in options else 0)
    if nav == "Calendario":
        calendar.calendar_view()
    elif nav == "Crea Evento":
        events.create_event_view()
    elif nav == "Artisti":
        artists.artists_view()
    elif nav == "Format":
        formats.formats_view()
    elif nav == "Persone":
        people.people_view()
    elif nav == "Struttura":
        structure.structure_view()