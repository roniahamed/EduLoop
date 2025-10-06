# Dockerfile

# --- Stage 1: The Builder ---
FROM python:3.11-buster AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- পরিবর্তন #১: একটি WORKDIR সেট করুন ---
WORKDIR /app

# ভার্চয়াল এনভায়রনমেন্ট তৈরি করুন
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# শুধুমাত্র requirements.txt কপি করুন
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# এখন বাকি সব কোড কপি করুন
COPY . .


# --- Stage 2: The Runner ---
FROM python:3.11-slim-buster AS runner

WORKDIR /app

# builder স্টেজ থেকে venv কপি করুন
COPY --from=builder /opt/venv /opt/venv

# --- পরিবর্তন #২: সঠিক পাথ থেকে কোড কপি করুন ---
# builder-এর WORKDIR থেকে কোড কপি করুন
COPY --from=builder /app /app

ENV PATH="/opt/venv/bin:$PATH"

RUN python manage.py collectstatic --no-input

RUN adduser --system --group django
RUN chown -R django:django /app
USER django

EXPOSE 8020

CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8020", "eduloop.wsgi:application"]