import pytesseract
import cv2
from flask import Flask, render_template, request
from price_calc import calculate_prices
from map_vendors import generate_vendor_map
from flask import request
from medicine_data import medicine_database
from vendor_graph import generate_vendor_graph
from chatbot import get_chatbot_response

import os
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
app = Flask(__name__)
current_medicine = None
# Upload folder setup
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Welcome Page
@app.route('/')
def welcome():
    return render_template('welcome.html')


# Dashboard Page (after name input)

@app.route('/dashboard', methods=['POST'])
def dashboard():

    name = request.form.get('username')

    # Dummy medicine (before upload)
    generate_vendor_map()
    dummy_medicine = {
        "name": "Upload medicine to see details",
        "contents": "-",
        "applications": "-",
        "side_effects": "-",
        "expiry": "-",
        "dose": "-",
        "vendors": "-"
    }

    return render_template(
        'dashboard.html',
        name=name,
        medicine=dummy_medicine,
        days_left=0
    )


# Upload Route
@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['medicine_image']

    if not file:
        return "No file uploaded"

    filename = file.filename.lower()

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        filename
    )

    file.save(filepath)

    img = cv2.imread(filepath)

    if img is None:
        return "Error reading image"

    texts = []

    # Try rotations
    for angle in [0, 90, 180, 270]:

        if angle == 90:
            rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

        elif angle == 180:
            rotated = cv2.rotate(img, cv2.ROTATE_180)

        elif angle == 270:
            rotated = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

        else:
            rotated = img

        # Convert to grayscale
        gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)

        # Mild blur (not heavy)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        # Otsu threshold
        _, thresh = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        # OCR
        text = pytesseract.image_to_string(
            thresh,
            config='--oem 3 --psm 6'
        )

        texts.append(text.lower())

    extracted_text = " ".join(texts)

    print("\nFULL OCR TEXT:")
    print(extracted_text)

    # Clean text
    import re
    extracted_text = re.sub(
        r'[^a-z0-9 ]',
        ' ',
        extracted_text
    )

    words_detected = extracted_text.split()

    print("\nDetected Words:")
    print(words_detected)

    # 🔥 FUZZY MATCHING (VERY IMPORTANT)
    from difflib import get_close_matches

    medicine_key = None

    print("\nChecking medicines...")

    for key in medicine_database:

        print("Checking:", key)

        keywords = medicine_database[key]["keywords"]

        for keyword in keywords:

            match = get_close_matches(
                keyword,
                words_detected,
                n=1,
                cutoff=0.6   # similarity %
            )

            if match:

                medicine_key = key

                print("Matched:", match[0])

                break

        if medicine_key:
            break

    if medicine_key:
        global current_medicine
        current_medicine = medicine_key

        medicine = medicine_database[medicine_key]
        price_data = calculate_prices(
 medicine["price_per_tablet"],
    medicine["tablets_per_strip"]
)
       


        return render_template(
            "dashboard.html",
            name="User",
            medicine=medicine,
            price_data=price_data
        )

    else:

        print("No medicine matched")

        return "Medicine not detected from image"
@app.route('/vendor-map')
def vendor_map():

    generate_vendor_map()

    return render_template(
        "vendor_map.html"
    )
@app.route('/update-location', methods=['POST'])
def update_location():

    lat = float(request.form.get("lat"))
    lon = float(request.form.get("lon"))

    generate_vendor_map(lat, lon)

    return "Location Updated"
@app.route('/get-graph')
def get_graph():

    global current_medicine

    generate_vendor_graph(current_medicine)

    return "Graph Ready"
@app.route('/chat', methods=['POST'])
def chat():

    user_msg = request.form['message']

    reply = get_chatbot_response(user_msg)

    return reply
if __name__ == '__main__':
    app.run(debug=True)