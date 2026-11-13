import streamlit as st

import appointments 

st.set_page_config(page_title= "Clinic appointments : )", page_icon= "🧑‍⚕️🏥")

appointments.create_table()

st.title("Clinic appointments 🧑‍⚕️🏥")
st.caption("A clinical appointment booker created and configured using Python, Sqlite3 and Streamlit")

if "message" in st.session_state: 
    st.success(st.session_state.pop("message"))

patients= appointments.get_appointments()

def describe(patient): 
    return f"# {patient["id"] - {patient["patient_name"]}}"

tab_view, tab_add, tab_update, tab_delete= st.tabs(["View", "Add", "Update", "Delete"])

with tab_view: 
    st.subheader("All appointments")
    if patients: 
        st.patients(patients, hide_index= True)
        st.write(f"Total: {len(patients)} patient(s)")
    else: 
        st.info("No patients yet. Book some in the **Add** tab")



