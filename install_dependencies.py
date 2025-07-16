#!/usr/bin/env python3
"""
Setup script for YouTube Automation project
This script helps users set up the environment and dependencies
"""

import subprocess
import sys
import os
import shutil

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print("✅ pip is available")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error: pip is not available")
        return False

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing Python dependencies...")

    # Try different installation methods in order of preference
    install_methods = [
        # Method 1: User space (safest)
        ([sys.executable, "-m", "pip", "install", "--user", "-r", "requirements.txt"],
         "Installing in user space..."),

        # Method 2: System-wide (if user has permissions)
        ([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
         "Installing system-wide..."),

        # Method 3: Override system protection (last resort)
        ([sys.executable, "-m", "pip", "install", "--break-system-packages", "-r", "requirements.txt"],
         "Installing with system override...")
    ]

    for cmd, description in install_methods:
        try:
            print(f"🔄 {description}")
            subprocess.run(cmd, check=True, capture_output=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            continue

    # If all methods fail, provide helpful guidance
    print("❌ All installation methods failed")
    print("\n💡 Manual installation options:")
    print("1. Try: pip install --user pandas pathvalidate yt-dlp")
    print("2. Use system packages: sudo apt install python3-pandas python3-pip")
    print("3. Install yt-dlp separately: pip install --user yt-dlp")
    return False

def check_ytdlp():
    """Check if yt-dlp is available"""
    if shutil.which('yt-dlp'):
        print("✅ yt-dlp found in PATH")
        return True
    else:
        print("⚠️  yt-dlp not found in PATH")
        print("💡 It will be installed with other dependencies")
        return False

def create_sample_excel():
    """Create a sample Excel file if it doesn't exist"""
    if not os.path.exists('video_links.xlsx'):
        print("\n📄 Creating sample video_links.xlsx file...")
        try:
            import pandas as pd

            # Create sample data
            sample_data = {
                'Link': [
                    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    'https://www.youtube.com/shorts/example1',
                    'https://www.youtube.com/shorts/example2'
                ]
            }

            df = pd.DataFrame(sample_data)
            df.to_excel('video_links.xlsx', index=False)
            print("✅ Sample video_links.xlsx created")
            print("   Please replace the sample URLs with your actual YouTube URLs")

        except ImportError:
            print("⚠️  Cannot create sample Excel file (pandas not installed yet)")
            print("   Please create video_links.xlsx manually with a 'Link' column")

def main():
    """Main setup function"""
    print("🚀 YouTube Automation Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check pip
    if not check_pip():
        return False
    
    # Check yt-dlp
    check_ytdlp()
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create sample Excel file
    create_sample_excel()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit video_links.xlsx with your YouTube URLs")
    print("2. Run: python3 download_videos.py")
    print("3. For uploads, set up OAuth credentials (see README.md)")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
