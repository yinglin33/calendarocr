import cv2
from pytesseract import image_to_string

def process_image(filename):

    img = cv2.imread(filename, 0)
    img = cv2.GaussianBlur(img, (5, 5), 0)

    #ret, img_binary = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    #img_adaptive = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    # Adding custom options
    custom_config = '--oem 3 --psm 6'

    return image_to_string(img, config=custom_config)


if __name__ == '__main__':
    print(process_image("image2.jpg"))
