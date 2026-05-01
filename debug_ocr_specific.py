import os
import sys
from ultralytics import YOLO
import cv2
import easyocr

MODEL_PATH = r"C:\Users\joshi\OneDrive\Desktop\L1 meter\best (2).pt"
model = YOLO(MODEL_PATH)
reader = easyocr.Reader(['en'], gpu=False)

paths = [
    r"C:\Users\joshi\OneDrive\Desktop\L1 meter\test_img\WhatsApp Image 2026-03-04 at 9.37.17 AM (1).jpeg", # 8
    r"C:\Users\joshi\OneDrive\Desktop\L1 meter\test_img\WhatsApp Image 2026-03-04 at 9.37.18 AM (1).jpeg", # 10
    r"C:\Users\joshi\OneDrive\Desktop\L1 meter\test_img\WhatsApp Image 2026-03-04 at 9.37.18 AM.jpeg" # 11
]

for p in paths:
    img = cv2.imread(p)
    if img is None: continue
    print(f"\n--- {os.path.basename(p)} ---")
    results = model(img)[0]
    names = results.names
    for box in results.boxes:
        cls = int(box.cls)
        name = names[cls]
        if name in ["SL_No", "SL.No"]:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            crop = img[max(0,y1-50):min(img.shape[0],y2+50), max(0,x1-50):min(img.shape[1],x2+50)]
            ocr_res = reader.readtext(crop)
            print(f"SL_No Crop OCR:")
            for bbox, text, conf in ocr_res:
                print(f"  [{conf:.2f}] {text}")

