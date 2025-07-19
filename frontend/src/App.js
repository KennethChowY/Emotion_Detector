import React, { useState, useRef } from 'react';


export default function App() {

  // just variables
  const [isRecording, setIsRecording] = useState(false);
  const [emotion, setEmotion] = useState('');
  const [status, setStatus] = useState('Click the button to start recording');
  
  // useRef to hold var
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);

  // Starts recording and trys to get users microphone
  const startRecording = async () => {
    setEmotion('');
    setStatus('Getting microphone...');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      // new MediaRecorder instance 
      mediaRecorder.current = new MediaRecorder(stream);
      
      // When audio avaliable
      mediaRecorder.current.ondataavailable = (event) => {
        audioChunks.current.push(event.data);
      };
      
      // When recording is stopped
      mediaRecorder.current.onstop = async () => {
        setStatus('Processing...');

        // Combining audio
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
        const audioFile = new File([audioBlob], "voice_recording.webm", { type: "audio/webm" });

        const formData = new FormData();
        formData.append("file", audioFile);

        try {
          // Sending to backend
          const response = await fetch('/predict', {
            method: 'POST',
            body: formData,
          });

          if (response.ok) {
            const data = await response.json();
            // Update state
            setEmotion(data.emotion);
            setStatus('Analysis Complete!');
          } else {
            console.error("Failed to get emotion from server.");
            setStatus('Error during analysis. Please try again.');
          }
        } catch (error) {
          console.error("Error sending audio to server:", error);
          setStatus('Could not connect to the server.');
        }

        // Clear the audio for new recording
        audioChunks.current = [];
        // turn off indicator
        stream.getTracks().forEach(track => track.stop());
      };
      
      // Start recording
      mediaRecorder.current.start();
      setIsRecording(true);
      setStatus('Recording... Click stop to finish.');

    } catch (error) {
      console.error("Error accessing microphone:", error);
      setStatus('Microphone access denied. Please allow microphone access in your browser settings.');
    }
  };

  // Stop recoerding
  const stopRecording = () => {
    if (mediaRecorder.current) {
      mediaRecorder.current.stop();
      setIsRecording(false);
   
    }
  };

  // Toggle recording state
  const handleToggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };


  // Ui
  return (
    <div className="bg-gray-900 text-white min-h-screen flex flex-col items-center justify-center font-sans p-4">
      <div className="w-full max-w-md mx-auto bg-gray-800 rounded-2xl shadow-2xl p-8 space-y-8 text-center">
        <h1 className="text-4xl font-bold text-cyan-400">Voice Emotion Detector</h1>
        <p className="text-gray-400">{status}</p>

        {/* Record/Stop Button */}
        <button
          onClick={handleToggleRecording}
          className={`px-8 py-4 rounded-full text-lg font-semibold transition-all duration-300 ease-in-out focus:outline-none focus:ring-4 focus:ring-opacity-50 ${
            isRecording 
              ? 'bg-red-600 hover:bg-red-700 focus:ring-red-500' 
              : 'bg-cyan-500 hover:bg-cyan-600 focus:ring-cyan-400'
          }`}
        >
          {isRecording ? 'Stop Recording' : 'Start Recording'}
        </button>

        {/* Display detected emotion */}
        {emotion && (
          <div className="mt-8 p-6 bg-gray-700 rounded-xl">
            <h2 className="text-2xl font-semibold text-gray-300">Detected Emotion:</h2>
            <p className="text-5xl font-bold text-teal-400 mt-2 capitalize">{emotion}</p>
          </div>
        )}
      </div>
    </div>
  );
}
