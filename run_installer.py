#!/usr/bin/env python3
"""
Sleep Monitoring Breathing Rate Detection - Installer Script
Automated installation and setup for the breathing monitor application.
"""

import os
import sys
import subprocess
import platform
import webbrowser
import time

def print_banner():
    """Print installation banner"""
    print("=" * 60)
    print("🌬️  Sleep Monitoring - Breathing Rate Detection")
    print("=" * 60)
    print("Automated Installation Script")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please install Python 3.8 or higher from https://python.org")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_camera():
    """Check if camera is available"""
    print("🔍 Checking camera availability...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✅ Camera detected and working")
                return True
            else:
                print("⚠️  Camera detected but not accessible")
                return False
        else:
            print("❌ No camera detected")
            return False
    except ImportError:
        print("⚠️  OpenCV not installed - will install during setup")
        return True
    except Exception as e:
        print(f"⚠️  Camera check failed: {e}")
        return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    requirements = [
        "Flask==2.3.3",
        "opencv-python==4.8.1.78",
        "numpy==1.24.3",
        "scipy==1.11.3",
        "Werkzeug==2.3.7"
    ]
    
    for package in requirements:
        try:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"   ✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")
            return False
    
    return True

def create_desktop_shortcut():
    """Create desktop shortcut (Windows)"""
    if platform.system() == "Windows":
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "Breathing Monitor.lnk")
            target = os.path.join(os.getcwd(), "breathing_monitor", "python_version", "minimal_monitor.py")
            wDir = os.path.join(os.getcwd(), "breathing_monitor", "python_version")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
            print("✅ Desktop shortcut created")
        except ImportError:
            print("⚠️  Desktop shortcut creation skipped (optional dependencies not available)")
        except Exception as e:
            print(f"⚠️  Desktop shortcut creation failed: {e}")

def create_start_script():
    """Create start script for easy launching"""
    script_content = f"""#!/bin/bash
# Sleep Monitoring - Breathing Rate Detection
# Start script for easy launching

cd "{os.path.join(os.getcwd(), 'breathing_monitor', 'python_version')}"
python minimal_monitor.py
"""
    
    script_path = "start_breathing_monitor.sh"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make executable on Unix systems
    if platform.system() != "Windows":
        os.chmod(script_path, 0o755)
    
    print(f"✅ Start script created: {script_path}")

def create_batch_file():
    """Create Windows batch file for easy launching"""
    if platform.system() == "Windows":
        batch_content = f"""@echo off
echo Starting Sleep Monitoring - Breathing Rate Detection...
cd /d "{os.path.join(os.getcwd(), 'breathing_monitor', 'python_version')}"
python minimal_monitor.py
pause
"""
        
        batch_path = "start_breathing_monitor.bat"
        with open(batch_path, 'w') as f:
            f.write(batch_content)
        
        print(f"✅ Batch file created: {batch_path}")

def test_installation():
    """Test if the installation works"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        import flask
        import cv2
        import numpy as np
        import scipy
        print("✅ All dependencies imported successfully")
        
        # Test camera access
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✅ Camera access test passed")
            else:
                print("⚠️  Camera access test failed")
        else:
            print("⚠️  Camera not accessible")
        
        return True
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def show_usage_instructions():
    """Show usage instructions"""
    print("\n" + "=" * 60)
    print("🎉 Installation Complete!")
    print("=" * 60)
    print("\n📱 How to use:")
    print("1. Run the application:")
    print("   python breathing_monitor/python_version/minimal_monitor.py")
    print("\n2. Open your browser:")
    print("   Desktop: http://localhost:5000")
    print("   Mobile:  https://localhost:5000/mobile")
    print("\n3. Position your chest in the camera view")
    print("4. Click 'Start Monitoring'")
    print("5. Wait for results (30+ seconds recommended)")
    
    print("\n🔧 Quick Start:")
    if platform.system() == "Windows":
        print("   Double-click: start_breathing_monitor.bat")
    else:
        print("   Run: ./start_breathing_monitor.sh")
    
    print("\n📚 Documentation:")
    print("   README.md - Complete documentation")
    print("   INSTALLATION.md - Detailed installation guide")
    print("   WEB_ARCHITECTURE.md - Technical details")
    
    print("\n🌐 Web Interface:")
    print("   Desktop: http://localhost:5000")
    print("   Mobile:  https://localhost:5000/mobile")
    
    print("\n" + "=" * 60)

def main():
    """Main installation process"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check camera
    check_camera()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed")
        sys.exit(1)
    
    # Create shortcuts and scripts
    create_start_script()
    if platform.system() == "Windows":
        create_batch_file()
        create_desktop_shortcut()
    
    # Test installation
    if not test_installation():
        print("⚠️  Installation test failed, but you can still try running the application")
    
    # Show usage instructions
    show_usage_instructions()
    
    # Ask if user wants to start the application
    try:
        response = input("\n🚀 Would you like to start the application now? (y/n): ").lower()
        if response in ['y', 'yes']:
            print("\n🌬️ Starting Sleep Monitoring...")
            print("Opening browser in 3 seconds...")
            time.sleep(3)
            
            # Start the application
            app_path = os.path.join("breathing_monitor", "python_version", "minimal_monitor.py")
            subprocess.Popen([sys.executable, app_path])
            
            # Open browser
            time.sleep(2)
            webbrowser.open("http://localhost:5000")
            
    except KeyboardInterrupt:
        print("\n👋 Installation complete. You can start the application later.")
    except Exception as e:
        print(f"\n⚠️  Could not start application automatically: {e}")
        print("You can start it manually using the instructions above.")

if __name__ == "__main__":
    main()
