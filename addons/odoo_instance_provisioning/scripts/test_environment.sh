#!/bin/bash

# Test script to verify Odoo binary detection and containerized environment handling

set -e

# Set locale
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# Mock environment variables
export PGUSER="odoo"
export PGPASSWORD="odoo"
export PGHOST="db"
export PGPORT="5432"

DB_NAME="test_002_db"
ADMIN_EMAIL="admin@test.com"
ADMIN_PASSWORD="admin"
COMPANY_NAME="Test Company"

# Configuration with detection logic
ODOO_USER="${PGUSER:-odoo}"
ODOO_PASSWORD="${PGPASSWORD:-odoo}"
DB_HOST="${PGHOST:-localhost}"
DB_PORT="${PGPORT:-5432}"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "🧪 Testing Odoo Binary Detection and Environment"
log "================================================="

# Test Odoo binary detection
log "Environment detection:"
log "  PGHOST: $DB_HOST"
log "  Is containerized: $([ -n "$PGHOST" ] && [ "$PGHOST" != "localhost" ] && echo "YES" || echo "NO")"

log ""
log "Odoo binary detection:"

if [ -f "/usr/bin/odoo" ]; then
    ODOO_PATH="/usr/bin"
    ODOO_BIN="odoo"
    ADDONS_PATH="${ADDONS_PATH:-/mnt/extra-addons}"
    log "  ✅ Found Odoo at /usr/bin/odoo (containerized)"
elif [ -f "/opt/odoo/odoo-bin" ]; then
    ODOO_PATH="/opt/odoo"
    ODOO_BIN="odoo-bin"
    ADDONS_PATH="${ADDONS_PATH:-/opt/odoo/addons}"
    log "  ✅ Found Odoo at /opt/odoo/odoo-bin (traditional)"
elif command -v odoo >/dev/null 2>&1; then
    ODOO_PATH=$(dirname $(which odoo))
    ODOO_BIN="odoo"
    ADDONS_PATH="${ADDONS_PATH:-/mnt/extra-addons}"
    log "  ✅ Found Odoo in PATH: $(which odoo)"
else
    ODOO_PATH="${ODOO_PATH:-/opt/odoo}"
    ODOO_BIN="odoo-bin"
    ADDONS_PATH="${ADDONS_PATH:-/opt/odoo/addons}"
    log "  ⚠️  Using default fallback: $ODOO_PATH/$ODOO_BIN"
fi

log ""
log "Final configuration:"
log "  ODOO_PATH: $ODOO_PATH"
log "  ODOO_BIN: $ODOO_BIN"
log "  ADDONS_PATH: $ADDONS_PATH"
log "  Full binary path: $ODOO_PATH/$ODOO_BIN"

log ""
log "Binary existence check:"
if [ -f "$ODOO_PATH/$ODOO_BIN" ]; then
    log "  ✅ Binary exists at $ODOO_PATH/$ODOO_BIN"
elif command -v "$ODOO_BIN" >/dev/null 2>&1; then
    log "  ✅ Binary found in PATH: $(which $ODOO_BIN)"
else
    log "  ❌ Binary NOT found at $ODOO_PATH/$ODOO_BIN"
    log "  ❌ Binary NOT found in PATH"
fi

log ""
log "Database creation strategy:"
if [ -n "$PGHOST" ] && [ "$PGHOST" != "localhost" ]; then
    log "  ✅ Will use SQL CREATE DATABASE (containerized)"
else
    log "  ✅ Will use createdb command (local)"
fi

log ""
log "🎯 Test completed"
