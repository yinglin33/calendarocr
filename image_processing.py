import cv2
import pytesseract
def process_image(filename)

    img = cv2.imread(filename)

    # Adding custom options
    custom_config = '--oem 3 --psm 6'

    return pytesseract.image_to_string(img, config=custom_config)
