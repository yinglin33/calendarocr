import datetime
import cv2
from pytesseract import image_to_string
from PIL import Image


def process_image(filename):

    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 600,600)
    img = cv2.imread(filename, 0) #the 0 converts the image greyscale
    #original_dimensions = img.shape
    #print(original_dimensions)
    #img = cv2.resize(img, (500, 500))
    #img = cv2.resize(img, original_dimensions)
    img = cv2.GaussianBlur(img, (5, 5), 0)

    ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

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
    Calendar= datetime.datetime(2020, 1, 1, 0, 0, 0)
    # the parameters are year, month, day, hour, minutes, seconds
    index= -1
    #might be a good idea to remove spaces from string to help with processing
    today = datetime.datetime.today()
    cal=cal.lower()
    event_name = ""

    cal_del_index = -1
    for i in range(len(months_short)):
        cal_del_index = cal.find(months_short[i])
        cal_del_index2= cal.find(months_long[i])
        if cal_del_index != -1:
            Calendar = Calendar.replace(month=i)
            index=i

#                    cal = cal[cal_del_index2 : cal_del_index2 + len(months_long[i])]
#            else:
#                cal = cal[ cal_del_index1 : cal_del_index1 + len(months_short[i]) ]

            break
    #need to account for months in numeric form
    date_del_index= -1
    for i in range(1,dates[index]):
        if cal.find(str(i)) != -1:
            Calendar = Calendar.replace(day=i)
            date_del_index = cal.find(str(i))
#    if date_delete_index >= 0 and Calendar.day > 9:
#        cal = cal [date_delete_index : date_delete_index + 2 ]
#    elif date_delete_index >=0 :
#        cal = cal[date_delete_index : date_delete_index + 1]
    year_del_index = -1
    for i in range (2000, today.year):
        year_del_index = cal.find(str(i))
        if year_del_index != -1:
            Calendar = Calendar.replace(year=i)
    #note we need to do more to account for start and end date. We are using start date
    time_index = -1
    if cal.find("pm") != -1:
        time_index = find_n(cal, ' ', cal.find("pm"))
        Calendar = Calendar.replace(hour=12)
    if cal.find("p.m") != -1:
        time_index = find_n(cal, ' ', cal.find("p.m"))
        Calendar = Calendar.replace(hour=12)
    if cal.find("am") != -1:
        time_index = find_n(cal, ' ', cal.find("am"))
        Calendar = Calendar.replace(hour=0)
    if cal.find("a.m") != -1:
        time_index = find_n(cal, ' ', cal.find("a.m"))
        Calendar = Calendar.replace(hour=0)
    if time_index != -1 and time_index >= len(cal) and isnumeric(cal[time_index]):
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
    start = bigstring.find(searchterm)
    while start >= 0:
        temp = bigstring.find(searchterm, start+len(searchterm))
        if n > temp:
            start = temp
        else:
            break
    return start

    return image_to_string(img, config=custom_config)


if __name__ == '__main__':
    print(process_image("image2.jpg"))
