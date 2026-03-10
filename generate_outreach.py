#!/usr/bin/env python3
"""Generate outreach templates page and leads CSV."""
import os, re, csv

COMPANIES = [
    {"name": "LH Custom Contracting LLC", "type": "Bathroom remodeler", "phone": "+1 435-229-1535", "city": "Utah"},
    {"name": "Desert Plumbing Corporation", "type": "Plumber", "phone": "+1 435-668-1430", "city": "Utah"},
    {"name": "Digital Marble and Granite", "type": "Marble contractor", "phone": "+1 435-680-8050", "city": "Utah"},
    {"name": "Magicman Handyman LLC", "type": "Handyman", "phone": "+1 435-635-3095", "city": "Utah"},
    {"name": "Wasatch Mountain Electrical Services", "type": "Electrician", "phone": "+1 385-206-5462", "city": "Utah"},
    {"name": "Shalom Electrical Services", "type": "Electrical installation service", "phone": "+1 201-424-7624", "city": "Utah"},
    {"name": "PoPo's Remodeling", "type": "Handyman", "phone": "+1 801-200-3404", "city": "Utah"},
    {"name": "Eagle Valley Design", "type": "Cabinet maker", "phone": "+1 801-854-8762", "city": "Utah"},
    {"name": "RCI Drywall", "type": "Drywall contractor", "phone": "+1 801-420-7905", "city": "Utah"},
    {"name": "Kstone & Tile", "type": "Tile contractor", "phone": "+1 801-427-2745", "city": "Utah"},
    {"name": "Caron Electric LLC", "type": "Electrician", "phone": "+1 435-790-4457", "city": "Utah"},
    {"name": "Bright Electric LLC", "type": "Electrician", "phone": "+1 435-592-1315", "city": "Utah"},
    {"name": "Heber City Utah Kitchen Remodeling", "type": "Kitchen remodeler", "phone": "+1 435-236-3299", "city": "Heber City, UT"},
    {"name": "C J Electrical", "type": "Electrician", "phone": "+1 435-787-1865", "city": "Utah"},
    {"name": "Lowery Electric", "type": "Electrician", "phone": "+1 435-753-0343", "city": "Utah"},
    {"name": "DREAM KITCHEN and COUNTERTOP INC", "type": "Cabinet maker", "phone": "+1 801-809-9199", "city": "Utah"},
    {"name": "Intermountain Kitchen and Bath Design", "type": "Kitchen remodeler", "phone": "+1 801-548-0160", "city": "Utah"},
    {"name": "Joshua & Sons Electricians Company", "type": "Electrician", "phone": "+1 385-348-4906", "city": "Utah"},
    {"name": "Ramirez Brothers Electricians", "type": "Electrician", "phone": "+1 385-330-4243", "city": "Utah"},
    {"name": "First Choice Home Electrician Salt Lake City", "type": "Electrician", "phone": "+1 801-657-4857", "city": "Salt Lake City, UT"},
    {"name": "Utah Electric Co", "type": "Electrician", "phone": "+1 801-998-8527", "city": "Utah"},
    {"name": "Electrician Salt Lake City", "type": "Electrician", "phone": "+1 801-516-3723", "city": "Salt Lake City, UT"},
    {"name": "Falcon Electric LLC", "type": "Electrician", "phone": "+1 801-486-0185", "city": "Utah"},
    {"name": "Any Electrical Co", "type": "Electrician", "phone": "+1 801-888-2772", "city": "Utah"},
    {"name": "Velmex USA Electrical & Mechanical Repair", "type": "Auto repair shop", "phone": "+1 385-259-9079", "city": "Utah"},
    {"name": "Cedar City Electric Contractors", "type": "Electrician", "phone": "+1 435-592-0063", "city": "Cedar City, UT"},
    {"name": "Elkhorn Construction", "type": "General contractor", "phone": "+1 801-690-6860", "city": "Utah"},
    {"name": "Crimson Rock Construction", "type": "General contractor", "phone": "+1 801-859-8764", "city": "Utah"},
    {"name": "Ram Construction", "type": "General contractor", "phone": "+1 801-298-2262", "city": "Utah"},
    {"name": "Affordable Drywall Repair Salt Lake City", "type": "Drywall contractor", "phone": "+1 801-801-4090", "city": "Salt Lake City, UT"},
    {"name": "Salt Lake City Service", "type": "Water damage restoration", "phone": "+1 385-480-1052", "city": "Salt Lake City, UT"},
    {"name": "Viana's Services", "type": "Handyman", "phone": "+1 801-231-0571", "city": "Utah"},
    {"name": "Simmons Construction & Contracting", "type": "General contractor", "phone": "+1 435-313-9146", "city": "Utah"},
    {"name": "Davis & Sons Electrical", "type": "Electrician", "phone": "+1 801-935-1221", "city": "Utah"},
    {"name": "Edmonds Handyman Services", "type": "Handyman", "phone": "+1 707-601-3080", "city": "Utah"},
    {"name": "Next Level Refinishing", "type": "Bathroom remodeler", "phone": "+1 801-633-4814", "city": "Utah"},
    {"name": "Safeway Electric", "type": "Electrician", "phone": "+1 385-600-6109", "city": "Utah"},
    {"name": "Electrical Consulting Engineers LLC", "type": "Electrical installation service", "phone": "+1 801-521-8007", "city": "Utah"},
    {"name": "Trejos Mobile Mechanic", "type": "Auto repair shop", "phone": "+1 702-372-3901", "city": "Utah"},
    {"name": "Mortenson Electric Inc", "type": "Electrician", "phone": "+1 435-757-6500", "city": "Utah"},
    {"name": "Stateline Electric", "type": "Electrician", "phone": "+1 435-279-7626", "city": "Utah"},
    {"name": "Custom Built Woodworks LLC", "type": "Contractor", "phone": "+1 801-388-9583", "city": "Utah"},
    {"name": "Gary Tolman Construction", "type": "Home builder", "phone": "+1 801-776-4668", "city": "Utah"},
    {"name": "Bell-Built Homes", "type": "Home builder", "phone": "+1 801-458-1685", "city": "Utah"},
    {"name": "Handyman Direct LLC", "type": "Handyman", "phone": "+1 801-759-3773", "city": "Utah"},
    {"name": "West Coast Refinishing Tub LLC", "type": "Bathroom remodeler", "phone": "+1 801-243-5569", "city": "Utah"},
    {"name": "KV Construction", "type": "General contractor", "phone": "+1 435-680-0664", "city": "Utah"},
    {"name": "TILEDGE", "type": "Tile contractor", "phone": "+1 435-282-0543", "city": "Utah"},
    {"name": "Infinite Tile And Stone", "type": "Tile contractor", "phone": "+1 435-375-8452", "city": "Utah"},
    {"name": "Salt Creek Builders LLC", "type": "Kitchen remodeler", "phone": "+1 801-641-5300", "city": "Utah"},
    {"name": "Color Country Electric", "type": "Electrician", "phone": "+1 435-680-8898", "city": "Utah"},
]

