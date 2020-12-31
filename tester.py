#!/usr/bin/python
import sys
from image_processing import process_image
import difflib #library for comparing differences

"""
Running the tester.py file:
    Arguments:
        1: image number
        2: greyscale (0: without, 1: with)
        3: read (0: don't read, 1: read)
        4: blur (1: averaging, 2: gaussian, 3: median, 4: bilateral filtering)
        5: threshold (1: simple, 2: adaptive, 3: otsu's)

IMPORTANT: greyscale is needed to apply threshold

Examples:
$ python3 tester.py 6 1 1 2 2
=> image 6, greyscale, read, gaussian, adaptive
$ python3 tester.py 7
=> image 7, no greyscale, don't read, no blur, no threshold
$ python3 tester.py 1 1 1
=> image 1, greyscale, read
$ python3 tester.py 8 1 0 3 3
=> image 8, greyscale, don't read, median, otsu's
"""

TEXT_1 = """
how to create
random, sample text
in microsoft word
\u00a9 kent L\u00f6fgren, Sweden
"""

TEXT_2 = """
engineers
on the green
engineering organization fair
monday, september 30, 2019
2pm - 6pm \u2022 warren mall
meet orgs, get free food, and have fun
"""

TEXT_3 = """
acm eats @ in-n-out
10/03/19 @ 9:00pm. 2910 damon ave, san diego, ca 92109
"""

#what to do about the C++ symbol?
TEXT_4 = """
acm x tse
advance c++ workshops
november 8 & 15 6:30-9 pm
tse.ucsd.edu
"""

TEXT_5 = """
poems. 35
xxi.
a book.
he ate and drank the precious words,
his spirit grew robust;
he knew no more that he was poor,
nor that his frame was dust.
he danced along the dingy days,
and this bequest of wings
was but a book. what liberty
a loosened spirit brings!
"""

TEXT_6 = """
Alexa's Party: November
19, 2021
"""

TEXT_7 = """
Alexa's Party: November 19, 2021
"""

TEXT_8 = """
Alexa's Party:
November 19,
2021
"""

TEXT_9, TEXT_10, TEXT_11, TEXT_12, TEXT_13 = TEXT_8, TEXT_8, TEXT_8, TEXT_8, TEXT_8


text_list = [TEXT_1, TEXT_2, TEXT_3, TEXT_4, TEXT_5, TEXT_6, TEXT_7, TEXT_8,
            TEXT_9, TEXT_10, TEXT_11, TEXT_12, TEXT_13]

def difference(i, greyscale, read, blur, threshold):
    print(text_list[i])

    processed = process_image('image' + str(i + 1) + ".jpg", greyscale, read,
                blur, threshold).lower().strip()
    problem_list = []

    """
    Uses difflib to check how many differences there are between the original,
    correct string and the string processed using ocr.
    """
    for x, y in enumerate(difflib.ndiff(text_list[i].lower().strip(), processed)):
        if y[0] == ' ': continue
        elif y[0] == '-':
            problem_list.append('Delete "{}" from position {}'.format(y[-1], x))
        elif y[0] == '+':
            problem_list.append('Add "{}" to position {}'.format(y[-1], x))

    print(processed + "\n")
    print(problem_list)
    print("THERE ARE THIS MANY PROBLEMS IN TEXT_" + str(i + 1) + ": " + str(len(problem_list)))

if len(sys.argv) == 2:
    difference(int(sys.argv[1]) - 1, 0, 0, None, None)
elif len(sys.argv) == 3:
    difference(int(sys.argv[1]) - 1, int(sys.argv[2]), 0, None, None)
elif len(sys.argv) == 4:
    difference(int(sys.argv[1]) - 1, int(sys.argv[2]), int(sys.argv[3]), None, None)
elif len(sys.argv) == 5:
    difference(int(sys.argv[1]) - 1, int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), None)
elif len(sys.argv) == 6:
    difference(int(sys.argv[1]) - 1, int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
else: #not finished yet
    for i in range(13):
        difference(i)
