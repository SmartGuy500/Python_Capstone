import streamlit as st

import appointments


st.set_page_config(page_title="Clinic appointments", page_icon="🏥")
appointments.create_table()

st.title("Clinic appointments")
st.caption("Manage clinic appointments using Python, SQLite, and Streamlit.")

if "message" in st.session_state:
    st.success(st.session_state.pop("message"))

patients = appointments.get_appointments()


def describe(patient):
    return (
        f"#{patient['id']} - {patient['patient_name']} "
        f"with Dr. {patient['doctor']} on {patient['day']} at {patient['time']}"
    )


tab_view, tab_add, tab_update, tab_delete = st.tabs(
    ["View", "Add", "Update", "Delete"]
)

with tab_view:
    st.subheader("All appointments")
    if patients:
        st.dataframe(patients, hide_index=True)
        st.write(f"Total: {len(patients)} appointment(s)")
    else:
        st.info("No appointments yet. Book one in the Add tab.")

with tab_add:
    st.subheader("Add an appointment")
    with st.form("add_appointment_form", clear_on_submit=True):
        patient_name = st.text_input("Patient name")
        patient_contact = st.text_input("Phone number")
        doctor = st.text_input("Doctor's name")
        day = st.text_input("Day of appointment")
        time = st.text_input("Time of appointment")
        reason = st.text_input("Reason for appointment")
        submitted = st.form_submit_button("Add appointment")

    if submitted:
        if not patient_name.strip():
            st.error("Please enter the patient's name.")
        elif not doctor.strip():
            st.error("Please enter the doctor's name.")
        elif not day.strip():
            st.error("Please enter the appointment day.")
        elif not time.strip():
            st.error("Please enter the appointment time.")
        else:
            appointments.add_appointments(
                patient_name.strip(),
                patient_contact.strip(),
                doctor.strip(),
                day.strip(),
                time.strip(),
                reason.strip(),
            )
            st.session_state["message"] = (
                f"Added {patient_name.strip()}'s appointment successfully."
            )
            st.rerun()

with tab_update:
    st.subheader("Update an appointment")
    if patients:
        patient = st.selectbox(
            "Choose an appointment",
            patients,
            format_func=describe,
            key="update_choice",
        )
        patient_id = patient["id"]
        with st.form("update_appointment_form"):
            new_patient_name = st.text_input(
                "Patient name",
                value=patient["patient_name"],
                key=f"update_name_{patient_id}",
            )
            new_patient_contact = st.text_input(
                "Phone number",
                value=patient["patient_contact"] or "",
                key=f"update_contact_{patient_id}",
            )
            new_doctor = st.text_input(
                "Doctor's name",
                value=patient["doctor"],
                key=f"update_doctor_{patient_id}",
            )
            new_day = st.text_input(
                "Day of appointment",
                value=patient["day"],
                key=f"update_day_{patient_id}",
            )
            new_time = st.text_input(
                "Time of appointment",
                value=patient["time"],
                key=f"update_time_{patient_id}",
            )
            new_reason = st.text_input(
                "Reason for appointment",
                value=patient["reason"] or "",
                key=f"update_reason_{patient_id}",
            )
            update_submitted = st.form_submit_button("Save changes")

        if update_submitted:
            if not new_patient_name.strip():
                st.error("Please enter the patient's name.")
            elif not new_doctor.strip():
                st.error("Please enter the doctor's name.")
            elif not new_day.strip():
                st.error("Please enter the appointment day.")
            elif not new_time.strip():
                st.error("Please enter the appointment time.")
            else:
                appointments.update_appointments(
                    patient_id,
                    new_patient_name.strip(),
                    new_patient_contact.strip(),
                    new_doctor.strip(),
                    new_day.strip(),
                    new_time.strip(),
                    new_reason.strip(),
                )
                st.session_state["message"] = (
                    f"Updated {new_patient_name.strip()}'s appointment successfully."
                )
                st.rerun()
    else:
        st.info("There are no appointments to update.")

with tab_delete:
    st.subheader("Delete an appointment")
    if patients:
        patient = st.selectbox(
            "Choose an appointment",
            patients,
            format_func=describe,
            key="delete_choice",
        )
        st.warning(
            f"Delete appointment #{patient['id']} for {patient['patient_name']} "
            f"with Dr. {patient['doctor']}?"
        )
        confirmed = st.checkbox(
            f"Confirm deletion of {patient['patient_name']}'s appointment",
            key=f"delete_confirm_{patient['id']}",
        )
        if st.button("Delete appointment", type="primary", disabled=not confirmed):
            appointments.delete_appointments(patient["id"])
            st.session_state["message"] = (
                f"Deleted {patient['patient_name']}'s appointment successfully."
            )
            st.rerun()
    else:
        st.info("There are no appointments to delete.")
