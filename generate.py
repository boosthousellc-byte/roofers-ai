#!/usr/bin/env python3
"""Generate website samples for all companies."""
import os, json, re

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

# ── Theme config per business type ─────────────────────────────────────────
THEMES = {
    "Electrician": {
        "primary": "#f59e0b", "primary_dark": "#d97706", "bg_dark": "#1a1200",
        "bg_mid": "#2d2000", "accent": "#fbbf24",
        "icon": "⚡", "hero_tag": "Licensed Electricians",
        "services": [
            ("⚡", "Panel Upgrades", "Safely upgrade your electrical panel to meet modern power demands."),
            ("💡", "Lighting Installation", "Indoor and outdoor lighting solutions for every space."),
            ("🔌", "Outlet & Switch Repair", "Fix faulty outlets, switches, and wiring throughout your home."),
            ("🏠", "Residential Wiring", "Complete wiring for new construction and remodels."),
            ("🏢", "Commercial Electrical", "Reliable electrical services for businesses of all sizes."),
            ("🚨", "Emergency Services", "24/7 emergency electrical repairs when you need us most."),
        ],
        "why_items": [
            ("🏅", "Licensed & Insured", "Fully licensed electricians with comprehensive insurance coverage."),
            ("⏱️", "Fast Response", "Same-day and emergency appointments available."),
            ("💰", "Upfront Pricing", "No hidden fees — transparent quotes before any work begins."),
            ("✅", "Code Compliant", "All work meets or exceeds local and national electrical codes."),
        ],
        "areas": ["Salt Lake City", "Provo", "Ogden", "Orem", "West Valley City", "Sandy", "Layton", "St. George", "Cedar City", "Logan"],
        "process": ["Call or Book Online", "Free Estimate", "Expert Installation", "Final Inspection"],
        "testimonials": [
            ("Sarah M.", "SLC", "⭐⭐⭐⭐⭐", "They upgraded our entire panel in one day. Professional, clean, and priced fairly. Highly recommend!"),
            ("James T.", "Provo", "⭐⭐⭐⭐⭐", "Had an emergency outage on a Sunday — they came within 2 hours and fixed it. Amazing service."),
            ("Linda K.", "Ogden", "⭐⭐⭐⭐⭐", "Installed recessed lighting throughout our home. The result is stunning and they left the place spotless."),
        ],
        "metrics": [("2,500+", "Jobs Completed"), ("15+", "Years in Business"), ("4.9★", "Average Rating")],
        "tagline": "Your Trusted Local Electricians",
        "hero_desc": "Safe, reliable electrical services for residential and commercial clients across Utah.",
    },
    "Plumber": {
        "primary": "#0284c7", "primary_dark": "#0369a1", "bg_dark": "#0a1628",
        "bg_mid": "#0d2137", "accent": "#38bdf8",
        "icon": "🔧", "hero_tag": "Licensed Plumbing Experts",
        "services": [
            ("🚿", "Drain Cleaning", "Fast, effective drain clearing — no more slow or blocked drains."),
            ("🚰", "Leak Detection & Repair", "Pinpoint and fix leaks before they cause costly damage."),
            ("🏠", "Pipe Installation", "New installations and full repipes for any home or business."),
            ("🔥", "Water Heater Services", "Installation, repair, and replacement of all water heater types."),
            ("🚽", "Fixture Installation", "Sinks, toilets, faucets, and more installed professionally."),
            ("🆘", "Emergency Plumbing", "Around-the-clock response for burst pipes and urgent issues."),
        ],
        "why_items": [
            ("🏅", "Licensed & Insured", "Certified master plumbers with full liability coverage."),
            ("⏱️", "Same-Day Service", "Fast dispatch for urgent plumbing problems."),
            ("💰", "Fair Flat-Rate Pricing", "Know your price upfront — no surprise invoices."),
            ("✅", "Quality Guaranteed", "All work backed by our satisfaction guarantee."),
        ],
        "areas": ["Salt Lake City", "Provo", "Ogden", "Park City", "Logan", "St. George", "Heber City", "Murray", "Draper", "South Jordan"],
        "process": ["Contact Us", "Diagnose & Quote", "Professional Repair", "Guarantee & Follow-Up"],
        "testimonials": [
            ("Mike R.", "SLC", "⭐⭐⭐⭐⭐", "Had a burst pipe at midnight — they were here in 45 minutes and had it fixed fast. Lifesavers!"),
            ("Carol J.", "Provo", "⭐⭐⭐⭐⭐", "Replaced our old galvanized pipes with copper. Outstanding craftsmanship and fair pricing."),
            ("Dave H.", "Ogden", "⭐⭐⭐⭐⭐", "They installed a new water heater perfectly. Cleaned up after themselves, too. Will use again."),
        ],
        "metrics": [("1,800+", "Repairs Done"), ("12+", "Years in Business"), ("4.8★", "Average Rating")],
        "tagline": "Reliable Plumbing You Can Count On",
        "hero_desc": "Expert plumbing services for homes and businesses throughout Utah. Available 24/7.",
    },
    "Marble contractor": {
        "primary": "#64748b", "primary_dark": "#475569", "bg_dark": "#0f1117",
        "bg_mid": "#1a1d27", "accent": "#cbd5e1",
        "icon": "🪨", "hero_tag": "Premium Stone & Marble Specialists",
        "services": [
            ("🪨", "Marble Countertops", "Stunning natural marble surfaces crafted for kitchens and baths."),
            ("✨", "Granite Fabrication", "Custom-cut granite slabs installed with precision."),
            ("🏠", "Flooring Installation", "Marble and stone flooring for timeless elegance."),
            ("🛁", "Bathroom Surfaces", "Transform showers, tub surrounds, and vanities."),
            ("🔧", "Repair & Restoration", "Restore cracked, chipped, or dull stone to its original beauty."),
            ("🎨", "Custom Fabrication", "Unique designs cut and polished to your exact specifications."),
        ],
        "why_items": [
            ("🏅", "Master Craftsmen", "Decades of experience working with natural stone."),
            ("🪨", "Premium Materials", "We source only the finest marble and granite."),
            ("📐", "Precise Fabrication", "Laser-measured, computer-cut for a perfect fit every time."),
            ("✅", "Lifetime Quality", "Our installations are built to last a lifetime."),
        ],
        "areas": ["Salt Lake City", "Park City", "Provo", "Heber City", "St. George", "Ogden", "Draper", "Midvale", "Murray", "Sandy"],
        "process": ["Design Consultation", "Material Selection", "Custom Fabrication", "Expert Installation"],
        "testimonials": [
            ("Rachel P.", "Park City", "⭐⭐⭐⭐⭐", "Our new marble countertops are absolutely breathtaking. Every guest comments on them."),
            ("Tom W.", "SLC", "⭐⭐⭐⭐⭐", "Granite kitchen island and floors — they transformed our home. Incredible craftsmanship."),
            ("Anna S.", "Draper", "⭐⭐⭐⭐⭐", "Repaired our cracked marble vanity and it looks brand new. Fast, professional, and affordable."),
        ],
        "metrics": [("500+", "Projects Installed"), ("20+", "Years of Craftsmanship"), ("4.9★", "Average Rating")],
        "tagline": "Natural Stone & Marble Excellence",
        "hero_desc": "Premium marble and granite fabrication and installation for Utah's finest homes.",
    },
    "Handyman": {
        "primary": "#16a34a", "primary_dark": "#15803d", "bg_dark": "#071a0e",
        "bg_mid": "#0d2b16", "accent": "#4ade80",
        "icon": "🔨", "hero_tag": "Trusted Local Handyman",
        "services": [
            ("🔨", "Home Repairs", "Doors, windows, drywall, trim — we fix it all."),
            ("🖼️", "Furniture Assembly", "Flat-pack and custom furniture assembled quickly and correctly."),
            ("🎨", "Painting & Patching", "Interior and exterior painting, drywall patching, and touch-ups."),
            ("🚿", "Minor Plumbing", "Faucet and fixture repairs, caulking, and minor leaks."),
            ("💡", "Minor Electrical", "Outlet covers, light fixtures, ceiling fans, and more."),
            ("🏡", "Yard & Exterior", "Deck repairs, fence fixes, and general property maintenance."),
        ],
        "why_items": [
            ("🏅", "Experienced Pro", "Years of experience across dozens of home repair specialties."),
            ("⏱️", "Shows Up On Time", "We respect your schedule and arrive when we say we will."),
            ("💰", "Affordable Rates", "Competitive hourly and flat-rate pricing with no hidden costs."),
            ("✅", "Work Guaranteed", "Not satisfied? We'll make it right at no extra charge."),
        ],
        "areas": ["Salt Lake City", "West Jordan", "Taylorsville", "Midvale", "Murray", "Kearns", "Millcreek", "Holladay", "Cottonwood Heights", "Sandy"],
        "process": ["Tell Us What's Needed", "Get a Quote", "We Fix It", "You're Happy"],
        "testimonials": [
            ("Brenda L.", "Murray", "⭐⭐⭐⭐⭐", "Fixed our fence, patched the drywall, and installed a new ceiling fan all in one visit. Incredible!"),
            ("Frank D.", "Sandy", "⭐⭐⭐⭐⭐", "I've used them 4 times now. Always reliable, affordable, and does excellent work."),
            ("Gina M.", "Midvale", "⭐⭐⭐⭐⭐", "Assembled all my new IKEA furniture in a few hours. Saved me days of frustration!"),
        ],
        "metrics": [("3,000+", "Jobs Completed"), ("10+", "Years of Service"), ("4.9★", "Average Rating")],
        "tagline": "No Job Too Small — We Do It All",
        "hero_desc": "Your local handyman for home repairs, improvements, and maintenance throughout Utah.",
    },
    "Electrical installation service": {
        "primary": "#7c3aed", "primary_dark": "#6d28d9", "bg_dark": "#13091f",
        "bg_mid": "#1e0e35", "accent": "#a78bfa",
        "icon": "🔌", "hero_tag": "Certified Electrical Installation",
        "services": [
            ("🔌", "New Construction Wiring", "Complete electrical rough-in and finish for new builds."),
            ("🏢", "Commercial Installations", "Code-compliant electrical systems for offices and retail."),
            ("🔋", "EV Charger Installation", "Level 1 and Level 2 home and commercial EV charging stations."),
            ("☀️", "Solar System Integration", "Connect and commission solar and battery storage systems."),
            ("📟", "Generator Hookups", "Standby and portable generator installation and transfer switches."),
            ("🔍", "Electrical Inspections", "Full system audits and compliance reports."),
        ],
        "why_items": [
            ("🏅", "Master Electricians", "Our team includes certified master electricians."),
            ("📋", "Permit & Code Experts", "We handle all permits and ensure full code compliance."),
            ("⚡", "Modern Technology", "We use the latest tools and materials for every project."),
            ("✅", "Project Management", "From design to inspection — we manage the entire process."),
        ],
        "areas": ["Salt Lake City", "Provo", "Orem", "Ogden", "Murray", "Draper", "Sandy", "Lehi", "American Fork", "Springville"],
        "process": ["Project Assessment", "Design & Permitting", "Professional Installation", "Inspection & Sign-Off"],
        "testimonials": [
            ("Bob N.", "Lehi", "⭐⭐⭐⭐⭐", "Wired our entire new office building on time and under budget. Truly professional."),
            ("Lisa C.", "Provo", "⭐⭐⭐⭐⭐", "Installed our EV charger and solar integration flawlessly. Very knowledgeable team."),
            ("Mark T.", "SLC", "⭐⭐⭐⭐⭐", "Handled permits, installation, and inspections for our remodel. Stress-free experience."),
        ],
        "metrics": [("800+", "Projects Completed"), ("18+", "Years Experience"), ("4.9★", "Average Rating")],
        "tagline": "Expert Electrical Installation Services",
        "hero_desc": "Professional electrical installation for residential, commercial, and industrial projects in Utah.",
    },
    "Cabinet maker": {
        "primary": "#92400e", "primary_dark": "#78350f", "bg_dark": "#1a0e00",
        "bg_mid": "#2d1a00", "accent": "#fbbf24",
        "icon": "🪵", "hero_tag": "Custom Cabinet Craftsmen",
        "services": [
            ("🪵", "Custom Kitchen Cabinets", "Handcrafted kitchen cabinetry designed for your space."),
            ("🛁", "Bathroom Vanities", "Beautiful, functional vanity cabinets and storage solutions."),
            ("🏠", "Built-In Shelving", "Custom built-ins for living rooms, offices, and bedrooms."),
            ("🍷", "Entertainment Centers", "Media walls and entertainment centers built to impress."),
            ("🔧", "Cabinet Refacing", "Refresh existing cabinets at a fraction of replacement cost."),
            ("✨", "Countertop Installation", "We pair our cabinets with premium countertop surfaces."),
        ],
        "why_items": [
            ("🏅", "Master Craftsmen", "Every cabinet is built by skilled artisans, not machines."),
            ("🎨", "Fully Custom", "Designed from scratch to fit your exact space and style."),
            ("🪵", "Premium Materials", "Solid wood, soft-close hardware, and quality finishes throughout."),
            ("✅", "Lifetime Warranty", "We stand behind our craftsmanship with a lifetime guarantee."),
        ],
        "areas": ["Salt Lake City", "Provo", "Ogden", "Park City", "Heber City", "Lehi", "American Fork", "St. George", "Logan", "Bountiful"],
        "process": ["Design Consultation", "Custom Blueprint", "Expert Build", "Professional Install"],
        "testimonials": [
            ("Diane F.", "Park City", "⭐⭐⭐⭐⭐", "Our new kitchen cabinets are absolutely gorgeous. The craftsmanship is incredible."),
            ("Steve H.", "SLC", "⭐⭐⭐⭐⭐", "Built a stunning built-in entertainment wall for our living room. Better than we imagined!"),
            ("Karen O.", "Provo", "⭐⭐⭐⭐⭐", "Refaced our kitchen cabinets — looks like a completely new kitchen for much less money."),
        ],
        "metrics": [("400+", "Kitchens Built"), ("25+", "Years of Craftsmanship"), ("4.9★", "Average Rating")],
        "tagline": "Handcrafted Cabinets for Beautiful Homes",
        "hero_desc": "Custom cabinetry and built-ins crafted with premium materials and expert precision.",
    },
    "Drywall contractor": {
        "primary": "#0891b2", "primary_dark": "#0e7490", "bg_dark": "#05141a",
        "bg_mid": "#07212d", "accent": "#22d3ee",
        "icon": "🏗️", "hero_tag": "Expert Drywall Services",
        "services": [
            ("🏗️", "Drywall Installation", "Full drywall hanging for new construction and remodels."),
            ("🔧", "Drywall Repair", "Patch holes, cracks, and water damage quickly and cleanly."),
            ("🎨", "Taping & Mudding", "Seamless finishing with professional taping and joint compound."),
            ("✨", "Texture Application", "Orange peel, knockdown, smooth, and custom textures."),
            ("🏢", "Commercial Drywall", "Large commercial projects completed on schedule."),
            ("💧", "Water Damage Repair", "Remove and replace moisture-damaged drywall completely."),
        ],
        "why_items": [
            ("🏅", "Skilled Finishers", "Level 5 finishes and flawless results on every project."),
            ("⏱️", "Fast Turnaround", "Most repairs completed in a single day."),
            ("🧹", "Clean Worksite", "We protect your home and clean up completely after every job."),
            ("✅", "Satisfaction Guarantee", "We won't leave until you're completely happy."),
        ],
        "areas": ["Salt Lake City", "West Valley", "Taylorsville", "Murray", "Millcreek", "Kearns", "Sandy", "Draper", "South Jordan", "Herriman"],
        "process": ["Free Assessment", "Prep & Protect", "Expert Repair", "Flawless Finish"],
        "testimonials": [
            ("Amy B.", "West Valley", "⭐⭐⭐⭐⭐", "Repaired major water damage — you'd never know anything happened. Seamless finish!"),
            ("Don R.", "Sandy", "⭐⭐⭐⭐⭐", "Hung and finished drywall for our entire basement. Came in on budget and ahead of schedule."),
            ("Maria G.", "Murray", "⭐⭐⭐⭐⭐", "Fixed a big hole in our living room wall and matched the texture perfectly. Incredible."),
        ],
        "metrics": [("2,000+", "Projects Completed"), ("14+", "Years Experience"), ("4.8★", "Average Rating")],
        "tagline": "Flawless Drywall Installation & Repair",
        "hero_desc": "Professional drywall installation, repair, and finishing throughout the Salt Lake Valley.",
    },
    "Tile contractor": {
        "primary": "#0f766e", "primary_dark": "#0d6660", "bg_dark": "#041413",
        "bg_mid": "#082421", "accent": "#2dd4bf",
        "icon": "🔲", "hero_tag": "Expert Tile Installation",
        "services": [
            ("🔲", "Floor Tile Installation", "Ceramic, porcelain, stone, and luxury vinyl tile flooring."),
            ("🚿", "Shower & Tub Surrounds", "Waterproof, stunning tile work for bathrooms."),
            ("🍳", "Kitchen Backsplash", "Transform your kitchen with a custom tile backsplash."),
            ("🏠", "Natural Stone", "Travertine, slate, marble, and more installed flawlessly."),
            ("🔧", "Tile Repair & Regrout", "Fix cracked tiles and refresh grout for a like-new look."),
            ("🏢", "Commercial Tile", "Large-scale tile projects for commercial spaces."),
        ],
        "why_items": [
            ("🏅", "Master Tile Setters", "Precision layout and installation for a perfect result."),
            ("🎨", "Design Expertise", "We help you choose patterns, colors, and materials."),
            ("💧", "Waterproofing", "Proper substrate prep and waterproofing on every wet area."),
            ("✅", "Quality Guaranteed", "All tile work backed by our craftsmanship warranty."),
        ],
        "areas": ["Salt Lake City", "Provo", "Ogden", "St. George", "Orem", "Logan", "Cedar City", "Heber City", "Park City", "Payson"],
        "process": ["Design Consultation", "Material Selection", "Surface Prep", "Expert Installation"],
        "testimonials": [
            ("Pam S.", "St. George", "⭐⭐⭐⭐⭐", "Our new bathroom tile is stunning. The herringbone pattern came out perfect."),
            ("Eric W.", "Provo", "⭐⭐⭐⭐⭐", "Tiled our entire basement floor and bathroom. Flawless results and great pricing."),
            ("Julia R.", "SLC", "⭐⭐⭐⭐⭐", "Kitchen backsplash was installed in one day and looks incredible. Love it!"),
        ],
        "metrics": [("1,200+", "Rooms Tiled"), ("16+", "Years Experience"), ("4.9★", "Average Rating")],
        "tagline": "Beautiful Tile Installation for Every Space",
        "hero_desc": "Expert tile installation for floors, showers, backsplashes, and more across Utah.",
    },
    "Kitchen remodeler": {
        "primary": "#dc2626", "primary_dark": "#b91c1c", "bg_dark": "#1a0505",
        "bg_mid": "#2d0a0a", "accent": "#fbbf24",
        "icon": "🍳", "hero_tag": "Dream Kitchen Specialists",
        "services": [
            ("🍳", "Full Kitchen Remodel", "Complete transformation from design to final installation."),
            ("🪵", "Cabinet Installation", "New cabinets or refacing — we do it all beautifully."),
            ("🪨", "Countertop Install", "Granite, quartz, marble, and butcher block surfaces."),
            ("🚰", "Plumbing Upgrades", "New sinks, fixtures, and plumbing relocation."),
            ("💡", "Lighting Design", "Under-cabinet lighting, pendants, and recessed lighting."),
            ("🎨", "Full Design Service", "2D & 3D design plans so you can see it before we build it."),
        ],
        "why_items": [
            ("🏅", "Award-Winning Design", "Our kitchens win neighbors' envy and resale value."),
            ("📐", "Full-Service Remodel", "We handle design, permits, and every trade involved."),
            ("🗓️", "On-Time Delivery", "Detailed project timelines we actually stick to."),
            ("✅", "5-Year Warranty", "All labor and materials covered for 5 full years."),
        ],
        "areas": ["Salt Lake City", "Provo", "Heber City", "Park City", "Ogden", "Orem", "Lehi", "Draper", "South Jordan", "Riverton"],
        "process": ["Free Design Consult", "3D Rendering", "Professional Build", "Final Walkthrough"],
        "testimonials": [
            ("Kim N.", "Draper", "⭐⭐⭐⭐⭐", "They turned our outdated kitchen into something out of a magazine. We're obsessed!"),
            ("Paul K.", "Park City", "⭐⭐⭐⭐⭐", "From design to install took 6 weeks as promised. The kitchen exceeded expectations."),
            ("Sue T.", "Provo", "⭐⭐⭐⭐⭐", "Complete remodel — cabinets, counters, backsplash, lighting. Absolutely perfect."),
        ],
        "metrics": [("350+", "Kitchens Remodeled"), ("22+", "Years in Business"), ("4.9★", "Average Rating")],
        "tagline": "Utah's Premier Kitchen Remodeling Experts",
        "hero_desc": "Transform your kitchen with expert design, quality craftsmanship, and on-time delivery.",
    },
    "Bathroom remodeler": {
        "primary": "#0284c7", "primary_dark": "#0369a1", "bg_dark": "#060e1a",
        "bg_mid": "#0a1830", "accent": "#38bdf8",
        "icon": "🛁", "hero_tag": "Bathroom Remodeling Experts",
        "services": [
            ("🛁", "Full Bathroom Remodel", "Complete bathroom transformations from floor to ceiling."),
            ("🚿", "Shower Replacement", "Walk-in showers, tub-to-shower conversions, and enclosures."),
            ("🪨", "Vanity & Countertop", "Beautiful vanities with stone or solid-surface tops."),
            ("🔲", "Tile & Flooring", "Waterproof tile and luxury vinyl flooring installed flawlessly."),
            ("🚽", "Fixture Upgrades", "Toilets, faucets, and accessories replaced or upgraded."),
            ("💡", "Lighting & Mirrors", "Lighting upgrades and custom mirror installations."),
        ],
        "why_items": [
            ("🏅", "Remodeling Specialists", "We focus exclusively on bathrooms and kitchens."),
            ("📐", "Design Included", "Free design consultation with every project."),
            ("🗓️", "Fast Completion", "Most bathroom remodels completed in 1–2 weeks."),
            ("✅", "Worry-Free Warranty", "2-year labor warranty on all remodeling projects."),
        ],
        "areas": ["Salt Lake City", "West Jordan", "Sandy", "Murray", "Midvale", "Taylorsville", "South Jordan", "Riverton", "Herriman", "Draper"],
        "process": ["Free Consultation", "Design & Quote", "Demo & Build", "Final Reveal"],
        "testimonials": [
            ("Lori P.", "Sandy", "⭐⭐⭐⭐⭐", "Our master bath was completely transformed. The tile work and new shower are gorgeous!"),
            ("Chris B.", "Murray", "⭐⭐⭐⭐⭐", "Finished ahead of schedule and the result looks like a high-end spa. Absolutely love it."),
            ("Tina F.", "South Jordan", "⭐⭐⭐⭐⭐", "Best money we ever spent. The crew was professional and the quality is outstanding."),
        ],
        "metrics": [("600+", "Bathrooms Remodeled"), ("18+", "Years in Business"), ("4.9★", "Average Rating")],
        "tagline": "Beautiful Bathroom Transformations",
        "hero_desc": "Expert bathroom remodeling that delivers spa-quality results for Utah homeowners.",
    },
    "General contractor": {
        "primary": "#374151", "primary_dark": "#1f2937", "bg_dark": "#0d0f12",
        "bg_mid": "#171a1f", "accent": "#f59e0b",
        "icon": "🏗️", "hero_tag": "Licensed General Contractor",
        "services": [
            ("🏗️", "New Home Construction", "Full custom home builds from foundation to finish."),
            ("🏠", "Home Additions", "Expand your living space with expertly planned additions."),
            ("🔧", "Whole-Home Remodels", "Gut remodels and major renovations done right."),
            ("🏢", "Commercial Build-Outs", "Office, retail, and industrial construction and remodeling."),
            ("📐", "Project Management", "Full oversight of every trade and subcontractor."),
            ("✅", "Permit Services", "We handle all permits, inspections, and code compliance."),
        ],
        "why_items": [
            ("🏅", "Licensed & Bonded", "Utah licensed general contractor, fully bonded and insured."),
            ("📋", "Full Project Management", "One point of contact from groundbreaking to final walkthrough."),
            ("🗓️", "On Schedule & Budget", "Detailed project planning to stay on time and on budget."),
            ("✅", "Quality Guarantee", "We stand behind our work with a comprehensive warranty."),
        ],
        "areas": ["Salt Lake City", "Provo", "Ogden", "St. George", "Logan", "Cedar City", "Park City", "Heber City", "Vernal", "Price"],
        "process": ["Consultation & Design", "Detailed Bid", "Construction", "Final Inspection"],
        "testimonials": [
            ("Rob H.", "St. George", "⭐⭐⭐⭐⭐", "Built our dream home on time and exactly on budget. Incredible attention to detail."),
            ("Nancy L.", "SLC", "⭐⭐⭐⭐⭐", "Our whole-home remodel was managed flawlessly. We barely had to lift a finger."),
            ("John W.", "Ogden", "⭐⭐⭐⭐⭐", "Added a 1,200 sq ft addition — permits handled, perfect craftsmanship, no surprises."),
        ],
        "metrics": [("300+", "Projects Completed"), ("20+", "Years in Business"), ("4.8★", "Average Rating")],
        "tagline": "Building Utah's Best Homes & Businesses",
        "hero_desc": "Full-service general contracting for residential and commercial projects across Utah.",
    },
    "Auto repair shop": {
        "primary": "#1d4ed8", "primary_dark": "#1e40af", "bg_dark": "#080c1a",
        "bg_mid": "#0e1530", "accent": "#60a5fa",
        "icon": "🚗", "hero_tag": "Trusted Auto Repair Experts",
        "services": [
            ("🚗", "Engine Diagnostics", "Advanced computer diagnostics to identify any issue fast."),
            ("🔧", "Brake Service", "Brake pad, rotor, and caliper repair and replacement."),
            ("🛢️", "Oil Change & Fluids", "Full-service oil changes and fluid top-offs or flushes."),
            ("⚙️", "Transmission Service", "Transmission fluid service, repairs, and rebuilds."),
            ("❄️", "A/C & Heating", "Climate control diagnosis and repair for year-round comfort."),
            ("🔋", "Battery & Electrical", "Battery testing, replacement, and electrical diagnostics."),
        ],
        "why_items": [
            ("🏅", "ASE Certified Techs", "Our mechanics hold current ASE certifications."),
            ("💰", "Honest Pricing", "Written estimates before any work — no surprise charges."),
            ("⏱️", "Fast Service", "Most repairs completed same day or next day."),
            ("✅", "Warranty Included", "12-month/12,000-mile warranty on parts and labor."),
        ],
        "areas": ["Salt Lake City", "West Valley", "Kearns", "Taylorsville", "Murray", "Midvale", "Sandy", "Draper", "South Jordan", "Riverton"],
        "process": ["Drop Off", "Diagnose & Estimate", "Expert Repair", "Quality Check & Pick Up"],
        "testimonials": [
            ("Alex M.", "Murray", "⭐⭐⭐⭐⭐", "Diagnosed my check engine light in minutes and fixed it same day. Honest and fair pricing."),
            ("Beth T.", "Sandy", "⭐⭐⭐⭐⭐", "They've kept my car running for years. Wouldn't trust anyone else with my vehicle."),
            ("Carl J.", "West Valley", "⭐⭐⭐⭐⭐", "Needed brakes urgently — they fit me in and had me back on the road in 2 hours."),
        ],
        "metrics": [("5,000+", "Repairs Done"), ("15+", "Years in Business"), ("4.8★", "Average Rating")],
        "tagline": "Honest, Reliable Auto Repair",
        "hero_desc": "Comprehensive auto repair and maintenance from certified mechanics you can trust.",
    },
    "Water damage restoration": {
        "primary": "#0369a1", "primary_dark": "#075985", "bg_dark": "#050f1a",
        "bg_mid": "#081826", "accent": "#38bdf8",
        "icon": "💧", "hero_tag": "24/7 Water Damage Restoration",
        "services": [
            ("💧", "Emergency Water Removal", "Fast water extraction to minimize damage and mold risk."),
            ("💨", "Structural Drying", "Industrial-grade drying equipment for walls, floors, and ceilings."),
            ("🔬", "Mold Remediation", "Safe, certified mold testing, removal, and prevention."),
            ("🏗️", "Reconstruction", "Full repair and rebuild after water damage is resolved."),
            ("🔍", "Damage Assessment", "Thorough documentation for insurance claims."),
            ("🚿", "Sewage Cleanup", "Safe removal and sanitization of sewage backups."),
        ],
        "why_items": [
            ("🚨", "24/7 Emergency Response", "We respond to water emergencies any time of day or night."),
            ("🏅", "IICRC Certified", "Industry-certified technicians and restoration processes."),
            ("📋", "Insurance Assistance", "We work directly with your insurance company."),
            ("✅", "Guaranteed Dry", "We use moisture meters to confirm complete drying."),
        ],
        "areas": ["Salt Lake City", "West Valley", "Taylorsville", "Murray", "Sandy", "Draper", "South Jordan", "West Jordan", "Kearns", "Millcreek"],
        "process": ["Emergency Call", "Rapid Extraction", "Dry & Monitor", "Restore & Rebuild"],
        "testimonials": [
            ("Heather W.", "Sandy", "⭐⭐⭐⭐⭐", "They arrived at 2am and had the water out fast. Saved our floors and walls. True lifesavers."),
            ("Gary F.", "Murray", "⭐⭐⭐⭐⭐", "Handled everything including the insurance claim. Professional, fast, and thorough."),
            ("Donna P.", "West Valley", "⭐⭐⭐⭐⭐", "Mold was discovered and fully remediated. We feel safe in our home again. Thank you!"),
        ],
        "metrics": [("1,500+", "Homes Restored"), ("10+", "Years Experience"), ("4.9★", "Average Rating")],
        "tagline": "Fast Response Water Damage Restoration",
        "hero_desc": "24/7 emergency water damage restoration, drying, and reconstruction for Utah homeowners.",
    },
    "Contractor": {
        "primary": "#6b21a8", "primary_dark": "#581c87", "bg_dark": "#0f0518",
        "bg_mid": "#1a0829", "accent": "#c084fc",
        "icon": "🔨", "hero_tag": "Professional Contractor",
        "services": [
            ("🔨", "Custom Woodwork", "Handcrafted wood projects built to your specifications."),
            ("🏠", "Home Renovations", "Full-service renovation and improvement projects."),
            ("🪵", "Finish Carpentry", "Trim, molding, wainscoting, and built-in installations."),
            ("🏗️", "Structural Work", "Framing, load-bearing modifications, and structural repairs."),
            ("🎨", "Interior Finishing", "Painting, flooring, and interior finish work."),
            ("🔧", "Commercial Contracting", "Small to mid-size commercial projects handled professionally."),
        ],
        "why_items": [
            ("🏅", "Licensed & Insured", "Properly licensed and insured for your protection."),
            ("🪵", "Quality Materials", "We use premium materials built to last for decades."),
            ("⏱️", "Timely Completion", "Projects completed on schedule without cutting corners."),
            ("✅", "Craftsman Warranty", "All work guaranteed for quality and durability."),
        ],
        "areas": ["Salt Lake City", "Provo", "Ogden", "Lehi", "American Fork", "Pleasant Grove", "Springville", "Spanish Fork", "Payson", "Nephi"],
        "process": ["Initial Consultation", "Design & Proposal", "Expert Build", "Final Review"],
        "testimonials": [
            ("Tyler B.", "Lehi", "⭐⭐⭐⭐⭐", "Built our deck and pergola — it's absolutely beautiful and incredibly well-made."),
            ("Cindy R.", "Provo", "⭐⭐⭐⭐⭐", "Finished our basement to a professional standard. We use it as our family's favorite room."),
            ("Sam V.", "SLC", "⭐⭐⭐⭐⭐", "Custom built-ins for my home office. Exactly what I envisioned. Exceptional craftsmanship."),
        ],
        "metrics": [("700+", "Projects Built"), ("17+", "Years Experience"), ("4.9★", "Average Rating")],
        "tagline": "Quality Craftsmanship for Every Project",
        "hero_desc": "Professional contracting and custom woodwork for Utah homes and businesses.",
    },
    "Home builder": {
        "primary": "#15803d", "primary_dark": "#166534", "bg_dark": "#071a0b",
        "bg_mid": "#0c2912", "accent": "#4ade80",
        "icon": "🏡", "hero_tag": "Custom Home Builder",
        "services": [
            ("🏡", "Custom Home Design", "Work with our designers to create your perfect floor plan."),
            ("🏗️", "New Home Construction", "Full construction management from foundation to move-in."),
            ("🎨", "Interior Selections", "Guided selection of finishes, fixtures, and materials."),
            ("🔧", "Site Preparation", "Land clearing, grading, utilities, and foundation work."),
            ("📐", "Architectural Plans", "In-house design team for custom architectural drawings."),
            ("🔑", "Turnkey Delivery", "Move-in ready homes with everything completed."),
        ],
        "why_items": [
            ("🏅", "Award-Winning Builder", "Recognized for quality and customer satisfaction."),
            ("🗓️", "On-Time Delivery", "We complete homes on schedule with no delays."),
            ("💰", "Transparent Budgeting", "Detailed cost breakdowns with no hidden surprises."),
            ("✅", "10-Year Warranty", "Structural and workmanship warranty for peace of mind."),
        ],
        "areas": ["Salt Lake City", "Provo", "Lehi", "Draper", "South Jordan", "Riverton", "Herriman", "Saratoga Springs", "Eagle Mountain", "Payson"],
        "process": ["Land & Design", "Planning & Permits", "Custom Build", "Final Walkthrough & Keys"],
        "testimonials": [
            ("Jason & Amy L.", "Saratoga Springs", "⭐⭐⭐⭐⭐", "Built our dream home in 8 months exactly as promised. We are absolutely in love with it."),
            ("The Harrison Family", "Lehi", "⭐⭐⭐⭐⭐", "The quality of construction is unmatched. Our neighbors constantly compliment our home."),
            ("Brad M.", "Draper", "⭐⭐⭐⭐⭐", "Process was smooth from design to move-in. They made building a custom home stress-free."),
        ],
        "metrics": [("150+", "Homes Built"), ("28+", "Years in Business"), ("4.9★", "Average Rating")],
        "tagline": "Building Your Dream Home in Utah",
        "hero_desc": "Custom home construction built with quality materials, expert craftsmanship, and care.",
    },
}

