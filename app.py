import csv
import json
import os
import re
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

BASE_DIR = Path(__file__).parent
SLOTS_FILE = BASE_DIR / "slots.csv"
BOOKINGS_FILE = BASE_DIR / "bookings.csv"
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

DEPARTMENTS = ["Cardiology", "Dermatology", "General Medicine", "Orthopedics", "Pediatrics"]
DOCTORS = {
    "Cardiology": ["Dr. Asha Rao", "Dr. Vikram Shah"],
    "Dermatology": ["Dr. Meera Nair"],
    "General Medicine": ["Dr. Rahul Menon", "Dr. Sana Khan"],
    "Orthopedics": ["Dr. Arjun Das"],
    "Pediatrics": ["Dr. Neha Iyer"],
}

def ensure_demo_data():
    """Create a small, clearly labelled demo schedule if no schedule exists."""
    if not SLOTS_FILE.exists():
        rows = []
        times = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
        for day_offset in range(1, 8):
            day = date.today() + timedelta(days=day_offset)
            for department, doctors in DOCTORS.items():
                for doctor in doctors:
                    for time in times:
                        rows.append({
                            "slot_id": str(uuid.uuid4())[:8],
                            "doctor": doctor,
                            "department": department,
                            "date": day.isoformat(),
                            "time": time,
                            "available": "true",
                        })
        with SLOTS_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["slot_id", "doctor", "department", "date", "time", "available"])
            writer.writeheader()
            writer.writerows(rows)

    if not BOOKINGS_FILE.exists():
        with BOOKINGS_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "booking_id", "patient_name", "phone", "department", "doctor",
                "appointment_date", "appointment_time", "created_at"
            ])
            writer.writeheader()