def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

# ── Email & SMS templates by business type ──────────────────────────────────
TEMPLATES = {
    "Electrician": {
        "subject": "Free Website We Built for {name} — No Strings Attached",
        "email": """Hi there,

My name is [YOUR NAME] and I'm a local web designer based in Utah.

I was researching electricians in the area and came across {name}. I went ahead and built a professional website sample for you — completely free — to show you what your online presence could look like.

You can see it here: [YOUR DOMAIN]/companies/{slug}

The site includes:
• A professional homepage with your services and phone number
• Licensed & insured trust signals customers look for
• Customer testimonial section
• Service area coverage map
• Mobile-friendly design

A lot of homeowners Google electricians before calling — a strong website means more calls, more jobs.

If you'd like to claim it, customize it, or just take a look, I'd love to connect. No obligation at all.

Best,
[YOUR NAME]
[YOUR PHONE]
[YOUR EMAIL]""",
        "sms": """Hi! I'm [NAME], a local web designer. I built a free website sample for {name} — no catch. You can see it at [YOUR DOMAIN]/companies/{slug}. Want me to send it over? Happy to chat about it.""",
        "call_script": """Hi, is this the owner of {name}?

Great — my name is [YOUR NAME], I'm a web designer based here in Utah. I actually built a free website sample for {name} — no charge, no obligation. I was researching local electricians and wanted to show you what a professional website could look like for your business.

I can text you the link right now so you can take a look. Is that okay?

[If yes] → Perfect, sending it now. The site has your services, phone number, and trust signals like your license info. If you like it and want to take it live, we can talk about that — but totally no pressure.

[If hesitant] → Totally understand. It takes 10 seconds to look at. I'll text you the link and you can check it out whenever. Sound good?"""
    },
    "Plumber": {
        "subject": "Built a Free Website for {name} — Take a Look",
        "email": """Hi,

I'm [YOUR NAME], a web designer in Utah. I put together a free website sample for {name} and wanted to share it with you.

Preview it here: [YOUR DOMAIN]/companies/{slug}

Most homeowners search Google before calling a plumber. A clean, professional website means you show up and win the call. The sample I built includes your services, a click-to-call button, testimonials, and service areas.

No cost, no obligation. If you want to make it yours, I'd love to chat.

[YOUR NAME]
[YOUR PHONE]""",
        "sms": """Hey! I'm [NAME], a local web designer. I built a free website sample for {name} — check it out: [YOUR DOMAIN]/companies/{slug}. Would you want to take it live?""",
        "call_script": """Hi, is this the owner of {name}?

I'm [YOUR NAME] — I'm a web designer here in Utah. Quick question: do you currently have a website for {name}?

[If no/weak] → That's actually why I'm calling. I went ahead and built a free website sample for you — completely free, no obligation. I can text you the link right now. It's got your services, phone number, and a professional design. Want to take a look?

[If yes] → Got it! I still built a sample that might be worth comparing. I can text it over — just takes a second to look at. No pressure at all."""
    },
    "Handyman": {
        "subject": "Free Website for {name} — I Built It Already",
        "email": """Hey there,

I'm [YOUR NAME], a web designer in Utah who works with local contractors.

I built a free website sample for {name} — you can see it here:
[YOUR DOMAIN]/companies/{slug}

Most people find handymen through Google, word of mouth, or Facebook — but a professional website converts those searchers into paying customers. The sample shows your services, builds trust, and makes it easy to call you.

If you're interested in taking it live, I'd love to connect. If not, no hard feelings — just wanted to share it.

[YOUR NAME]
[YOUR PHONE]""",
        "sms": """Hi! I'm [NAME] — built a free website for {name}. See it here: [YOUR DOMAIN]/companies/{slug}. No catch — would you want this for your business?""",
        "call_script": """Hi, is this {name}?

I'm [YOUR NAME], a web designer in Utah. I built a free professional website for your business — no charge. A lot of handymen miss out on leads because customers can't find them online. I wanted to show you what it could look like.

Can I text you the link real quick?"""
    },
    "General contractor": {
        "subject": "{name} — Your Free Website Sample Is Ready",
        "email": """Hi,

My name is [YOUR NAME]. I'm a web designer who specializes in working with contractors across Utah.

I put together a custom website sample for {name}:
[YOUR DOMAIN]/companies/{slug}

The site is built to help you win more bids — it showcases your services, builds credibility, and makes it simple for homeowners to reach you. It's mobile-friendly and includes trust signals like licensing, insurance, and reviews.

I'd love to get on a call and walk you through it. Completely free to look at.

[YOUR NAME]
[YOUR PHONE]""",
        "sms": """Hi! I'm [NAME], a web designer in Utah. I built a free website sample for {name}: [YOUR DOMAIN]/companies/{slug}. Would you be open to a quick chat about it?""",
        "call_script": """Hello, is this the owner of {name}?

This is [YOUR NAME] — I'm a local web designer. I built a free website sample specifically for {name}. Contractors with strong websites consistently win more bids because homeowners check them out before they ever pick up the phone.

Can I text you the link? It only takes a second to look at, and there's no obligation."""
    },
    "Kitchen remodeler": {
        "subject": "Free Website for {name} — See It Here",
        "email": """Hi there,

I'm [YOUR NAME], a web designer in Utah. Kitchen remodeling is a high-consideration purchase — homeowners spend weeks researching before calling anyone.

I built a free website sample for {name} to help you capture those searchers:
[YOUR DOMAIN]/companies/{slug}

It includes a portfolio-style layout, service descriptions, testimonials, and a strong call to action. The kind of site that turns Google searches into phone calls.

Happy to walk you through it — no cost, no commitment.

[YOUR NAME]
[YOUR PHONE]""",
        "sms": """Hey! Built a free website sample for {name} — [YOUR DOMAIN]/companies/{slug}. Kitchen remodelers with great websites get way more leads. Want to chat about it?""",
        "call_script": """Hi, is this the owner of {name}?

I'm [YOUR NAME], a web designer. I built a free website sample for you — kitchen remodeling is one of those services where homeowners do a lot of research online before calling. A great website makes you the obvious choice.

Can I text you the link? I'd love your feedback."""
    },
    "Bathroom remodeler": {
        "subject": "Built a Website for {name} — Free to View",
        "email": """Hi,

I'm [YOUR NAME], a web designer in Utah. I built a free website sample for {name}:
[YOUR DOMAIN]/companies/{slug}

Bathroom remodels are a significant investment — homeowners research heavily before choosing a contractor. The website I built positions {name} as the professional, trustworthy choice with before/after framing, services, and a strong CTA.

No strings attached. Would love to connect if you're interested.

[YOUR NAME]
[YOUR PHONE]""",
        "sms": """Hi! I'm [NAME]. Built a free site for {name}: [YOUR DOMAIN]/companies/{slug}. Homeowners google remodelers before calling — want to put your best foot forward?""",
        "call_script": """Hi, is this {name}?

I'm [YOUR NAME] — I'm a web designer and I built a free website sample for your business. Bathroom remodelers who have a professional site get way more leads from Google. I'd love to text you the link — no commitment."""
    },
    "Tile contractor": {
        "subject": "Free Website Built for {name}",
        "email": """Hi,

I'm [YOUR NAME], a web designer based in Utah.

I built a free website sample for {name}:
[YOUR DOMAIN]/companies/{slug}

Tile work is visual — homeowners want to see your style and expertise before calling. The site I built showcases your services, builds trust, and makes it easy to reach you.

No cost to view. Happy to customize it for you if you're interested.

[YOUR NAME]
[YOUR PHONE]""",
        "sms": """Hey! Built a free website for {name}: [YOUR DOMAIN]/companies/{slug}. Tile work is visual — a great site brings in more calls. Want to check it out?""",
        "call_script": """Hi, is this the owner of {name}?

I'm [YOUR NAME], a web designer. Tile work is very visual — homeowners love seeing examples of work and a professional site before calling. I built a free sample for you. Can I text you the link?"""
    },
    "Cabinet maker": {
        "subject": "Free Website Sample for {name}",
        "email": """Hi,

I'm [YOUR NAME], a web designer in Utah who loves working with craftsmen.

Custom cabinetry is a premium service — your website should reflect that. I built a free sample for {name}:
[YOUR DOMAIN]/companies/{slug}

It's designed to showcase craftsmanship, build trust, and convert visitors into leads. No cost, no obligation.

[YOUR NAME]
[YOUR PHONE]""",
        "sms": """Hi! Built a free site for {name}: [YOUR DOMAIN]/companies/{slug}. Custom cabinets deserve a premium website — want to take a look?""",
        "call_script": """Hi, is this {name}?

I'm [YOUR NAME] — I build websites for craftsmen and contractors. I put together a free website sample for your cabinet business. High-end woodwork deserves a site that shows it off. Can I text you the link?"""
    },
    "Drywall contractor": {
        "subject": "Free Website for {name} — Already Built It",
        "email": """Hi,

I'm [YOUR NAME], a web designer in Utah. I built a free website sample for {name}:
[YOUR DOMAIN]/companies/{slug}

Homeowners searching for drywall repair want to find someone they can trust quickly. The site I built makes {name} look professional and makes it easy to call.

No charge, no commitment. Let me know if you'd like to take it live.

[YOUR NAME]
[YOUR PHONE]""",
        "sms": """Hey! Built a free site for {name}: [YOUR DOMAIN]/companies/{slug}. Want more drywall leads from Google? Let me know!""",
        "call_script": """Hi, is this {name}?

I'm [YOUR NAME], a web designer. I built a free website for your drywall business — it's already done. Can I text you the link to take a look?"""
    },
    "Home builder": {
        "subject": "{name} — Your Free Website Sample Is Ready",
        "email": """Hi,

I'm [YOUR NAME], a web designer who works with home builders in Utah.

Custom home building is one of the biggest decisions a family makes — your website needs to inspire confidence. I built a free sample for {name}:
[YOUR DOMAIN]/companies/{slug}

It's designed to showcase your portfolio, communicate quality, and generate qualified leads. No cost to view.

[YOUR NAME]
[YOUR PHONE]""",
        "sms": """Hi! Built a free website for {name}: [YOUR DOMAIN]/companies/{slug}. Home buyers research heavily online — want your site to make the right impression?""",
        "call_script": """Hi, is this {name}?

I'm [YOUR NAME] — I specialize in websites for home builders. I built a free sample for your business that's designed to inspire trust in prospective buyers. Can I text you the link?"""
    },
    "Water damage restoration": {
        "subject": "Free Website for {name} — Built & Ready",
        "email": """Hi,

I'm [YOUR NAME], a web designer in Utah. Water damage restoration is an urgent, high-stakes service — homeowners call whoever they find first and trust most.

I built a free website for {name} to help you win those calls:
[YOUR DOMAIN]/companies/{slug}

It emphasizes 24/7 availability, fast response, and trust — exactly what stressed homeowners need to see. No cost to check it out.

[YOUR NAME]
[YOUR PHONE]""",
        "sms": """Hi! Built a free site for {name}: [YOUR DOMAIN]/companies/{slug}. Restoration leads go to whoever shows up first online — want to be that company?""",
        "call_script": """Hi, is this {name}?

I'm [YOUR NAME] — I built a free website for your restoration business. Water damage leads go to whoever homeowners find and trust first. I'd love to text you the link."""
    },
    "Auto repair shop": {
        "subject": "Free Website Sample Built for {name}",
        "email": """Hi,

I'm [YOUR NAME], a web designer in Utah. I built a free website sample for {name}:
[YOUR DOMAIN]/companies/{slug}

Car owners want to know they can trust a mechanic before they hand over their keys. The site I built builds that trust with services, certifications, and reviews front and center.

No cost, no obligation. Happy to chat.

[YOUR NAME]
[YOUR PHONE]""",
        "sms": """Hey! Built a free site for {name}: [YOUR DOMAIN]/companies/{slug}. Customers Google mechanics before calling — want more of those calls?""",
        "call_script": """Hi, is this {name}?

I'm [YOUR NAME], a web designer. I built a free website for your shop — car owners research mechanics online before calling. I'd love to text you the link to take a look."""
    },
    "Marble contractor": {
        "subject": "Free Premium Website Sample for {name}",
        "email": """Hi,

I'm [YOUR NAME], a web designer in Utah who loves working with craftspeople.

Stone and marble work is stunning — your website should reflect that. I built a free sample for {name}:
[YOUR DOMAIN]/companies/{slug}

It's designed to convey premium quality and craftsmanship to attract the right clients. No cost to view.

[YOUR NAME]
[YOUR PHONE]""",
        "sms": """Hi! Built a free site for {name}: [YOUR DOMAIN]/companies/{slug}. Premium stone deserves a premium website — want to take a look?""",
        "call_script": """Hi, is this {name}?

I'm [YOUR NAME] — I build premium websites for craftsmen. I put together a free site for your marble and stone business. Can I text you the link?"""
    },
    "Electrical installation service": {
        "subject": "Free Website Built for {name}",
        "email": """Hi,

I'm [YOUR NAME], a web designer in Utah. I built a free website sample for {name}:
[YOUR DOMAIN]/companies/{slug}

Commercial and residential electrical installation clients look for expertise and credibility online before signing contracts. The site I built showcases your capabilities and makes it easy to reach you.

No cost, no commitment. Let me know if you'd like to talk.

[YOUR NAME]
[YOUR PHONE]""",
        "sms": """Hi! Built a free site for {name}: [YOUR DOMAIN]/companies/{slug}. Want more commercial and residential installation leads? Let's chat!""",
        "call_script": """Hi, is this {name}?

I'm [YOUR NAME], a web designer. I built a free site for your electrical installation business. Commercial clients especially check websites before reaching out — can I text you the link?"""
    },
    "Contractor": {
        "subject": "Free Website for {name} — Ready to View",
        "email": """Hi,

I'm [YOUR NAME], a web designer in Utah. I built a free website sample for {name}:
[YOUR DOMAIN]/companies/{slug}

A professional website helps you win more bids and attract better clients. The sample showcases your services, builds trust, and makes it easy to get in touch.

No cost, no obligation.

[YOUR NAME]
[YOUR PHONE]""",
        "sms": """Hi! Built a free site for {name}: [YOUR DOMAIN]/companies/{slug}. Want more leads from your website? Happy to chat.""",
        "call_script": """Hi, is this {name}?

I'm [YOUR NAME], a web designer. I built a free website for your business — can I text you the link to take a look? No commitment."""
    },
}

