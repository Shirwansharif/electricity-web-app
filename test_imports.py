#!/usr/bin/env python3
"""
Simple test to verify the application structure and imports
"""

import sys
import os

def test_file_structure():
    """Test if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js',
        '.gitignore'
    ]
    
    print("Testing file structure...")
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    else:
        print("\n✅ All required files present!")
        return True

def test_python_syntax():
    """Test Python file syntax"""
    print("\nTesting Python syntax...")
    try:
        with open('app.py', 'r') as f:
            code = f.read()
            compile(code, 'app.py', 'exec')
        print("✅ app.py syntax is valid!")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in app.py: {e}")
        return False

def test_html_structure():
    """Test if HTML file has required elements"""
    print("\nTesting HTML structure...")
    try:
        with open('templates/index.html', 'r') as f:
            html = f.read()
        
        required_elements = [
            'uploadForm',
            'webcam',
            'recognizeForm',
            'Bootstrap',
            'app.js'
        ]
        
        all_present = all(elem in html for elem in required_elements)
        
        if all_present:
            print("✅ HTML structure looks good!")
            return True
        else:
            print("❌ Some required HTML elements missing")
            return False
    except Exception as e:
        print(f"❌ Error reading HTML: {e}")
        return False

def main():
    print("=" * 60)
    print("Face Recognition System - Structure Test")
    print("=" * 60)
    
    results = []
    results.append(test_file_structure())
    results.append(test_python_syntax())
    results.append(test_html_structure())
    
    print("\n" + "=" * 60)
    if all(results):
        print("🎉 All tests passed! Application structure is ready.")
        print("=" * 60)
        return 0
    else:
        print("❌ Some tests failed. Please review the issues above.")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
