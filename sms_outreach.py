#!/usr/bin/env python3
"""
Interactive SMS outreach script — sends one at a time with confirmation.
Uses Quo (formerly OpenPhone) API to text all 51 Utah contractor companies
about their free website.

Setup:
  1. Copy .env.example → .env and fill in your Quo API key & phone number ID
  2. Get your API key from Quo workspace settings → API
  3. Get your phone number ID by running: python3 sms_outreach.py --list-numbers
  4. Run: python3 sms_outreach.py
  5. Approve or skip each message before it sends
  6. Results are logged to leads.csv automatically
"""

import os, csv, re, time, sys, json
from datetime import date
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from dotenv import load_dotenv

load_dotenv()

# ── Config ───────────────────────────────────────────────────────────────────
QUO_API_KEY      = os.getenv("QUO_API_KEY")
QUO_PHONE_NUMBER_ID = os.getenv("QUO_PHONE_NUMBER_ID")
LEADS_CSV        = os.path.join(os.path.dirname(__file__), "leads.csv")
LIVE_DOMAIN      = "https://roofers-ai.netlify.app"

QUO_API_BASE     = "https://api.openphone.com/v1"

SENDER_NAME      = "Derek Lee"

# ── Company data with SMS templates ──────────────────────────────────────────
COMPANIES = [
    {"name": "LH Custom Contracting LLC",                    "type": "Bathroom remodeler",          "phone": "+14352291535"},
    {"name": "Desert Plumbing Corporation",                  "type": "Plumber",                      "phone": "+14356681430"},
    {"name": "Digital Marble and Granite",                   "type": "Marble contractor",            "phone": "+14356808050"},
    {"name": "Magicman Handyman LLC",                        "type": "Handyman",                     "phone": "+14356353095"},
    {"name": "Wasatch Mountain Electrical Services",         "type": "Electrician",                  "phone": "+13852065462"},
    {"name": "Shalom Electrical Services",                   "type": "Electrical installation service","phone": "+12014247624"},
    {"name": "PoPo's Remodeling",                            "type": "Handyman",                     "phone": "+18012003404"},
    {"name": "Eagle Valley Design",                          "type": "Cabinet maker",                "phone": "+18018548762"},
    {"name": "RCI Drywall",                                  "type": "Drywall contractor",           "phone": "+18014207905"},
    {"name": "Kstone & Tile",                                "type": "Tile contractor",              "phone": "+18014272745"},
    {"name": "Caron Electric LLC",                           "type": "Electrician",                  "phone": "+14357904457"},
    {"name": "Bright Electric LLC",                          "type": "Electrician",                  "phone": "+14355921315"},
    {"name": "Heber City Utah Kitchen Remodeling",           "type": "Kitchen remodeler",            "phone": "+14352363299"},
    {"name": "C J Electrical",                               "type": "Electrician",                  "phone": "+14357871865"},
    {"name": "Lowery Electric",                              "type": "Electrician",                  "phone": "+14357530343"},
    {"name": "DREAM KITCHEN and COUNTERTOP INC",             "type": "Cabinet maker",                "phone": "+18018099199"},
    {"name": "Intermountain Kitchen and Bath Design",        "type": "Kitchen remodeler",            "phone": "+18015480160"},
    {"name": "Joshua & Sons Electricians Company",           "type": "Electrician",                  "phone": "+13853484906"},
    {"name": "Ramirez Brothers Electricians",                "type": "Electrician",                  "phone": "+13853304243"},
    {"name": "First Choice Home Electrician Salt Lake City", "type": "Electrician",                  "phone": "+18016574857"},
    {"name": "Utah Electric Co",                             "type": "Electrician",                  "phone": "+18019988527"},
    {"name": "Electrician Salt Lake City",                   "type": "Electrician",                  "phone": "+18015163723"},
    {"name": "Falcon Electric LLC",                          "type": "Electrician",                  "phone": "+18014860185"},
    {"name": "Any Electrical Co",                            "type": "Electrician",                  "phone": "+18018882772"},
    {"name": "Velmex USA Electrical & Mechanical Repair",   "type": "Auto repair shop",             "phone": "+13852599079"},
    {"name": "Cedar City Electric Contractors",              "type": "Electrician",                  "phone": "+14355920063"},
    {"name": "Elkhorn Construction",                         "type": "General contractor",           "phone": "+18016906860"},
    {"name": "Crimson Rock Construction",                    "type": "General contractor",           "phone": "+18018598764"},
    {"name": "Ram Construction",                             "type": "General contractor",           "phone": "+18012982262"},
    {"name": "Affordable Drywall Repair Salt Lake City",     "type": "Drywall contractor",           "phone": "+18018014090"},
    {"name": "Salt Lake City Service",                       "type": "Water damage restoration",     "phone": "+13854801052"},
    {"name": "Viana's Services",                             "type": "Handyman",                     "phone": "+18012310571"},
    {"name": "Simmons Construction & Contracting",           "type": "General contractor",           "phone": "+14353139146"},
    {"name": "Davis & Sons Electrical",                      "type": "Electrician",                  "phone": "+18019351221"},
    {"name": "Edmonds Handyman Services",                    "type": "Handyman",                     "phone": "+17076013080"},
    {"name": "Next Level Refinishing",                       "type": "Bathroom remodeler",           "phone": "+18016334814"},
    {"name": "Safeway Electric",                             "type": "Electrician",                  "phone": "+13856006109"},
    {"name": "Electrical Consulting Engineers LLC",          "type": "Electrical installation service","phone": "+18015218007"},
    {"name": "Trejos Mobile Mechanic",                       "type": "Auto repair shop",             "phone": "+17023723901"},
    {"name": "Mortenson Electric Inc",                       "type": "Electrician",                  "phone": "+14357576500"},
    {"name": "Stateline Electric",                           "type": "Electrician",                  "phone": "+14352797626"},
    {"name": "Custom Built Woodworks LLC",                   "type": "Contractor",                   "phone": "+18013889583"},
    {"name": "Gary Tolman Construction",                     "type": "Home builder",                 "phone": "+18017764668"},
    {"name": "Bell-Built Homes",                             "type": "Home builder",                 "phone": "+18014581685"},
    {"name": "Handyman Direct LLC",                          "type": "Handyman",                     "phone": "+18017593773"},
    {"name": "West Coast Refinishing Tub LLC",               "type": "Bathroom remodeler",           "phone": "+18012435569"},
    {"name": "KV Construction",                              "type": "General contractor",           "phone": "+14356800664"},
    {"name": "TILEDGE",                                      "type": "Tile contractor",              "phone": "+14352820543"},
    {"name": "Infinite Tile And Stone",                      "type": "Tile contractor",              "phone": "+14353758452"},
    {"name": "Salt Creek Builders LLC",                      "type": "Kitchen remodeler",            "phone": "+18016415300"},
    {"name": "Color Country Electric",                       "type": "Electrician",                  "phone": "+14356808898"},
]

