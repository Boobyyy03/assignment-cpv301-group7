import cv2

# Load the image
img = cv2.imread("D:/FPT/SP24/CPV301/Lab/lab 7&8/Image/1.jpg")

# Check if the image is loaded successfully
if img is None:
    print("Error: Unable to load the image.")
else:
    # Specify the desired width and height
    desired_width = 800
    desired_height = 600

    # Resize the image
    resized_img = cv2.resize(img, (desired_width, desired_height))

    # Display the original and resized images
    cv2.imwrite("resize3.jpg",resized_img)
    cv2.imshow("Resized Image", resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()