#!/usr/bin/env python3
import cv2
import numpy as np
import time
from datetime import datetime
from flask import Flask, render_template, jsonify, request
import threading
from scipy.signal import find_peaks
import ssl
import os

class MinimalBreathingMonitor:
    def __init__(self, camera_index=None):
        self.cap = None
        self.camera_index = camera_index  # None=auto-detect, 0=laptop camera, 1=external webcam, etc.
        self.breathing_data = []
        self.timestamps = []
        self.is_monitoring = False
        self.start_time = None
        self.try_index = 0  # Track the number of monitoring sessions
        self.output_file = None  # File handle for writing data
        
        # Very minimal settings
        self.sample_rate = 5  # Hz (5 samples per second for accuracy)
        self.max_data_points = 1000  # Keep more data points for higher frequency
        
        # Detect available cameras if not specified
        if self.camera_index is None:
            self.camera_index = self._find_available_camera()
        
        print(f"✅ Minimal Breathing Monitor initialized (using camera {self.camera_index})")
    
    def _find_available_camera(self):
        """Find the first available camera, preferring external webcams"""
        print("🔍 Detecting available cameras...")
        
        # Try indices 0-5 to find cameras that can actually read frames
        available_cameras = []
        camera_names = {}
        
        for i in range(5):
            try:
                # Check if this camera exists in sysfs first
                try:
                    with open(f'/sys/class/video4linux/video{i}/name', 'r') as f:
                        name = f.read().strip()
                        camera_names[i] = name
                        print(f"   🔍 Found video{i}: {name}")
                except:
                    continue  # Skip if device doesn't exist
                
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    # Some cameras (especially USB) need significant time to initialize
                    ret, frame = False, None
                    is_usb = 'usb' in name.lower()
                    
                    print(f"      Testing camera {i} (USB={is_usb})...")
                    
                    if is_usb:
                        # USB cameras often need a "warm-up" - grab frames to flush buffer
                        print(f"      Warming up USB camera (grabbing frames)...")
                        for warmup in range(5):
                            cap.grab()  # Grab without retrieving
                        time.sleep(1)  # Give it a moment
                        
                        # Now try to read actual frames
                        for attempt in range(15):  # More attempts
                            ret, frame = cap.read()
                            if ret and frame is not None:
                                print(f"      ✓ Success on attempt {attempt + 1}")
                                break
                            if attempt < 5:
                                time.sleep(0.1)  # Quick retries first
                            else:
                                time.sleep(1.0)  # Slower retries after
                            print(f"      Attempt {attempt + 1} failed, retrying...")
                    else:
                        # Built-in cameras usually work quickly
                        for attempt in range(3):
                            ret, frame = cap.read()
                            if ret and frame is not None:
                                print(f"      ✓ Success on attempt {attempt + 1}")
                                break
                            time.sleep(0.3)
                    
                    if ret and frame is not None:
                        backend = cap.getBackendName()
                        available_cameras.append(i)
                        print(f"   ✓ Camera {i}: {camera_names[i]} (backend: {backend})")
                    else:
                        camera_type = "USB camera" if is_usb else "camera"
                        print(f"   ✗ Camera {i}: Can't read frames from {camera_type}")
                    cap.release()
                else:
                    cap.release()
                    print(f"   ✗ Camera {i}: Failed to open")
                
                # Wait a bit between cameras to avoid conflicts
                time.sleep(0.2)
                
            except Exception as e:
                print(f"   ✗ Camera {i}: Error - {e}")
        
        if not available_cameras:
            print("   ⚠️  No cameras detected! Defaulting to index 0")
            return 0
        
        print(f"\n📷 Found {len(available_cameras)} working camera(s): {available_cameras}")
        
        # Prefer external USB camera over integrated camera
        for cam_idx in available_cameras:
            cam_name = camera_names.get(cam_idx, "").lower()
            if 'usb' in cam_name or 'external' in cam_name or 'webcam' in cam_name:
                print(f"   → Using camera {cam_idx} (external USB webcam: {camera_names[cam_idx]})")
                return cam_idx
        
        # If no USB camera found, prefer higher index (usually external)
        if len(available_cameras) > 1:
            preferred_camera = available_cameras[-1]  # Use last camera (often external)
            print(f"   → Using camera {preferred_camera} ({camera_names.get(preferred_camera, 'Unknown')})")
            return preferred_camera
        else:
            # Only one camera available, use it
            preferred_camera = available_cameras[0]
            print(f"   → Using camera {preferred_camera} ({camera_names.get(preferred_camera, 'Only camera')})")
            return preferred_camera
    
    def start_monitoring(self):
        if self.is_monitoring:
            return False
        
        # Initialize camera (already validated during detection, so should be fast)
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            print(f"❌ Failed to open camera {self.camera_index}")
            return False
        
        # Don't apply custom resolution/FPS - use camera defaults for better compatibility
        # This prevents issues with USB cameras that don't support specific resolutions
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        
        print(f"✓ Camera initialized: {width}x{height} @ {fps}fps")
        
        self.is_monitoring = True
        self.start_time = time.time()
        self.breathing_data = []
        self.timestamps = []
        
        # Create output file with format: Try_(index)_(starttime).txt
        self.try_index += 1
        start_time_str = datetime.fromtimestamp(self.start_time).strftime('%Y%m%d_%H%M%S')
        filename = f"Try_{self.try_index}_{start_time_str}.txt"
        self.output_file = open(filename, 'w')
        print(f"📝 Writing data to: {filename}")
        
        # Start monitoring
        threading.Thread(target=self._monitor_loop, daemon=True).start()
        print("🚀 Minimal monitoring started")
        return True
    
    def stop_monitoring(self):
        self.is_monitoring = False
        
        # Close output file
        if self.output_file:
            self.output_file.close()
            self.output_file = None
            print("📝 Data file closed")
        
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
                        current_time = time.time()
                        current_timestamp = current_time - self.start_time
                        self.breathing_data.append(float(brightness))
                        self.timestamps.append(current_timestamp)
                        
                        # Keep only recent data
                        if len(self.breathing_data) > self.max_data_points:
                            self.breathing_data.pop(0)
                            self.timestamps.pop(0)
                        
                        # Write data to file with actual time
                        if self.output_file:
                            actual_time_str = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Include milliseconds
                            self.output_file.write(f"{actual_time_str},{brightness:.1f}\n")
                            self.output_file.flush()  # Ensure data is written immediately
                        
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
            
            # Filter data to only use data after 20 seconds (to avoid initial inconsistencies)
            mask = timestamps >= 20.0
            
            # Check if we have enough data after 20 seconds
            if np.sum(mask) < 20:  # Need at least 20 data points after 20s
                print("⚠️ Insufficient data after 20 seconds for respiration rate calculation")
                print(f"   Collected {len(data)} total points, but only {np.sum(mask)} after 20s")
                return None
            
            # Use only data from 20 seconds onwards
            data = data[mask]
            timestamps = timestamps[mask]
            print(f"📊 Using data from 20s onwards: {len(data)} points (range: {timestamps[0]:.1f}s - {timestamps[-1]:.1f}s)")
            
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
                
                # If coefficient of variation > 0.35, breathing is irregular (relaxed from 0.25)
                if cv > 0.35:
                    print("⚠️ Irregular breathing pattern detected (CV > 0.35) - possible missing peaks")
                    return "N/A"
                
                # Check for outliers (intervals that are significantly different)
                # An interval is an outlier if it's more than 3.0 standard deviations from the mean (relaxed from 2.0)
                # Allow some outliers if most data is good
                outliers = np.abs(time_intervals - mean_interval) > (3.0 * std_interval)
                outlier_count = np.sum(outliers)
                outlier_percentage = (outlier_count / len(time_intervals)) * 100
                
                if outlier_count > 0:
                    outlier_intervals = time_intervals[outliers]
                    print(f"📊 {outlier_count} outlier interval(s) detected: {outlier_intervals} ({outlier_percentage:.1f}% of intervals)")
                    print(f"   Outliers are more than 3.0 std devs from mean ({mean_interval:.2f}s ± {3.0*std_interval:.2f}s)")
                    
                    # Only reject if more than 30% of intervals are outliers (allow some natural variation)
                    if outlier_percentage > 30:
                        print("⚠️ Too many outliers detected - rejecting calculation")
                        return "N/A"
                    else:
                        print(f"✓ Acceptable outlier percentage ({outlier_percentage:.1f}% ≤ 30%) - continuing with calculation")
            
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
