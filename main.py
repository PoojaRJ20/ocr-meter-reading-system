import os
import cv2
import re
import numpy as np
import zxingcpp
from ultralytics import YOLO
import easyocr

# -------------------------
# SETTINGS
# -------------------------

MODEL_PATH = r"C:\Users\joshi\OneDrive\Desktop\L1 meter\best (2).pt"
IMAGE_FOLDER = r"C:\Users\joshi\OneDrive\Desktop\L1 meter\test_img"

PAD = 150

model = YOLO(MODEL_PATH)
names = model.model.names
reader = easyocr.Reader(['en'], gpu=False)

# -------------------------
# HELPER: DISTANCE LOGIC
# -------------------------

def get_center(box):
    x1, y1, x2, y2 = box
    return ((x1 + x2)//2, (y1 + y2)//2)

def get_closest_box(ref_box, boxes):

    rx, ry = get_center(ref_box)

    min_dist = float("inf")
    best_box = None

    for b in boxes:
        bx, by = get_center(b)
        dist = (rx - bx)**2 + (ry - by)**2

        if dist < min_dist:
            min_dist = dist
            best_box = b

    return best_box


# -------------------------
# DEVICE ID EXTRACTION
# -------------------------

def extract_device_id(values):

    candidates = []

    for v in values:
        v = v.strip().upper()

        matches_alpha = re.finditer(r'(?<!\d)([A-Z]\d{6,7})(?!\d)', v)
        for m in matches_alpha:
            s = m.group(1)
            start_idx = m.start()
            if start_idx > 0 and v[start_idx-1].isalpha():
                prefix = v[:start_idx]
                allow = any(prefix.endswith(p) for p in ('SNO', 'NO', 'SLNO', 'SRNO', 'SL.NO', 'SR.', 'SL.', 'SR', 'L.NO', 'P.', 'C.'))
                if not allow:
                    continue
            
            # Explicitly ban BIS Registration numbers (R followed by 7 digits)
            if re.fullmatch(r'R\d{7}', s):
                continue

            candidates.append(s)

        matches_digit = re.finditer(r'(?<!\d)(\d{7,8})(?!\d)', v)
        for m in matches_digit:
            start_idx = m.start()
            if start_idx > 0 and v[start_idx-1].isalpha():
                prefix = v[:start_idx]
                allow = any(prefix.endswith(p) for p in ('SNO', 'NO', 'SLNO', 'SRNO', 'SL.NO', 'SR.', 'SL.', 'SR', 'L.NO', 'P.', 'C.'))
                if not allow:
                    continue
            candidates.append(m.group(1))

    if not candidates:
        return None

    # prefer UXXXXXXX format
    for c in candidates:
        if re.match(r'[A-Z]\d{6,7}', c):
            return c

    return candidates[0]



# -------------------------
# QR DECODER (STRONG)
# -------------------------

def decode_codes(img):

    results = []

    try:
        variants = [
            img,
            cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
            cv2.resize(img, None, fx=2, fy=2),
            cv2.resize(img, None, fx=4, fy=4)
        ]

        for v in variants:
            res = zxingcpp.read_barcodes(v)
            for r in res:
                if r.text:
                    results.append(r.text.strip())

    except:
        pass

    return results


# -------------------------
# SMART OCR
# -------------------------

def smart_ocr(img):

    values = []

    try:
        results = reader.readtext(img)

        for _, text, conf in results:

            if conf < 0.35:
                continue

            text = text.upper().replace(" ", "")

            # remove GPS noise
            if "LAT" in text or "LONG" in text:
                continue

            # remove decimals
            if re.search(r'\d+\.\d+', text):
                continue

            # fix OCR mistakes
            text = text.replace("O","0").replace("I","1") \
                       .replace("B","8").replace("S","5") \
                       .replace("G","6").replace("Z","2")

            if re.search(r'[A-Z]\d{6,7}', text) or re.search(r'\d{7,8}', text):
                values.append(text)

    except:
        pass

    return values


# -------------------------
# OCR PIPELINE
# -------------------------

def get_best_ocr(img):

    variants = []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    variants.append(gray)

    sharp = cv2.filter2D(gray, -1,
        np.array([[0,-1,0],[-1,5,-1],[0,-1,0]]))
    variants.append(sharp)

    thresh = cv2.threshold(sharp, 0, 255,
                           cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    variants.append(thresh)

    adaptive = cv2.adaptiveThreshold(gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2)
    variants.append(adaptive)

    big = cv2.resize(thresh, None, fx=4, fy=4)
    variants.append(big)

    all_values = []

    for v in variants:
        all_values.extend(smart_ocr(v))

    return extract_device_id(all_values)


# -------------------------
# DISPLAY CHECK
# -------------------------

def check_display(display_crop):

    try:
        gray = cv2.cvtColor(display_crop, cv2.COLOR_BGR2GRAY)

        brightness = gray.mean()
        contrast = gray.std()

        edges = cv2.Canny(gray, 50, 150)

        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        digit_contours = sum(
            1 for c in contours
            if cv2.boundingRect(c)[2] * cv2.boundingRect(c)[3] > 60
        )

        if brightness < 35 or contrast < 10:
            return "Not Working"

        if digit_contours < 5:
            return "Not Working"

        return "Working"

    except:
        return "Working"


# -------------------------
# MAIN PIPELINE
# -------------------------

def process_image(img_path):

    img = cv2.imread(img_path)

    if img is None:
        return None, "Unknown", "Load Failed"

    h, w = img.shape[:2]
    results = model(img)[0]

    device_id = None
    meter_status = "Unknown"

    slno_boxes = []
    qr_bar_boxes = []
    decoded_values = []

    # collect detections
    for box in results.boxes:

        cls = int(box.cls)
        name = names[cls]

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if name in ["SL_No", "SL.No"]:
            slno_boxes.append((x1,y1,x2,y2))

        if name in ["QR", "Bar"]:
            qr_bar_boxes.append((x1,y1,x2,y2))

        if name == "Display":
            meter_status = check_display(img[y1:y2, x1:x2])

    # -------------------------
    # STEP 1: QR near SL_NO
    # -------------------------

    for box in slno_boxes:

        x1,y1,x2,y2 = box

        pad_x = int((x2-x1)*1.8)
        pad_y = int((y2-y1)*1.8)

        crop = img[max(0,y1-pad_y):min(h,y2+pad_y),
                   max(0,x1-pad_x):min(w,x2+pad_x)]

        vals = decode_codes(crop)

        if vals:
            decoded_values.extend(vals)
            break

    # -------------------------
    # STEP 2: nearest QR
    # -------------------------

    if not decoded_values and qr_bar_boxes:

        if slno_boxes:
            target = get_closest_box(slno_boxes[0], qr_bar_boxes)
        else:
            target = qr_bar_boxes[0]

        x1,y1,x2,y2 = target

        crop = img[max(0,y1-PAD):min(h,y2+PAD),
                   max(0,x1-PAD):min(w,x2+PAD)]

        vals = decode_codes(crop)
        decoded_values.extend(vals)

    # -------------------------
    # STEP 3: QR result
    # -------------------------

    if decoded_values:
        device_id = extract_device_id(decoded_values)
        if device_id:
            return device_id, meter_status, "QR/Barcode"

    # -------------------------
    # STEP 4: SL OCR
    # -------------------------

    for box in slno_boxes:

        x1,y1,x2,y2 = box

        crop = img[max(0,y1-150):min(h,y2+150),
                   max(0,x1-150):min(w,x2+150)]

        device_id = get_best_ocr(crop)

        if device_id:
            return device_id, meter_status, "SL_No OCR"

    # -------------------------
    # STEP 5: FULL OCR
    # -------------------------

    device_id = get_best_ocr(img)

    if device_id:
        return device_id, meter_status, "Full OCR"

    return None, meter_status, "None"


# -------------------------
# RUN
# -------------------------

def process_folder():

    files = [f for f in os.listdir(IMAGE_FOLDER)
             if f.lower().endswith((".jpg",".jpeg",".png"))]

    print(f"Total images: {len(files)}")

    for i, file in enumerate(files):

        print("\n==============================")
        print(f"[{i+1}/{len(files)}] Processing: {file}")

        path = os.path.join(IMAGE_FOLDER, file)

        device_id, status, source = process_image(path)

        print(f"Device ID   : {device_id}")
        print(f"Meter Status: {status}")
        print(f"Source      : {source}")


if __name__ == "__main__":
    process_folder()
    print("\n✅ Finished all images")