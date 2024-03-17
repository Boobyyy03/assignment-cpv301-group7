import face_recognition
import os
import numpy as np
import json

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            img_path = os.path.join(folder, filename)
            image = face_recognition.load_image_file(img_path)
            images.append(image)
    return images

def compute_face_encodings(images):
    encodings = []
    for image in images:
        face_encoding = face_recognition.face_encodings(image)
        if face_encoding:
            encodings.append(face_encoding[0])
    return encodings

# Provide the correct relative path to the folder containing images
folder_path = r'C:\Users\DP-COMPUTER\Desktop\Automated-Attendance-System-with-Face-Recognition-main\Training_ Finding encodings\faces'

# Load images from the folder
images = load_images_from_folder(folder_path)

# Compute face encodings
encodings = compute_face_encodings(images)

# Convert encodings to list of lists
encodings = [encoding.tolist() for encoding in encodings]

# Store encodings to a JSON file
with open('encodings.json', 'w') as file:
    json.dump(encodings, file)