# fallback
for t in ["Custom home builder"]:
    TEMPLATES[t] = TEMPLATES["Home builder"]

def get_template(t):
    return TEMPLATES.get(t, TEMPLATES["Contractor"])


def generate_outreach_page(companies, out_path):
    type_groups = {}
    for c in companies:
        type_groups.setdefault(c["type"], []).append(c)

    # build per-company cards for the "all companies" tab
    company_rows = []
    for c in companies:
        slug = slugify(c["name"])
        tmpl = get_template(c["type"])
        subj = tmpl["subject"].format(name=c["name"], slug=slug)
        email_body = tmpl["email"].format(name=c["name"], slug=slug)
        sms_body = tmpl["sms"].format(name=c["name"], slug=slug)
        call_body = tmpl["call_script"].format(name=c["name"], slug=slug)

        company_rows.append({
            "name": c["name"],
            "type": c["type"],
            "phone": c["phone"],
            "slug": slug,
            "subject": subj,
            "email": email_body,
            "sms": sms_body,
            "call": call_body,
        })

    # sidebar list
    sidebar_items = "\n".join(
        f'<li class="co-item" data-idx="{i}" onclick="showCompany({i})">'
        f'<span class="co-name">{r["name"]}</span>'
        f'<span class="co-type">{r["type"]}</span></li>'
        for i, r in enumerate(company_rows)
    )

    # JS data blob
    import json
    js_data = json.dumps(company_rows, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Outreach Toolkit — Utah Contractor Websites</title>
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:'Segoe UI',system-ui,sans-serif;background:#f1f5f9;color:#1e293b;height:100vh;overflow:hidden;display:flex;flex-direction:column}}
    /* TOP BAR */
    .topbar{{background:#0f172a;color:#fff;padding:14px 24px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}}
    .topbar h1{{font-size:17px;font-weight:800;letter-spacing:-0.3px}}
    .topbar h1 span{{color:#f59e0b}}
    .topbar-meta{{font-size:13px;color:#64748b}}
    /* LAYOUT */
    .layout{{display:flex;flex:1;overflow:hidden}}
    /* SIDEBAR */
    .sidebar{{width:280px;background:#fff;border-right:1px solid #e2e8f0;display:flex;flex-direction:column;flex-shrink:0}}
    .sidebar-search{{padding:12px;border-bottom:1px solid #e2e8f0}}
    .sidebar-search input{{width:100%;padding:8px 12px;border:1px solid #e2e8f0;border-radius:6px;font-size:13px;outline:none}}
    .sidebar-search input:focus{{border-color:#1a56db}}
    .co-list{{overflow-y:auto;flex:1;list-style:none;padding:4px 0}}
    .co-item{{padding:10px 16px;cursor:pointer;border-left:3px solid transparent;transition:all 0.12s}}
    .co-item:hover{{background:#f8fafc;border-left-color:#cbd5e1}}
    .co-item.active{{background:#eff6ff;border-left-color:#1a56db}}
    .co-name{{display:block;font-size:13px;font-weight:600;color:#1e293b;line-height:1.3}}
    .co-type{{display:block;font-size:11px;color:#94a3b8;margin-top:2px}}
    /* MAIN */
    .main{{flex:1;overflow-y:auto;padding:28px}}
    .company-header{{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:24px;margin-bottom:20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}}
    .company-header-left h2{{font-size:20px;font-weight:800;color:#0f172a}}
    .company-header-left p{{font-size:13px;color:#64748b;margin-top:4px}}
    .company-header-right{{display:flex;gap:10px;flex-wrap:wrap}}
    .btn{{padding:9px 18px;border-radius:6px;font-size:13px;font-weight:600;cursor:pointer;border:none;transition:all 0.15s;display:inline-flex;align-items:center;gap:6px;text-decoration:none}}
    .btn-blue{{background:#1a56db;color:#fff}}.btn-blue:hover{{background:#1341a3}}
    .btn-green{{background:#16a34a;color:#fff}}.btn-green:hover{{background:#15803d}}
    .btn-yellow{{background:#f59e0b;color:#1a1a1a}}.btn-yellow:hover{{filter:brightness(0.9)}}
    .btn-ghost{{background:#f1f5f9;color:#475569;border:1px solid #e2e8f0}}.btn-ghost:hover{{background:#e2e8f0}}
    /* TABS */
    .tabs{{display:flex;gap:4px;margin-bottom:16px}}
    .tab{{padding:8px 16px;border-radius:6px;font-size:13px;font-weight:600;cursor:pointer;border:1px solid #e2e8f0;background:#fff;color:#64748b;transition:all 0.12s}}
    .tab.active{{background:#1a56db;color:#fff;border-color:#1a56db}}
    .tab-panel{{display:none}}.tab-panel.active{{display:block}}
    /* TEMPLATE BOX */
    .template-box{{background:#fff;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;margin-bottom:16px}}
    .template-header{{padding:14px 18px;background:#f8fafc;border-bottom:1px solid #e2e8f0;display:flex;justify-content:space-between;align-items:center}}
    .template-label{{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:#64748b}}
    .copy-btn{{padding:5px 12px;border-radius:5px;font-size:12px;font-weight:600;cursor:pointer;border:1px solid #e2e8f0;background:#fff;color:#475569;transition:all 0.12s}}
    .copy-btn:hover{{background:#1a56db;color:#fff;border-color:#1a56db}}
    .copy-btn.copied{{background:#16a34a;color:#fff;border-color:#16a34a}}
    .template-body{{padding:18px;font-size:13px;line-height:1.75;color:#334155;white-space:pre-wrap;font-family:inherit}}
    .subject-line{{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:12px 16px;margin-bottom:16px;font-size:13px}}
    .subject-line strong{{color:#92400e;font-size:11px;text-transform:uppercase;letter-spacing:0.06em;display:block;margin-bottom:4px}}
    .preview-link{{display:inline-flex;align-items:center;gap:6px;padding:8px 14px;background:#eff6ff;border:1px solid #bfdbfe;border-radius:6px;font-size:13px;color:#1d4ed8;font-weight:600;text-decoration:none;margin-bottom:16px}}
    .preview-link:hover{{background:#dbeafe}}
    /* PLACEHOLDER NOTICE */
    .notice{{background:#fef3c7;border:1px solid #fde68a;border-radius:8px;padding:12px 16px;font-size:13px;color:#92400e;margin-bottom:20px}}
    .notice strong{{display:block;margin-bottom:4px}}
    /* EMPTY STATE */
    .empty{{text-align:center;padding:80px 24px;color:#94a3b8}}
    .empty h2{{font-size:20px;font-weight:700;color:#475569;margin-bottom:8px}}
    /* STATUS BADGE */
    .status-badge{{display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:99px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.05em}}
    .status-new{{background:#eff6ff;color:#1d4ed8}}
    .status-contacted{{background:#fef3c7;color:#92400e}}
    .status-interested{{background:#dcfce7;color:#15803d}}
    .status-closed{{background:#f0fdf4;color:#166534}}
    .status-notinterested{{background:#fef2f2;color:#b91c1c}}
  </style>
</head>
<body>

<div class="topbar">
  <h1>⚡ Outreach <span>Toolkit</span> — Utah Contractor Websites</h1>
  <span class="topbar-meta">{len(companies)} companies · Email, SMS &amp; Call Scripts</span>
</div>

<div class="layout">
  <!-- SIDEBAR -->
  <div class="sidebar">
    <div class="sidebar-search">
      <input type="text" id="searchInput" placeholder="Search companies…" oninput="filterList(this.value)"/>
    </div>
    <ul class="co-list" id="coList">
{sidebar_items}
    </ul>
  </div>

  <!-- MAIN -->
  <div class="main" id="mainPane">
    <div class="empty">
      <div style="font-size:48px;margin-bottom:16px">👈</div>
      <h2>Select a company to view outreach templates</h2>
      <p>Click any company from the list on the left to see their personalized email, SMS, and call script.</p>
    </div>
  </div>
</div>

<script>
const DATA = {js_data};

let activeIdx = null;

function showCompany(idx) {{
  activeIdx = idx;
  const r = DATA[idx];
  document.querySelectorAll('.co-item').forEach((el,i) => el.classList.toggle('active', i === idx));

  const websiteUrl = `[YOUR DOMAIN]/companies/${{r.slug}}.html`;

  document.getElementById('mainPane').innerHTML = `
    <div class="company-header">
      <div class="company-header-left">
        <h2>${{r.name}}</h2>
        <p>${{r.type}} &bull; ${{r.phone}}</p>
      </div>
      <div class="company-header-right">
        <a href="../companies/${{r.slug}}.html" target="_blank" class="btn btn-ghost">👁 Preview Site</a>
        <a href="tel:${{r.phone.replace(/\\s/g,'').replace(/-/g,'')}}" class="btn btn-green">📞 Call Now</a>
      </div>
    </div>

    <div class="notice">
      <strong>📌 Before sending — replace these placeholders:</strong>
      [YOUR NAME] · [YOUR PHONE] · [YOUR EMAIL] · [YOUR DOMAIN]
    </div>

    <div class="tabs">
      <button class="tab active" onclick="showTab(this,'email-panel')">📧 Email</button>
      <button class="tab" onclick="showTab(this,'sms-panel')">💬 SMS</button>
      <button class="tab" onclick="showTab(this,'call-panel')">📞 Call Script</button>
    </div>

    <!-- EMAIL -->
    <div id="email-panel" class="tab-panel active">
      <div class="subject-line">
        <strong>Subject Line</strong>
        ${{r.subject}}
        <button class="copy-btn" style="margin-left:8px" onclick="copyText('${{escapejs(r.subject)}}', this)">Copy</button>
      </div>
      <a class="preview-link" href="../companies/${{r.slug}}.html" target="_blank">🔗 ${{websiteUrl}}</a>
      <div class="template-box">
        <div class="template-header">
          <span class="template-label">Email Body</span>
          <button class="copy-btn" onclick="copyEl('email-body-${{idx}}',this)">Copy Email</button>
        </div>
        <div class="template-body" id="email-body-${{idx}}">${{r.email.replace(/\\[YOUR DOMAIN\\]\\/companies\\/${{r.slug}}/g, websiteUrl)}}</div>
      </div>
    </div>

    <!-- SMS -->
    <div id="sms-panel" class="tab-panel">
      <div class="template-box">
        <div class="template-header">
          <span class="template-label">SMS Message</span>
          <button class="copy-btn" onclick="copyEl('sms-body-${{idx}}',this)">Copy SMS</button>
        </div>
        <div class="template-body" id="sms-body-${{idx}}">${{r.sms.replace(/\\[YOUR DOMAIN\\]\\/companies\\/${{r.slug}}/g, websiteUrl)}}</div>
      </div>
    </div>

    <!-- CALL -->
    <div id="call-panel" class="tab-panel">
      <div class="template-box">
        <div class="template-header">
          <span class="template-label">Call Script</span>
          <button class="copy-btn" onclick="copyEl('call-body-${{idx}}',this)">Copy Script</button>
        </div>
        <div class="template-body" id="call-body-${{idx}}">${{r.call}}</div>
      </div>
    </div>
  `;
}}

function showTab(btn, panelId) {{
  btn.closest('.main, body').querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  btn.closest('.main, body').querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(panelId).classList.add('active');
}}

function copyText(text, btn) {{
  navigator.clipboard.writeText(text).then(() => {{
    btn.textContent = 'Copied!'; btn.classList.add('copied');
    setTimeout(() => {{ btn.textContent = 'Copy'; btn.classList.remove('copied'); }}, 2000);
  }});
}}

function copyEl(id, btn) {{
  const el = document.getElementById(id);
  navigator.clipboard.writeText(el.innerText).then(() => {{
    btn.textContent = '✓ Copied!'; btn.classList.add('copied');
    setTimeout(() => {{ btn.textContent = btn.textContent.startsWith('Copy') ? btn.textContent : 'Copy'; btn.classList.remove('copied'); }}, 2000);
  }});
}}

function escapejs(s) {{
  return s.replace(/'/g, "\\\\'").replace(/"/g, '\\\\"').replace(/\\n/g,'\\\\n');
}}

function filterList(q) {{
  const items = document.querySelectorAll('.co-item');
  const lower = q.toLowerCase();
  items.forEach(el => {{
    const name = el.querySelector('.co-name').textContent.toLowerCase();
    const type = el.querySelector('.co-type').textContent.toLowerCase();
    el.style.display = (name.includes(lower) || type.includes(lower)) ? '' : 'none';
  }});
}}
</script>
</body>
</html>'''

    with open(out_path, "w") as f:
        f.write(html)
    print(f"  ✓ outreach/index.html — interactive outreach toolkit")


def generate_leads_csv(companies, out_path):
    fieldnames = [
        "Company Name", "Business Type", "Phone", "City",
        "Website URL", "Status", "Email Sent", "SMS Sent", "Called",
        "Date Contacted", "Follow-Up Date", "Response Notes", "Deal Value", "Priority"
    ]
    rows = []
    for c in companies:
        slug = slugify(c["name"])
        rows.append({
            "Company Name": c["name"],
            "Business Type": c["type"],
            "Phone": c["phone"],
            "City": c["city"],
            "Website URL": f"[YOUR DOMAIN]/companies/{slug}.html",
            "Status": "New Lead",
            "Email Sent": "No",
            "SMS Sent": "No",
            "Called": "No",
            "Date Contacted": "",
            "Follow-Up Date": "",
            "Response Notes": "",
            "Deal Value": "",
            "Priority": "Medium",
        })

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  ✓ leads.csv — {len(rows)} companies ready for Google Sheets")


def main():
    base = os.path.dirname(__file__)
    generate_outreach_page(COMPANIES, os.path.join(base, "outreach", "index.html"))
    generate_leads_csv(COMPANIES, os.path.join(base, "leads.csv"))
    print(f"\nDone!")


if __name__ == "__main__":
    main()
