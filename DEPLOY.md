# Deployment Guide

## 1. Install Dependencies (Local Testing)

```bash
pip install reportlab requests flask flask-cors gunicorn
```

## 2. Test Locally

### Run an audit from the CLI:
```bash
python audit_engine.py --url https://example.com --business "Test" --city "Your City" --industry dentist --generate-pdf
```

### Run the API server locally:
```bash
python server.py
```
Then open `audit-frontend/index.html` in your browser (or serve it with `python -m http.server 3000 --directory audit-frontend`).

## 3. Deploy Frontend to Vercel (Free)

```bash
cd audit-frontend
npx vercel --prod
```

After deploy, update `API_BASE` in `audit-frontend/index.html` to point to your backend URL.

## 4. Deploy Backend to DigitalOcean ($4/mo Droplet)

```bash
# On your droplet:
sudo apt update && sudo apt install python3-pip -y
pip3 install reportlab requests flask flask-cors gunicorn

# Clone repo and run:
gunicorn server:app --bind 0.0.0.0:8080 --workers 2

# For production, use systemd or supervisor to keep it running.
# Set up nginx as reverse proxy with SSL (Let's Encrypt).
```

## 5. Add AI API Key (Optional Enhancement)

Set `AI_API_KEY` environment variable for AI-powered content recommendations.
Budget: ~$5-15/month covers ~100 audits.

## 6. Start Running Audits

Use the audit tool + Loom to record walkthroughs of audit results.
Send the Loom + PDF to prospects from the playbook templates.
