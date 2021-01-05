import sys
from image_processing import processImage
import os
from convert_to_calendar import convertToCalendar
from make_event import makeCalendarEvent

"""
Arguments:
    1: name of image file to process
    2: whether to delete the file or not (0: keep, 1: delete)
"""

processed_string = ""

if len(sys.argv) == 2:
    processed_string = process_image(sys.argv[1], 1, 1, 1, 3)
elif len(sys.argv) == 3:
    processed_string = process_image(sys.argv[1], 1, 1, 1, 3)
    if (sys.argv[2] == "1"):
        os.remove(sys.argv[1])
else:
    print("Please enter the correct amount of arguments.")
    sys.exit()

date, name = convertToCalendar(processed_string)

makeCalendarEvent(date, name)
