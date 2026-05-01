import os
import sys

# Import functions from main
from main import process_image, IMAGE_FOLDER

paths = [
    os.path.join(IMAGE_FOLDER, "WhatsApp Image 2026-03-04 at 9.37.17 AM (1).jpeg"), # 8
    os.path.join(IMAGE_FOLDER, "WhatsApp Image 2026-03-04 at 9.37.18 AM (1).jpeg"), # 10
    os.path.join(IMAGE_FOLDER, "WhatsApp Image 2026-03-04 at 9.37.18 AM.jpeg"), # 11
]

for idx, p in zip([8, 10, 11], paths):
    print(f"\nEvaluating Image {idx}: {os.path.basename(p)}")
    device_id, status, source = process_image(p)
    print(f"Device ID   : {device_id}")
    print(f"Status      : {status}")
    print(f"Source      : {source}")
