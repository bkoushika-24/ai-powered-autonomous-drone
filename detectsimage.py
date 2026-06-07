from ultralytics import YOLO
import cv2

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Load an image
image_path = "test.jpg"
image = cv2.imread(image_path)

# Run inference
results = model(image)

# Display results
for result in results:
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
        conf = box.conf[0].item()  # Confidence score
        cls = int(box.cls[0].item())  # Class ID

        if conf > 0.5:  # Confidence threshold
            label = f"{model.names[cls]} {conf:.2f}"
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

cv2.imshow("YOLO Object Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
