from flask import Flask, request
from flask_cors import CORS
from compute_emotion import predicting_emotion
import os
import subprocess

app = Flask(__name__)
CORS(app)

@app.route("/predict", methods=["POST"])

def predict():
    if 'file' not in request.files:
        return {"error": "No file part in the request"}, 400 # 400 is for bad response
    file = request.files["file"]

    if file.filename == '':
        return {"error": "No file selected"}, 400
    upload_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_dir, exist_ok=True) # Create the directory if it doesn't exist

    input_path = os.path.join(upload_dir, file.filename)

    output_filename = os.path.splitext(file.filename)[0] + ".wav"
    output_path = os.path.join(upload_dir, output_filename)

  
    file.save(input_path)

    # Converts the recorded audio file using ffmpeg conversion

    try:
        subprocess.run(['ffmpeg', '-i', input_path, output_path, '-y'], check = True) 
    except subprocess.CalledProcessError:
        # If ffmpeg fails, return an error
        return {"error": "Failed to convert the audio file."}, 500 # 500 is for internal server error


    # Get the emotion from the predicting_emotion file
    emotion = predicting_emotion(output_path)
    os.remove(input_path)
    os.remove(output_path)

    # Returns a json file
    return {"emotion": str(emotion)}

# For testing
if __name__ == "__main__":
    app.run(debug = True)