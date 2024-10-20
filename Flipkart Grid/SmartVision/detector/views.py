from django.shortcuts import render
import os
import requests
import json
from django.shortcuts import render
from django.core.files.storage import default_storage
import tensorflow as tf
from PIL import Image
import numpy as np
import cv2
import time
from pytesseract import pytesseract

# Load the local fruit/vegetable model
model = tf.keras.models.load_model('/Users/vishwaskisaniya/Developer/amazonML/Flipkart Grid/SmartVision/models/cnnFruitModel.h5')

def index(request):
    return render(request, 'detector/index.html')

# Function to handle the RoboFlow object detection (using HTTP request)
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import default_storage
import requests
import json

from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render
import requests

def detect_object(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        # Save the uploaded image to a temporary location
        image_path = default_storage.save('temp_image.jpg', image)

        # Create a file URL that points to the correct media file location
        image_url = request.build_absolute_uri(default_storage.url(image_path))

        # RoboFlow API credentials
        api_key = 'wlM4fbrScwixZIs7sgoV'
        model_url = 'https://detect.roboflow.com/infer'  # Change this to your specific model URL if needed
        
        # Prepare the payload
        payload = {
            "api_key": api_key,
            "inputs": {
                "image": {"type": "url", "value": image_url}
            }
        }

        headers = {
            'Content-Type': 'application/json'
        }

        # Make API request
        response = requests.post(model_url, headers=headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response
            result = response.json()
            output = result.get('predictions', {}).get('predictions', [])
            count_objects = result.get('predictions', {}).get('count_objects', 0)
            output_image = result.get('predictions', {}).get('output_image', {}).get('base64', None)
        else:
            # Handle error response
            output = []  # Or log the error message
            count_objects = 0
            output_image = None

        # Return the results to a new template
        return render(request, 'detector/roboflow_result.html', {
            'output': output,
            'count_objects': count_objects,
            'output_image': output_image,
            'image_url': image_url
        })

# Function to handle the local fruit/vegetable model detection
LABELS = ['Apple','Fresh Banana', 'Banana', 'Rotten grapes', 'Fresh Apple', 'Rotten Orange', 
          'Mango', 'Rotten Apple', 'Fresh Apple', 'Rotten Banana', 'Pineapple', 'Rotten Pineapple', 
          'Watermelon', 'Other']

def detect_fruit(request):
    if request.method == "POST":
        uploaded_image = request.FILES['image']
        
        # Use uploaded_image instead of image
        image_path = default_storage.save('temp_fruit_image.jpg', uploaded_image)

        # Preprocess image for model
        img = Image.open(image_path)
        img = img.resize((112, 112))  # Adjust to your model's input size
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Make prediction
        prediction = model.predict(img_array)
        predicted_label_index = np.argmax(prediction)
        predicted_label = LABELS[predicted_label_index]
        
        # Return the result (adjust this part as per your needs)
        return render(request, 'detector/result.html', {'prediction': predicted_label})

# Function to capture images from mobile camera stream and extract text
def capture_from_camera(request):
    if request.method == "POST":
        camera_url = request.POST.get('camera_url', 'http://192.168.1.7:8080/video')
        interval = int(request.POST.get('interval', 5))  # Capture interval in seconds
        num_items = int(request.POST.get('num_items', 5))  # Number of captures
        save_folder = 'items'
        
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        camera = cv2.VideoCapture(camera_url)
        capture_count = 0
        last_capture_time = time.time()
        extracted_texts = []  # Store extracted texts for display

        while capture_count < num_items:
            ret, frame = camera.read()
            if not ret:
                print("Failed to grab frame. Check the camera connection.")
                break

            current_time = time.time()
            if current_time - last_capture_time >= interval:
                capture_count += 1
                image_name = f"item_{capture_count}"
                image_path = os.path.join(save_folder, f"{image_name}.jpeg")
                cv2.imwrite(image_path, frame)
                print(f"Captured and saved {image_path}")

                # Extract text from the image
                extracted_text = extract_text(image_path)
                extracted_texts.append(extracted_text)

                last_capture_time = current_time

        camera.release()
        cv2.destroyAllWindows()

        # Return the captured and extracted texts to the frontend
        return render(request, 'detector/capture_result.html', {'extracted_texts': extracted_texts})

# Function to extract text using Tesseract
def extract_text(image_path):
    path_to_tesseract = r"/opt/homebrew/bin/tesseract"
    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(Image.open(image_path))
    return text.strip()
