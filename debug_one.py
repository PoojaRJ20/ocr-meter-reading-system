import easyocr
import cv2

reader = easyocr.Reader(['en'], gpu=False)

path = r"C:\Users\joshi\OneDrive\Desktop\L1 meter\test_img\WhatsApp Image 2026-03-04 at 9.37.01 AM (1).jpeg"
img = cv2.imread(path)

with open("out_one.txt", "w") as f:
    if img is None:
        f.write("Failed to load image.\n")
    else:
        results = reader.readtext(img)
        for bbox, text, conf in results:
            f.write(f"[{conf:.2f}] {text}\n")
