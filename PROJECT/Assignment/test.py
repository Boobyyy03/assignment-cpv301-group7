import cv2 as cv

# Load the video file
#video_path = 'C:\\Users\\Administrator\\Documents\\GitHub\\assignment-cpv301-group7\\LABs\\humanVideos\\human_1feet1human.mp4'
cap = cv.VideoCapture(0)

# Check if the video file was successfully opened
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Create the HOG descriptor for human detection
hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HO)

# Read frames from the video
while True:
    # Read the next frame
    ret, frame = cap.read()

    # If the frame was not successfully read, exit the loop
    if not ret:
        break

    # Resize the frame for faster processing (optional)
    frame = cv.resize(frame, (640, 480))

    # Convert the frame to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect humans in the frame
    humans, _ = hog.detectMultiScale(gray, winStride=(8, 8), padding=(4, 4), scale=1.05)

    # Draw rectangles around the detected humans
    for (x, y, w, h) in humans:
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the frame with human detection
    cv.imshow('Human Detection', frame)

    # Exit the loop if 'q' is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the windows
cap.release()
cv.destroyAllWindows()