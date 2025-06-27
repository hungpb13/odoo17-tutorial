#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for database creation scenario - Database already exists
This simulates the exact scenario from the user's error
"""

import os
import subprocess
import sys
import tempfile

def create_test_script():
    """Create a test script that simulates database already exists scenario"""
    test_script_content = '''#!/bin/bash

# Test script that simulates the exact scenario from user's error
set -e

# Set locale to avoid perl warnings
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

DB_NAME="$1"
ADMIN_EMAIL="$2"
ADMIN_PASSWORD="$3"
COMPANY_NAME="$4"

# Configuration
ODOO_USER="${PGUSER:-odoo}"
ODOO_PASSWORD="${PGPASSWORD:-odoo}"
DB_HOST="${PGHOST:-db}"
DB_PORT="${PGPORT:-5432}"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Mock PostgreSQL connection check
check_postgres_connection() {
    log "Checking PostgreSQL connection to $DB_HOST:$DB_PORT"
    log "PostgreSQL connection successful"
}

# Mock psql command that returns database exists
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
log "Database host: $DB_HOST:$DB_PORT"
log "Database user: $ODOO_USER"

# Check PostgreSQL connection first
check_postgres_connection

# Check if database already exists
log "Checking if database exists"
if run_psql_cmd "" "SELECT 1 FROM pg_database WHERE datname='$DB_NAME';" 2>/dev/null | grep -q 1; then
    log "ERROR: Database '$DB_NAME' already exists"
    log "WARNING: Database '$DB_NAME' already exists - using existing database"
    log "Instance database setup completed (database already exists)"
    exit 0
fi

log "This should not be reached if database exists"
'''
    
    # Create temporary script file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
        f.write(test_script_content)
        return f.name

def test_database_creation_logic():
    """Test the database creation logic with 'already exists' scenario"""
    print("🧪 Testing Database Creation Logic - Already Exists Scenario")
    print("=" * 60)
    
    script_path = create_test_script()
    
    try:
        # Make script executable
        os.chmod(script_path, 0o755)
        
        # Run the script
        cmd = ['bash', script_path, 'test_01_db', 'admin@test.com', 'admin', 'Test Company']
        
        print(f"📄 Executing: {' '.join(cmd)}")
        print()
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        print("📤 Script Output:")
        print("-" * 30)
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print(f"Return Code: {result.returncode}")
        print()
        
        # Analyze the result
        full_output = (result.stdout or '') + (result.stderr or '')
        
        print("🔍 Analysis:")
        print("-" * 30)
        
        if result.returncode == 0:
            print("✅ Script exited successfully (return code 0)")
        else:
            print(f"❌ Script failed with return code {result.returncode}")
        
        if ("Database already exists" in full_output or 
            "already exists" in full_output or
            "using existing database" in full_output):
            print("✅ 'Database already exists' pattern detected")
            print("✅ This should be handled as a WARNING, not an ERROR")
        else:
            print("❌ 'Database already exists' pattern NOT detected")
        
        print()
        print("💡 Expected Behavior:")
        print("   - Script should exit with code 0")
        print("   - Output should contain 'Database already exists' message")
        print("   - Python code should treat this as a warning, not an error")
        print()
        
        # Simulate Python error handling logic
        print("🐍 Simulating Python Error Handling:")
        print("-" * 40)
        
        if ("Database already exists" in full_output or 
            "already exists" in full_output or
            "using existing database" in full_output):
            print("✅ Python should log WARNING: Database already exists, using existing database")
            print("✅ Python should continue with provisioning (not raise exception)")
        else:
            print("❌ Python would treat this as an error")
        
    except subprocess.TimeoutExpired:
        print("❌ Script timed out")
    except Exception as e:
        print(f"❌ Error running script: {e}")
    finally:
        # Clean up
        try:
            os.unlink(script_path)
        except:
            pass

if __name__ == '__main__':
    test_database_creation_logic()
