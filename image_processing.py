import cv2
import pytesseract

img = cv2.imread('tester.jpg')

# Adding custom options
custom_config = '--oem 3 --psm 6'
print(pytesseract.image_to_string(img, config=custom_config))
