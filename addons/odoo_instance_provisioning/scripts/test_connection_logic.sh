#!/bin/bash

# Test script to verify PostgreSQL connection logic
# This simulates the exact scenario from the user's error

set -e

# Set locale
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# Mock environment to simulate container
export PGUSER="odoo"
export PGPASSWORD="odoo"
export PGHOST="db"
export PGPORT="5432"

DB_NAME="test_001_db"
ADMIN_EMAIL="admin@test.com"
ADMIN_PASSWORD="admin"
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

# Mock PostgreSQL commands that simulate container environment
run_psql_cmd() {
    local database="$1"
    local sql_cmd="$2"
    
    log "Mock psql command - database: '$database', sql: '$sql_cmd'"
    
    # Simulate different scenarios
    if [ -z "$database" ] || [ "$database" = "postgres" ]; then
        log "✅ Connecting to postgres database for administrative operations"
        return 0
    elif [ "$database" = "odoo" ]; then
        log "❌ ERROR: database 'odoo' does not exist"
        return 1
    else
        log "✅ Connecting to specific database: $database"
        return 0
    fi
}

run_postgres_cmd() {
    local cmd="$1"
    log "Mock postgres command: $cmd"
    
    if [[ "$cmd" == *"createdb"* ]]; then
        log "✅ Database creation would succeed"
        return 0
    fi
    return 0
}

check_postgres_connection() {
    log "Checking PostgreSQL connection to $DB_HOST:$DB_PORT"
    log "PostgreSQL connection successful"
}

log "🧪 Testing PostgreSQL Connection Logic"
log "======================================"

log "Starting instance creation for database: $DB_NAME"
log "Database host: $DB_HOST:$DB_PORT"
log "Database user: $ODOO_USER"

# Check PostgreSQL connection first
check_postgres_connection

# Check if database already exists
log "Checking if database exists"
if run_psql_cmd "" "SELECT 1 FROM pg_database WHERE datname='$DB_NAME';" 2>/dev/null; then
    log "WARNING: Database '$DB_NAME' already exists - using existing database"
    exit 0
fi

# Create PostgreSQL database
log "Creating PostgreSQL database: $DB_NAME"
run_postgres_cmd "createdb '$DB_NAME'" || error_exit "Failed to create database"

# Grant privileges to Odoo user - this is where the error occurred
log "Granting privileges to Odoo user"
if run_psql_cmd "" "GRANT ALL PRIVILEGES ON DATABASE \"$DB_NAME\" TO $ODOO_USER;"; then
    log "✅ Privileges granted successfully"
else
    error_exit "Failed to grant privileges"
fi

log "✅ All steps completed successfully"
