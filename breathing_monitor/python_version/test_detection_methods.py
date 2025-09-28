#!/usr/bin/env python3
"""
Test script for the improved white spot detection methods
"""
import cv2
import numpy as np
import sys
import os

# Add the current directory to the path to import the monitor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from minimal_monitor import MinimalBreathingMonitor

def test_detection_methods():
    """Test the new detection methods"""
    print("🧪 Testing White Spot Detection Methods")
    print("=" * 50)
    
    # Initialize monitor
    monitor = MinimalBreathingMonitor()
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not open camera")
        return
    
    print("📷 Camera opened successfully")
    print("📋 Available detection methods:")
    print("   - auto: Try Hough first, then Blob if Hough fails")
    print("   - hough: Method 1 - Color Thresholding & Hough Circle Transform")
    print("   - blob: Method 2 - Blob Detection with SimpleBlobDetector")
    print("\n🎯 Instructions:")
    print("   1. Place a white circle/spot on a black background")
    print("   2. Press '1' to test Hough method")
    print("   3. Press '2' to test Blob method") 
    print("   4. Press 'a' to test Auto method")
    print("   5. Press 't' to test all methods")
    print("   6. Press 'q' to quit")
    print("   7. Press 'r' to adjust radius range")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame")
            break
        
        # Resize frame for display
        display_frame = cv2.resize(frame, (640, 480))
        
        # Draw center region
        h, w = display_frame.shape[:2]
        center_region = display_frame[h//4:3*h//4, w//4:3*w//4]
        cv2.rectangle(display_frame, (w//4, h//4), (3*w//4, 3*h//4), (0, 255, 0), 2)
        cv2.putText(display_frame, 'Detection Region', (w//4, h//4 - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Show current method
        cv2.putText(display_frame, f'Method: {monitor.detection_method.upper()}', 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(display_frame, f'Radius: {monitor.min_radius}-{monitor.max_radius}', 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Show instructions
        cv2.putText(display_frame, '1:Hough 2:Blob A:Auto T:Test All Q:Quit R:Radius', 
                   (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow('White Spot Detection Test', display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('1'):
            print("\n🔍 Testing Hough Circle Detection...")
            monitor.set_detection_method('hough')
            result = monitor.detect_white_spot(frame, method='hough')
            if result:
                print(f"✅ Hough: Circle detected at {result}")
            else:
                print("❌ Hough: No circle detected")
                
        elif key == ord('2'):
            print("\n🔍 Testing Blob Detection...")
            monitor.set_detection_method('blob')
            result = monitor.detect_white_spot(frame, method='blob')
            if result:
                print(f"✅ Blob: Circle detected at {result}")
            else:
                print("❌ Blob: No circle detected")
                
        elif key == ord('a'):
            print("\n🔍 Testing Auto Detection...")
            monitor.set_detection_method('auto')
            result = monitor.detect_white_spot(frame, method='auto')
            if result:
                print(f"✅ Auto: Circle detected at {result}")
            else:
                print("❌ Auto: No circle detected")
                
        elif key == ord('t'):
            print("\n🔍 Testing All Methods...")
            results = monitor.test_detection_methods(frame)
            print("📊 Test Results:")
            for method, success in results.items():
                if method.endswith('_center'):
                    continue
                if method.endswith('_error'):
                    print(f"   {method}: {results[method]}")
                else:
                    status = "✅ Success" if success else "❌ Failed"
                    print(f"   {method.upper()}: {status}")
                    if success and f"{method}_center" in results:
                        print(f"      Center: {results[f'{method}_center']}")
                        
        elif key == ord('r'):
            print("\n⚙️ Adjusting radius range...")
            try:
                min_r = int(input("Enter minimum radius (default 10): ") or "10")
                max_r = int(input("Enter maximum radius (default 50): ") or "50")
                monitor.set_detection_radius(min_r, max_r)
                print(f"✅ Radius range set to {min_r}-{max_r}")
            except ValueError:
                print("❌ Invalid input, using defaults")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\n👋 Test completed!")

if __name__ == "__main__":
    test_detection_methods()
