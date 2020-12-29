from image_processing import process_image
import difflib #library for comparing differences


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

text_list = [TEXT_1, TEXT_2, TEXT_3, TEXT_4, TEXT_5]

for i in range(5):
    print(text_list[i])

    processed = process_image('image' + str(i + 1) + ".jpg").lower().strip()
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
    print("THERE ARE THIS MANY PROBLEMS IN TEXT_" + str(i + 1) + ": " + str(len(problem_list)))
