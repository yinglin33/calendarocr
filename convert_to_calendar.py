import datetime
from PIL import Image
import re

def convertToCalendar(cal):
    months_short=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    dates =[31,28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months_long = ["january","february","march","april","may","june","july","august","september","october","november","december" ]
    days = [" mon", " tues", " wed", " thur", " fri"]
    #todo account for leap years for feburary
    today = datetime.datetime.today()
    Calendar= datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
    # the parameters are year, month, day, hour, minutes, seconds
    index= -1
    #might be a good idea to remove spaces from string to help with processing
    event_name = cal
    possible_date_regex = ["[0-1][0-9]/[0-3][0-9]/[0-9][0-9][0-9][0-9]", "[1-9]/[0-3][0-9]/[0-9][0-9][0-9][0-9]", "[0-1][0-9]/[1-9]/[0-9][0-9][0-9][0-9]", "[1-9]/[1-9]/[0-9][0-9][0-9][0-9]", "[0-1][0-9]/[0-3][0-9]/[0-9][0-9]", "[1-9]/[0-3][0-9]/[0-9][0-9]", "[0-1][0-9]/[1-9]/[0-9][0-9]", "[1-9]/[1-9]/[0-9][0-9]", "[0-1][0-9]/[0-3][0-9]", "[1-9]/[0-3][0-9]", "[0-1][0-9]/[1-9]", "[1-9]/[1-9]" ]
    date_not_regex = True
    cal_del_index = -1
    date_del_index= -1
    for i in range( len(possible_date_regex)-1, -1, -1):
        print(i)
        x = re.findall(possible_date_regex[i], cal)
        if len(x) != 0:
            print("match")
            cal_del_index = cal.find(x[0])
            date_del_index = cal.find(x[0])
            date_not_regex = False
            info=[]
            info=x[0].split("/")
            Calendar = Calendar.replace(month = int(info[0]))
            Calendar = Calendar.replace(day = int(info[1]))
            if len(info) == 3 and len(info[2]) == 4:
                Calendar = Calendar.replace(year = int(info[2]))
            elif len(info) == 3 and len(info[2]) == 2:
                Calendar = Calendar.replace( year = ((Calendar.year // 100)*100 + int(info[2])))

    if date_not_regex:
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
        for i in range(1,dates[index]+1):
            if cal.find(" "+str(i)+" ") != -1 or cal.find(" " + str(i)) != -1 and (cal.find(" "+str(i)) + 1 + len(str(i))) < len(cal) or cal.find(str(i)+" ") != -1 and (cal.find(str(i)+" ") + 1 + len(str(i))) < len(cal) :
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
   # print(str(time_index))
   # print(cal[time_index])
    if time_index != -1 and time_index < len(cal) and cal[time_index].isnumeric():
        #print("Time number:" + cal[time_index])
        Calendar = Calendar.replace(hour = (Calendar.hour + int(cal[time_index])))

    #how do we delete time
    day_index = -1
    for day in days:
        if cal.lower().find(day) != -1:
           day_index = cal.lower().find(day)

    if time_index >= 0 and len(cal[:time_index]) < len(event_name):
        event_name=cal[0:time_index]
    if cal_del_index >= 0 and len(cal[:cal_del_index]) < len(event_name):
        event_name=cal[0:cal_del_index]
    if year_del_index >= 0 and len(cal[:year_del_index]) < len(event_name):
        event_name=cal[0:year_del_index]
    if date_del_index >= 0 and len(cal[:date_del_index]) < len(event_name):
        event_name=cal[0:date_del_index]
    if day_index >= 0 and len(cal[:day_index]) < len(event_name):
        event_name = cal[0:day_index]

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
