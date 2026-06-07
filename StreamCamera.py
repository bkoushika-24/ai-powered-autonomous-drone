import cv2
from djitellopy import Tello

# Connect to the drone
tello = Tello()
tello.connect()
tello.streamon()  # Start video stream

while True:
    frame = tello.get_frame_read().frame  # Get the video frame
    frame = cv2.resize(frame, (640, 480))  # Resize for display
    
    cv2.imshow("Tello Camera", frame)  # Show the frame
    
    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

tello.streamoff()
cv2.destroyAllWindows()
