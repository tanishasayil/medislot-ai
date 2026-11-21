# Test plan – MediSlot AI

Run these tests using future dates and available slots shown in the app.

1. **Successful booking:** Valid name, phone, department, future date and available time. Expected: booking ID shown and slot becomes unavailable.
2. **Unavailable time:** Valid details but a time not listed. Expected: no booking; alternatives shown if available.
3. **Missing phone:** Omit phone. Expected: validation asks for the missing phone; no booking.
4. **Invalid department:** Use a department not in the allowed list. Expected: validation rejects it.
5. **Past date:** Request yesterday. Expected: validation rejects the date.
6. **Duplicate booking attempt:** Book a slot, then request the same slot again. Expected: second request is rejected as unavailable.

Record actual outcomes and screenshots after running the application. Do not claim tests passed until you have run them.
