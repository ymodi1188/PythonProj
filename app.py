from flask import Flask, request, jsonify
import cv2
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

def analyze_frame(frame):
    # This function should analyze the frame and return the mood
    # For now, it's a placeholder that always returns "Happy"
    return "Happy"
from flask import Flask, render_template

app = Flask(__name__)

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
