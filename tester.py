import sys
from imageProcessing import processImage
import difflib #library for comparing differences

"""
This code is for comparing an image file's actual text to the text derived
from OCR.

Running the tester.py file:
    Arguments:
        1: greyscale (0: without, 1: with)
        2: read (0: don't read, 1: read)
        3: blur (0: no blur, 1: averaging, 2: gaussian, 3: median, 4: bilateral filtering)
        4: threshold (0: no blur, 1: simple, 2: adaptive, 3: otsu's)

IMPORTANT: greyscale is needed to apply threshold
"""

TEXT = """
Alexa's Party:
November 19,
2021
"""

def difference(greyscale, read, blur, threshold):
    print(TEXT)

    processed = processImage('sampleImage.jpg', greyscale, 1,
                blur, threshold).lower().strip()
    problem_list = []

    """
    Uses difflib to check how many differences there are between the original,
    correct string and the string processed using ocr.
    """
    for x, y in enumerate(difflib.ndiff(TEXT.lower().strip(), processed)):
        if y[0] == ' ': continue
        elif y[0] == '-':
            problem_list.append('Delete "{}" from position {}'.format(y[-1], x))
        elif y[0] == '+':
            problem_list.append('Add "{}" to position {}'.format(y[-1], x))

    print(processed + "\n")
    print(problem_list)
    print("THERE ARE THIS MANY PROBLEMS IN THE SAMPLE IMAGE: " + str(len(problem_list)))

if __name__ == '__main__':
    difference(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