def read_rows(path):
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_rows(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def extract_booking_details(request_text, api_key):
    """Use Gemini only to extract fields; Python validates all extracted values."""
    client = genai.Client(api_key=api_key)
    schema = {
        "type": "OBJECT",
        "properties": {
            "patient_name": {"type": "STRING"},
            "phone": {"type": "STRING"},
            "department": {"type": "STRING"},
            "preferred_date": {"type": "STRING", "description": "Date in YYYY-MM-DD format"},
            "preferred_time": {"type": "STRING", "description": "24-hour HH:MM format"},
        },
        "required": ["patient_name", "phone", "department", "preferred_date", "preferred_time"],
    }
    prompt = f"""
Extract appointment details from the patient's request.
Return only the requested JSON fields. Do not invent missing information.
If a field is missing or ambiguous, return an empty string for that field.
Allowed departments: {", ".join(DEPARTMENTS)}.
Convert a clearly stated date to YYYY-MM-DD and time to 24-hour HH:MM.
Do not provide medical advice or infer a diagnosis.

Patient request:
{request_text}
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
            temperature=0.1,
        ),
    )
    return json.loads(response.text)

def validate_details(data):
    required = ["patient_name", "phone", "department", "preferred_date", "preferred_time"]
    missing = [key for key in required if not str(data.get(key, "")).strip()]
    if missing:
        return False, "Please provide: " + ", ".join(missing).replace("_", " ") + "."
    if data["department"] not in DEPARTMENTS:
        return False, f"Department must be one of: {', '.join(DEPARTMENTS)}."
    if not re.fullmatch(r"[0-9+\-\s()]{8,18}", data["phone"]):
        return False, "Please provide a valid phone number (8–18 digits/phone characters)."
    try:
        appt_date = date.fromisoformat(data["preferred_date"])
        datetime.strptime(data["preferred_time"], "%H:%M")
    except ValueError:
        return False, "Date or time format is invalid. Use YYYY-MM-DD and HH:MM."
    if appt_date <= date.today():
        return False, "Please choose a future date."
    return True, "Details validated."

def book_slot(data):
    """Python, not the LLM, performs the availability check and CSV update."""
    slots = read_rows(SLOTS_FILE)
    matching = [
        row for row in slots
        if row["department"] == data["department"]
        and row["date"] == data["preferred_date"]
        and row["time"] == data["preferred_time"]
        and row["available"].lower() == "true"
    ]
    if not matching:
        alternatives = [
            row for row in slots
            if row["department"] == data["department"]
            and row["date"] == data["preferred_date"]
            and row["available"].lower() == "true"
        ][:5]
        return None, alternatives

    chosen = matching[0]
    chosen["available"] = "false"
    fields = ["slot_id", "doctor", "department", "date", "time", "available"]
    write_rows(SLOTS_FILE, slots, fields)

    booking = {
        "booking_id": "MED-" + uuid.uuid4().hex[:8].upper(),
        "patient_name": data["patient_name"].strip(),
        "phone": data["phone"].strip(),
        "department": data["department"],
        "doctor": chosen["doctor"],
        "appointment_date": chosen["date"],
        "appointment_time": chosen["time"],
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    with BOOKINGS_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(booking.keys()))
        writer.writerow(booking)
    return booking, []

st.set_page_config(page_title="MediSlot AI", page_icon="🏥", layout="centered")
ensure_demo_data()

st.title("🏥 MediSlot AI")
st.caption("AI-powered hospital appointment booking assistant")
st.info("Student demonstration only. Uses sample doctors and simulated appointment slots. Do not enter real patient or medical information.")

with st.sidebar:
    st.header("About this project")
    st.write("Problem Statement 59 – Hospital Appointment Bot")
    st.write("Gemini extracts details; Python checks and books a slot.")
    st.caption(f"Model setting: {MODEL_NAME}")
    st.caption("Demo schedule: next 7 days")

api_key = os.getenv("GEMINI_API_KEY", "")
try:
    api_key = st.secrets.get("GEMINI_API_KEY", api_key)
except Exception:
    # Streamlit secrets.toml is optional for local development.
    pass

if not api_key:
    st.warning("Gemini API key not found. Add GEMINI_API_KEY to your .env file or Streamlit secrets.")
    st.markdown("[Get a Gemini API key](https://aistudio.google.com/app/apikey)")

st.subheader("Book an appointment")
request_text = st.text_area(
    "Describe the appointment request",
    placeholder="Example: My name is Ananya Sharma, phone 9876543210. I need a Cardiology appointment tomorrow at 10 AM.",
    height=120,
)
st.caption("Include patient name, phone number, department, future date and preferred time.")

if st.button("Extract details and check availability", type="primary", use_container_width=True):
    if not request_text.strip():
        st.error("Enter an appointment request first.")
    elif not api_key:
        st.error("Configure your Gemini API key before making a request.")
    else:
        try:
            with st.spinner("Gemini is extracting the appointment details..."):
                details = extract_booking_details(request_text, api_key)
            st.session_state["extracted_details"] = details
        except Exception as exc:
            st.error(f"Gemini request failed: {exc}")

if "extracted_details" in st.session_state:
    details = st.session_state["extracted_details"]
    st.subheader("Extracted details")
    st.json(details)
    valid, message = validate_details(details)
    if not valid:
        st.warning(message)
    else:
        st.success(message)
        if st.button("Confirm and book appointment", use_container_width=True):
            booking, alternatives = book_slot(details)
            if booking:
                st.success("Appointment booked successfully!")
                st.write(f"**Booking ID:** `{booking['booking_id']}`")
                st.write(f"**Patient:** {booking['patient_name']}")
                st.write(f"**Doctor:** {booking['doctor']}")
                st.write(f"**Department:** {booking['department']}")
                st.write(f"**Date:** {booking['appointment_date']}")
                st.write(f"**Time:** {booking['appointment_time']}")
                st.session_state.pop("extracted_details", None)
            else:
                st.error("That exact slot is not available. No booking was made.")
                if alternatives:
                    st.write("Available alternatives on the selected date:")
                    for slot in alternatives:
                        st.write(f"- {slot['time']} — {slot['doctor']}")
                else:
                    st.write("No alternative slots are available for this department on that date.")

st.divider()
with st.expander("View demo availability"):
    available = [r for r in read_rows(SLOTS_FILE) if r["available"].lower() == "true"]
    st.dataframe(available, use_container_width=True, hide_index=True)
with st.expander("View demo bookings"):
    bookings = read_rows(BOOKINGS_FILE)
    if bookings:
        st.dataframe(bookings, use_container_width=True, hide_index=True)
    else:
        st.write("No appointments booked yet.")

st.caption("MediSlot AI is an academic prototype, not a real hospital booking service.")
