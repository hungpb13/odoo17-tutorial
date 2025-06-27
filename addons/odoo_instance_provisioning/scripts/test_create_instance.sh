#!/bin/bash

# Test script to simulate database creation with existing database
# This simulates the scenario where database already exists

set -e

# Set locale
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

DB_NAME="test_db"
ADMIN_EMAIL="admin@test.com"
ADMIN_PASSWORD="password123"
COMPANY_NAME="Test Company"

# Configuration
ODOO_USER="${PGUSER:-odoo}"
ODOO_PASSWORD="${PGPASSWORD:-odoo}"
DB_HOST="${PGHOST:-localhost}"
DB_PORT="${PGPORT:-5432}"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

error_exit() {
    log "ERROR: $1"
    exit 1
}

# Mock function that simulates database already exists
run_psql_cmd() {
    local database="$1"
    local sql_cmd="$2"
    
    # Simulate database exists check
    if [[ "$sql_cmd" == *"pg_database"* ]] && [[ "$sql_cmd" == *"datname"* ]]; then
        echo "1"  # Simulate database exists
        return 0
    fi
    
    return 0
}

log "Starting instance creation for database: $DB_NAME"

# Check if database already exists (this should trigger the early exit)
log "Checking if database exists"
if run_psql_cmd "" "SELECT 1 FROM pg_database WHERE datname='$DB_NAME';" 2>/dev/null | grep -q 1; then
    log "WARNING: Database '$DB_NAME' already exists - using existing database"
    log "Instance database setup completed (database already exists)"
    exit 0
fi

log "This should not be reached if database exists"