# fallback for unlisted types
THEMES["Custom home builder"] = THEMES["Home builder"]


def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def get_theme(t):
    return THEMES.get(t, THEMES["General contractor"])


def html_page(company):
    n = company["name"]
    t = company["type"]
    ph = company["phone"]
    city = company["city"]
    th = get_theme(t)
    slug = slugify(n)

    services_html = "\n".join(
        f'''        <div class="service-card">
          <div class="service-icon">{s[0]}</div>
          <h3>{s[1]}</h3>
          <p>{s[2]}</p>
        </div>'''
        for s in th["services"]
    )

    why_items_html = "\n".join(
        f'''          <div class="why-item">
            <div class="why-item-icon">{w[0]}</div>
            <div class="why-item-text">
              <h4>{w[1]}</h4>
              <p>{w[2]}</p>
            </div>
          </div>'''
        for w in th["why_items"]
    )

    metrics_html = "\n".join(
        f'''          <div class="metric-card">
            <div class="metric-val">{m[0]}</div>
            <div class="metric-label">{m[1]}</div>
          </div>'''
        for m in th["metrics"]
    )

    process_html = "\n".join(
        f'''        <div class="process-step">
          <div class="step-num">{i+1}</div>
          <h3>{p}</h3>
          <p>{'Simple, streamlined, and stress-free every step of the way.' if i == 0 else 'Our team handles every detail professionally and efficiently.' if i == 1 else 'Expert work completed on schedule and to the highest standard.' if i == 2 else 'We verify everything is perfect before we consider the job done.'}</p>
        </div>'''
        for i, p in enumerate(th["process"])
    )

    testimonials_html = "\n".join(
        f'''        <div class="testimonial-card">
          <div class="stars">{r[2]}</div>
          <p class="testimonial-text">"{r[3]}"</p>
          <div class="testimonial-author">
            <div class="author-avatar">{r[0][0]}</div>
            <div>
              <div class="author-name">{r[0]}</div>
              <div class="author-loc">{r[1]}, Utah</div>
            </div>
          </div>
        </div>'''
        for r in th["testimonials"]
    )

    areas_html = "\n".join(
        f'          <span class="area-chip">{a}</span>'
        for a in th["areas"]
    )

    checklist = [
        f'Licensed &amp; Insured in Utah',
        f'Free Estimates Available',
        f'Serving {city}',
        f'Locally Owned &amp; Operated',
        f'5-Star Rated Service',
    ]
    checklist_html = "\n".join(
        f'              <li>{c}</li>' for c in checklist
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{n} | {t} in {city}</title>
  <meta name="description" content="{n} — {th["hero_desc"]} Call us at {ph}." />
  <link rel="stylesheet" href="../css/styles.css" />
  <style>
    :root {{
      --primary: {th["primary"]};
      --primary-dark: {th["primary_dark"]};
      --accent: {th["accent"]};
      --bg-dark: {th["bg_dark"]};
      --bg-mid: {th["bg_mid"]};
    }}
  </style>
</head>
<body>

<!-- HEADER -->
<header class="site-header">
  <div class="container">
    <div class="logo">{th["icon"]} <span>{n.split()[0]}</span> {" ".join(n.split()[1:]) if len(n.split()) > 1 else ""}</div>
    <nav class="nav">
      <a href="#services">Services</a>
      <a href="#about">About</a>
      <a href="#process">Process</a>
      <a href="#reviews">Reviews</a>
      <a href="#contact">Contact</a>
      <a href="tel:{ph.replace(' ','').replace('-','')}" class="btn btn-accent nav-cta">{ph}</a>
    </nav>
  </div>
</header>

<!-- HERO -->
<section class="hero">
  <div class="container hero-inner">
    <div>
      <div class="hero-eyebrow">{th["hero_tag"]} &bull; {city}</div>
      <h1>{th["tagline"].replace(" ", " <em>", 1).replace(" ", "</em> ", 1) if len(th["tagline"].split()) > 3 else "<em>" + th["tagline"] + "</em>"}</h1>
      <p class="hero-sub">{th["hero_desc"]}</p>
      <div class="hero-actions">
        <a href="tel:{ph.replace(' ','').replace('-','')}" class="btn btn-accent">{th["icon"]} Call {ph}</a>
        <a href="#services" class="btn btn-outline">View Services</a>
      </div>
      <div class="hero-stats">
        {"".join(f'<div><div class="hero-stat-num">{m[0]}</div><div class="hero-stat-label">{m[1]}</div></div>' for m in th["metrics"])}
      </div>
    </div>
    <div class="hero-card">
      <div class="hero-card-title">Why Choose {n.split()[0]}?</div>
      <ul class="hero-checklist">
{checklist_html}
      </ul>
    </div>
  </div>
</section>

<!-- TRUST BAR -->
<div class="trust-bar">
  <div class="container">
    <div class="trust-item"><span class="trust-icon">🏅</span> Licensed &amp; Insured</div>
    <div class="trust-item"><span class="trust-icon">⭐</span> 5-Star Rated</div>
    <div class="trust-item"><span class="trust-icon">📍</span> Locally Owned</div>
    <div class="trust-item"><span class="trust-icon">🆓</span> Free Estimates</div>
    <div class="trust-item"><span class="trust-icon">🔒</span> Satisfaction Guaranteed</div>
  </div>
</div>

<!-- SERVICES -->
<section class="section services" id="services">
  <div class="container">
    <div class="section-header">
      <span class="tag">Our Services</span>
      <h2>What We Do Best</h2>
      <p>Comprehensive {t.lower()} services delivered with professionalism and attention to detail.</p>
    </div>
    <div class="grid-3">
{services_html}
    </div>
  </div>
</section>

<!-- WHY US -->
<section class="section why-us" id="about">
  <div class="container">
    <div class="why-grid">
      <div class="why-content">
        <span class="tag" style="background:rgba(255,255,255,0.1);color:var(--accent)">Why Choose Us</span>
        <h2 style="color:#fff;margin-top:12px">The {n.split()[0]} Difference</h2>
        <p>We're not just another {t.lower()}. We're your neighbors, and we treat your home like our own. Every job is completed to the highest standard with honesty, skill, and pride.</p>
        <div class="why-list">
{why_items_html}
        </div>
      </div>
      <div class="why-image-wrap">
{metrics_html}
        <a href="tel:{ph.replace(' ','').replace('-','')}" class="btn btn-accent" style="margin-top:8px">{th["icon"]} Call Us: {ph}</a>
      </div>
    </div>
  </div>
</section>

<!-- PROCESS -->
<section class="section process" id="process">
  <div class="container">
    <div class="section-header">
      <span class="tag">How It Works</span>
      <h2>Our Simple Process</h2>
      <p>Getting started is easy. Here's how we work with you from first contact to finished project.</p>
    </div>
    <div class="process-steps">
{process_html}
    </div>
  </div>
</section>

<!-- TESTIMONIALS -->
<section class="section testimonials" id="reviews">
  <div class="container">
    <div class="section-header">
      <span class="tag">Reviews</span>
      <h2>What Our Customers Say</h2>
      <p>Don't just take our word for it. Here's what real customers in Utah have to say.</p>
    </div>
    <div class="grid-3">
{testimonials_html}
    </div>
  </div>
</section>

<!-- SERVICE AREAS -->
<section class="section-sm areas" id="areas">
  <div class="container areas-inner">
    <div>
      <span class="tag" style="background:rgba(255,255,255,0.1);color:var(--accent)">Service Areas</span>
      <h2 style="margin-top:12px">Serving Utah &amp; Surrounding Communities</h2>
      <p style="color:#94a3b8;margin-top:8px">We proudly serve homeowners and businesses throughout the region. Contact us to confirm service in your area.</p>
      <div class="areas-list">
{areas_html}
      </div>
    </div>
    <div>
      <div class="why-image-wrap" style="gap:16px">
        <div style="font-size:40px;text-align:center;padding:8px">{th["icon"]}</div>
        <h3 style="color:#fff;text-align:center;font-size:20px">{n}</h3>
        <p style="color:#94a3b8;text-align:center;font-size:14px">{t} &bull; {city}</p>
        <a href="tel:{ph.replace(' ','').replace('-','')}" class="btn btn-accent" style="text-align:center;justify-content:center">{ph}</a>
        <p style="color:#64748b;font-size:12px;text-align:center">Available for consultations &amp; free estimates</p>
      </div>
    </div>
  </div>
</section>

<!-- CTA BANNER -->
<section class="cta-banner" id="contact">
  <div class="container">
    <h2>Ready to Get Started?</h2>
    <p>Contact us today for a free estimate. No obligation, no pressure — just honest expert advice.</p>
    <div class="cta-actions">
      <a href="tel:{ph.replace(' ','').replace('-','')}" class="btn btn-accent" style="font-size:18px;padding:18px 36px">{th["icon"]} Call Now: {ph}</a>
    </div>
    <span class="phone-big">{ph}</span>
    <p style="margin-top:12px;font-size:14px;opacity:0.7">Licensed &bull; Insured &bull; Free Estimates &bull; Locally Owned</p>
  </div>
</section>

<!-- FOOTER -->
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="logo">{th["icon"]} <span>{n.split()[0]}</span> {" ".join(n.split()[1:]) if len(n.split()) > 1 else ""}</div>
        <p>{th["hero_desc"]}</p>
        <div class="footer-phone" style="margin-top:16px">{ph}</div>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <ul>
          {"".join(f"<li>{s[1]}</li>" for s in th["services"][:4])}
        </ul>
      </div>
      <div class="footer-col">
        <h4>Service Areas</h4>
        <ul>
          {"".join(f"<li>{a}</li>" for a in th["areas"][:5])}
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2025 {n}. All rights reserved.</span>
      <span>Licensed {t} &bull; {city}</span>
    </div>
  </div>
</footer>

</body>
</html>
'''


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "companies")
    os.makedirs(out_dir, exist_ok=True)

    index_cards = []
    all_types = sorted(set(c["type"] for c in COMPANIES))

    for company in COMPANIES:
        slug = slugify(company["name"])
        path = os.path.join(out_dir, f"{slug}.html")
        html = html_page(company)
        with open(path, "w") as f:
            f.write(html)
        print(f"  ✓ {company['name']} → companies/{slug}.html")

        th = get_theme(company["type"])
        index_cards.append(f'''    <div class="company-card" data-type="{company['type']}">
      <div class="company-card-type">{company['type']}</div>
      <h3>{company['name']}</h3>
      <div class="company-card-phone">{th['icon']} {company['phone']}</div>
      <div class="company-card-actions">
        <a href="companies/{slug}.html" class="card-btn card-btn-primary">View Website</a>
        <a href="tel:{company['phone'].replace(' ','').replace('-','')}" class="card-btn card-btn-secondary">Call Now</a>
      </div>
    </div>''')

    filter_btns = '<button class="filter-btn active" data-type="all">All Companies</button>\n    '
    filter_btns += "\n    ".join(
        f'<button class="filter-btn" data-type="{t}">{t}</button>' for t in all_types
    )

    index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Utah Contractor Directory — Website Samples</title>
  <meta name="description" content="Sample websites for local Utah contractors, electricians, plumbers, remodelers, and more." />
  <link rel="stylesheet" href="css/styles.css" />
</head>
<body>

<section class="index-hero">
  <div class="container">
    <h1>Utah Contractor <span style="color:#f59e0b">Directory</span></h1>
    <p>Sample websites for {len(COMPANIES)} local businesses across Utah. Click any company to view their website.</p>
    <div style="display:flex;gap:12px;justify-content:center;margin-top:20px;flex-wrap:wrap">
      <span class="badge">⚡ {len(COMPANIES)} Companies</span>
      <span class="badge">🏅 {len(all_types)} Business Types</span>
      <span class="badge">📍 Utah Based</span>
    </div>
  </div>
</section>

<div style="background:#f8fafc;padding:32px 0 0">
  <div class="container">
    <div class="filter-bar">
    {filter_btns}
    </div>
  </div>
</div>

<div style="background:#f8fafc;padding:0 0 60px">
  <div class="container">
    <div class="company-grid">
{"".join(index_cards)}
    </div>
  </div>
</div>

<footer style="background:#0f172a;color:#64748b;text-align:center;padding:24px;font-size:13px">
  &copy; 2025 Utah Contractor Directory &bull; {len(COMPANIES)} Local Business Website Samples
</footer>

<script src="js/main.js"></script>
</body>
</html>
'''

    with open(os.path.join(os.path.dirname(__file__), "index.html"), "w") as f:
        f.write(index_html)
    print(f"\n  ✓ index.html — directory of all {len(COMPANIES)} companies")
    print(f"\nDone! Generated {len(COMPANIES)} company pages + 1 index page.")


if __name__ == "__main__":
    main()
