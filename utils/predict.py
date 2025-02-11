import cv2
import numpy as np
import tensorflow as tf

labels = ['1. Eczema 1677',
          '10. Warts Molluscum and other Viral Infections - 2103',
          '2. Melanoma 15.75k',
          '3. Atopic Dermatitis - 1.25k',
          '4. Basal Cell Carcinoma (BCC) 3323',
          '5. Melanocytic Nevi (NV) - 7970',
          '6. Benign Keratosis-like Lesions (BKL) 2624',
          '7. Psoriasis pictures Lichen Planus and related diseases - 2k',
          '8. Seborrheic Keratoses and other Benign Tumors - 1.8k',
          '9. Tinea Ringworm Candidiasis and other Fungal Infections - 1.7k']


def predict(image_path):
    # Load face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    # Read image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Check if a face is detected
    if len(faces) == 0:
        return "Error: No face detected in the image. Please upload an image containing a human face."
    
    # Preprocess image
    image = cv2.resize(image, (128, 128))
    image = image / 255.0
    
    # Load model
    model = tf.keras.models.load_model("model.h5", compile=False)
    
    # Predict
    prediction = model.predict(np.array([image]))
    prediction_index = np.argmax(prediction)
    label = labels[prediction_index]
    prediction_percentage = np.max(prediction)
    
    return label, prediction_percentage