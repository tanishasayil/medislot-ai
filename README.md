# MediSlot AI – Hospital Appointment Bot

**Problem Statement 59 | GenAI (LLM) Mini Project**

A Streamlit prototype that uses Google's Gemini API to extract appointment details from natural-language requests. Python validates the details, checks a CSV-based demo schedule, books an available slot, and records the booking.

## Features
- Natural-language appointment request input
- Gemini-powered structured detail extraction
- Python validation of patient details, department, date and time
- CSV-based appointment availability
- Booking confirmation with a unique booking ID
- Alternative slot suggestions when the requested slot is unavailable

## Tech stack
Python, Streamlit, Google Gen AI Python SDK (`google-genai`), CSV.

## Setup (macOS/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and replace the placeholder with your Gemini API key. Never commit `.env`.

Get an API key from https://aistudio.google.com/app/apikey

## Run
```bash
streamlit run app.py
```

The app creates a sample schedule for the next seven days in `slots.csv` and stores confirmed demo bookings in `bookings.csv`.

## Sample test request
Use a future date shown in the app's availability table, for example:
`My name is Ananya Sharma, phone 9876543210. I need a Cardiology appointment on 2026-11-21 at 10:00.`

Use the actual future date displayed by your running app if this example date has passed.

## Important limitations
- This is a classroom prototype with simulated doctors and slots, not connected to a real hospital.
- Do not enter real patient data.
- CSV storage is suitable for a single-user demonstration only. A production booking service needs a transactional database, authentication, access control, audit logging, privacy safeguards and concurrency protection.
- The LLM extracts fields only. Python is the authority for availability and booking.

## Repository contents
- `app.py` – Streamlit application and booking logic
- `requirements.txt` – Python dependencies
- `.env.example` – environment variable template (no secret)
- `slots.csv` and `bookings.csv` – generated locally on first run


### 1. MediSlot AI – Application Homepage
The main interface where patients enter their appointment requirements.
<img width="1457" height="787" alt="01_Homepage" src="https://github.com/user-attachments/assets/8c7146dc-056c-4f38-9cfd-9b3eb82bdcb3" />


### 2. Gemini-Powered Information Extraction
Gemini extracts the patient's name, department, preferred date and time into structured JSON.
<img width="757" height="629" alt="02_Extracted_details" src="https://github.com/user-attachments/assets/a9669472-e8a4-49b6-b299-12289b235dea" />

### 3. Appointment Slot Unavailability
The application detects when the requested appointment slot is unavailable and displays alternative slots.
<img width="810" height="783" alt="03_Unavailable_slot" src="https://github.com/user-attachments/assets/0aecccea-acbe-4a51-8e35-bf032820402d" />

### 4. Alternative Slot Selection and Booking
The patient selects an available alternative slot, and the application confirms the appointment.
<img width="771" height="715" alt="04_Alternative_slot_booking" src="https://github.com/user-attachments/assets/f96331cc-1e2c-4465-be28-d304f2a12a9e" />

### 5. Booking Records and Slot Status
The booking records are updated, and the booked slot is marked as unavailable to prevent duplicate bookings.
<img width="1464" height="363" alt="06_Booking_records" src="https://github.com/user-attachments/assets/2b75a9e6-bc21-4cfc-9abf-16fec16514da" />
