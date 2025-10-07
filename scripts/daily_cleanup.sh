#!/bin/bash

# Production-grade Daily cleanup script for Eduloop project
# This script cleans expired sessions, optimizes database and maintains logs
# Created: $(date)
# Version: 1.0

# Exit on any error
set -e

# Production environment variables
PROJECT_DIR="/home/roni/Desktop/Eduloop"
VENV_DIR="/home/roni/Desktop/Eduloop/env"
LOG_DIR="/home/roni/Desktop/Eduloop/logs"
LOG_FILE="$LOG_DIR/cleanup.log"
ERROR_LOG="$LOG_DIR/cleanup_error.log"
LOCK_FILE="$PROJECT_DIR/cleanup.lock"

# Email notification settings (optional)
ADMIN_EMAIL="admin@eduloop.com"  # Change this to your email
SEND_EMAIL_ON_ERROR=false  # Set to true if you want email notifications

# Function to log with timestamp
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

# Function to log errors
log_error() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR: $1" | tee -a $ERROR_LOG $LOG_FILE
    if [ "$SEND_EMAIL_ON_ERROR" = true ]; then
        echo "Cleanup script error: $1" | mail -s "EduLoop Cleanup Error" $ADMIN_EMAIL 2>/dev/null || true
    fi
}

# Function to cleanup and exit
cleanup_and_exit() {
    rm -f $LOCK_FILE
    log_message "Cleanup script finished."
    exit $1
}

# Trap to ensure cleanup on exit
trap 'cleanup_and_exit $?' EXIT

# Check if script is already running
if [ -f $LOCK_FILE ]; then
    PID=$(cat $LOCK_FILE)
    if ps -p $PID > /dev/null 2>&1; then
        log_error "Cleanup script is already running (PID: $PID)"
        exit 1
    else
        log_message "Removing stale lock file"
        rm -f $LOCK_FILE
    fi
fi

# Create lock file
echo $$ > $LOCK_FILE

log_message "Starting production-grade daily cleanup..."

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    log_error "Project directory not found: $PROJECT_DIR"
    exit 1
fi

# Check if virtual environment exists
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    log_error "Virtual environment not found: $VENV_DIR"
    exit 1
fi

# Change to project directory
cd $PROJECT_DIR || {
    log_error "Failed to change to project directory: $PROJECT_DIR"
    exit 1
}

# Activate virtual environment
source $VENV_DIR/bin/activate || {
    log_error "Failed to activate virtual environment"
    exit 1
}

# Check Django management command availability
if ! python manage.py help clearsessions >/dev/null 2>&1; then
    log_error "Django clearsessions command not available"
    exit 1
fi

# Clean expired sessions with detailed logging
log_message "Cleaning expired sessions..."
SESSION_COUNT_BEFORE=$(python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduloop.settings')
django.setup()
from django.contrib.sessions.models import Session
from django.utils import timezone
print(Session.objects.filter(expire_date__lt=timezone.now()).count())
" 2>/dev/null || echo "0")

python manage.py clearsessions >> $LOG_FILE 2>&1

if [ $? -eq 0 ]; then
    SESSION_COUNT_AFTER=$(python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduloop.settings')
django.setup()
from django.contrib.sessions.models import Session
print(Session.objects.count())
" 2>/dev/null || echo "0")
    
    DELETED_SESSIONS=$((SESSION_COUNT_BEFORE))
    log_message "Session cleanup completed successfully. Deleted $DELETED_SESSIONS expired sessions. Total remaining: $SESSION_COUNT_AFTER"
else
    log_error "Session cleanup failed"
    exit 1
fi

# Database optimization (PostgreSQL)
log_message "Optimizing database..."
python manage.py dbshell << 'EOF' >> $LOG_FILE 2>&1 || log_error "Database optimization failed"
ANALYZE;
VACUUM (ANALYZE, VERBOSE);
EOF

if [ $? -eq 0 ]; then
    log_message "Database optimization completed successfully"
fi

# Clean old log files (keep last 30 days)
log_message "Cleaning old log files..."
CLEANED_LOGS=$(find $LOG_DIR -name "*.log" -type f -mtime +30 2>/dev/null | wc -l)
find $LOG_DIR -name "*.log" -type f -mtime +30 -delete 2>/dev/null || true
log_message "Cleaned $CLEANED_LOGS old log files"

# Clean old backup files if any (keep last 7 days)
if [ -d "$PROJECT_DIR/backups" ]; then
    log_message "Cleaning old backup files..."
    CLEANED_BACKUPS=$(find $PROJECT_DIR/backups -name "*.sql" -type f -mtime +7 2>/dev/null | wc -l)
    find $PROJECT_DIR/backups -name "*.sql" -type f -mtime +7 -delete 2>/dev/null || true
    log_message "Cleaned $CLEANED_BACKUPS old backup files"
fi

# Check disk space
DISK_USAGE=$(df $PROJECT_DIR | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 85 ]; then
    log_error "Disk usage is high: ${DISK_USAGE}%"
fi

# Check memory usage
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
log_message "System memory usage: ${MEMORY_USAGE}%"

# Generate daily report
TOTAL_SESSIONS=$(python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduloop.settings')
django.setup()
from django.contrib.sessions.models import Session
print(Session.objects.count())
" 2>/dev/null || echo "0")

log_message "Daily cleanup summary: Sessions remaining: $TOTAL_SESSIONS, Disk usage: ${DISK_USAGE}%, Memory usage: ${MEMORY_USAGE}%"

# Deactivate virtual environment
deactivate

log_message "Production cleanup completed successfully."