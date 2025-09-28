# Mobile Breathing Monitor

This is a mobile-optimized version of the breathing monitor that works directly with your iPhone camera.

## Features

- 📱 **Mobile-optimized interface** designed for iPhone Safari
- 📹 **Direct camera access** using getUserMedia API
- 🔒 **HTTPS support** for secure camera access
- 📊 **Real-time breathing pattern visualization**
- 🎯 **Automatic respiration rate calculation**
- 📐 **Responsive design** that works in portrait and landscape

## Setup Instructions

### 1. Generate SSL Certificates (Required for Mobile)

For iPhone camera access, you need HTTPS. Generate SSL certificates:

```bash
cd breathing_monitor/python_version
./generate_ssl.sh
```

This creates `cert.pem` and `key.pem` files needed for HTTPS.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python minimal_monitor.py
```

The server will start and show:
- Desktop interface: `http://localhost:5000`
- Mobile interface: `https://localhost:5000/mobile`

## Using on iPhone

### 1. Access the Mobile Interface

1. Make sure your iPhone is on the same network as your computer
2. Find your computer's IP address (e.g., `192.168.1.100`)
3. Open Safari on your iPhone
4. Go to: `https://YOUR_IP_ADDRESS:5000/mobile`

### 2. Accept SSL Certificate

Since we're using self-signed certificates:
1. Safari will show a security warning
2. Tap "Advanced"
3. Tap "Proceed to [your-ip-address]"

### 3. Allow Camera Access

1. When prompted, tap "Allow" to give camera access
2. Position your chest in the green box
3. Stay still and breathe normally
4. Watch the breathing pattern chart
5. Tap "Stop" when you have enough data

## Mobile Interface Features

### Camera View
- **Green box overlay** shows the breathing detection area
- **Position your chest** within the green box for best results
- **Front camera** is used by default for self-monitoring

### Breathing Detection
- **Real-time data collection** at 5 Hz (5 samples per second)
- **Automatic brightness analysis** of the chest region
- **Amplified signal processing** to detect subtle breathing changes

### Chart Visualization
- **Fixed 60-second time window** for consistent viewing
- **Real-time updates** showing breathing patterns
- **Responsive design** that adapts to screen orientation

### Respiration Rate Analysis
- **Automatic peak detection** to identify breathing cycles
- **Smart filtering** to remove unrealistic intervals
- **Normal range validation** (6-40 breaths per minute)
- **Status indicators** showing if breathing is normal, slow, or elevated

## Troubleshooting

### Camera Not Working
- Ensure you're using HTTPS (not HTTP)
- Check that camera permissions are granted
- Try refreshing the page
- Make sure you're using Safari (other browsers may have limitations)

### SSL Certificate Issues
- Accept the self-signed certificate when prompted
- If issues persist, regenerate certificates: `./generate_ssl.sh`

### Network Access
- Ensure your iPhone and computer are on the same WiFi network
- Check firewall settings on your computer
- Try accessing via `localhost` if testing on the same device

### Poor Detection
- Ensure good lighting
- Stay relatively still
- Position chest clearly in the green box
- Avoid sudden movements or talking
- Monitor for at least 30 seconds for accurate results

## Technical Details

### Browser Compatibility
- **Safari on iOS**: Full support with camera access
- **Chrome on Android**: Should work with camera access
- **Desktop browsers**: Limited camera access without HTTPS

### Data Processing
- **Sampling rate**: 5 Hz (200ms intervals)
- **Detection region**: Center 1/3 of camera frame
- **Signal processing**: Brightness normalization and amplification
- **Peak detection**: Local maxima with adaptive thresholds

### Security
- **HTTPS required** for camera access on mobile
- **Self-signed certificates** for development/testing
- **Local network only** - no data sent to external servers

## Development Notes

The mobile interface uses:
- **getUserMedia API** for camera access
- **Canvas API** for frame capture and analysis
- **Chart.js** for real-time visualization
- **Responsive CSS** for mobile optimization
- **Progressive Web App** features for better mobile experience

For production use, consider:
- Using proper SSL certificates from a trusted CA
- Implementing user authentication
- Adding data persistence
- Optimizing for different screen sizes
- Adding offline capabilities

