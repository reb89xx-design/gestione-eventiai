import streamlit as st
import calendar
import pandas as pd
from ..models import fetch_events, fetch_artists, fetch_formats
from datetime import date
from dateutil.relativedelta import relativedelta

def _events_match_filters(row, artist_filter, format_filter):
    if artist_filter:
        if not row['artists'] or not any(int(a) in artist_filter for a in row['artists']):
            return False
    if format_filter:
        if pd.isna(row.get('format_id')) or int(row.get('format_id')) not in format_filter:
            return False
    return True

def calendar_view():
    st.header("Calendario")
    artists_df = fetch_artists()
    formats_df = fetch_formats()
    if 'calendar_month' not in st.session_state:
        st.session_state.calendar_month = date.today().replace(day=1)
    artist_filter = st.session_state.get('artist_filter', [])
    format_filter = st.session_state.get('format_filter', [])

    col_top = st.columns([1,1,4])
    with col_top[0]:
        if st.button('◀ Mese precedente'):
            st.session_state.calendar_month = (st.session_state.calendar_month - relativedelta(months=1)).replace(day=1)
    with col_top[1]:
        if st.button('Mese successivo ▶'):
            st.session_state.calendar_month = (st.session_state.calendar_month + relativedelta(months=1)).replace(day=1)
    with col_top[2]:
        if st.button("Clear filters"):
            st.session_state['artist_filter'] = []
            st.session_state['format_filter'] = []

    cm = st.session_state.calendar_month
    start = cm
    last_day = calendar.monthrange(cm.year, cm.month)[1]
    end = cm.replace(day=last_day)
    events_df = fetch_events(start.isoformat(), end.isoformat())
    if events_df is None or events_df.empty:
        st.info("Nessun evento nel mese selezionato.")
        return

    events_df['date'] = pd.to_datetime(events_df['date']).dt.date
    if artist_filter or format_filter:
        artist_filter_ids = [int(x) for x in artist_filter] if artist_filter else []
        format_filter_ids = [int(x) for x in format_filter] if format_filter else []
        mask = events_df.apply(lambda row: _events_match_filters(row, artist_filter_ids, format_filter_ids), axis=1)
        events_df = events_df[mask]

    if events_df.empty:
        st.info("Nessun evento dopo l'applicazione dei filtri.")
        return

    st.table(events_df[['id', 'title', 'date', 'format_name', 'promoter_name']])