# ocr-meter-reading-system
AI-powered OCR and meter reading automation system built using Computer Vision and deep learning techniques. The project integrates YOLO-based object detection, image preprocessing, QR/barcode decoding, and OCR fallback mechanisms for accurate extraction of meter readings and enterprise document data from real-world images. 
# Intelligent OCR & Meter Reading Automation System

## Overview
This project is an AI-powered OCR and meter reading automation system developed using Computer Vision and deep learning techniques. The system automatically extracts meter readings and enterprise document data from real-world images.

The pipeline integrates YOLO-based object detection, image preprocessing, QR/barcode decoding, and OCR fallback mechanisms for robust and accurate extraction.

---

## Features

- YOLO-based object detection
- OCR-based text extraction
- QR and barcode decoding
- Image preprocessing using OpenCV
- OCR fallback mechanism
- Meter reading automation
- Real-time image processing

---

## Workflow

Image Input  
↓  
YOLO Detection  
↓  
Display Cropping  
↓  
Image Enhancement  
↓  
QR/Barcode Detection  
↓  
OCR Extraction  
↓  
Validation Logic  
↓  
Final Meter Reading

---

## Tech Stack

- Python
- OpenCV
- YOLO
- OCR
- NumPy
- Deep Learning

---

## Project Structure

```bash
ocr-meter-reading-system/
│
├── images/
├── outputs/
├── models/
├── utils/
├── main.py
├── requirements.txt
└── README.md
```

---

## Results

- Successfully extracted meter readings from real-world images
- Implemented OCR fallback logic for low-quality images
- Improved OCR accuracy using contour detection and brightness correction
- Integrated barcode and QR extraction workflows

---

## Future Improvements

- Deploy as web application
- Improve OCR accuracy using transformer-based OCR
- Add multilingual text support
- Real-time video stream processing

---

## Author

Pooja Joshi
