import os
import easyocr
import cv2

reader = easyocr.Reader(['en'], gpu=False)

folder = r"C:\Users\joshi\OneDrive\Desktop\L1 meter\test_img"
files = [f for f in os.listdir(folder) if f.endswith((".jpeg", ".jpg", ".png"))]

with open("ocr_results.txt", "w", encoding="utf-8") as f:
    for file in files:
        path = os.path.join(folder, file)
        img = cv2.imread(path)
        if img is None:
            f.write(f"\n--- {file} (Failed to load) ---\n")
            continue
            
        res = reader.readtext(img)
        f.write(f"\n--- {file} ---\n")
        f.write("RAW BLOCKS:\n")
        for bbox, text, conf in res:
            f.write(f"[{conf:.2f}] '{text}'\n")
