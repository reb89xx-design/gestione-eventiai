import streamlit as st
from ..models import fetch_formats, create_format, update_format, delete_format

def formats_view():
    st.header("Format")
    if 'pending_delete' not in st.session_state:
        st.session_state['pending_delete'] = None

    formats = fetch_formats()
    for _, r in formats.iterrows():
        cols = st.columns([4,1,1,1])
        cols[0].write(r['name'])
        if cols[1].button("Apri calendario", key=f"format_cal_{r['id']}"):
            st.session_state['format_filter'] = [int(r['id'])]
            st.session_state['artist_filter'] = []
            st.session_state['nav_to'] = "Calendario"
            st.experimental_rerun()
        if cols[2].button("Modifica", key=f"edit_format_{r['id']}"):
            new = st.text_input("Nome format", value=r['name'], key=f"input_format_{r['id']}")
            if st.button("Salva", key=f"save_format_{r['id']}"):
                update_format(r['id'], new)
                st.success("Format aggiornato")
                st.experimental_rerun()
        if cols[3].button("Elimina", key=f"del_format_{r['id']}"):
            st.session_state['pending_delete'] = ("format", int(r['id']), r['name'])

    st.markdown("---")
    with st.form("add_format"):
        name = st.text_input("Nuovo format")
        if st.form_submit_button("Aggiungi format"):
            if not name:
                st.error("Inserisci un nome")
            else:
                create_format(name)
                st.success("Format aggiunto")
                st.experimental_rerun()

    if st.session_state.get('pending_delete'):
        typ, oid, name = st.session_state['pending_delete']
        if typ == "format":
            st.warning(f"Confermi l'eliminazione del format: {name}?")
            colc, cold = st.columns([1,1])
            if colc.button("Conferma eliminazione"):
                delete_format(oid)
                st.success("Format eliminato")
                st.session_state['pending_delete'] = None
                st.experimental_rerun()
            if cold.button("Annulla"):
                st.session_state['pending_delete'] = None
                st.experimental_rerun()