# ── SMS templates by type ─────────────────────────────────────────────────────
SMS_TEMPLATES = {
    "Electrician":                  "Hi! I'm {sender}, a local web designer building my 2026 portfolio. I picked {name} as a project and already built you a free website: {url}. Can I text you more details? No strings attached.",
    "Plumber":                      "Hey! I'm {sender}, a web designer in Utah. I'm building my 2026 portfolio and built a free website for {name}: {url}. Would love to walk you through it — no catch at all.",
    "Handyman":                     "Hi! I'm {sender} — building my 2026 portfolio and put together a free website for {name}: {url}. No catch — take a look and let me know what you think!",
    "General contractor":           "Hi! I'm {sender}, a web designer in Utah building my 2026 portfolio. I put together a free website for {name}: {url}. Would love to get your thoughts — no obligation.",
    "Kitchen remodeler":            "Hey! I'm {sender}. Building my 2026 portfolio and picked {name} as a project — already built you a free website: {url}. Homeowners research kitchens online for weeks. Want to chat about it?",
    "Bathroom remodeler":           "Hi! I'm {sender}. Building my 2026 portfolio and created a free site for {name}: {url}. Homeowners google remodelers before calling — this site puts your best foot forward. Take a look!",
    "Tile contractor":              "Hey! I'm {sender}. Building my 2026 portfolio and built a free website for {name}: {url}. Tile work is visual — a great site brings in more calls. Check it out!",
    "Cabinet maker":                "Hi! I'm {sender}. Building my 2026 portfolio and created a free site for {name}: {url}. Custom cabinets deserve a premium website — want to take a look?",
    "Drywall contractor":           "Hey! I'm {sender}. Building my 2026 portfolio and put together a free site for {name}: {url}. Want more drywall leads from Google? Take a look!",
    "Home builder":                 "Hi! I'm {sender}. Building my 2026 portfolio and picked {name} as a project — already built you a free website: {url}. Home buyers research heavily online. Want to see it?",
    "Water damage restoration":     "Hi! I'm {sender}. Building my 2026 portfolio and created a free site for {name}: {url}. Restoration leads go to whoever shows up first online — take a look!",
    "Auto repair shop":             "Hey! I'm {sender}. Building my 2026 portfolio and put together a free site for {name}: {url}. Customers Google mechanics before calling — check it out!",
    "Marble contractor":            "Hi! I'm {sender}. Building my 2026 portfolio and built a free site for {name}: {url}. Premium stone deserves a premium website — want to take a look?",
    "Electrical installation service": "Hi! I'm {sender}. Building my 2026 portfolio and created a free site for {name}: {url}. Commercial clients check websites before reaching out. Take a look!",
    "Contractor":                   "Hi! I'm {sender}. Building my 2026 portfolio and put together a free website for {name}: {url}. No catch — would love your thoughts!",
}

