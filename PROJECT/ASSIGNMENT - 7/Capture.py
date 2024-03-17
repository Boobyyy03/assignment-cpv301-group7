import face_recognition
import cv2
import os
import numpy as np
from datetime import datetime
import json
import time
from tkinter import messagebox

def record():
    faces_encodings = []
    face_names = []

    # Get the details of trained encodings from the file: 'encodings.json'
    with open('encodings.json', 'r') as file:
        faces_encodings = json.load(file)
    faces_encodings = [np.array(encoding) for encoding in faces_encodings]
    
    # Get the Roll numbers of the students from the file: 'Roll_Numbers.json'
    with open('Roll_Numbers.json', 'r') as file:
        face_names = json.load(file)
    
    def mark_attendance(name):
        with open('Attendance.csv', 'r+') as f:
            data = f.readlines()
            name_list = [line.split(',')[0] for line in data]
            if name not in name_list:
                cur_datetime = datetime.now()
                date_time = cur_datetime.strftime('%H:%M:%S')
                date = time.strftime("%d-%m-%Y")
                f.write(f'\n{name},{date_time},{date}')
            else: 
                time.sleep(5)
                messagebox.showerror('Python error', 'Your Attendance is already marked!!\nPress [esc] to return')
    
    process_this_frame = True
    capture = cv2.VideoCapture('http://192.168.1.34:4747/video') # Replace with your video capture source
    name = 'Unknown'

    while True:
        stop_record = 0
        ret, frame = capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)
        names = []

        if len(face_locations) == 0:
            name = 'Unknown'

        if process_this_frame:
            for encode, faceLoc in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(faces_encodings, encode)
                face_distances = face_recognition.face_distance(faces_encodings, encode)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index] and face_distances[best_match_index] <= 0.45:
                    name = face_names[best_match_index]
                    mark_attendance(name)
                    names.append(name)
                    stop_record = 1
                    
        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 4)

            label_width, label_height = cv2.getTextSize(name, cv2.FONT_HERSHEY_TRIPLEX, 1.0, 1)[0]

            label_x = left + (right - left - label_width) // 2
            label_y = bottom + label_height + 10
            text_x = left + (right - left - label_width) // 2
            text_y = bottom + label_height + 5

            cv2.rectangle(frame, (label_x - 5, label_y - label_height - 5), (label_x + label_width + 5, label_y + 5),
                          (255, 255, 255), cv2.FILLED)

            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (0, 0, 0), 1)

        frame = cv2.resize(frame, (800, 500))
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) == 27 or cv2.waitKey(1) == ord('q') or stop_record:
            break

# Test function
# record()
