import cv2 as cv 


#img = cv .imread("D:/FPT/SP24/CPV301/Lab/Picture/cat1.jpg")

cap = cv.VideoCapture("D:/FPT/SP24/CPV301/Lab/Picture/test3.avi")


classNames = []
classFile = "D:/FPT/SP24/CPV301/Assignment/model/classes.txt" 
with open(classFile,'rt') as f :
    classNames = f.read().rstrip('\n').split('\n')

configPath = "D:/FPT/SP24/CPV301/Assignment/model/yolov4.cfg"
weightsPath = "D:/FPT/SP24/CPV301/Assignment/model/yolov4.weights"

net = cv.dnn.DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5,127.5,127.5))
net.setInputSwapRB(True)
while True:
    ret, frame1 = cap.read()
    classIds, confs, bbox = net.detect(frame1,confThreshold=0.5,nmsThreshold = 0.4)

    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(),confs.flatten(),bbox):
            cv.rectangle(frame1,box,color=(0,0,255),thickness= 2)
            cv.putText(frame1,classNames[classId],(box[0] + 10,box[1] + 30),
                    cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    cv.imshow("Input image", frame1)

    
    if (cv.waitKey(0) & 0xFF == ord('d')):
        break
    
cap.release()
cv.destroyAllWindows()
