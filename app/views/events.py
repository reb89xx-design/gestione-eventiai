import streamlit as st
from ..models import create_event, fetch_artists, fetch_formats, fetch_people
from datetime import date

def create_event_view():
    st.header("Crea Evento")
    artists_df = fetch_artists()
    formats_df = fetch_formats()
    people_df = fetch_people()
    with st.form("create_event_form"):
        title = st.text_input("Titolo")
        date_ev = st.date_input("Data", value=date.today())
        fmt = st.selectbox("Format", options=formats_df['name'].tolist()) if not formats_df.empty else None
        promoter = st.selectbox("Promoter", options=["Nessuno"] + people_df['name'].tolist()) if not people_df.empty else "Nessuno"
        artist_sel = st.multiselect("Artisti", options=artists_df['name'].tolist()) if not artists_df.empty else []
        notes = st.text_area("Note")
        if st.form_submit_button("Crea"):
            if not title:
                st.error("Inserisci un titolo.")
            else:
                format_id = int(formats_df[formats_df['name']==fmt]['id'].iloc[0]) if fmt is not None else None
                promoter_id = None
                if promoter != "Nessuno":
                    promoter_id = int(people_df[people_df['name']==promoter]['id'].iloc[0])
                artist_ids = [int(artists_df[artists_df['name']==n]['id'].iloc[0]) for n in artist_sel]
                create_event(title, date_ev.isoformat(), format_id, promoter_id, notes, artist_ids)
                st.success("Evento creato.")
