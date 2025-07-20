# Voice Emotion Detector based on CREMA-D dataset

A full stack web application that can predict emotions based on the user's voice using a deep learning model built.


## Description
A website that allows user to record their voice and detect emotions. Where it is analyzed by a ResNet model trained to classify emotions.

### Features
Real time audio recording: Captures microphone audio on the browser using MediaRecorder API
Deep Learning Model: Custom trained Res-Net model to classify 6 different emotions (anger, disgust, fear, happy, neutral, sad). (This model can be found inside notebooks folder labeled resnet_model_best.keras)
Audio Processing: Pipeline that converts raw audio into log mel spectrogram, which is further used to train the model.



### Limitations
- The model has a 64% validation accuracy and can be improved. 
- Might not generalize well outside the training dataset (CREMA_D)

### Improvements in the future
- Try and improve accuracy 
- Try other model architectures 
- Use more features


## Setup
Run on two terminal


### Backend Server (Terminal 1)
```bash
# Navigate to the backend folder
cd backend

# Create a virtual environment
python3 -m venv venv
# Activate the environment
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Run the server
python server.py
```

### Frontend (Terminal 2)
```bash
# Navigate to frontend folder
cd frontend

# Install the required packages
npm install

# Run the server
npm start
```


You can open browser and type `http://localhost:3000` to see the application.