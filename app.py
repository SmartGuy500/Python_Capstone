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
    return f"# {patient["id"] - {patient["reason"]}}"

tab_view, tab_add, tab_update, tab_delete= st.tabs(["View", "Add", "Update", "Delete"])

with tab_view: 
    st.subheader("All appointments")
    if patients: 
        st.patients(patients, hide_index= True)
        st.write(f"Total: {len(patients)} patient(s)")
    else: 
        st.info("No patients yet. Book some in the **Add** tab")

with tab_add: 
    st.subheader("Add appointment(s)")
    with st.form("add_form", clear_on_submit= True): 
        patient_name= st.text_input("Name(s): ")
        patient_contact= st.text_input("Phone Number: ")
        doctor= st.text_input("Doctor's name: ")
        day= st.text_input("Day of appointment: ")
        time= st.text("Time of appointment: ")
        reason= st.text_input("Reason for appointment: ", placeholder= "Medical check-in")
        submitted= st.form_submit_button("Add appointment")

    if submitted: 
        if patient_name.strip=="": 
            st.error("Please enter a name: ")
        elif doctor.strip=="": 
            st.error("Please enter your doctor's name: ")
        elif day.strip=="": 
            st.error("Please enter a day: ")
        elif time.strip=="": 
            st.error("Please enter a time: ")
        else: 
            appointments.add_appointments(patient_name.strip(), patient_contact.strip(), doctor.strip(), day.strip(), time.strip(), reason.strip())
            st.session_state["message"]= f"Added {patient_name.strip()}, , {doctor.strip()}, {day.strip()}, and {time.strip()} successfully"
            st.rerun()

with tab_update: 
    st.subheader("Update appointment(s)")
    if patients: 
        patient= st.selectbox("Choose a patient: ", patients, format_func=describe, key="update_choice")

        new_patient_name= st.text_input("Name: ", value=patient["patient_name"], key=f"name_{patient["id"]}")
        new_patient_contact= st.text_input("Contact Number: ", value=patient["patient_contact"], key=f"name_{patient["patient_contact"]}")
        new_doctor= st.text_input("Doctor: ", value=patient["doctor"], key=f"name_{patient["doctor"]}")
        new_day= st.text_input("Day: ", value=patient["day"], key=f"name_{patient["day"]}")
        new_time= st.text_input("Time: ", value=patient["time"], key=f"name_{patient["time"]}")
        new_reason= st.text_input("Reason: ", value=patient["reason"], key=f"name_{patient["reason"]}")

        if st.button("Save changes"): 
            if new_patient_name.strip=="": 
                st.error("Please enter a name: ")
            elif new_doctor.strip=="": 
                st.error("Please enter your doctor's name: ")
            elif new_day.strip=="": 
                st.error("Please enter a day: ")
            elif new_time.strip=="": 
                st.error("Please enter a time: ")
            else: 
                appointments.update_appointments(patient["id", new_patient_name.strip(), new_patient_contact.strip(), new_doctor.strip(), new_day.strip(), new_time.strip(), new_reason.strip()])
                st.session_state["message"]= f"Updated {patient_name.strip()} successfully"
                st.rerun()
    else: 
        st.info("There is no appointment(s) to update")

with tab_delete: 
    st.subheader("Delete appointment(s)")
    if not patients:
        st.info("There is no appointment(s) to delete")
    else: 
        patient= st.selectbox("Choose an appointment", patients, format_func=describe, key="delete_choice")
        sure= st.selectbox(f"Yes I confirm I am deleting {patient["patient_name"]}")



    



