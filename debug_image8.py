import cv2
import easyocr

path = r"C:\Users\joshi\OneDrive\Desktop\L1 meter\test_img\WhatsApp Image 2026-03-04 at 9.37.17 AM (1).jpeg"
img = cv2.imread(path)
reader = easyocr.Reader(['en'], gpu=False)

res = reader.readtext(img)
for bbox, text, conf in res:
    if conf > 0.1:
        print(f"[{conf:.2f}] {text}")
