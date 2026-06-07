from djitellopy import tello 
import cvzone
import cv2
from time import sleep

import getter as kg
import Control as ct

# Detection Thresholds
thres = 0.50  # Confidence threshold
nmsThres = 0.2  # Non-maximum suppression threshold

# Load Class Names
classNames = []
classFile = 'ss.names'
try:
    with open(classFile, 'r') as f:
        classNames = f.read().strip().split("\n")  # Ensure proper splitting
except FileNotFoundError:
    print(f"Error: {classFile} not found!")
    exit()

print("Classes Loaded:", classNames)

# Load Model Configuration & Weights
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = "frozen_inference_graph.pb"

# Check if files exist
import os
if not os.path.exists(configPath) or not os.path.exists(weightsPath):
    print("Error: Model files not found!")
    exit()

# Initialize DNN Model
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)  # Fixed missing parameters
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

print("Model successfully loaded and initialized!")
