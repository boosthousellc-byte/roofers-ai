FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY audit_engine.py server.py ./

ENV PORT=8080

EXPOSE 8080

CMD gunicorn server:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60
