import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)
    has_website = Column(Boolean, default=False)
    category = Column(String(255), nullable=True)
    
    # Cascading location fields
    country = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)
    address = Column(String(500), nullable=True)
    
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    
    # Target Service & Pitch
    service_needed = Column(String(100), nullable=False, index=True)  # Website Development, ERP Software, Custom Software
    pitch_hook = Column(String(500), nullable=True)
    
    # Cold Caller Workflow
    call_status = Column(String(50), default="New Lead", index=True)
    # Options: "New Lead", "Attempted", "Busy / Callback", "Interested", "Follow-up Scheduled", "Not Interested", "Wrong Number", "Converted"
    caller_notes = Column(Text, nullable=True)
    last_feedback = Column(Text, nullable=True)
    next_follow_up = Column(String(100), nullable=True)
    caller_name = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    logs = relationship("CallLog", back_populates="lead", cascade="all, delete-orphan", order_by="desc(CallLog.created_at)")


class CallLog(Base):
    __tablename__ = "call_logs"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    call_status = Column(String(50), nullable=False)
    caller_name = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    follow_up_date = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    lead = relationship("Lead", back_populates="logs")
