from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
from PIL import Image
import io
import random
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, DateTime, LargeBinary
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

app = Flask(__name__)
image_dir = 'images'  # Change this to the desired directory name
os.makedirs(image_dir, exist_ok=True)




def get_image_filename():
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    return f"{image_dir}/{timestamp}.jpg"
def analyze_frame(frame):
    # Perform face detection here and store face images in the database
    # This function should return the mood, but for now, it's a placeholder that always returns "Happy"
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        # Store a random face image in the database
        random_face = random.choice(faces)
        x, y, w, h = random_face
        face_roi = frame[y:y + h, x:x + w]

        # Convert the face image to bytes
        _, buffer = cv2.imencode('.jpg', face_roi)
        face_image_data = buffer.tobytes()
        print("face detected")
        image_filename = get_image_filename()
        cv2.imwrite(image_filename, face_roi)
        print(f"Saved face image as {image_filename}")
            
        print("face added")
        # Store the face image in the database

    return "Happy"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_mood():
    if 'frame' in request.files:
        frame = request.files['frame'].read()
        image = Image.open(io.BytesIO(frame))
        image = np.array(image)

        # Assuming image is in BGR format
        mood = analyze_frame(image)
        return jsonify({"mood": mood})
    else:
        return jsonify({"error": "No frame received"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)