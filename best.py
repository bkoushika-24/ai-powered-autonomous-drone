from ultralytics import YOLO
import cv2
from djitellopy import Tello

# Load trained YOLO model
model = YOLO("runs/train/exp/weights/best.pt")  

# Connect to Tello drone
tello = Tello()
tello.connect()
tello.streamon()

print(f"Battery: {tello.get_battery()}%")

while True:
    # Get video frame from Tello
    frame = tello.get_frame_read().frame
    frame = cv2.resize(frame, (640, 480))

    # Run YOLO object detection
    results = model(frame)

    # Draw detected objects
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
            conf = box.conf[0].item()  # Confidence score
            cls = int(box.cls[0].item())  # Class ID

            if conf > 0.5:  # Confidence threshold
                label = f"{model.names[cls]} {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show detection results
    cv2.imshow("Tello Object Detection", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop streaming and close windows
tello.streamoff()
cv2.destroyAllWindows()
