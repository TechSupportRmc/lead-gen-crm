"""
Comprehensive cascading location hierarchy (Country -> State -> City).
Specifically includes India -> Maharashtra -> Jalgaon as well as top global locations.
Also supports custom city addition.
"""

LOCATIONS_DATA = {
    "India": {
        "Maharashtra": [
            "Jalgaon",
            "Mumbai",
            "Pune",
            "Nagpur",
            "Nashik",
            "Chhatrapati Sambhajinagar (Aurangabad)",
            "Thane",
            "Solapur",
            "Kolhapur",
            "Amravati",
            "Nanded",
            "Dhule",
            "Bhusawal",
            "Ahmednagar",
            "Chandrapur",
            "Sangli",
            "Satara",
            "Akola",
            "Latur",
        ],
        "Gujarat": [
            "Ahmedabad",
            "Surat",
            "Vadodara",
            "Rajkot",
            "Bhavnagar",
            "Jamnagar",
            "Gandhinagar",
            "Anand",
            "Vapi",
        ],
        "Karnataka": [
            "Bengaluru",
            "Mysuru",
            "Hubballi-Dharwad",
            "Mangaluru",
            "Belagavi",
            "Kalaburagi",
            "Shivamogga",
        ],
        "Delhi (NCR)": [
            "New Delhi",
            "Central Delhi",
            "South Delhi",
            "Gurugram",
            "Noida",
            "Faridabad",
            "Ghaziabad",
        ],
        "Tamil Nadu": [
            "Chennai",
            "Coimbatore",
            "Madurai",
            "Tiruchirappalli",
            "Salem",
            "Tiruppur",
            "Erode",
        ],
        "Telangana": [
            "Hyderabad",
            "Warangal",
            "Nizamabad",
            "Karimnagar",
            "Khammam",
        ],
        "Rajasthan": [
            "Jaipur",
            "Jodhpur",
            "Udaipur",
            "Kota",
            "Bikaner",
            "Ajmer",
            "Bhilwara",
        ],
        "Madhya Pradesh": [
            "Indore",
            "Bhopal",
            "Jabalpur",
            "Gwalior",
            "Ujjain",
        ],
        "Uttar Pradesh": [
            "Lucknow",
            "Kanpur",
            "Varanasi",
            "Agra",
            "Prayagraj",
            "Meerut",
            "Bareilly",
        ],
        "West Bengal": [
            "Kolkata",
            "Howrah",
            "Durgapur",
            "Asansol",
            "Siliguri",
        ],
        "Punjab": [
            "Ludhiana",
            "Amritsar",
            "Jalandhar",
            "Patiala",
            "Mohali",
        ],
    },
    "United States": {
        "California": [
            "Los Angeles",
            "San Francisco",
            "San Diego",
            "San Jose",
            "Sacramento",
            "Fresno",
            "Oakland",
            "Irvine",
        ],
        "Texas": [
            "Houston",
            "Dallas",
            "Austin",
            "San Antonio",
            "Fort Worth",
            "El Paso",
            "Arlington",
        ],
        "New York": [
            "New York City",
            "Buffalo",
            "Rochester",
            "Albany",
            "Syracuse",
        ],
        "Florida": [
            "Miami",
            "Orlando",
            "Tampa",
            "Jacksonville",
            "Fort Lauderdale",
        ],
        "Illinois": [
            "Chicago",
            "Naperville",
            "Aurora",
            "Rockford",
            "Joliet",
        ],
        "Washington": [
            "Seattle",
            "Bellevue",
            "Spokane",
            "Tacoma",
            "Vancouver",
        ],
    },
    "United Kingdom": {
        "England": [
            "London",
            "Manchester",
            "Birmingham",
            "Leeds",
            "Liverpool",
            "Bristol",
            "Sheffield",
            "Newcastle",
        ],
        "Scotland": [
            "Edinburgh",
            "Glasgow",
            "Aberdeen",
            "Dundee",
        ],
        "Wales": [
            "Cardiff",
            "Swansea",
            "Newport",
        ],
    },
    "United Arab Emirates": {
        "Dubai": ["Dubai City", "Deira", "Bur Dubai", "Jumeirah", "Business Bay"],
        "Abu Dhabi": ["Abu Dhabi City", "Al Ain", "Al Dhafra"],
        "Sharjah": ["Sharjah City", "Al Majaz", "Industrial Area"],
        "Ajman": ["Ajman City"],
    },
    "Canada": {
        "Ontario": ["Toronto", "Ottawa", "Mississauga", "Brampton", "Hamilton", "Markham"],
        "British Columbia": ["Vancouver", "Surrey", "Burnaby", "Richmond", "Victoria"],
        "Quebec": ["Montreal", "Quebec City", "Laval", "Gatineau"],
        "Alberta": ["Calgary", "Edmonton", "Red Deer"],
    },
    "Australia": {
        "New South Wales": ["Sydney", "Newcastle", "Central Coast", "Wollongong"],
        "Victoria": ["Melbourne", "Geelong", "Ballarat", "Bendigo"],
        "Queensland": ["Brisbane", "Gold Coast", "Sunshine Coast", "Cairns"],
        "Western Australia": ["Perth", "Fremantle"],
    },
    "Germany": {
        "Bavaria": ["Munich", "Nuremberg", "Augsburg", "Regensburg"],
        "Berlin": ["Berlin"],
        "North Rhine-Westphalia": ["Cologne", "Dusseldorf", "Dortmund", "Essen"],
        "Hesse": ["Frankfurt", "Wiesbaden", "Kassel"],
    },
    "Singapore": {
        "Singapore": ["Central", "Jurong East", "Tampines", "Woodlands", "Toa Payoh"]
    },
}

