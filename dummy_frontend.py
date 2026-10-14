import streamlit as st
import requests
import json

st.set_page_config(page_title="Orion IT Solutions - Appointment Booking", page_icon="💻", layout="centered")

st.title("🚀 Orion IT Solutions")
st.subheader("Book a Consultation with Muhammad Mayer Chishty")
st.markdown("Select your desired service, date, and time slot below to schedule an appointment with our team.")

# Form inputs
client_name = st.text_input("Your Full Name", "Valued Client")
service_type = st.selectbox(
    "Select Service",
    [
        "Website Development",
        "UI/UX Design",
        "AI Automation",
        "AI Agents",
        "Graphic Design",
        "Brand Identity"
    ]
)
reason_notes = st.text_area("Project Details / Requirements", "Looking for professional development and AI integration.")
appointment_date = st.date_input("Appointment Date")
appointment_time = st.selectbox("Time Slot", ["10:00 AM", "11:30 AM", "01:00 PM", "03:00 PM", "05:00 PM"])

if st.button("Confirm Appointment"):
    payload = {
        "patient_name": client_name,
        "service": service_type,
        "reason": reason_notes,
        "start_time": f"{appointment_date} {appointment_time}",
        "canceled": False
    }
    
    try:
        response = requests.post("http://127.0.0.1:4444/schedule-appointment", json=payload)
        if response.status_code == 200:
            st.success("🎉 Appointment successfully booked! Our team will get in touch with you shortly.")
            st.json(response.json())
        else:
            st.error(f"Failed to book appointment. Server response: {response.text}")
    except Exception as e:
        st.error(f"Connection error: Could not connect to backend server. Details: {e}")