import streamlit as st
import calendar
import pandas as pd
from ..models import fetch_events, fetch_artists, fetch_formats
from datetime import date

def calendar_view():
    st.header("Calendario")
    artists_df = fetch_artists()
    formats_df = fetch_formats()
    # simple next/prev month navigation stored in session
    if 'calendar_month' not in st.session_state:
        st.session_state.calendar_month = date.today().replace(day=1)
    col1, col2 = st.columns(2)
    with col1:
        if st.button('◀ Mese precedente'):
            import datetime
            st.session_state.calendar_month = (st.session_state.calendar_month - pd.DateOffset(months=1)).date()
    with col2:
        if st.button('Mese successivo ▶'):
            st.session_state.calendar_month = (st.session_state.calendar_month + pd.DateOffset(months=1)).date()

    cm = st.session_state.calendar_month
    start = cm
    last_day = calendar.monthrange(cm.year, cm.month)[1]
    end = cm.replace(day=last_day)
    events_df = fetch_events(start.isoformat(), end.isoformat())
    if events_df is None or events_df.empty:
        st.info("Nessun evento nel mese selezionato.")
    else:
        events_df['date'] = pd.to_datetime(events_df['date']).dt.date
        st.table(events_df[['id','title','date','format_name','promoter_name']])
