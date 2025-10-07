#!/bin/bash

# EduLoop Production Monitoring Script
# Use this to check the status of automated cleanup jobs

LOG_DIR="/home/roni/Desktop/Eduloop/logs"
CLEANUP_LOG="$LOG_DIR/cleanup.log"
ERROR_LOG="$LOG_DIR/cleanup_error.log"

echo "=== EduLoop Production Cleanup Status ==="
echo "Date: $(date)"
echo ""

# Check if cleanup script ran today
if [ -f "$CLEANUP_LOG" ]; then
    TODAY=$(date '+%Y-%m-%d')
    if grep -q "$TODAY" "$CLEANUP_LOG"; then
        echo " Daily cleanup ran today"
        echo "Last successful run:"
        grep "$TODAY.*completed successfully" "$CLEANUP_LOG" | tail -1
    else
        echo "Daily cleanup did NOT run today"
    fi
else
    echo "No cleanup log found"
fi

echo ""

# Check for recent errors
if [ -f "$ERROR_LOG" ]; then
    ERROR_COUNT=$(wc -l < "$ERROR_LOG")
    if [ $ERROR_COUNT -gt 0 ]; then
        echo "Found $ERROR_COUNT errors in error log"
        echo "Recent errors:"
        tail -3 "$ERROR_LOG"
    else
        echo " No errors in error log"
    fi
else
    echo "No error log found (good)"
fi

echo ""

# Check current session count
cd /home/roni/Desktop/Eduloop
source env/bin/activate 2>/dev/null
TOTAL_SESSIONS=$(python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduloop.settings')
django.setup()
from django.contrib.sessions.models import Session
from django.utils import timezone
total = Session.objects.count()
expired = Session.objects.filter(expire_date__lt=timezone.now()).count()
print(f'Total: {total}, Expired: {expired}')
" 2>/dev/null || echo "Unable to check")
deactivate 2>/dev/null

echo " Current session status: $TOTAL_SESSIONS"

echo ""

# Check disk usage
DISK_USAGE=$(df /home/roni/Desktop/Eduloop | tail -1 | awk '{print $5}')
echo " Disk usage: $DISK_USAGE"

# Check memory usage  
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.0f%%", $3/$2 * 100.0}')
echo "Memory usage: $MEMORY_USAGE"

echo ""

# Check cron job status
echo " Cron job status:"
crontab -l | grep -E "(cleanup|maintenance)" | wc -l | xargs echo "Active cleanup jobs:"

echo ""
echo "=== End Status Report ==="