def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def get_sms(company):
    tmpl = SMS_TEMPLATES.get(company["type"], SMS_TEMPLATES["Contractor"])
    slug = slugify(company["name"])
    return tmpl.format(
        sender=SENDER_NAME,
        name=company["name"],
        url=f"{LIVE_DOMAIN}/companies/{slug}.html",
    )

# ── Quo API helpers ──────────────────────────────────────────────────────────
def quo_request(method, endpoint, body=None):
    """Make a request to the Quo (OpenPhone) API."""
    url = f"{QUO_API_BASE}{endpoint}"
    data = json.dumps(body).encode() if body else None
    req = Request(url, data=data, method=method)
    req.add_header("Authorization", QUO_API_KEY)
    req.add_header("Content-Type", "application/json")
    resp = urlopen(req)
    return json.loads(resp.read().decode())

def list_phone_numbers():
    """List all phone numbers in the Quo workspace."""
    result = quo_request("GET", "/phone-numbers")
    numbers = result.get("data", [])
    if not numbers:
        print("\n❌  No phone numbers found in your Quo workspace.\n")
        return
    print(f"\n{'─'*60}")
    print("  📱  Your Quo Phone Numbers")
    print(f"{'─'*60}")
    for num in numbers:
        print(f"  ID:     {num['id']}")
        print(f"  Number: {num.get('formattedNumber', num.get('number', 'N/A'))}")
        print(f"  Name:   {num.get('name', 'N/A')}")
        print(f"  Type:   {num.get('type', 'N/A')}")
        print()
    print("  Copy the ID of your business number into .env as QUO_PHONE_NUMBER_ID")
    print(f"{'─'*60}\n")

def send_sms(to_number, message):
    """Send an SMS via the Quo API. Returns the message ID on success."""
    body = {
        "content": message,
        "from": QUO_PHONE_NUMBER_ID,
        "to": [to_number],
    }
    result = quo_request("POST", "/messages", body)
    return result.get("data", {}).get("id", "sent")

