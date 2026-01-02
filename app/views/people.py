import streamlit as st
from ..models import fetch_people, create_person, update_person, delete_person

ROLES = ["PROMOTER", "TOUR_MANAGER", "MASCOT", "VOCALIST", "BALLERINA", "DJ", "SERVICE_IMPIANTI", "OTHER"]

def people_view():
    st.header("Persone & Ruoli")
    if 'pending_delete' not in st.session_state:
        st.session_state['pending_delete'] = None

    people = fetch_people()
    for _, r in people.iterrows():
        cols = st.columns([4,1,1,1])
        cols[0].write(f"{r['name']} — {r['role']}")
        if cols[1].button("Filtra ruolo", key=f"filter_role_{r['id']}"):
            st.session_state['people_role_filter'] = r['role']
            st.session_state['nav_to'] = "Persone"
            st.experimental_rerun()
        if cols[2].button("Modifica", key=f"edit_person_{r['id']}"):
            new_name = st.text_input("Nome", value=r['name'], key=f"input_person_name_{r['id']}")
            new_role = st.selectbox("Ruolo", ROLES, index=ROLES.index(r['role']) if r['role'] in ROLES else len(ROLES)-1, key=f"input_person_role_{r['id']}")
            if st.button("Salva", key=f"save_person_{r['id']}"):
                update_person(r['id'], new_name, new_role)
                st.success("Persona aggiornata")
                st.experimental_rerun()
        if cols[3].button("Elimina", key=f"del_person_{r['id']}"):
            st.session_state['pending_delete'] = ("person", int(r['id']), r['name'])

    st.markdown("---")
    with st.form("add_person"):
        name = st.text_input("Nome persona")
        role = st.selectbox("Ruolo", ROLES)
        if st.form_submit_button("Aggiungi persona"):
            if not name:
                st.error("Inserisci un nome")
            else:
                create_person(name, role)
                st.success("Persona aggiunta")
                st.experimental_rerun()

    if st.session_state.get('pending_delete'):
        typ, oid, name = st.session_state['pending_delete']
        if typ == "person":
            st.warning(f"Confermi l'eliminazione della persona: {name}?")
            colc, cold = st.columns([1,1])
            if colc.button("Conferma eliminazione"):
                delete_person(oid)
                st.success("Persona eliminata")
                st.session_state['pending_delete'] = None
                st.experimental_rerun()
            if cold.button("Annulla"):
                st.session_state['pending_delete'] = None
                st.experimental_rerun()