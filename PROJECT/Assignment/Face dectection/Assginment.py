import cv2 as cv

face_cascade = cv.CascadeClassifier("D:/FPT/SP24/CPV301/Assignment/cascade/haarcascade_frontalface_default.xml")

eyes_cascade = cv.CascadeClassifier("D:/FPT/SP24/CPV301/Assignment/cascade/haarcascade_eye_tree_eyeglasses.xml")

nose_cascade = cv.CascadeClassifier("D:/FPT/SP24/CPV301/Assignment/cascade/haarcascade_mcs_nose.xml")

mouth_cascade = cv.CascadeClassifier("D:/FPT/SP24/CPV301/Assignment/cascade/haarcascade_mcs_mouth.xml")


cap = cv.VideoCapture(0)


while (True):
    ret,frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.1,4)


    for (x,y,w,h) in  faces :
        cv.rectangle(frame,(x,y),(x+w,y+h), (255,0,0),2)
        cv.putText(frame,"Face", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        
    eyes = eyes_cascade.detectMultiScale(gray,1.1,4)

    for (x,y,w,h) in  eyes :
        cv.rectangle(frame,(x,y),(x+w,y+h), (0,255,0),2)
        cv.putText(frame, "Eyes", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
    noses = nose_cascade.detectMultiScale(gray,1.1,4)

    for (x,y,w,h) in  noses :
        cv.rectangle(frame,(x,y),(x+w,y+h), (0,0,255),2)
        cv.putText(frame, "Nose", (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)    
    
    mouths = mouth_cascade.detectMultiScale(gray,1.1,4)
    for (x,y,w,h) in mouths :
        cv.rectangle(frame,(x,y),(x+w,y+h), (0,255,0),2)
        cv.putText(frame, "Mouth", (x, y-4), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)  
        
    cv.imshow("Input image",frame)
    if cv.waitKey(1) == ord(("d")):
        break
cap.release()
cv.destroyAllWindows()