# ── CSV tracking ─────────────────────────────────────────────────────────────
def load_sent():
    """Return set of company names already marked SMS Sent = Yes in leads.csv."""
    sent = set()
    if not os.path.exists(LEADS_CSV):
        return sent
    with open(LEADS_CSV, newline="") as f:
        for row in csv.DictReader(f):
            if row.get("SMS Sent", "").strip().lower() == "yes":
                sent.add(row["Company Name"])
    return sent

def update_csv(company_name, status, notes=""):
    """Update the leads.csv row for a company after sending."""
    if not os.path.exists(LEADS_CSV):
        return
    rows = []
    with open(LEADS_CSV, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["Company Name"] == company_name:
                row["SMS Sent"] = "Yes" if status == "sent" else "No"
                row["Status"] = "Contacted" if status == "sent" else row["Status"]
                row["Date Contacted"] = str(date.today()) if status == "sent" else row["Date Contacted"]
                if notes:
                    row["Response Notes"] = notes
            rows.append(row)
    with open(LEADS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def check_env():
    if not QUO_API_KEY:
        print("\n❌  Missing QUO_API_KEY in .env")
        print("    Get your API key from Quo workspace settings → API")
        print("    Then add it to .env\n")
        sys.exit(1)
    if not QUO_PHONE_NUMBER_ID:
        print("\n❌  Missing QUO_PHONE_NUMBER_ID in .env")
        print("    Run: python3 sms_outreach.py --list-numbers")
        print("    Then copy your business number ID into .env\n")
        sys.exit(1)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    # Allow listing phone numbers without full env check
    if "--list-numbers" in sys.argv:
        if not QUO_API_KEY:
            print("\n❌  Set QUO_API_KEY in .env first, then re-run.\n")
            sys.exit(1)
        list_phone_numbers()
        return

    check_env()
    already_sent = load_sent()

    pending = [c for c in COMPANIES if c["name"] not in already_sent]

    if not pending:
        print("\n✅  All companies have already been texted. Check leads.csv for responses.\n")
        return

    print(f"\n{'─'*60}")
    print(f"  📱  SMS Outreach via Quo — {len(pending)} companies remaining")
    print(f"  From: {QUO_PHONE_NUMBER_ID}  |  Sender: {SENDER_NAME}")
    print(f"  Site: {LIVE_DOMAIN}")
    print(f"{'─'*60}")
    print("  Commands:  [Enter] = Send   [s] = Skip   [q] = Quit\n")

    sent_count = 0
    skip_count = 0

    for i, company in enumerate(pending, 1):
        msg = get_sms(company)
        print(f"[{i}/{len(pending)}] {company['name']}")
        print(f"  To:   {company['phone']}")
        print(f"  Type: {company['type']}")
        print(f"  Msg:  {msg}")
        print()

        while True:
            try:
                choice = input("  → Send? [Enter=yes / s=skip / q=quit]: ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print("\n\nInterrupted. Progress saved to leads.csv.")
                sys.exit(0)

            if choice == "q":
                print(f"\nDone. Sent: {sent_count}  Skipped: {skip_count}")
                sys.exit(0)
            elif choice == "s":
                skip_count += 1
                print(f"  ⏭  Skipped\n")
                break
            elif choice == "":
                try:
                    msg_id = send_sms(company["phone"], msg)
                    update_csv(company["name"], "sent")
                    sent_count += 1
                    print(f"  ✅  Sent! Message ID: {msg_id}\n")
                    time.sleep(1)  # 1s pause between sends
                except HTTPError as e:
                    error_body = e.read().decode() if e.fp else str(e)
                    update_csv(company["name"], "error", error_body)
                    print(f"  ❌  Failed: {e.code} — {error_body}\n")
                break

    print(f"\n{'─'*60}")
    print(f"  Done!  ✅ Sent: {sent_count}   ⏭ Skipped: {skip_count}")
    print(f"  leads.csv updated with today's date and SMS status.")
    print(f"{'─'*60}\n")

if __name__ == "__main__":
    main()
