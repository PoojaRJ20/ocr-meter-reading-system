import gradio as gr
from main import process_image

def process(filepath):
    if not filepath:
        return "None", "Unknown", "No image provided"
        
    device_id, meter_status, decoded_values = process_image(filepath)
    
    device_id_str = str(device_id) if device_id else "None"
    status_str = str(meter_status) if meter_status else "Unknown"
    codes_str = "\n".join(decoded_values) if decoded_values else "No codes found"
    
    return device_id_str, status_str, codes_str

with gr.Blocks(title="Meter Scanner") as demo:
    gr.Markdown("# Meter Scanner and Status Check\nUpload an image of the meter to extract the device ID, serial numbers, and check the meter's display status.")
    with gr.Row():
        with gr.Column(scale=1):
            img_input = gr.Image(type="filepath", label="Upload Meter Photo")
            submit_btn = gr.Button("Scan Meter", variant="primary")
        with gr.Column(scale=1):
            out_device_id = gr.Textbox(label="Device ID / Serial Number", interactive=False)
            out_status = gr.Textbox(label="Meter Status (Working / Not Working)", interactive=False)
            out_codes = gr.Textbox(label="Decoded QR/Barcode Values", lines=4, interactive=False)
            
    submit_btn.click(fn=process, inputs=img_input, outputs=[out_device_id, out_status, out_codes])

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Default(primary_hue="blue", neutral_hue="slate"))
