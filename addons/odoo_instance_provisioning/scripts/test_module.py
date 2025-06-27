#!/usr/bin/env python3
"""
Quick test script for Odoo Instance Provisioning module
"""

def test_module_structure():
    """Test if module files are in place"""
    import os
    
    base_path = "."
    required_files = [
        "__manifest__.py",
        "__init__.py",
        "models/__init__.py",
        "models/saas_instance.py",
        "models/saas_instance_request.py", 
        "models/saas_instance_log.py",
        "models/res_config_settings.py",
        "controllers/__init__.py",
        "controllers/provisioning_api.py",
        "views/saas_instance_views.xml",
        "views/saas_instance_request_views.xml",
        "views/saas_instance_log_views.xml",
        "views/provisioning_menus.xml",
        "views/provisioning_settings_views.xml",
        "security/ir.model.access.csv",
        "data/cron_data.xml",
        "scripts/create_instance.sh",
        "scripts/backup_instance.sh",
        "scripts/drop_database.sh",
        "README.md"
    ]
    
    print("🔍 Checking module structure...")
    missing_files = []
    
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print("\n❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("\n✅ All required files present!")
    return True


def test_model_names():
    """Test if model names don't conflict"""
    print("\n🔍 Checking model naming for conflicts...")
    
    import re
    
    # Check main model file
    with open("models/saas_instance.py", "r") as f:
        content = f.read()
        
    # Should use new model name
    if "saas.instance.provisioning" in content:
        print("✅ Main model uses non-conflicting name: saas.instance.provisioning")
    else:
        print("❌ Main model name conflict detected!")
        return False
        
    # Check log model file  
    with open("models/saas_instance_log.py", "r") as f:
        content = f.read()
        
    if "saas.instance.provisioning.log" in content:
        print("✅ Log model uses non-conflicting name: saas.instance.provisioning.log")
    else:
        print("❌ Log model name conflict detected!")
        return False
        
    # Check views use correct model names
    with open("views/saas_instance_views.xml", "r") as f:
        content = f.read()
        
    if "saas.instance.provisioning" in content and "saas.instance\"" not in content:
        print("✅ Instance views use correct model name")
    else:
        print("❌ Instance views have model name issues!")
        return False
        
    print("✅ All model names are conflict-free!")
    return True


def test_dependencies():
    """Test if dependencies are available"""
    print("\n🔍 Testing Python dependencies...")
    
    # Test required dependencies
    try:
        import requests
        print("✅ requests library available")
    except ImportError:
        print("❌ requests library missing!")
        return False
        
    try:
        import psycopg2
        print("✅ psycopg2 library available")
    except ImportError:
        print("❌ psycopg2 library missing!")
        return False
    
    # Test optional dependencies
    try:
        import docker
        print("✅ docker library available (optional)")
    except ImportError:
        print("⚠️  docker library missing (optional - some features may not work)")
    
    print("✅ All required dependencies available!")
    return True


def main():
    """Run all tests"""
    print("🚀 Odoo Instance Provisioning Module Tests")
    print("=" * 50)
    
    tests = [
        test_module_structure,
        test_model_names, 
        test_dependencies
    ]
    
    all_passed = True
    
    for test in tests:
        try:
            if not test():
                all_passed = False
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with error: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Module ready for installation.")
        print("\nNext steps:")
        print("1. Install module in Odoo")
        print("2. Configure system parameters") 
        print("3. Test API endpoints")
        print("4. Create test instance")
    else:
        print("❌ Some tests failed. Please fix issues before installing.")
    
    return all_passed


if __name__ == "__main__":
    main()
