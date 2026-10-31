import io
import numpy as np
import cv2
from flask import Flask, render_template, request, jsonify
import easyocr
import ssl

# Bypass SSL restrictions for automated baseline file downloads
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

# Initialize EasyOCR engine (Ultra-stable processing architecture)
print("--> Initializing High-Stability Local Character Analysis Engine...")
reader = easyocr.Reader(['en'], gpu=False)
print("--> Core Engine Activated and Standing By.")

@app.route('/')
def home_view():
    return render_template('components/index.html')

@app.route('/process-image', methods=['POST'])
def process_image_endpoint():
    if 'document_img' not in request.files:
        return jsonify({'error': 'Missing critical payload key: document_img'}), 400
        
    img_payload = request.files['document_img']
    if img_payload.filename == '':
        return jsonify({'error': 'Empty target file structure received'}), 400

    try:
        # Zero-Storage Memory Pipeline: Read image entirely in volatile memory
        raw_stream = img_payload.read()
        binary_buffer = np.frombuffer(raw_stream, np.uint8)
        img = cv2.imdecode(binary_buffer, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({'error': 'Matrix validation failed. Invalid image format.'}), 400

        # Execute stable text scanning route (Returns: [ [ [x,y coordinates], text_token, confidence ] ])
        ocr_results = reader.readtext(img)
        
        if not ocr_results:
            return jsonify({'extracted_text': "Process completed: No text lines found."})

        parsed_blocks = []
        for bounding_box, text_string, confidence in ocr_results:
            text_string = str(text_string).strip()
            if not text_string:
                continue
                
            # Calculate geometric centers of the bounding box
            # box coordinates index map: 0=top-left, 1=top-right, 2=bottom-right, 3=bottom-left
            y_center = (bounding_box[0][1] + bounding_box[2][1]) / 2
            x_center = (bounding_box[0][0] + bounding_box[1][0]) / 2
            
            parsed_blocks.append({'x': x_center, 'y': y_center, 'text': text_string})

        # Intelligent Row Sorting Algorithm
        grouped_rows = []
        row_threshold_pixels = 18  # Pixel cluster buffer grouping text on a shared horizontal plane

        for block in parsed_blocks:
            is_matched_to_row = False
            for row in grouped_rows:
                # If this text item sits closely on the vertical plane to an existing row, group it
                if abs(row[0]['y'] - block['y']) < row_threshold_pixels:
                    row.append(block)
                    is_matched_to_row = True
                    break
            if not is_matched_to_row:
                grouped_rows.append([block])

        # Sort all compiled row arrays vertically from top to bottom
        grouped_rows.sort(key=lambda r: r[0]['y'])

        # Compile output lines with robust columnar spacing alignment delimiters
        compiled_output_lines = []
        for row in grouped_rows:
            # Sort separate column text pieces from left to right along the horizontal X-axis
            row.sort(key=lambda item: item['x'])
            row_string = "   |   ".join([item['text'] for item in row])
            compiled_output_lines.append(row_string)

        formatted_structured_text = "\n".join(compiled_output_lines)
        return jsonify({'extracted_text': formatted_structured_text})

    except Exception as runtime_fault:
        return jsonify({'error': f"Core Spatial Engine Failure: {str(runtime_fault)}"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)