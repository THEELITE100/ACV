import os
import uuid
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
def improved_pencil_sketch(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    invert = 255 - gray
    blur1 = cv2.GaussianBlur(invert, (21,21), 0)
    blur2 = cv2.GaussianBlur(invert, (51,51), 0)
    blur = cv2.addWeighted(blur1, 0.5, blur2, 0.5, 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    edges = cv2.Canny(gray, 30, 120)
    edges = cv2.dilate(edges, np.ones((2,2), np.uint8))
    edges = 255 - edges
    final = cv2.multiply(sketch, edges, scale=1/255)
    return cv2.addWeighted(final, 1.3, cv2.GaussianBlur(final, (0,0), 3), -0.3, 0)
def balanced_watercolor(image):
    gaussian_blur = cv2.GaussianBlur(image, (0, 0), 3)
    original_detail = cv2.addWeighted(image, 1.5, gaussian_blur, -0.5, 0)
    painterly = image.copy()
    for _ in range(3):
        painterly = cv2.bilateralFilter(painterly, d=9, sigmaColor=75, sigmaSpace=75)
    watercolor_base = cv2.addWeighted(painterly, 0.7, original_detail, 0.3, 0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(cv2.GaussianBlur(gray, (3,3), 0), 50, 150)
    edges_inv = cv2.cvtColor(255 - edges, cv2.COLOR_GRAY2BGR)
    result = cv2.multiply(watercolor_base, edges_inv, scale=1/255)
    return result
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    style = request.form.get('style', 'pencil')    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], unique_filename)    
    file.save(input_path)
    img = cv2.imread(input_path)
    if style == 'pencil':
        processed_img = improved_pencil_sketch(img)
    elif style == 'watercolor':
        processed_img = balanced_watercolor(img)
    else:
        return jsonify({'error': 'Invalid style selected'}), 400
    cv2.imwrite(output_path, processed_img)
    return jsonify({
        'original_url': f"/{input_path}",
        'processed_url': f"/{output_path}"
    })
if __name__ == '__main__':
    app.run(debug=True)