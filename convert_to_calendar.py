import datetime
from PIL import Image
import re
'''
Takes a string (cal) and looks for month, date, time, and event name in the string. Returns a string 
containing the event name and Datetime object containing the month, date, time.
'''

''' 
TODO change convertToCalendar so it returns the time interval of the event
     todo account for leap years for feburary
     might be a good idea to remove spaces from string to help with processing
'''

def convertToCalendar(cal):
    
    #lists containing date keywords
    monthShort=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    dates =[31,28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    monthLong = ["january","february","march","april","may","june","july","august","september","october","november","december" ]
    days = [" mon", " tues", " wed", " thur", " fri"]
    
    #list containing regex expressions for dates in the form of XX/XX/XXXX
    possibleDateRegex = ["[0-1][0-9]/[0-3][0-9]/[0-9][0-9][0-9][0-9]", "[1-9]/[0-3][0-9]/[0-9][0-9][0-9][0-9]", "[0-1][0-9]/[1-9]/[0-9][0-9][0-9][0-9]", "[1-9]/[1-9]/[0-9][0-9][0-9][0-9]", "[0-1][0-9]/[0-3][0-9]/[0-9][0-9]", "[1-9]/[0-3][0-9]/[0-9][0-9]", "[0-1][0-9]/[1-9]/[0-9][0-9]", "[1-9]/[1-9]/[0-9][0-9]", "[0-1][0-9]/[0-3][0-9]", "[1-9]/[0-3][0-9]", "[0-1][0-9]/[1-9]", "[1-9]/[1-9]" ]
 
    #Creates datetime object based on today's time
    today = datetime.datetime.today()
    # made default datetime object using today's time
    #the parameters are year, month, day, hour, minutes, seconds
    Calendar= datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
    
    #default event name   
    eventName = cal

    #tracks if the date is in regex form or XX/XX/XXXX 
    dateNotRegex = True

    index= -1

    #Tracking these indexes to eventually determine the event name
    calDelIndex = -1
    dateDelIndex= -1
    yearDelIndex = -1
    timeIndex = -1 
    day_index = -1
    
    #searches for matches from possibleDateRegex backwards. 
    #This is because regex's at the end of the list are substrings of regex's at the beginning
    for i in range( len(possibleDateRegex)-1, -1, -1):
        x = re.findall(possibleDateRegex[i], cal)
        if len(x) != 0:
            calDelIndex = cal.find(x[0])
            dateDelIndex = cal.find(x[0])
            dateNotRegex = False
            info=[]

            #splits the match into month, day, year
            info=x[0].split("/")
            
            #replaces month and day
            Calendar = Calendar.replace(month = int(info[0]))
            Calendar = Calendar.replace(day = int(info[1]))
            
            # replaces year based on if year was represented with 4 numbers or 2 numbers
            # ex : 1/1/2021 vs 1/1/21
            # if there was no year in the date year stays the same
            if len(info) == 3 and len(info[2]) == 4:
                Calendar = Calendar.replace(year = int(info[2]))
            elif len(info) == 3 and len(info[2]) == 2:
                Calendar = Calendar.replace( year = ((Calendar.year // 100)*100 + int(info[2])))

    # if date was found in regex no need to look for month or day
    if dateNotRegex:

        #searches for the month in the string using monthShort
        for i in range(len(monthShort)):
            
            calDelIndex = cal.lower().find(monthShort[i])
            calDelIndex2= cal.lower().find(monthLong[i])
            if calDelIndex != -1:
                Calendar = Calendar.replace(month=(i+1))
                index=i

#                    cal = cal[calDelIndex2 : calDelIndex2 + len(monthLong[i])]
#            else:
#                cal = cal[ calDelIndex1 : calDelIndex1 + len(monthShort[i]) ]

                break
    #need to account for months in numeric form
        for i in range(1,dates[index]+1):
            if cal.find(" "+str(i)+" ") != -1 or cal.find(" " + str(i)) != -1 and (cal.find(" "+str(i)) + 1 + len(str(i))) < len(cal) or cal.find(str(i)+" ") != -1 and (cal.find(str(i)+" ") + 1 + len(str(i))) < len(cal) :
                Calendar = Calendar.replace(day=i)
                dateDelIndex = cal.find(str(i))

    for i in range (2000, today.year+1):
        yearDelIndex = cal.find(str(i))
        if yearDelIndex != -1:
            Calendar = Calendar.replace(year=i)
    #note we need to do more to account for start and end date. We are using start date
    if cal.lower().find("pm") != -1:
        timeIndex = find_n(cal, ' ', cal.lower().find("pm"))
        Calendar = Calendar.replace(hour=12)
    if cal.lower().find("p.m") != -1:
        timeIndex = find_n(cal, ' ', cal.lower().find("p.m"))
        Calendar = Calendar.replace(hour=12)
    if cal.lower().find("am ") != -1:
        timeIndex = find_n(cal, ' ', cal.lower().find("am"))
        Calendar = Calendar.replace(hour=0)
    if cal.lower().find("a.m") != -1:
        timeIndex = find_n(cal, ' ', cal.lower().find("a.m"))
        Calendar = Calendar.replace(hour=0)
    if timeIndex != -1 and timeIndex < len(cal) and cal[timeIndex].isnumeric():
        Calendar = Calendar.replace(hour = (Calendar.hour + int(cal[timeIndex])))

    for day in days:
        if cal.lower().find(day) != -1:
           day_index = cal.lower().find(day)

    if timeIndex >= 0 and len(cal[:timeIndex]) < len(eventName):
        eventName=cal[0:timeIndex]
    if calDelIndex >= 0 and len(cal[:calDelIndex]) < len(eventName):
        eventName=cal[0:calDelIndex]
    if yearDelIndex >= 0 and len(cal[:yearDelIndex]) < len(eventName):
        eventName=cal[0:yearDelIndex]
    if dateDelIndex >= 0 and len(cal[:dateDelIndex]) < len(eventName):
        eventName=cal[0:dateDelIndex]
    if day_index >= 0 and len(cal[:day_index]) < len(eventName):
        eventName = cal[0:day_index]

    return Calendar, eventName

# finds the instance of searchterm in bigstring that is before index n and the closest to index n
def find_n(bigstring, searchterm, n):
    start = bigstring.find(searchterm)+1
    while start >= 0:
        temp = bigstring.find(searchterm, start+len(searchterm))
        if n > temp and temp+1 != n and bigstring[temp+1] !=" ":
            start = temp+1
        else:
            break
    return start
