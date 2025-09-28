#!/usr/bin/env python3
import cv2
import numpy as np
import time
from flask import Flask, render_template, jsonify, request
import threading
from scipy.signal import find_peaks
import ssl
import os

class OpticalFlowBreathingMonitor:
    def __init__(self):
        self.cap = None
        self.breathing_data = []
        self.timestamps = []
        self.is_monitoring = False
        self.start_time = None
        
        # Optical flow parameters
        self.lk_params = dict(winSize=(15, 15),
                             maxLevel=2,
                             criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        
        # Feature detection parameters
        self.feature_params = dict(maxCorners=100,
                                  qualityLevel=0.3,
                                  minDistance=7,
                                  blockSize=7)
        
        # Monitoring settings
        self.sample_rate = 10  # Hz (10 samples per second for higher accuracy)
        self.max_data_points = 2000  # Keep more data points for analysis
        
        # Optical flow tracking variables
        self.old_gray = None
        self.p0 = None  # Previous points
        self.track_points = []
        self.breathing_region = None
        
        print("✅ Optical Flow Breathing Monitor initialized")
    
    def start_monitoring(self):
        if self.is_monitoring:
            return False
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.is_monitoring = True
        self.start_time = time.time()
        self.breathing_data = []
        self.timestamps = []
        self.track_points = []
        
        # Initialize optical flow tracking
        self._initialize_tracking()
        
        # Start monitoring
        threading.Thread(target=self._monitor_loop, daemon=True).start()
        print("🚀 Optical flow monitoring started")
        return True
    
    def stop_monitoring(self):
        self.is_monitoring = False
        
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None
        
        # Calculate respiration rate
        respiration_rate = self.calculate_respiration_rate()
        
        print("⏹️ Monitoring stopped")
        if respiration_rate is not None:
            print(f"📊 Respiration Rate: {respiration_rate:.1f} breaths/min")
        
        return respiration_rate
    
    def _initialize_tracking(self):
        """Initialize feature points for optical flow tracking"""
        if not self.cap or not self.cap.isOpened():
            return
        
        ret, frame = self.cap.read()
        if not ret:
            return
        
        # Convert to grayscale
        self.old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Define breathing region (center of frame)
        h, w = self.old_gray.shape
        self.breathing_region = (w//4, h//4, w//2, h//2)  # Center region
        
        # Extract features from breathing region
        x, y, w_roi, h_roi = self.breathing_region
        roi = self.old_gray[y:y+h_roi, x:x+w_roi]
        
        # Find good features to track
        points = cv2.goodFeaturesToTrack(roi, mask=None, **self.feature_params)
        
        if points is not None:
            # Adjust coordinates to full frame and reshape for optical flow
            points[:, 0, 0] += x
            points[:, 0, 1] += y
            self.p0 = points.astype(np.float32)
            print(f"🎯 Initialized tracking with {len(points)} feature points")
        else:
            print("⚠️ No features found for tracking")
    
    def _monitor_loop(self):
        """Main monitoring loop using optical flow"""
        while self.is_monitoring:
            try:
                if not self.cap or not self.cap.isOpened():
                    time.sleep(1)
                    continue
                
                ret, frame = self.cap.read()
                if ret:
                    # Use optical flow for breathing detection
                    breathing_magnitude = self.optical_flow_breathing_detection(frame)
                    if breathing_magnitude is not None:
                        self.breathing_data.append(float(breathing_magnitude))
                        self.timestamps.append(time.time() - self.start_time)
                        
                        # Keep only recent data
                        if len(self.breathing_data) > self.max_data_points:
                            self.breathing_data.pop(0)
                            self.timestamps.pop(0)
                        
                        print(f"Optical Flow Data: {breathing_magnitude:.3f}")
                
                # Higher frequency sampling for accuracy
                time.sleep(1.0 / self.sample_rate)
                
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(2)
    
    def optical_flow_breathing_detection(self, frame):
        """Detect breathing using optical flow motion tracking"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if self.old_gray is None or self.p0 is None or len(self.p0) == 0:
                # Reinitialize tracking if needed
                self._initialize_tracking()
                return None
            
            # Calculate optical flow
            p1, st, err = cv2.calcOpticalFlowPyrLK(self.old_gray, gray, self.p0, None, **self.lk_params)
            
            # Select good points
            if p1 is not None and st is not None:
                good_new = p1[st == 1]
                good_old = self.p0[st == 1]
                
                if len(good_new) > 0:
                    # Calculate motion vectors
                    motion_vectors = good_new - good_old
                    
                    # Filter points within breathing region
                    x, y, w_roi, h_roi = self.breathing_region
                    region_mask = ((good_new[:, 0] >= x) & (good_new[:, 0] <= x + w_roi) & 
                                  (good_new[:, 1] >= y) & (good_new[:, 1] <= y + h_roi))
                    
                    if np.any(region_mask):
                        # Get motion vectors within breathing region
                        region_vectors = motion_vectors[region_mask]
                        
                        # Calculate vertical motion (breathing is primarily vertical)
                        vertical_motion = region_vectors[:, 1]  # Y component
                        
                        # Calculate breathing magnitude (average vertical displacement)
                        breathing_magnitude = np.mean(np.abs(vertical_motion))
                        
                        # Update tracking points
                        self.p0 = good_new.reshape(-1, 1, 2)
                        self.old_gray = gray.copy()
                        
                        return breathing_magnitude
                    else:
                        # No points in breathing region, reinitialize
                        self._initialize_tracking()
                        return None
                else:
                    # No good points, reinitialize
                    self._initialize_tracking()
                    return None
            else:
                # Reinitialize tracking
                self._initialize_tracking()
                return None
                
        except Exception as e:
            print(f"Optical flow error: {e}")
            return None
    
    def calculate_respiration_rate(self):
        """Calculate respiration rate from optical flow data using improved peak detection"""
        try:
            if len(self.breathing_data) < 50:  # Need more data points for optical flow
                print("⚠️ Insufficient data for respiration rate calculation")
                return None
            
            # Convert to numpy array for processing
            data = np.array(self.breathing_data)
            timestamps = np.array(self.timestamps)
            
            # Check data variation
            data_range = np.max(data) - np.min(data)
            print(f"📊 Optical flow data range: {data_range:.4f} (min: {np.min(data):.4f}, max: {np.max(data):.4f})")
            
            if data_range < 0.001:  # Very small variation for optical flow
                print("⚠️ Data variation too small for reliable peak detection")
                return None
            
            # Apply smoothing for optical flow data
            from scipy.ndimage import gaussian_filter1d
            smoothed_data = gaussian_filter1d(data, sigma=1.0)
            
            # Calculate adaptive thresholds
            data_mean = np.mean(smoothed_data)
            data_std = np.std(smoothed_data)
            
            # Use relative height threshold
            height_threshold = data_mean + (0.2 * data_std)
            
            # Use adaptive prominence for optical flow data
            prominence_threshold = max(0.001, data_std * 0.5)
            
            print(f"📊 Optical flow thresholds - Height: {height_threshold:.4f}, Prominence: {prominence_threshold:.4f}")
            
            # Find peaks with optical flow optimized parameters
            peaks, properties = find_peaks(smoothed_data, 
                                         height=height_threshold,
                                         distance=5,  # Minimum 0.5 seconds between peaks (10 Hz sampling)
                                         prominence=prominence_threshold)
            
            print(f"📊 Found {len(peaks)} breathing peaks at positions: {peaks}")
            
            if len(peaks) < 2:
                print("⚠️ Not enough breathing cycles detected")
                # Try with more relaxed parameters
                peaks, _ = find_peaks(smoothed_data, 
                                    height=data_mean,
                                    distance=3,
                                    prominence=0.0005)
                print(f"📊 Relaxed search found {len(peaks)} peaks")
                
                if len(peaks) < 2:
                    return None
            
            # Calculate time between peaks
            peak_times = timestamps[peaks]
            time_intervals = np.diff(peak_times)
            
            print(f"📊 Time intervals between peaks: {time_intervals}")
            
            # Filter realistic breathing intervals
            valid_intervals = time_intervals[(time_intervals >= 0.5) & (time_intervals <= 4.0)]
            
            if len(valid_intervals) < 1:
                print("⚠️ No valid breathing intervals found")
                return None
            
            # Calculate average breathing interval
            avg_interval = np.mean(valid_intervals)
            
            # Convert to breaths per minute
            respiration_rate = 60.0 / avg_interval
            
            print(f"📊 Calculated respiration rate: {respiration_rate:.1f} breaths/min")
            
            # Validate result
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
            'data_count': len(self.breathing_data),
            'track_points': len(self.p0) if self.p0 is not None else 0
        }
    
    def cleanup(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()

# Flask app initialization
app = Flask(__name__)

# Global instance
monitor = OpticalFlowBreathingMonitor()

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
    """Video streaming route with optical flow visualization"""
    def generate():
        while True:
            try:
                if monitor.cap and monitor.cap.isOpened():
                    ret, frame = monitor.cap.read()
                    if ret:
                        # Resize frame for web display
                        frame = cv2.resize(frame, (640, 480))
                        
                        # Draw breathing region
                        if monitor.breathing_region:
                            x, y, w, h = monitor.breathing_region
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            cv2.putText(frame, 'Breathing Region', (x, y - 10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        
                        # Draw tracking points
                        if monitor.p0 is not None:
                            for point in monitor.p0:
                                x, y = point[0]
                                cv2.circle(frame, (int(x), int(y)), 3, (0, 0, 255), -1)
                        
                        # Add status text
                        status_text = f"Tracking Points: {len(monitor.p0) if monitor.p0 is not None else 0}"
                        cv2.putText(frame, status_text, (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                        
                        # Convert to JPEG for web streaming
                        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                        if ret:
                            frame_bytes = buffer.tobytes()
                            yield (b'--frame\r\n'
                                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                
                # Control frame rate
                time.sleep(0.1)  # 10 FPS for video feed
                
            except Exception as e:
                print(f"Video feed error: {e}")
                time.sleep(0.1)
    
    return app.response_class(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    try:
        print("🌬️ Optical Flow Breathing Monitor")
        print("📱 Desktop: http://localhost:5001")
        print("📱 Mobile: http://localhost:5001/mobile")
        print("🔒 HTTPS Mobile: https://localhost:5001/mobile")
        print("⏹️  Press Ctrl+C to stop")
        
        # Check if SSL certificates exist for HTTPS
        cert_file = 'cert.pem'
        key_file = 'key.pem'
        
        if os.path.exists(cert_file) and os.path.exists(key_file):
            print("🔒 SSL certificates found. Starting HTTPS server...")
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.load_cert_chain(cert_file, key_file)
            app.run(host='0.0.0.0', port=5001, debug=False, threaded=True, ssl_context=context)
        else:
            print("⚠️  SSL certificates not found. Starting HTTP server...")
            print("   For mobile camera access, you'll need HTTPS.")
            print("   Generate certificates with: openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes")
            app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    finally:
        monitor.cleanup()
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
