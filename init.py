#!/usr/bin/env python3
"""Initialize the website project structure and install dependencies"""

import os
import subprocess
import sys

def setup_project():
    # Get the current directory
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Create directories
    directories = [
        'templates',
        'templates/components',
        'static',
        'static/css',
        'static/js',
        'db',
    ]
    
    print("🔨 Creating directory structure...")
    for dir_path in directories:
        full_path = os.path.join(base_path, dir_path)
        os.makedirs(full_path, exist_ok=True)
        print(f"  ✓ Created: {dir_path}")
    
    # Install requirements
    print("\n📦 Installing Python dependencies...")
    requirements_file = os.path.join(base_path, 'requirements.txt')
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
        print("  ✓ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error installing dependencies: {e}")
        return False
    
    print("\n✅ Project setup complete!")
    print(f"\nTo start the server, run:")
    print(f"  python app.py")
    print(f"\nThen open: http://localhost:5000")
    
    return True

if __name__ == '__main__':
    success = setup_project()
    sys.exit(0 if success else 1)
