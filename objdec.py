import cv2
import numpy as np
from djitellopy import Tello
from ultralytics import YOLO

# Load YOLOv8 model (download or train your own)
model = YOLO("yolov8n.pt")

# Connect to Tello
tello = Tello()
tello.connect()
tello.streamon()

print(f"Battery: {tello.get_battery()}%")

while True:
    frame = tello.get_frame_read().frame
    frame = cv2.resize(frame, (640, 480))

    # Perform object detection
    results = model(frame)
    
    # Draw detections on frame
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())

            if conf > 0.5:  # Confidence threshold
                label = f"{model.names[cls]} {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the video feed
    cv2.imshow("Tello Object Detection", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

tello.streamoff()
cv2.destroyAllWindows()
