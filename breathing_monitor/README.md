# 🌬️ Minimal Breathing Monitor

A high-precision, camera-based breathing monitoring system designed for WiFi research validation.

## ✨ Features

- **Ultra-sensitive breathing detection** with 0-10 Y-axis range
- **High-frequency sampling** at 5 Hz (5 samples per second)
- **Live camera view** with positioning guide
- **Real-time breathing graph** with dynamic scaling
- **Professional UI** optimized for research use
- **Resource efficient** - camera only active when monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Webcam/camera
- Modern web browser

### Installation
```bash
cd breathing_monitor/python_version
pip install -r requirements.txt
```

### Run the Application
```bash
python3 minimal_monitor.py
```

### Access the Interface
Open your browser to: `http://localhost:5000`

## 📱 How to Use

1. **Start Monitoring**: Click "Start Monitoring" button
2. **Position Yourself**: Ensure your chest is within the green rectangle in the camera view
3. **Stay Still**: Minimize movement for best results
4. **Breathe Normally**: Watch the real-time breathing graph
5. **Stop Monitoring**: Click "Stop Monitoring" when done

## 🔬 Technical Details

- **Sampling Rate**: 5 Hz (5 samples per second)
- **Data Points**: Up to 100 samples (20 seconds of data)
- **Detection Method**: Brightness variation analysis in chest region
- **Amplification**: 2x amplification for enhanced sensitivity
- **Chart Updates**: Real-time updates every 1 second

## 🎯 Perfect for WiFi Research

- **Ground truth validation** for WiFi-based breathing detection
- **High temporal resolution** for detailed pattern analysis
- **Quantifiable data** for correlation studies
- **Real-time feedback** for immediate validation

## 🛠️ Architecture

- **Backend**: Python Flask with OpenCV
- **Frontend**: HTML5 + Chart.js + JavaScript
- **Computer Vision**: OpenCV for camera processing
- **Signal Processing**: NumPy for mathematical operations
- **Real-time**: Multi-threaded architecture

## 📊 Data Output

The system provides:
- Real-time breathing pattern visualization
- Timestamped data points
- Amplified brightness values (0-10 range)
- Dynamic Y-axis scaling for optimal visibility

## 🔧 Troubleshooting

- **Camera not working**: Ensure camera is not used by other applications
- **Graph not updating**: Check browser console for JavaScript errors
- **Poor sensitivity**: Adjust positioning within the green rectangle
- **Performance issues**: Close other applications using the camera

## 📝 License

This project is designed for research and educational purposes.

---

**Built for WiFi-based breathing detection research validation** 🌬️📡
