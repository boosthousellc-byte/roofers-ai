#!/usr/bin/env python3
"""
Interactive SMS outreach script — sends one at a time with confirmation.
Uses Twilio to text all 51 Utah contractor companies about their free website.

Setup:
  1. Copy .env.example → .env and fill in your Twilio credentials
  2. Run: python3 sms_outreach.py
  3. Approve or skip each message before it sends
  4. Results are logged to leads.csv automatically
"""

import os, csv, re, time, sys
from datetime import date
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

load_dotenv()

# ── Config ───────────────────────────────────────────────────────────────────
ACCOUNT_SID  = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN   = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER  = os.getenv("TWILIO_FROM_NUMBER")
LEADS_CSV    = os.path.join(os.path.dirname(__file__), "leads.csv")
LIVE_DOMAIN  = "https://roofers-ai.netlify.app"

SENDER_NAME  = "Derek Lee"

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
    "Electrician":                  "Hi! I'm {sender}, a local web designer. I built a free website for {name} — no catch. Check it out: {url}. Would love to get you more calls from Google. Interested?",
    "Plumber":                      "Hey! I'm {sender}, a local web designer. Built a free website for {name}: {url}. Plumbers with great sites get way more leads. Want to take it live?",
    "Handyman":                     "Hi! I'm {sender} — built a free website for {name}: {url}. No catch — would you want this for your business?",
    "General contractor":           "Hi! I'm {sender}, a web designer in Utah. Built a free website for {name}: {url}. Want more leads from Google? Happy to chat.",
    "Kitchen remodeler":            "Hey! I'm {sender}. Built a free website for {name} — {url}. Kitchen remodelers with great sites get way more leads. Want to chat about it?",
    "Bathroom remodeler":           "Hi! I'm {sender}. Built a free site for {name}: {url}. Homeowners google remodelers before calling — want to put your best foot forward?",
    "Tile contractor":              "Hey! I'm {sender}. Built a free website for {name}: {url}. Tile work is visual — a great site brings in more calls. Want to check it out?",
    "Cabinet maker":                "Hi! I'm {sender}. Built a free site for {name}: {url}. Custom cabinets deserve a premium website — want to take a look?",
    "Drywall contractor":           "Hey! I'm {sender}. Built a free site for {name}: {url}. Want more drywall leads from Google? Let me know!",
    "Home builder":                 "Hi! I'm {sender}. Built a free website for {name}: {url}. Home buyers research heavily online — want your site to make the right impression?",
    "Water damage restoration":     "Hi! I'm {sender}. Built a free site for {name}: {url}. Restoration leads go to whoever shows up first online — want to be that company?",
    "Auto repair shop":             "Hey! I'm {sender}. Built a free site for {name}: {url}. Customers Google mechanics before calling — want more of those calls?",
    "Marble contractor":            "Hi! I'm {sender}. Built a free site for {name}: {url}. Premium stone deserves a premium website — want to take a look?",
    "Electrical installation service": "Hi! I'm {sender}. Built a free site for {name}: {url}. Want more commercial and residential installation leads? Let's chat!",
    "Contractor":                   "Hi! I'm {sender}. Built a free website for {name}: {url}. Want more leads? Happy to chat.",
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
    missing = [k for k in ("TWILIO_ACCOUNT_SID","TWILIO_AUTH_TOKEN","TWILIO_FROM_NUMBER") if not os.getenv(k)]
    if missing:
        print("\n❌  Missing environment variables:", ", ".join(missing))
        print("    Copy .env.example → .env and fill in your Twilio credentials.\n")
        sys.exit(1)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    check_env()
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    already_sent = load_sent()

    pending = [c for c in COMPANIES if c["name"] not in already_sent]

    if not pending:
        print("\n✅  All companies have already been texted. Check leads.csv for responses.\n")
        return

    print(f"\n{'─'*60}")
    print(f"  📱  SMS Outreach — {len(pending)} companies remaining")
    print(f"  From: {FROM_NUMBER}  |  Sender: {SENDER_NAME}")
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
                    message = client.messages.create(
                        body=msg,
                        from_=FROM_NUMBER,
                        to=company["phone"],
                    )
                    update_csv(company["name"], "sent")
                    sent_count += 1
                    print(f"  ✅  Sent! SID: {message.sid}\n")
                    time.sleep(1)  # 1s pause between sends to stay within rate limits
                except TwilioRestException as e:
                    update_csv(company["name"], "error", str(e))
                    print(f"  ❌  Failed: {e}\n")
                break

    print(f"\n{'─'*60}")
    print(f"  Done!  ✅ Sent: {sent_count}   ⏭ Skipped: {skip_count}")
    print(f"  leads.csv updated with today's date and SMS status.")
    print(f"{'─'*60}\n")

if __name__ == "__main__":
    main()
