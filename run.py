import sys
from imageProcessing import processImage
import os
from convertToCalendar import convertToCalendar
from makeEvent import makeCalendarEvent

"""
Arguments when running the file:
    1: name of image file to process
    2: whether to delete the file or not (0: keep, 1: delete)

Example: python3 run.py sample_image.jpg 1
=> creates the calendar event and deletes the image after
"""

processedString = ""

if len(sys.argv) == 2: #if one argument is given after file name in run command
    processedString = processImage(sys.argv[1], 1, 0, 1, 3)
elif len(sys.argv) == 3: #if two arguments are given after file name in run command
    processedString = processImage(sys.argv[1], 1, 0, 1, 3)
    if (sys.argv[2] == "1"):
        os.remove(sys.argv[1]) #removes the file from the working directory
else:
    print("Please enter the correct amount of arguments.")
    sys.exit()

date, name = convertToCalendar(processedString)

makeCalendarEvent(date, name)
