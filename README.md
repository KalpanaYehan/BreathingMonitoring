# Sleep Monitoring - Breathing Rate Detection

A real-time breathing rate monitoring system using computer vision and signal processing techniques. **Designed for local installation** to ensure privacy and optimal performance.

## Features

- **Non-contact monitoring**: Uses camera to detect chest movements
- **Real-time analysis**: Live breathing rate calculation
- **Local processing**: Complete privacy - all data stays on your computer
- **Web interface**: Desktop and mobile-friendly UI
- **Quality control**: Advanced algorithms to ensure data reliability
- **Adaptive detection**: Works with various breathing patterns
- **Easy installation**: Simple setup with automated installer

## Technical Implementation

### Signal Processing
- **Gaussian smoothing** (σ=0.5) for noise reduction
- **Adaptive thresholding** based on signal characteristics
- **Peak detection** with prominence and distance parameters
- **Statistical validation** for irregular breathing patterns

### Quality Control
- **Minimum 5 peaks** required for reliable calculation
- **Coefficient of variation** analysis for irregularity detection
- **Outlier detection** for missing peaks
- **Physiological range validation** (6-40 breaths/min)

### Research Foundation
Based on established research in respiratory monitoring:
- "Non-Contact Monitoring of Breathing Pattern and Respiratory Rate via RGB Signal Measurement" (PMC6631485)
- "Advancements in Methods and Camera-Based Sensors for the Quantification of Respiration" (PMC7766256)
- "Sensing Systems for Respiration Monitoring: A Technical Systematic Review" (PMC7570710)

## 🚀 Quick Installation

```bash
# Run the application
python breathing_monitor/python_version/minimal_monitor.py
```

## 📱 Usage

1. **Start the application:**
   ```bash
   python breathing_monitor/python_version/minimal_monitor.py
   ```

2. **Open in browser:**
   - Desktop: http://localhost:5000

3. **Position your chest in the camera view**

4. **Click "Start Monitoring"**

5. **Wait for results (30+ seconds recommended)**

## Usage

### Desktop Interface
- Open `http://localhost:5000` in your browser
- Position camera to view chest area
- Click "Start Monitoring" to begin detection
- View real-time breathing rate and video feed


## Algorithm Details

### Peak Detection Parameters
- **Distance**: 2 data points (0.4 seconds minimum between peaks)
- **Prominence**: Adaptive threshold (30% of signal variation)
- **Height**: Mean + 10% of standard deviation

### Quality Control Metrics
- **Coefficient of Variation**: < 0.3 for regular patterns
- **Outlier Detection**: 2 standard deviations from mean
- **Minimum Data**: 5 peaks for reliable calculation

### Signal Processing
- **Sampling Rate**: 5 Hz (5 samples per second)
- **Smoothing**: Gaussian filter (σ=0.5)
- **Region of Interest**: Center 50% of frame

