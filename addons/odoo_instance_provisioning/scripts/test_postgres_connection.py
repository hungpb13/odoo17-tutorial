#!/usr/bin/env python3
"""
Test script to verify PostgreSQL connection for Docker Compose setup
"""

import os
import sys
import subprocess

def test_docker_compose_postgres():
    """Test PostgreSQL connection in Docker Compose environment"""
    print("🚀 Testing PostgreSQL Connection for Docker Compose")
    print("=" * 60)
    
    # Check if we're in a Docker environment
    if os.path.exists('/.dockerenv'):
        print("✅ Running inside Docker container")
        # In Docker, PostgreSQL is accessible via 'db' hostname
        os.environ['PGHOST'] = 'db'
        os.environ['PGPORT'] = '5432'
        os.environ['PGUSER'] = 'odoo'
        os.environ['PGPASSWORD'] = 'odoo'
    else:
        print("🏠 Running on host machine")
        # On host, PostgreSQL is accessible via localhost:5432 (if port forwarded)
        os.environ['PGHOST'] = 'localhost'
        os.environ['PGPORT'] = '5432'
        os.environ['PGUSER'] = 'odoo'
        os.environ['PGPASSWORD'] = 'odoo'
    
    print(f"Testing connection to: {os.environ['PGHOST']}:{os.environ['PGPORT']}")
    
    # Test with psql if available
    try:
        result = subprocess.run([
            'psql', '-d', 'postgres', '-c', 'SELECT version();'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Direct psql connection successful")
            print(f"PostgreSQL version: {result.stdout.strip()}")
        else:
            print("❌ Direct psql connection failed")
            print(f"Error: {result.stderr}")
            
    except FileNotFoundError:
        print("⚠️  psql command not found, trying Python connection")
    except Exception as e:
        print(f"❌ psql test failed: {e}")
    
    # Test with Python psycopg2
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.environ['PGHOST'],
            port=os.environ['PGPORT'],
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'],
            database='postgres'
        )
        
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        
        print("✅ Python psycopg2 connection successful")
        print(f"PostgreSQL version: {version}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except ImportError:
        print("❌ psycopg2 not available")
        return False
    except Exception as e:
        print(f"❌ Python connection failed: {e}")
        return False

def test_check_postgres_script():
    """Test the check_postgres.sh script"""
    print("\n🔍 Testing check_postgres.sh script")
    print("-" * 40)
    
    script_path = os.path.join(os.path.dirname(__file__), 'check_postgres.sh')
    
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run([
            'bash', script_path
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ check_postgres.sh script passed")
            print("Output:")
            print(result.stdout)
            return True
        else:
            print("❌ check_postgres.sh script failed")
            print("Error:")
            print(result.stderr or result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ Script test failed: {e}")
        return False

def main():
    """Main test function"""
    print("Testing Odoo Instance Provisioning - PostgreSQL Connection")
    print("=" * 70)
    
    success = True
    
    # Test direct connection
    if not test_docker_compose_postgres():
        success = False
    
    # Test script
    if not test_check_postgres_script():
        success = False
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 All PostgreSQL connection tests passed!")
        print("Module should work correctly with your Docker Compose setup.")
    else:
        print("❌ Some tests failed. Please check PostgreSQL configuration.")
        print("\nTroubleshooting:")
        print("1. Ensure PostgreSQL container is running: docker ps | grep postgres")
        print("2. Check Docker Compose services: docker-compose ps")
        print("3. Verify environment variables in docker-compose.yml")
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