SERVICE_CATALOG = {
    "Website Development": {
        "description": "Businesses that lack modern websites, have broken/unresponsive sites, or need e-commerce/redesign.",
        "pitch_template": "Notice your business has great customer ratings in {city}, but your online web presence is missing/outdated. We build high-converting mobile websites to bring you 3x more direct customers.",
        "target_industries": [
            "Retail & Showrooms",
            "Doctors, Clinics & Hospitals",
            "Restaurants, Cafes & Hotels",
            "Schools, Colleges & Academies",
            "Real Estate & Builders",
            "Chartered Accountants & Legal Advisors",
            "Fitness Centers & Gyms",
            "Automobile Dealers & Garages",
        ],
    },
    "ERP Software": {
        "description": "Enterprises, manufacturers, distributors, and warehouses needing billing, stock, inventory, supply chain, and order management ERPs.",
        "pitch_template": "We implement automated ERP solutions for {industry} in {city} to streamline multi-warehouse inventory, GST billing, production batch tracking, and sales analytics in one single dashboard.",
        "target_industries": [
            "Manufacturing & Industrial Units (MIDC)",
            "Wholesale Distributors & Stockists",
            "Pipe, Plastic & Polymer Industries",
            "Agro Processing & Seed Mills",
            "Textile & Garment Manufacturers",
            "Chemical & Fertilizer Suppliers",
            "Logistics, Freight & Transport Agencies",
            "Construction & Raw Material Suppliers",
            "Pharmaceutical Distributors",
        ],
    },
    "Custom Software Development": {
        "description": "Companies requiring tailor-made web/mobile applications, CRM systems, booking portals, or specialized workflow automation.",
        "pitch_template": "We engineer custom software applications tailored to replace manual spreadsheet processes, automate customer bookings/invoicing, and connect with your team's WhatsApp/SMS workflows.",
        "target_industries": [
            "Diagnostic & Pathology Labs",
            "Coaching Institutes & EdTech",
            "Credit Societies & Micro-finance",
            "Hospital & Patient Management",
            "Courier & Fleet Tracking",
            "Event Management & Banquets",
            "Security & Manpower Agencies",
            "B2B Wholesale Portals",
        ],
    },
}


def get_countries():
    return sorted(list(LOCATIONS_DATA.keys()))


def get_states(country: str):
    return sorted(list(LOCATIONS_DATA.get(country, {}).keys()))


def get_cities(country: str, state: str):
    return LOCATIONS_DATA.get(country, {}).get(state, [])
