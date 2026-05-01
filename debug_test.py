import traceback
print("Starting script...")
try:
    import easyocr
    reader = easyocr.Reader(['en'], gpu=False)
    print("Reader initialized.")
    with open("test.txt", "w") as f:
        f.write("Success")
except Exception as e:
    with open("err.txt", "w") as f:
        f.write(traceback.format_exc())
