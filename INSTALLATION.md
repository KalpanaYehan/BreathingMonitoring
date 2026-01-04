# Sleep Monitoring - Installation Guide

## 📦 Local Installation (Recommended)

This breathing monitor is designed to run locally on your computer for optimal performance and privacy.

## 🚀 Quick Installation

### **Option 1: Direct Download (Easiest)**

1. **Download the application:**
   ```bash
   git clone https://github.com/yourusername/sleep-monitoring-breathing-detection.git
   cd sleep-monitoring-breathing-detection
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python breathing_monitor/python_version/minimal_monitor.py
   ```

### **Option 2: Python Package Installation**

1. **Install from source:**
   ```bash
   pip install -e .
   ```

2. **Run the application:**
   ```bash
   breathing-monitor
   ```

## 🔧 System Requirements

### **Operating Systems:**
- ✅ **Windows 10/11**
- ✅ **macOS 10.15+**
- ✅ **Linux (Ubuntu 18.04+)**

### **Hardware Requirements:**
- **Camera**: Built-in or USB webcam
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB free space
- **CPU**: Any modern processor

### **Software Requirements:**
- **Python 3.8+**
- **Camera drivers** (usually pre-installed)
- **Internet connection** (for initial setup only)

## 📱 Installation Methods

### **Method 1: GitHub Release (Recommended)**

1. **Go to GitHub Releases:**
   - Visit: `https://github.com/yourusername/sleep-monitoring-breathing-detection/releases`
   - Download the latest release

2. **Extract and run:**
   ```bash
   unzip sleep-monitoring-breathing-v1.0.0.zip
   cd sleep-monitoring-breathing-v1.0.0
   python breathing_monitor/python_version/minimal_monitor.py
   ```

### **Method 2: Git Clone**

```bash
git clone https://github.com/yourusername/sleep-monitoring-breathing-detection.git
cd sleep-monitoring-breathing-detection
pip install -r requirements.txt
python breathing_monitor/python_version/minimal_monitor.py
```

### **Method 3: PyPI Installation (Future)**

```bash
pip install sleep-monitoring-breathing
breathing-monitor
```

## 🖥️ Platform-Specific Instructions

### **Windows Installation:**

1. **Install Python:**
   - Download from [python.org](https://python.org)
   - Check "Add Python to PATH" during installation

2. **Install OpenCV:**
   ```cmd
   pip install opencv-python
   ```

3. **Run the application:**
   ```cmd
   python breathing_monitor/python_version/minimal_monitor.py
   ```

### **macOS Installation:**

1. **Install Python:**
   ```bash
   brew install python
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python breathing_monitor/python_version/minimal_monitor.py
   ```

### **Linux Installation:**

1. **Install Python and dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv breathing-monitor-env
   source breathing-monitor-env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python breathing_monitor/python_version/minimal_monitor.py
   ```

## 🔒 Security Considerations

### **Privacy Benefits:**
- ✅ **All data stays local** - No cloud processing
- ✅ **No internet required** - Works offline
- ✅ **No data transmission** - Complete privacy
- ✅ **Local processing** - Full control over data

### **Camera Permissions:**
- **Windows**: May prompt for camera access
- **macOS**: May prompt for camera access
- **Linux**: Usually works without prompts

## 🚀 Usage Instructions

### **Desktop Interface:**
1. **Open browser**: `http://localhost:5000`
2. **Position camera**: Point at your chest
3. **Click "Start Monitoring"**
4. **Wait for results**: Monitor for 30+ seconds
5. **View breathing rate**: Results appear automatically

### **Mobile Interface:**
1. **Open browser**: `https://localhost:5000/mobile`
2. **Grant camera permission**: When prompted
3. **Position phone**: Point at your chest
4. **Start monitoring**: Touch-friendly interface
5. **View results**: Real-time breathing rate

## 🔧 Troubleshooting

### **Common Issues:**

#### **Camera not detected:**
```bash
# Check camera permissions
# Restart the application
# Try different camera (if available)
```

#### **OpenCV installation issues:**
```bash
# Windows
pip install opencv-python-headless

# macOS
brew install opencv
pip install opencv-python

# Linux
sudo apt install python3-opencv
```

#### **Port already in use:**
```bash
# Change port in minimal_monitor.py
app.run(host='0.0.0.0', port=5001)
```

### **Performance Issues:**

#### **Slow processing:**
- **Close other applications**
- **Ensure good lighting**
- **Position camera properly**
- **Check system resources**

#### **Inaccurate results:**
- **Ensure good lighting**
- **Stay still during monitoring**
- **Monitor for longer periods**
- **Check camera positioning**

## 📊 Features

### **Core Functionality:**
- ✅ **Real-time breathing detection**
- ✅ **Advanced signal processing**
- ✅ **Quality control algorithms**
- ✅ **Statistical validation**
- ✅ **Mobile and desktop interfaces**
- ✅ **Professional web interface**

### **Technical Features:**
- ✅ **Gaussian smoothing** (σ=0.5)
- ✅ **Adaptive thresholding**
- ✅ **Peak detection algorithms**
- ✅ **Irregular pattern detection**
- ✅ **Physiological range validation**
- ✅ **Research-based algorithms**

## 🎯 Advantages of Local Installation

### **Performance:**
- **No network delays** - Instant processing
- **Full system resources** - Maximum performance
- **Real-time monitoring** - No latency
- **Offline operation** - No internet required

### **Privacy:**
- **Local data only** - Nothing leaves your computer
- **No cloud processing** - Complete privacy
- **No data transmission** - Secure monitoring
- **Full control** - You own your data

### **Reliability:**
- **No server dependencies** - Always works
- **No internet issues** - Offline operation
- **No platform limitations** - Full functionality
- **No deployment complexity** - Simple installation

## 📞 Support

### **Getting Help:**
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check README.md for details
- **Community**: Join discussions on GitHub

### **System Information:**
When reporting issues, include:
- **Operating System**: Windows/macOS/Linux version
- **Python Version**: `python --version`
- **Camera Type**: Built-in/USB webcam
- **Error Messages**: Complete error output

## 🎉 Ready to Use!

Once installed, your breathing monitor provides:
- **Professional-grade** breathing rate detection
- **Research-based** algorithms
- **Quality control** for reliable results
- **Beautiful interfaces** for desktop and mobile
- **Complete privacy** with local processing

**Start monitoring your breathing with confidence!**





