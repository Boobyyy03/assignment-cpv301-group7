import cv2 as cv 
from deepface import DeepFace
import numpy as np

model = DeepFace.build_model("Emotion")

emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

face_cascade = cv.CascadeClassifier("D:/FPT/SP24/CPV301/Lab/lab 7&8/haarcascade_frontalface_default.xml")

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        
        # Ensure resizing maintains grayscale format
        resized_face = cv.resize(face_roi, (48, 48), interpolation=cv.INTER_AREA)
        
        # Ensure resized_face has correct number of channels
        resized_face = cv.cvtColor(resized_face, cv.COLOR_GRAY2RGB)
        
        # Normalize resized_face
        normalized_face = resized_face / 255.0
        
        # Reshape normalized_face
        reshape_face = normalized_face[np.newaxis, ...]
        
        preds = model.predict(reshape_face)[0]
        emotion_idx = preds.argmax()
        emotion = emotion_labels[emotion_idx]
        cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv.putText(frame, emotion, (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
    cv.imshow("Input image", frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
