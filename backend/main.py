import io
import csv
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os

from .database import engine, Base, get_db
from .models import Lead, CallLog
from .locations import LOCATIONS_DATA, SERVICE_CATALOG, get_countries, get_states, get_cities
from .scraper import get_high_quality_leads

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Global Lead Generation & Cold Caller CRM Automation",
    description="Automated lead sourcing for Website Development, ERP & Custom Software with Cold Calling Feedback System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")


# Pydantic Schemas
class GenerateRequest(BaseModel):
    country: str
    state: str
    city: str
    service: str  # Website Development, ERP Software, Custom Software
    industry_niche: Optional[str] = "All Industries"
    count: Optional[int] = 15
    google_api_key: Optional[str] = None


class CallFeedbackRequest(BaseModel):
    caller_name: str
    call_status: str  # Interested, Follow-up Scheduled, Busy / Callback, Not Interested, Converted, etc.
    notes: str
    follow_up_date: Optional[str] = None


class ManualLeadRequest(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    website: Optional[str] = None
    category: Optional[str] = None
    country: str
    state: str
    city: str
    address: Optional[str] = None
    service_needed: str
    pitch_hook: Optional[str] = None


# Endpoints
@app.get("/api/locations")
def get_location_hierarchy():
    """Returns the full hierarchical Country -> State -> City tree."""
    return LOCATIONS_DATA


@app.get("/api/services")
def get_service_catalog():
    """Returns supported target services and their sub-industries."""
    return SERVICE_CATALOG


@app.post("/api/leads/generate")
async def generate_leads(req: GenerateRequest, db: Session = Depends(get_db)):
    """
    Generates new leads for the selected location (Country -> State -> City)
    and target service (Website Dev / ERP / Custom Software).
    Prevents duplicates and saves to SQLite database.
    """
    country = req.country.strip()
    state = req.state.strip()
    city = req.city.strip()
    service = req.service.strip()
    niche = req.industry_niche or "All Industries"
    count = min(max(req.count or 15, 5), 50)

    # 1. Fetch high-quality authentic leads
    leads_data = await get_high_quality_leads(
        country=country,
        state=state,
        city=city,
        service_needed=service,
        industry_niche=niche,
        count=count,
        google_api_key=req.google_api_key
    )

    added_count = 0
    created_leads = []

    for item in leads_data:
        # Check if already exists in DB
        existing = db.query(Lead).filter(
            Lead.name == item["name"],
            Lead.city == item["city"]
        ).first()

        if not existing:
            lead = Lead(**item)
            db.add(lead)
            db.flush()
            created_leads.append(lead)
            added_count += 1

    db.commit()

    return {
        "status": "success",
        "generated_count": len(leads_data),
        "added_to_database": added_count,
        "location": f"{city}, {state}, {country}",
        "service": service,
    }


@app.get("/api/leads")
def get_leads(
    country: Optional[str] = None,
    state: Optional[str] = None,
    city: Optional[str] = None,
    service: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Lead)

    if country and country != "All Countries":
        query = query.filter(Lead.country == country)
    if state and state != "All States":
        query = query.filter(Lead.state == state)
    if city and city != "All Cities":
        query = query.filter(Lead.city == city)
    if service and service != "All Services":
        query = query.filter(Lead.service_needed.ilike(f"%{service.replace('Development', '').strip()}%"))
    if status and status != "All Statuses":
        query = query.filter(Lead.call_status == status)
    if search:
        search_filter = f"%{search.strip()}%"
        query = query.filter(
            (Lead.name.ilike(search_filter)) |
            (Lead.category.ilike(search_filter)) |
            (Lead.caller_notes.ilike(search_filter)) |
            (Lead.phone.ilike(search_filter))
        )

    leads = query.order_by(Lead.id.desc()).all()
    return leads


@app.get("/api/leads/{lead_id}")
def get_lead_detail(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    logs = db.query(CallLog).filter(CallLog.lead_id == lead_id).order_by(CallLog.id.desc()).all()
    return {
        "lead": lead,
        "logs": logs
    }


@app.post("/api/leads/{lead_id}/call")
def log_call_feedback(lead_id: int, req: CallFeedbackRequest, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # Update lead status and details
    lead.call_status = req.call_status
    lead.caller_name = req.caller_name
    lead.caller_notes = req.notes
    lead.last_feedback = req.notes
    if req.follow_up_date:
        lead.next_follow_up = req.follow_up_date

    # Add call history log
    call_log = CallLog(
        lead_id=lead_id,
        call_status=req.call_status,
        caller_name=req.caller_name,
        notes=req.notes,
        follow_up_date=req.follow_up_date
    )
    db.add(call_log)
    db.commit()
    db.refresh(lead)

    return {"status": "success", "message": "Call feedback logged successfully", "lead": lead}


@app.post("/api/leads/manual")
def add_manual_lead(req: ManualLeadRequest, db: Session = Depends(get_db)):
    lead = Lead(
        name=req.name,
        phone=req.phone,
        email=req.email,
        website=req.website,
        has_website=bool(req.website),
        category=req.category or "General",
        country=req.country,
        state=req.state,
        city=req.city,
        address=req.address or f"{req.city}, {req.state}",
        service_needed=req.service_needed,
        pitch_hook=req.pitch_hook or "Manual lead entered for cold calling.",
        call_status="New Lead"
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return {"status": "success", "lead": lead}


@app.delete("/api/leads/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(lead)
    db.commit()
    return {"status": "success", "message": "Lead deleted"}


@app.post("/api/leads/purge-all")
def purge_all_leads(db: Session = Depends(get_db)):
    deleted = db.query(Lead).delete()
    db.commit()
    return {"status": "success", "deleted_count": deleted}


@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Lead).count()
    new_leads = db.query(Lead).filter(Lead.call_status == "New Lead").count()
    interested = db.query(Lead).filter(Lead.call_status == "Interested").count()
    followups = db.query(Lead).filter(Lead.call_status == "Follow-up Scheduled").count()
    converted = db.query(Lead).filter(Lead.call_status == "Converted").count()
    not_interested = db.query(Lead).filter(Lead.call_status == "Not Interested").count()
    attempted = db.query(Lead).filter(Lead.call_status.in_(["Attempted", "Busy / Callback"])).count()

    web_dev_count = db.query(Lead).filter(Lead.service_needed == "Website Development").count()
    erp_count = db.query(Lead).filter(Lead.service_needed == "ERP Software").count()
    custom_sw_count = db.query(Lead).filter(Lead.service_needed.like("%Custom Software%")).count()

    no_website_count = db.query(Lead).filter(Lead.has_website == False).count()

    return {
        "total_leads": total,
        "new_leads": new_leads,
        "interested": interested,
        "followups": followups,
        "converted": converted,
        "not_interested": not_interested,
        "in_progress": attempted,
        "by_service": {
            "Website Development": web_dev_count,
            "ERP Software": erp_count,
            "Custom Software": custom_sw_count,
        },
        "no_website_leads": no_website_count
    }


@app.get("/api/export")
def export_leads_csv(
    country: Optional[str] = None,
    city: Optional[str] = None,
    service: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Lead)
    if country and country != "All Countries":
        query = query.filter(Lead.country == country)
    if city and city != "All Cities":
        query = query.filter(Lead.city == city)
    if service and service != "All Services":
        query = query.filter(Lead.service_needed == service)
    if status and status != "All Statuses":
        query = query.filter(Lead.call_status == status)

    leads = query.order_by(Lead.id.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Lead ID", "Business Name", "Phone", "Email", "Category", 
        "City", "State", "Country", "Address", "Website", "Has Website",
        "Target Service", "Pitch Script / Hook", "Call Status", 
        "Caller Name", "Last Feedback / Notes", "Next Follow-up"
    ])

    for l in leads:
        writer.writerow([
            l.id, l.name, l.phone, l.email or "", l.category or "",
            l.city, l.state, l.country, l.address or "", l.website or "None",
            "Yes" if l.has_website else "No", l.service_needed, l.pitch_hook or "",
            l.call_status, l.caller_name or "", l.last_feedback or "", l.next_follow_up or ""
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=leads_cold_call_export.csv"}
    )


# Serve Frontend static assets
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def serve_index():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Frontend index.html not found"}
