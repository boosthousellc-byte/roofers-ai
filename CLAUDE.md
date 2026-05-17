# CLAUDE.md — Roofers-AI

## Project Overview

B2B website audit and lead generation tool targeting local contractors (roofers, electricians, plumbers, etc.) in Utah. Audits contractor websites for SEO, mobile-friendliness, SSL, and more — then generates PDF reports and powers SMS outreach campaigns.

## Tech Stack

- **Backend:** Python 3.10, Flask 3.0+, Flask-CORS
- **Frontend:** Vanilla HTML/CSS/JavaScript (no frameworks)
- **PDF Generation:** ReportLab 4.0+
- **SMS:** Twilio SDK
- **HTTP Client:** Requests 2.28+
- **Deployment:** DigitalOcean (backend via gunicorn), Vercel (frontend)

## Repository Structure

```
├── audit_engine.py          # Core audit logic — 13 check functions + scoring
├── server.py                # Flask API server (port 8080)
├── generate.py              # Sample company website generator
├── generate_outreach.py     # Outreach template + leads.csv generator
├── sms_outreach.py          # Twilio SMS campaign sender
├── test_audit_engine.py     # pytest test suite (14 tests)
├── requirements.txt         # pip dependencies
├── environment.yml          # Conda environment spec
├── .env.example             # Env var template (Twilio credentials)
├── index.html               # Company directory page
├── audit-frontend/          # Frontend audit tool (Vercel-deployable SPA)
├── funnel/                  # Client acquisition funnel pages
├── companies/               # 51 generated HTML company websites
├── outreach/                # Outreach email/SMS templates
├── leads.csv                # Lead tracking data
└── .github/workflows/       # CI/CD (lint + test on push, PyPI publish on release)
```

## Commands

### Run the API server
```bash
python server.py                    # Dev mode, port 8080
gunicorn server:app --bind 0.0.0.0:8080 --workers 2  # Production
```

### Run a CLI audit
```bash
python audit_engine.py --url <url> --business <name> --city <city> --industry <type> --generate-pdf
```

### Run tests
```bash
pytest
```

### Lint
```bash
flake8 . --max-complexity=10 --max-line-length=127
```

### Generate sample sites
```bash
python generate.py
python generate_outreach.py
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/industries` | List available industry profiles |
| POST | `/api/audit` | Run audit, return JSON (`{url, business, city, industry}`) |
| POST | `/api/audit/pdf` | Run audit, return PDF file |

## Testing

- Framework: **pytest** (14 tests in `test_audit_engine.py`)
- Tests cover all 13 audit checks plus industry profile validation
- CI runs `flake8` then `pytest` on every push via GitHub Actions
- Always run `pytest` before pushing changes

## Code Conventions

- **Python style:** snake_case functions/variables, SCREAMING_SNAKE_CASE constants
- **Max line length:** 127 characters
- **Max complexity:** 10 (flake8)
- **Docstrings:** Required on all functions and modules
- **No type hints** — the codebase does not use them; don't introduce them
- **Optional imports:** Wrap optional dependencies (reportlab, twilio) in try/except
- **HTML parsing:** Uses regex and string matching, not BeautifulSoup/lxml
- **Frontend:** Vanilla JS only — no frameworks, no jQuery, no build tools
- **CSS:** Dark theme by default, CSS custom properties for theming

## Environment Variables

```
PORT=8080                    # API server port (default: 8080)
TWILIO_ACCOUNT_SID=...       # Twilio credentials (for SMS outreach)
TWILIO_AUTH_TOKEN=...
TWILIO_FROM_NUMBER=+1...
AI_API_KEY=...               # Optional AI-powered recommendations
```

## CI/CD

- **On push:** Lint (flake8) + test (pytest) via conda on ubuntu-latest / Python 3.10
- **On release:** Build and publish to PyPI via trusted publishing
- Config: `.github/workflows/python-package-conda.yml` and `python-publish.yml`

## Architecture Notes

- No database — leads stored in CSV and localStorage
- Audit engine is stateless: fetch HTML → run checks → return scores
- Scoring uses industry-specific weights (defined in `INDUSTRY_PROFILES`)
- Grade scale: A+ (95+), A (90+), B+ (80+), B (70+), C (60+), D (50+), F (<50)
- Frontend and backend are fully decoupled (CORS enabled)
