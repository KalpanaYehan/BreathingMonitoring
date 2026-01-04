from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# Mock data for demonstration (since camera access isn't available in serverless)
class MockBreathingMonitor:
    def __init__(self):
        self.is_monitoring = False
        self.breathing_data = []
        self.timestamps = []
    
    def start_monitoring(self):
        self.is_monitoring = True
        return True
    
    def stop_monitoring(self):
        self.is_monitoring = False
        # Return mock breathing rate for demonstration
        return 14.5
    
    def get_data(self):
        return {
            'data_count': len(self.breathing_data),
            'is_monitoring': self.is_monitoring,
            'respiration_rate': 14.5 if self.is_monitoring else None
        }

monitor = MockBreathingMonitor()

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
    try:
        data = request.get_json()
        brightness = data.get('brightness', 0)
        timestamp = data.get('timestamp', 0)
        
        print(f"📊 Mobile Data Point: Brightness={brightness:.3f}, Time={timestamp:.1f}s")
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"❌ Error receiving data point: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)





