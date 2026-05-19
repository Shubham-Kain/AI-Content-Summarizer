#!/usr/bin/env python
"""
Dependency installer script for AI Content Summarizer
Run this script to install all required dependencies
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install all dependencies from requirements.txt"""
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    print("=" * 60)
    print("🚀 Installing AI Content Summarizer Dependencies")
    print("=" * 60)
    print()
    
    requirements_file = os.path.join(project_dir, "requirements.txt")
    
    if not os.path.exists(requirements_file):
        print(f"❌ Error: requirements.txt not found at {requirements_file}")
        sys.exit(1)
    
    print(f"📦 Requirements file: {requirements_file}")
    print()
    
    try:
        print("⏳ Installing packages...")
        print("-" * 60)
        
        # Run pip install
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file],
            capture_output=False
        )
        
        print("-" * 60)
        
        if result.returncode == 0:
            print()
            print("✅ All dependencies installed successfully!")
            print()
            print("📝 Next steps:")
            print("  1. Create a .env file with your API keys:")
            print("     GOOGLE_GEMINI_API_KEY=your-key-here")
            print("     OPENAI_API_KEY=your-key-here")
            print()
            print("  2. Run the application:")
            print("     streamlit run app.py")
            print()
            return 0
        else:
            print()
            print("❌ Installation failed. Please check the errors above.")
            return 1
            
    except Exception as e:
        print(f"❌ Error during installation: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(install_dependencies())
