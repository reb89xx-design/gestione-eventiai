import streamlit as st
from .db import init_db
from .auth import login_widget
from .views import calendar, events
import os

def main():
    st.set_page_config(page_title="Agenzia Eventi", layout="wide")
    init_db()
    st.sidebar.title("Agenzia — Menu")
    if not login_widget():
        st.title("Benvenuto — Agenzia Eventi")
        st.info("Accedi per iniziare.")
        return
    nav = st.sidebar.radio("Sezioni", ["Calendario", "Crea Evento", "Struttura"])
    if nav == "Calendario":
        calendar.calendar_view()
    elif nav == "Crea Evento":
        events.create_event_view()
    elif nav == "Struttura":
        st.header("Struttura & Persone")
        st.info("Gestione persone in Struttura - funzione in sviluppo")
