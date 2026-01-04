#!/usr/bin/env python3
"""
Create release package for Sleep Monitoring Breathing Rate Detection
"""

import os
import shutil
import zipfile
import tarfile
from datetime import datetime

def create_release_package():
    """Create release package"""
    print("📦 Creating release package...")
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version = "1.0.0"
    
    # Create release directory
    release_dir = f"sleep-monitoring-breathing-v{version}"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # Copy application files
    files_to_copy = [
        "breathing_monitor/",
        "README.md",
        "INSTALLATION.md",
        "WEB_ARCHITECTURE.md",
        "DEPLOYMENT_FULL.md",
        "requirements.txt",
        "setup.py",
        "run_installer.py",
        ".gitignore"
    ]
    
    for item in files_to_copy:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.copytree(item, os.path.join(release_dir, item))
            else:
                shutil.copy2(item, release_dir)
            print(f"✅ Copied {item}")
    
    # Create installation script
    install_script = f"""#!/bin/bash
# Sleep Monitoring - Breathing Rate Detection
# Installation script for {version}

echo "🌬️ Sleep Monitoring - Breathing Rate Detection"
echo "Version: {version}"
echo "Installation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

echo "✅ Python 3 detected"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Make scripts executable
chmod +x run_installer.py

echo ""
echo "🎉 Installation complete!"
echo ""
echo "To start the application:"
echo "  python3 run_installer.py"
echo ""
echo "Or run directly:"
echo "  python3 breathing_monitor/python_version/minimal_monitor.py"
"""
    
    with open(os.path.join(release_dir, "install.sh"), 'w') as f:
        f.write(install_script)
    
    # Make executable
    os.chmod(os.path.join(release_dir, "install.sh"), 0o755)
    
    # Create Windows batch file
    install_bat = f"""@echo off
echo 🌬️ Sleep Monitoring - Breathing Rate Detection
echo Version: {version}
echo Installation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python detected

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

echo.
echo 🎉 Installation complete!
echo.
echo To start the application:
echo   python run_installer.py
echo.
echo Or run directly:
echo   python breathing_monitor/python_version/minimal_monitor.py
pause
"""
    
    with open(os.path.join(release_dir, "install.bat"), 'w') as f:
        f.write(install_bat)
    
    # Create README for release
    release_readme = f"""# Sleep Monitoring - Breathing Rate Detection v{version}

## 🚀 Quick Start

### Windows:
1. Double-click `install.bat`
2. Follow the instructions
3. Run `python run_installer.py`

### macOS/Linux:
1. Run `chmod +x install.sh && ./install.sh`
2. Follow the instructions
3. Run `python3 run_installer.py`

## 📱 Usage

1. **Start the application:**
   ```bash
   python breathing_monitor/python_version/minimal_monitor.py
   ```

2. **Open in browser:**
   - Desktop: http://localhost:5000
   - Mobile: https://localhost:5000/mobile

3. **Position your chest in the camera view**

4. **Click "Start Monitoring"**

5. **Wait for results (30+ seconds recommended)**

## 🔧 Features

- ✅ Real-time breathing rate detection
- ✅ Advanced signal processing algorithms
- ✅ Quality control and validation
- ✅ Desktop and mobile interfaces
- ✅ Research-based methodology
- ✅ Complete privacy (local processing only)

## 📚 Documentation

- `README.md` - Complete project documentation
- `INSTALLATION.md` - Detailed installation guide
- `WEB_ARCHITECTURE.md` - Technical architecture details

## 🆘 Support

- GitHub Issues: Report bugs and request features
- Documentation: Check README.md for details
- Community: Join discussions on GitHub

## 📄 License

This project is for educational and research purposes.

---
**Version:** {version}  
**Release Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Python Required:** 3.8+
"""
    
    with open(os.path.join(release_dir, "RELEASE_README.md"), 'w') as f:
        f.write(release_readme)
    
    print(f"✅ Release package created: {release_dir}")
    return release_dir

def create_zip_package(release_dir):
    """Create ZIP package"""
    zip_filename = f"{release_dir}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, os.path.dirname(release_dir))
                zipf.write(file_path, arc_path)
    
    print(f"✅ ZIP package created: {zip_filename}")
    return zip_filename

def create_tar_package(release_dir):
    """Create TAR package"""
    tar_filename = f"{release_dir}.tar.gz"
    
    with tarfile.open(tar_filename, 'w:gz') as tar:
        tar.add(release_dir, arcname=os.path.basename(release_dir))
    
    print(f"✅ TAR package created: {tar_filename}")
    return tar_filename

def main():
    """Main function"""
    print("🌬️ Sleep Monitoring - Release Package Creator")
    print("=" * 50)
    
    # Create release package
    release_dir = create_release_package()
    
    # Create compressed packages
    zip_file = create_zip_package(release_dir)
    tar_file = create_tar_package(release_dir)
    
    print("\n🎉 Release packages created successfully!")
    print(f"📁 Directory: {release_dir}")
    print(f"📦 ZIP file: {zip_file}")
    print(f"📦 TAR file: {tar_file}")
    
    print("\n📤 Ready for distribution:")
    print("1. Upload to GitHub Releases")
    print("2. Share download links")
    print("3. Users can download and install locally")
    
    print(f"\n📋 Package contents:")
    for root, dirs, files in os.walk(release_dir):
        level = root.replace(release_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")

if __name__ == "__main__":
    main()
