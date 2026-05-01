import os
import cv2
from ultralytics import YOLO

MODEL_PATH = r"C:\Users\joshi\OneDrive\Desktop\L1 meter\best (2).pt"
IMAGE_FOLDER = r"C:\Users\joshi\OneDrive\Desktop\L1 meter\test_img"

model = YOLO(MODEL_PATH)
files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(".jpeg")]

print("File | Brightness | Contrast | Contours(>60)")
for f in files:
    img = cv2.imread(os.path.join(IMAGE_FOLDER, f))
    results = model(img)[0]
    names = results.names
    for box in results.boxes:
        cls = int(box.cls)
        if names[cls] == "Display":
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            crop = img[y1:y2, x1:x2]
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            b = gray.mean()
            c = gray.std()
            edges = cv2.Canny(gray, 50, 150)
            cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            dc = sum(1 for cnt in cnts if cv2.boundingRect(cnt)[2] * cv2.boundingRect(cnt)[3] > 60)
            print(f"{f[-18:]} | {b:.1f} | {c:.1f} | {dc}")
            break
