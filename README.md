# OmniLead AI - Global Lead Generation & Cold Caller CRM

An end-to-end automation system designed to discover high-value business leads for **Website Development**, **ERP Software**, and **Custom Software Development** worldwide, featuring cascading geographic filtering (**Country &rarr; State &rarr; City / Jalgaon**) and a built-in **Cold Caller CRM & Feedback Engine**.

---

## 🌟 Key Features

1. **Cascading Geographic Discovery (Country &rarr; State &rarr; City)**
   - Fully dependent dropdowns: Selecting **India** automatically populates states like **Maharashtra**, which dynamically populates cities like **Jalgaon**, **Mumbai**, **Pune**, etc.
   - Worldwide coverage: USA, UK, UAE, Canada, Australia, Germany, Singapore, etc.
   - **Custom City Support**: Type any town or district across the globe.

2. **Target Service Niche Segmentation**
   - **Website Development**: Scrapes and pinpoints businesses without a mobile-friendly website or with missing web presence.
   - **ERP Software**: Targets manufacturing units (MIDC), wholesale stockists, agro mills, pipe/plastic polymers, and distributors needing stock, batch tracking, and GST billing.
   - **Custom Software Development**: Identifies clinics, diagnostic labs, coaching academies, transport agencies, and credit societies needing bespoke booking, portal, and WhatsApp apps.

3. **Cold Caller Action Center**
   - **1-Click Calling**: Direct `tel:+...` dialer connection.
   - **1-Click WhatsApp**: Opens WhatsApp chat with a pre-written, professional introduction message.
   - **Tailored Pitch Angles**: Generates ready-to-use conversation hooks for cold callers.
   - **Live Disposition / Feedback Logger**:
     - *Statuses*: `Interested`, `Follow-up Scheduled`, `Busy / Callback`, `Attempted`, `Not Interested`, `Wrong Number`, `Converted`.
     - *Feedback Notes*: Record exact objections, decision-maker names, and requirements.
     - *Next Follow-up Scheduler*: Date and time picker for automatic reminders.
     - *Call History Log*: Keeps a timeline of every conversation attempt.

4. **Analytics & One-Click CSV Export**
   - Real-time conversion funnel and service interest breakdown.
   - Export filtered leads to CSV with phone numbers formatted for auto-dialers.

---

## 🚀 Quick Start Guide

### 1. Launch the Application
In your terminal, navigate to the project directory and run:
```bash
python run.py
```
Or directly with Uvicorn:
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

The app will open automatically in your browser at:
👉 **`http://localhost:8000`**

---

## 📂 Project Architecture

```
lead-gen-crm/
├── backend/
│   ├── database.py       # SQLite connection and SQLAlchemy session
│   ├── models.py         # Lead & CallLog data models
│   ├── locations.py      # Cascading Country -> State -> City hierarchy
│   ├── scraper.py        # Lead generation engine & OSM Overpass integration
│   ├── main.py           # FastAPI REST endpoints & static file serving
│   └── leads_crm.db      # SQLite database
├── frontend/
│   └── index.html        # Modern SPA (Tailwind CSS, Lucide icons, CRM UI)
├── run.py                # 1-click startup script with browser launcher
└── README.md
```
