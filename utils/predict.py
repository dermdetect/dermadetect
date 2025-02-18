import cv2
import numpy as np
import tensorflow as tf
import google.generativeai as genai
import json
import re
import os
from PIL import Image
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

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

def configure_genai():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return {"status": "error", "message": "GEMINI_API_KEY is not set.", "label": None, "confidence": None}
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def sanitize_response(response_content):
    try:
        json_match = re.search(r'{.*}', response_content, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in response.")
        sanitized_json = re.sub(r'(?<!\\)([\n\r\t])', '', json_match.group())
        sanitized_json = re.sub(r'\\', r'\\\\', sanitized_json)
        return json.loads(sanitized_json)
    except Exception as e:
        return {"status": "error", "message": f"Error sanitizing Gemini response: {str(e)}", "label": None, "confidence": None}

def analyze_image(image_path):
    try:
        model = configure_genai()
        if isinstance(model, dict):
            return model
        prompt = "Identify if the provided image is a human body part or not. Also you need to identify if the given skin is healthy or not. Respond in JSON format with 'is_human_body_part': true or false and 'healthy_skin': true or false."
        image = Image.open(image_path)
        response = model.generate_content(contents=[prompt, image])
        return sanitize_response(response.text)
    except Exception as e:
        return {"status": "error", "message": f"Gemini API call failed: {str(e)}", "label": None, "confidence": None}

def predict(image_path):
    try:
        analysis = analyze_image(image_path)
        if analysis.get("status") == "error":
            return analysis

        if str(analysis.get('is_human_body_part', '')).lower() in ['false', '0', 'no', 'none', 'null', '']:
            return {"status": "error", "message": "The image is not recognized as a human body part.", "label": None, "confidence": None}

        if str(analysis.get('healthy_skin', '')).lower() in ['true', '1', 'yes']:
            return {"status": "error", "message": "Detected healthy skin, no prediction required.", "label": None, "confidence": None}

        image = cv2.imread(image_path)
        image = cv2.resize(image, (128, 128)) / 255.0
        model = tf.keras.models.load_model("model.h5", compile=False)
        prediction = model.predict(np.array([image]))
        prediction_index = np.argmax(prediction)
        label = labels[prediction_index]
        prediction_percentage = float(np.max(prediction))

        return {
            "status": "success",
            "message": "Prediction successful.",
            "label": label,
            "confidence": prediction_percentage
        }
    except Exception as e:
        return {"status": "error", "message": f"Prediction failed: {str(e)}", "label": None, "confidence": None}



# # Example call
# print(predict("../test_images/image.jpg"))
# print(predict("../test_images/body.jpg"))
# print(predict("../test_images/body2.jpg"))
# print(predict("../test_images/nature.jpg"))
# print(predict("../test_images/0_0.jpg"))
