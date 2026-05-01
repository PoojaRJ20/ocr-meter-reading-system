import os
import easyocr
import cv2

reader = easyocr.Reader(['en'], gpu=False)

folder = r"C:\Users\joshi\OneDrive\Desktop\L1 meter\test_img"
files = [f for f in os.listdir(folder) if f.endswith(".jpeg")]

for file in files:
    path = os.path.join(folder, file)
    img = cv2.imread(path)
    res = reader.readtext(img)
    print(f"\n--- {file} ---")
    texts = []
    for bbox, text, conf in res:
        texts.append(text)
    print(" | ".join(texts))
