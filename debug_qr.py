import os
import cv2
import zxingcpp

def debug_full_qr(image_path):
    img = cv2.imread(image_path)
    res = zxingcpp.read_barcodes(img)
    print(f"\n--- {os.path.basename(image_path)} ---")
    if not res:
        print("No QR found originally, trying variations...")
        variants = [
            cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
            cv2.resize(img, None, fx=2, fy=2),
            cv2.resize(img, None, fx=4, fy=4)
        ]
        for v in variants:
            res = zxingcpp.read_barcodes(v)
            if res:
                break
    for r in res:
        print("QR Payload:", r.text)

paths = [
    r"C:\Users\joshi\OneDrive\Desktop\L1 meter\test_img\WhatsApp Image 2026-03-04 at 9.37.17 AM (1).jpeg", # 8
    r"C:\Users\joshi\OneDrive\Desktop\L1 meter\test_img\WhatsApp Image 2026-03-04 at 9.37.18 AM (1).jpeg", # 10
    r"C:\Users\joshi\OneDrive\Desktop\L1 meter\test_img\WhatsApp Image 2026-03-04 at 9.37.18 AM.jpeg" # 11
]

for p in paths:
    debug_full_qr(p)
