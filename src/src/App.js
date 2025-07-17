import React, { useState } from 'react';
import './App.css';

function App() {
  const [emotion, setEmotion] = useState(null);

  const handleUpload = (event) => {
    const file = event.target.files[0];

    const formData = new FormData();
    formData.append('file', file);

    fetch('http://localhost:8000/predict', {
      method: 'POST',
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => setEmotion(data.emotion))
      .catch((err) => console.error(err));
  };

  return (
    <div className="App">
      <h1>Voice Emotion Detector</h1>
      <input type="file" accept="audio/*" onChange={handleUpload} />
      {emotion && <h2>Detected Emotion: {emotion}</h2>}
    </div>
  );
}

export default App;
