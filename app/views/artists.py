import streamlit as st
from ..models import fetch_artists, create_artist, update_artist, delete_artist

def artists_view():
    st.header("Artisti")
    if 'pending_delete' not in st.session_state:
        st.session_state['pending_delete'] = None

    artists = fetch_artists()
    for _, r in artists.iterrows():
        cols = st.columns([4,1,1,1])
        cols[0].write(r['name'])
        if cols[1].button("Apri calendario", key=f"art_cal_{r['id']}"):
            st.session_state['artist_filter'] = [int(r['id'])]
            st.session_state['format_filter'] = []
            st.session_state['nav_to'] = "Calendario"
            st.experimental_rerun()
        if cols[2].button("Modifica", key=f"edit_artist_{r['id']}"):
            new = st.text_input("Nome artista", value=r['name'], key=f"input_artist_{r['id']}")
            if st.button("Salva", key=f"save_artist_{r['id']}"):
                update_artist(r['id'], new)
                st.success("Artista aggiornato")
                st.experimental_rerun()
        if cols[3].button("Elimina", key=f"del_artist_{r['id']}"):
            st.session_state['pending_delete'] = ("artist", int(r['id']), r['name'])

    st.markdown("---")
    with st.form("add_artist"):
        name = st.text_input("Nuovo artista")
        if st.form_submit_button("Aggiungi artista"):
            if not name:
                st.error("Inserisci un nome")
            else:
                create_artist(name)
                st.success("Artista aggiunto")
                st.experimental_rerun()

    # Confirmation area
    if st.session_state.get('pending_delete'):
        typ, oid, name = st.session_state['pending_delete']
        if typ == "artist":
            st.warning(f"Confermi l'eliminazione dell'artista: {name}?")
            colc, cold = st.columns([1,1])
            if colc.button("Conferma eliminazione"):
                delete_artist(oid)
                st.success("Artista eliminato")
                st.session_state['pending_delete'] = None
                st.experimental_rerun()
            if cold.button("Annulla"):
                st.session_state['pending_delete'] = None
                st.experimental_rerun()