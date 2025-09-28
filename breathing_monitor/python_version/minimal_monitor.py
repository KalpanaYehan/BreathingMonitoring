#!/usr/bin/env python3
import cv2
import numpy as np
import time
from flask import Flask, render_template, jsonify, request
import threading
from scipy.signal import find_peaks
import ssl
import os

class MinimalBreathingMonitor:
    def __init__(self):
        self.cap = None
        self.breathing_data = []
        self.timestamps = []
        self.is_monitoring = False
        self.start_time = None
        
        # Very minimal settings
        self.sample_rate = 5  # Hz (5 samples per second for accuracy)
        self.max_data_points = 1000  # Keep more data points for higher frequency
        
        print("✅ Minimal Breathing Monitor initialized")
    
    def start_monitoring(self):
        if self.is_monitoring:
            return False
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)  # Very small
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)  # Very small
        self.cap.set(cv2.CAP_PROP_FPS, 10)  # 10 FPS for higher accuracy
        
        self.is_monitoring = True
        self.start_time = time.time()
        self.breathing_data = []
        self.timestamps = []
        
        # Start monitoring
        threading.Thread(target=self._monitor_loop, daemon=True).start()
        print("🚀 Minimal monitoring started")
        return True
    
    def stop_monitoring(self):
        self.is_monitoring = False
        
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None
        
        # Calculate respiration rate
        respiration_rate = self.calculate_respiration_rate()
        
        print("⏹️ Monitoring stopped")
        if respiration_rate is not None and respiration_rate != "N/A":
            print(f"📊 Respiration Rate: {respiration_rate:.1f} breaths/min")
        elif respiration_rate == "N/A":
            print("📊 Respiration Rate: N/A (insufficient or irregular data)")
        
        return respiration_rate
    
    def _monitor_loop(self):
        while self.is_monitoring:
            try:
                if not self.cap or not self.cap.isOpened():
                    time.sleep(1)
                    continue
                
                ret, frame = self.cap.read()
                if ret:
                    # Use improved breathing detection
                    brightness = self.simple_breathing_detection(frame)
                    if brightness is not None:
                        self.breathing_data.append(float(brightness))
                        self.timestamps.append(time.time() - self.start_time)
                        
                        # Keep only recent data
                        if len(self.breathing_data) > self.max_data_points:
                            self.breathing_data.pop(0)
                            self.timestamps.pop(0)
                        
                        print(f"Data: {brightness:.1f}")
                
                # Higher frequency sampling for accuracy
                time.sleep(1.0 / self.sample_rate)  # 0.2 seconds between samples (5 Hz)
                
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(2)
    
    def simple_breathing_detection(self, frame):
        """Very sensitive breathing detection - amplifies small changes"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Get average brightness in even smaller center region for more sensitivity
            h, w = gray.shape
            center_region = gray[h//4:3*h//4, w//4:3*w//4]  # Even smaller region (1/2 instead of 1/3)
            brightness = np.mean(center_region)
            
            # Amplify small changes for better sensitivity
            # Normalize to 0-10 range and amplify subtle changes
            normalized_brightness = (brightness / 255.0) * 10
            
            # Apply amplification to make small changes more visible
            # This will make breathing patterns much more apparent
            amplified_brightness = normalized_brightness * 5  # Amplify by 2x
            
            return amplified_brightness
            
        except Exception as e:
            print(f"Detection error: {e}")
            return None
    
    def calculate_respiration_rate(self):
        """Calculate respiration rate from breathing data using improved peak detection"""
        try:
            if len(self.breathing_data) < 20:  # Need at least 20 data points
                print("⚠️ Insufficient data for respiration rate calculation")
                return None
            
            # Convert to numpy array for processing
            data = np.array(self.breathing_data)
            timestamps = np.array(self.timestamps)
            
            # Check data variation first
            data_range = np.max(data) - np.min(data)
            print(f"📊 Data range: {data_range:.3f} (min: {np.min(data):.3f}, max: {np.max(data):.3f})")
            
            if data_range < 0.1:  # Very small variation
                print("⚠️ Data variation too small for reliable peak detection")
                return None
            
            # Apply lighter smoothing for subtle variations
            from scipy.ndimage import gaussian_filter1d
            smoothed_data = gaussian_filter1d(data, sigma=0.5)  # Reduced from 1.0 to 0.5
            
            # Calculate adaptive thresholds based on data characteristics
            data_mean = np.mean(smoothed_data)
            data_std = np.std(smoothed_data)
            
            # Use relative height threshold (mean + small percentage of std)
            height_threshold = data_mean + (0.1 * data_std)  # Much more sensitive
            
            # Use much smaller prominence for subtle variations
            prominence_threshold = max(0.02, data_std * 0.3)  # Adaptive prominence
            
            print(f"📊 Adaptive thresholds - Height: {height_threshold:.3f}, Prominence: {prominence_threshold:.3f}")
            
            # Find peaks with adjusted parameters
            peaks, properties = find_peaks(smoothed_data, 
                                         height=height_threshold,
                                         distance=2,  # Reduced from 3 to 2 (0.4 seconds)
                                         prominence=prominence_threshold)
            
            # Convert peak positions to timestamps
            peak_times = timestamps[peaks]
            print(f"📊 Found {len(peaks)} peaks at timestamps: {peak_times}")
            
            if len(peaks) < 2:
                print("⚠️ Not enough breathing cycles detected")
                # Try with even more relaxed parameters
                peaks, _ = find_peaks(smoothed_data, 
                                    height=data_mean,  # Just above mean
                                    distance=1,  # Minimum distance
                                    prominence=0.01)  # Very small prominence
                print(f"📊 Relaxed search found {len(peaks)} peaks")
                
                if len(peaks) < 2:
                    return None
            
            # Quality control: Need at least 5 peaks for reliable breathing rate calculation
            if len(peaks) < 5:
                print(f"⚠️ Insufficient peaks for reliable calculation: {len(peaks)} peaks (need ≥5)")
                return "N/A"
            
            # Calculate time between peaks
            peak_times = timestamps[peaks]
            time_intervals = np.diff(peak_times)
            
            print(f"📊 Time intervals between peaks: {time_intervals}")
            
            # Check for irregular breathing patterns (missing peaks)
            if len(time_intervals) >= 3:  # Need at least 3 intervals to detect irregularity
                # Calculate coefficient of variation (CV) to detect irregularity
                mean_interval = np.mean(time_intervals)
                std_interval = np.std(time_intervals)
                cv = std_interval / mean_interval if mean_interval > 0 else 0
                
                print(f"📊 Interval analysis - Mean: {mean_interval:.2f}s, Std: {std_interval:.2f}s, CV: {cv:.3f}")
                
                # If coefficient of variation > 0.3, breathing is irregular (missing peaks)
                if cv > 0.3:
                    print("⚠️ Irregular breathing pattern detected - possible missing peaks")
                    return "N/A"
                
                # Check for outliers (intervals that are significantly different)
                # An interval is an outlier if it's more than 2 standard deviations from the mean
                outliers = np.abs(time_intervals - mean_interval) > (2 * std_interval)
                outlier_count = np.sum(outliers)
                
                if outlier_count > 0:
                    print(f"⚠️ {outlier_count} irregular intervals detected - possible missing peaks")
                    return "N/A"
            
            # Filter out unrealistic intervals (relaxed constraints)
            # Allow wider range for subtle breathing patterns
            valid_intervals = time_intervals[(time_intervals >= 2.0) & (time_intervals <= 8.0)]
            
            if len(valid_intervals) < 1:
                print("⚠️ No valid breathing intervals found")
                return None
            
            # Calculate average breathing interval
            avg_interval = np.mean(valid_intervals)
            
            # Convert to breaths per minute
            respiration_rate = 60.0 / avg_interval
            
            print(f"📊 Calculated respiration rate: {respiration_rate:.1f} breaths/min")
            
            # Validate result (relaxed range: 6-40 breaths/min)
            if 6 <= respiration_rate <= 40:
                return respiration_rate
            else:
                print(f"⚠️ Respiration rate {respiration_rate:.1f} outside normal range (6-40)")
                return None
                
        except Exception as e:
            print(f"Respiration rate calculation error: {e}")
            return None
    
    def get_data(self):
        return {
            'breathing_data': self.breathing_data,
            'timestamps': self.timestamps,
            'is_monitoring': self.is_monitoring,
            'data_count': len(self.breathing_data)
        }
    
    def cleanup(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()

# Flask app initialization
app = Flask(__name__)

# Global instance
monitor = MinimalBreathingMonitor()

@app.route('/')
def index():
    return render_template('minimal.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

@app.route('/api/start', methods=['POST'])
def start():
    success = monitor.start_monitoring()
    return jsonify({'success': success})

@app.route('/api/stop', methods=['POST'])
def stop():
    respiration_rate = monitor.stop_monitoring()
    return jsonify({
        'success': True, 
        'respiration_rate': respiration_rate
    })

@app.route('/api/data')
def get_data():
    return jsonify(monitor.get_data())

@app.route('/api/data_point', methods=['POST'])
def receive_data_point():
    """Receive data points from mobile interface and print to terminal"""
    try:
        data = request.get_json()
        brightness = data.get('brightness', 0)
        timestamp = data.get('timestamp', 0)
        
        # Print data point to terminal with formatting
        print(f"📊 Mobile Data Point: Brightness={brightness:.3f}, Time={timestamp:.1f}s")
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"❌ Error receiving data point: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/video_feed')
def video_feed():
    """Video streaming route for camera view"""
    def generate():
        while True:
            try:
                if monitor.cap and monitor.cap.isOpened():
                    ret, frame = monitor.cap.read()
                    if ret:
                        # Resize frame for web display
                        frame = cv2.resize(frame, (320, 240))
                        
                        # Add breathing detection region indicator
                        h, w = frame.shape[:2]
                        # Draw rectangle around the breathing detection region
                        cv2.rectangle(frame, 
                                    (w//3, h//3), 
                                    (2*w//3, 2*h//3), 
                                    (0, 255, 0), 2)  # Green rectangle
                        
                        # Add text label
                        cv2.putText(frame, 'Breathing Region', 
                                  (w//3, h//3 - 10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                        
                        # Convert to JPEG for web streaming
                        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                        if ret:
                            frame_bytes = buffer.tobytes()
                            yield (b'--frame\r\n'
                                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                
                # Control frame rate to prevent overwhelming the system
                time.sleep(0.1)  # 10 FPS for video feed
                
            except Exception as e:
                print(f"Video feed error: {e}")
                time.sleep(0.1)
    
    return app.response_class(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    try:
        print("🌬️ Minimal Breathing Monitor")
        print("📱 Desktop: http://localhost:5000")
        print("📱 Mobile: http://localhost:5000/mobile")
        print("🔒 HTTPS Mobile: https://localhost:5000/mobile")
        print("⏹️  Press Ctrl+C to stop")
        
        # Check if SSL certificates exist for HTTPS
        cert_file = 'cert.pem'
        key_file = 'key.pem'
        
        if os.path.exists(cert_file) and os.path.exists(key_file):
            print("🔒 SSL certificates found. Starting HTTPS server...")
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.load_cert_chain(cert_file, key_file)
            app.run(host='0.0.0.0', port=5000, debug=False, threaded=True, ssl_context=context)
        else:
            print("⚠️  SSL certificates not found. Starting HTTP server...")
            print("   For mobile camera access, you'll need HTTPS.")
            print("   Generate certificates with: openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes")
            app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    finally:
        monitor.cleanup()
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
