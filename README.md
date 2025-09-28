# Sleep Monitoring - Breathing Rate Detection

A real-time breathing rate monitoring system using computer vision and signal processing techniques.

## Features

- **Non-contact monitoring**: Uses camera to detect chest movements
- **Real-time analysis**: Live breathing rate calculation
- **Web interface**: Desktop and mobile-friendly UI
- **Quality control**: Advanced algorithms to ensure data reliability
- **Adaptive detection**: Works with various breathing patterns

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

## Installation

### Prerequisites
- Python 3.8+
- OpenCV
- NumPy
- SciPy
- Flask

### Setup
```bash
# Install dependencies
pip install -r breathing_monitor/python_version/requirements.txt

# Run the application
cd breathing_monitor/python_version
python minimal_monitor.py
```

## Usage

### Desktop Interface
- Open `http://localhost:5000` in your browser
- Position camera to view chest area
- Click "Start Monitoring" to begin detection
- View real-time breathing rate and video feed

### Mobile Interface
- Open `https://localhost:5000/mobile` (HTTPS required for camera access)
- Grant camera permissions when prompted
- Use touch-friendly interface for monitoring

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

## File Structure

```
breathing_monitor/
├── python_version/
│   ├── minimal_monitor.py      # Main application
│   ├── requirements.txt        # Dependencies
│   ├── templates/
│   │   ├── minimal.html       # Desktop interface
│   │   └── mobile.html        # Mobile interface
│   └── generate_ssl.sh        # SSL certificate generator
└── README.md                  # Project documentation
```

## Research References

1. **Gaussian Smoothing**: Standard practice in biomedical signal processing
2. **Adaptive Thresholding**: Based on respiratory monitoring research
3. **Peak Detection**: Validated algorithms for breathing detection
4. **Quality Control**: Statistical methods for data reliability

## License

This project is for educational and research purposes.

## Contributing

Please ensure all changes maintain the research-based approach and include proper documentation for algorithm choices.
