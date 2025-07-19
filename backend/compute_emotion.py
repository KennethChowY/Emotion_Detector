import librosa
import tensorflow as tf
import numpy as np
from tensorflow import keras # Do not know why tensorflow.keras does not work so do it this way instead
from keras import layers
import os



# The FrequencyMask class is needed here so the loaded model can run, since its not originally in the keras library
class FrequencyMask(layers.Layer):
    def __init__(self, max_mask_size=16, **kwargs):
        super(FrequencyMask, self).__init__(**kwargs)
        self.max_mask_size = max_mask_size

    def call(self, inputs, training=None):
        if not training:
            return inputs
        
        num_mels = tf.shape(inputs)[1]
        mask_size = tf.random.uniform(shape=[], minval=0, maxval=self.max_mask_size, dtype=tf.int32)
        mask_start = tf.random.uniform(shape=[], minval=0, maxval=num_mels - mask_size, dtype=tf.int32)
        mask_range = tf.range(num_mels, dtype=tf.int32)
        mask_condition = (mask_range < mask_start) | (mask_range >= mask_start + mask_size)
        mask = tf.cast(mask_condition, inputs.dtype)
        mask = tf.reshape(mask, (1, num_mels, 1, 1))
        return inputs * mask
    def get_config(self):
        config = super().get_config()
        config.update({"max_mask_size": self.max_mask_size})
        return config

# Loads the model
model = keras.models.load_model(
    "resnet_model_best.keras", 
    custom_objects = {"FrequencyMask": FrequencyMask}
)

# The emotion coded
emotion_code = {
  0: "anger",
  1: "disgust",
  2: "fear",
  3: "happy",
  4: "neutral",
  5: "sad"
}


# Normalizing settings (this was used in the training)
min_x = -80.0 
max_x = 0.0


def predicting_emotion(voice_file):

    # print("recieved voice_file") debugging
    # print(voice_file)
    MAX_LEN = 174 
    waveform, sr = librosa.load(voice_file, sr = 22050)

    # Converting to mel_spec
    mel_spec = librosa.feature.melspectrogram(y = waveform, sr = sr, n_mels = 128)
    log_mel_spec = librosa.power_to_db(mel_spec, ref = np.max)

    log_mel_spec = (log_mel_spec - min_x) / (max_x - min_x)

    # Padding and truncating 
    if log_mel_spec.shape[1] < MAX_LEN:
        pad_width = MAX_LEN - log_mel_spec.shape[1]
        log_mel_spec = np.pad(log_mel_spec, pad_width=((0, 0), (0, pad_width)), mode = 'constant')
    else:
        log_mel_spec = log_mel_spec[:, :MAX_LEN]

    # This is specifically used for this model because it was trained in this way
    log_mel_spec = log_mel_spec[..., np.newaxis] # Adding channel
    log_mel_spec = log_mel_spec[np.newaxis, ..., np.newaxis]


    # Predicts the model!
    predicted_emotion = model.predict(log_mel_spec)
    max_index = np.argmax(predicted_emotion)
    person_emotion = emotion_code[max_index]
    return person_emotion




# debugging
if __name__ == "__main__":
    # upload a file into the upload folder and uncomment below 
    # test_file = "uploads/testing.wav"
    voices_file = "uploads/voice_recording.wav"
    file_path = os.path.abspath(voices_file)
    predicted_emotion  = predicting_emotion(file_path)
    print(predicted_emotion)



# Emotion Label Mapping:
# 0: ANG
# 1: DIS
# 2: FEA
# 3: HAP
# 4: NEU
# 5: SAD