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
