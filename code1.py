import cv2
import pytesseract
import serial
# Open the serial connection to the Pico board
ser = serial.Serial('COM6', 128000)
# Function to extract a two-digit number from an image
def extract_two_digit_number(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply image processing techniques if needed (e.g., noise reduction, thresholding)
    # Perform OCR to extract the text from the image
    text = pytesseract.image_to_string(gray_image, config='--psm 7 --oem 3')
    # Process the extracted text to obtain the two-digit number
    number = ''.join(filter(str.isdigit, text))
    if len(number) == 2:
        return int(number)
    else:
        return None
# Open the camera
cap = cv2.VideoCapture(0)
while True:
    # Capture a frame from the camera
    _, frame = cap.read()
    # Extract the two-digit number from the frame
    speed_limit = extract_two_digit_number(frame)
    if speed_limit == 75 or speed_limit == 50 or speed_limit == 25 :
        # Print the received speed limit
        print("Received Speed Limit:", speed_limit)
        # Send the speed limit information to the Pico board
        ser.write(str(speed_limit).encode())
    else:
        # Print "No speed limit detected" if no valid speed limit is extracted
        print("No speed limit detected")
    # Display the frame
    cv2.imshow('Camera Frame', frame)
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release the camera
cap.release()
# Close all OpenCV windows
cv2.destroyAllWindows()