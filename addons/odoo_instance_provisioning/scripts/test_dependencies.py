#!/usr/bin/env python3
"""
Quick test script to check if all dependencies are available
Usage: python test_dependencies.py
"""

def test_dependencies():
    """Test if all required dependencies are available"""
    print("🔍 Testing Odoo Instance Provisioning dependencies...")
    print("=" * 50)
    
    # Required dependencies
    required = [
        ('psycopg2', 'PostgreSQL adapter'),
        ('requests', 'HTTP library'),
    ]
    
    # Optional dependencies
    optional = [
        ('docker', 'Docker API client'),
    ]
    
    all_good = True
    
    print("📦 Required dependencies:")
    for module, description in required:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"❌ {module} - {description} (MISSING)")
            all_good = False
    
    print("\n📦 Optional dependencies:")
    for module, description in optional:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"⚠️  {module} - {description} (optional, not installed)")
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 All required dependencies are available!")
        print("You can now install the Odoo module.")
    else:
        print("❌ Some required dependencies are missing.")
        print("Please install them using:")
        print("  pip install psycopg2-binary requests --user")
    
    return all_good

if __name__ == "__main__":
    test_dependencies()
