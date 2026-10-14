from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db, init_db, Appointment
import requests

app = FastAPI(title="Orion IT Solutions - Voice Agent Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/health")
def health_check():
    return {"status": "healthy", "agency": "Orion IT Solutions", "handler": "Muhammad Mayer Chishty"}

class ScheduleRequest(BaseModel):
    client_name: Optional[str] = Field(None, description="Client name")
    patient_name: Optional[str] = Field(None, description="Patient name fallback")
    name: Optional[str] = Field(None, description="General name fallback")
    service: Optional[str] = Field("General Consultation", description="Selected Service")
    reason: Optional[str] = Field("None", description="Project notes")
    start_time: Optional[str] = Field(None, description="Appointment Date and Time slot")
    appointment_date: Optional[str] = Field(None, description="Date")
    time_slot: Optional[str] = Field(None, description="Time slot")
    canceled: Optional[bool] = Field(False)

@app.post("/schedule-appointment")
def schedule_appointment(req: ScheduleRequest, db: Session = Depends(get_db)):
    try:
        from datetime import datetime as dt
        
        # 1. Name ko safely extract karna (Vapi kisi bhi field mein naam bhej sakta hai)
        final_client_name = req.client_name or req.patient_name or req.name or "Valued Client"
        
        # 2. Date aur Time ko safely handle karna
        time_str = req.start_time or req.appointment_date or dt.now().strftime("%Y-%m-%d %H:%M")
        parsed_time = dt.now()
        try:
            parsed_time = dt.fromisoformat(time_str.replace("Z", ""))
        except:
            pass

        # 3. Local Database Entry
        new_appointment = Appointment(
            patient_name=final_client_name,
            reason=f"Service: {req.service or 'General'} | Notes: {req.reason or 'None'}",
            start_time=parsed_time,
            canceled=False
        )
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)

        # 4. Make.com Webhook Integration (Guaranteed Trigger)
        make_webhook_url = "https://hook.eu1.make.com/4r1gi2jtk35jg7kvj38gbv6kbvu1hjjn"
        payload_data = {
            "client_name": final_client_name,
            "service": req.service or "General Consultation",
            "reason": req.reason or "None",
            "start_time": str(parsed_time)
        }
        
        try:
            requests.post(make_webhook_url, json=payload_data, timeout=5)
        except Exception as webhook_err:
            print(f"Webhook trigger failed: {webhook_err}")

        return {
            "status": "success", 
            "message": f"Appointment booked successfully for {final_client_name}!",
            "appointment_id": new_appointment.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/availability")
def check_availability(date: Optional[str] = None):
    slots = ["10:00 AM", "11:30 AM", "01:00 PM", "03:00 PM", "05:00 PM"]
    return {
        "date": date or datetime.now().strftime("%Y-%m-%d"),
        "availability": "Available",
        "slots": slots,
        "handler": "Muhammad Mayer Chishty"
    }

@app.get("/list-appointments")
def list_appointments(date: Optional[str] = None, db: Session = Depends(get_db)):
    return db.query(Appointment).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="127.0.0.1", port=4444, reload=True)