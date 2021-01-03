import sys
from image_processing import process_image
import os

"""
Arguments:
    1: name of image file to process
    2: whether to delete the file or not (0: keep, 1: delete)
"""

if len(sys.argv) == 2:
    print(process_image(sys.argv[1], 1, 1, 1, 3))
elif len(sys.argv) == 3:
    print(process_image(sys.argv[1], 1, 1, 1, 3))
    if (sys.argv[2] == "1"):
        os.remove(sys.argv[1])
else:
    print("Please enter the correct amount of arguments.")