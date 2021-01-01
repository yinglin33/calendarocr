import datetime
import cv2
from pytesseract import image_to_string
from PIL import Image

"""
links: https://www.freecodecamp.org/news/getting-started-with-tesseract-part-ii-f7f9a0899b3f/
"""

def process_image(filename, greyscale=0, read=0, blur=0, threshold=0):
    """
    Returns an image processed into a string using preprocessing methods specified
    by the defined parameters.

    parameters:
        filename: name of file in str
        greyscale: boolean value
        read: whether to read/display the file or not
        blur: 1 (averaging), 2 (gaussian), 3 (median), 4 (bilateral filtering)
        threshold: 1 (simple), 2 (adaptive), 3 (otsu's)
    """

    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 600,600)

    if greyscale:
        img = cv2.imread(filename, 0) #the 0 converts the image greyscale
    else:
        img = cv2.imread(filename)

    if blur == 1:
        img = cv.blur(img,(5,5))
    elif blur == 2:
        img = cv2.GaussianBlur(img, (5, 5), 0)
    elif blur == 3:
        img = cv2.medianBlur(img, 3)
    elif blur == 4:
        img = cv.bilateralFilter(img,9,75,75)

    if threshold == 1:
        ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    elif threshold == 2:
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    elif threshold == 3:
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    if read:
        cv2.imshow("image", img) #display image in 600x600
        cv2.waitKey(0) #wait until next key is pressed to exit viewing

    # Adding custom options
    custom_config = '--oem 3 --psm 6'

    return image_to_string(img, config=custom_config)

def convertToCalendar(cal):
    months_short=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    dates =[31,28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months_long = ["january","february","march","april","may","june","july","august","september","october","november","december" ]
    #todo account for leap years for feburary 
    today = datetime.datetime.today()
    Calendar= datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
    # the parameters are year, month, day, hour, minutes, seconds
    index= -1
    #might be a good idea to remove spaces from string to help with processing
    event_name = cal

    cal_del_index = -1
    for i in range(len(months_short)):
        cal_del_index = cal.lower().find(months_short[i])
        cal_del_index2= cal.lower().find(months_long[i])
        if cal_del_index != -1:
            Calendar = Calendar.replace(month=(i+1))
            index=i

#                    cal = cal[cal_del_index2 : cal_del_index2 + len(months_long[i])]
#            else:
#                cal = cal[ cal_del_index1 : cal_del_index1 + len(months_short[i]) ]

            break
    #need to account for months in numeric form
    date_del_index= -1
    for i in range(1,dates[index]+1):
        if cal.find(str(i)) != -1:
            Calendar = Calendar.replace(day=i)
            date_del_index = cal.find(str(i))
#    if date_delete_index >= 0 and Calendar.day > 9:
#        cal = cal [date_delete_index : date_delete_index + 2 ]
#    elif date_delete_index >=0 :
#        cal = cal[date_delete_index : date_delete_index + 1]
    year_del_index = -1
    for i in range (2000, today.year+1):
        year_del_index = cal.find(str(i))
        if year_del_index != -1:
            Calendar = Calendar.replace(year=i)
    #note we need to do more to account for start and end date. We are using start date
    time_index = -1
    if cal.lower().find("pm") != -1:
        time_index = find_n(cal, ' ', cal.lower().find("pm"))
        Calendar = Calendar.replace(hour=12)
    if cal.lower().find("p.m") != -1:
        time_index = find_n(cal, ' ', cal.lower().find("p.m"))
        Calendar = Calendar.replace(hour=12)
    if cal.lower().find("am ") != -1:
        time_index = find_n(cal, ' ', cal.lower().find("am"))
        Calendar = Calendar.replace(hour=0)
    if cal.lower().find("a.m") != -1:
        time_index = find_n(cal, ' ', cal.lower().find("a.m"))
        Calendar = Calendar.replace(hour=0)
    print(str(time_index))
    print(cal[time_index])
    if time_index != -1 and time_index < len(cal) and cal[time_index].isnumeric():
        print("Time number:" + cal[time_index])
        Calendar = Calendar.replace(hour = (Calendar.hour + int(cal[time_index])))
    #how do we delete time 

    if time_index >= 0 and len(cal[:time_index]) < len(event_name):
        event_name=cal[0:time_index]
    if cal_del_index >= 0 and len(cal[:cal_del_index]) < len(event_name):
        event_name=cal[0:cal_del_index]
    if year_del_index >= 0 and len(cal[:year_del_index]) < len(event_name):
        event_name=cal[0:year_del_index]
    if date_del_index >= 0 and len(cal[:date_del_index]) < len(event_name):
        event_name=cal[0:date_del_index]


    return Calendar, event_name

def find_n(bigstring, searchterm, n):
    start = bigstring.find(searchterm)+1
    while start >= 0:
        temp = bigstring.find(searchterm, start+len(searchterm))
        if n > temp and temp+1 != n and bigstring[temp+1] !=" ":
            start = temp+1
        else:
            break
    return start



if __name__ == '__main__':
    print(process_image("image2.jpg"))
