
FROM python:3

ENV PYTHONUNBUFFERED 1 
RUN mkdir /app

WORKDIR /app

ADD . /app


COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt 

COPY . /app

CMD ["python", "manage.py", "runserver", "localhost:8011"]





# # Use Python 3.11 slim image as base
# FROM python:3.11-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# ENV PYTHONPATH=/app

# # Set work directory
# WORKDIR /app

# # Install system dependencies
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#         postgresql-client \
#         build-essential \
#         libpq-dev \
#         gcc \
#         python3-dev \
#         curl \
#     && rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir --upgrade pip \
#     && pip install --no-cache-dir -r requirements.txt

# # Copy project
# COPY . .

# # Create non-root user
# RUN useradd --create-home --shell /bin/bash app \
#     && chown -R app:app /app
# USER app

# # Collect static files
# RUN python manage.py collectstatic --noinput

# # Create directory for Gunicorn logs
# RUN mkdir -p /app/logs

# # Expose port
# EXPOSE 8010

# # Health check
# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#     CMD curl -f http://localhost:8010/ || exit 1

# # Run the application
# CMD ["gunicorn", "--config", "gunicorn.conf.py", "eduloop.wsgi:application"]
