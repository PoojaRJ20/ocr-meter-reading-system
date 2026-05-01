import cv2
from ultralytics import YOLO
import easyocr
import os

model = YOLO(r"C:\Users\joshi\OneDrive\Desktop\L1 meter\best (1).pt")
names = model.model.names
reader = easyocr.Reader(['en'], gpu=False)

path = r"C:\Users\joshi\OneDrive\Desktop\L1 meter\test_img\WhatsApp Image 2026-03-04 at 9.37.01 AM (1).jpeg"
img = cv2.imread(path)
h, w = img.shape[:2]

results = model(img)[0]
PAD = 150

display_region = None
last_crop = None

for box in results.boxes:
    cls = int(box.cls)
    name = names[cls]
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    
    if name in ["QR", "Bar"]:
        x1p = max(0, x1-PAD)
        y1p = max(0, y1-PAD)
        x2p = min(w, x2+PAD)
        y2p = min(h, y2+PAD)
        last_crop = img[y1p:y2p, x1p:x2p]
        cv2.imwrite(f"crop_{name}.jpg", last_crop)
    
    if name == "Display":
        h_box = y2 - y1
        w_box = x2 - x1
        x1n = max(0, x1 - int(w_box * 2.5))
        x2n = min(w, x2 + int(w_box * 2.5))
        y1n = max(0, y1 - int(h_box * 4.0))
        y2n = min(h, y2 + int(h_box * 1.5))
        display_region = img[y1n:y2n, x1n:x2n]
        cv2.imwrite("crop_display.jpg", display_region)

with open("out_crops.txt", "w") as f:
    if display_region is not None:
        f.write("\n--- DISPLAY REGION ---\n")
        res = reader.readtext(display_region)
        for bbox, text, conf in res:
            f.write(f"[{conf:.2f}] {text}\n")
    
    if last_crop is not None:
        f.write("\n--- LAST CROP ---\n")
        res = reader.readtext(last_crop)
        for bbox, text, conf in res:
            f.write(f"[{conf:.2f}] {text}\n")
