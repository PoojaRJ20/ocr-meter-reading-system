import os
import cv2
from ultralytics import YOLO

MODEL_PATH = r"C:\Users\joshi\OneDrive\Desktop\L1 meter\best (2).pt"
IMAGE_PATH = r"C:\Users\joshi\OneDrive\Desktop\L1 meter\test_img\WhatsApp Image 2026-03-04 at 9.37.18 AM.jpeg"

model = YOLO(MODEL_PATH)

img = cv2.imread(IMAGE_PATH)
results = model(img)[0]
names = results.names

for box in results.boxes:
    cls = int(box.cls)
    name = names[cls]
    if name == "Display":
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        display_crop = img[y1:y2, x1:x2]
        cv2.imwrite("crop_display.jpg", display_crop)

        gray = cv2.cvtColor(display_crop, cv2.COLOR_BGR2GRAY)
        brightness = gray.mean()
        contrast = gray.std()

        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        digit_contours = sum(
            1 for c in contours
            if cv2.boundingRect(c)[2] * cv2.boundingRect(c)[3] > 60
        )

        print("-" * 30)
        print(f"File: {os.path.basename(IMAGE_PATH)}")
        print(f"Crop Shape: {display_crop.shape}")
        print(f"Brightness: {brightness:.2f}")
        print(f"Contrast: {contrast:.2f}")
        print(f"Digit Contours (Area > 60): {digit_contours}")
        
        # testing area thresh:
        dc_high = sum(1 for c in contours if cv2.boundingRect(c)[2] * cv2.boundingRect(c)[3] > 100)
        dc_low = sum(1 for c in contours if cv2.boundingRect(c)[2] * cv2.boundingRect(c)[3] > 30)
        print(f"Digit contours (>100): {dc_high}")
        print(f"Digit contours (>30): {dc_low}")

