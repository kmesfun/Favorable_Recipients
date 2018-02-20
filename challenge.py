#challenge.py
#Goal: The goal of the challenge is to match customer's pickup requests with available non-profit recipients.
from geopy.distance import vincenty
import pandas as pd
from pandas import read_csv
from collections import defaultdict
import datetime
import csv

#===============================================#

#Returns a list of the times between a time interval
#In: H-H(AM/PM)
#Out: list of time intervals
def timeInterval(time):
    times = []
    start = ''
    end = ''
    #possible times
    timeofday = {0:"8-9AM", 1:"9-10AM", 2:"10-11AM", 3:"11-12PM", 4:"12-1PM", 5:"1-2PM", 6:"2-3PM",7:"3-4PM",8:"4-5PM",9:"5-6PM",10:"6-7PM",11:"7-8PM",12:"8-9PM",13:"9-10PM",14:"10-11PM",15:"11-12AM"}

    for index,period in timeofday.items():
        if time == period and index < 4:
          for i in range(0,len(time)):
              if time[i] == '-':
                  start = time[0:i]
                  times.append( start+":00")
              elif time[i] == 'A' or time[i] == 'P':
                  end = time[time.index("-")+1:i]
          for min in range(1,60):
              if min < 10:
                  interval = start + ':0' + str(min)
                  times.append(interval)
              if min > 9:
                  interval = start + ':' + str(min)
                  times.append(interval)
          times.append(end+":00")
        # convert into military time

        if time == period and index > 4:
          for i in range(0,len(time)):
              if time[i] == '-':
                  start = time[0:i]
                  start = (int(start) + 12) % 24
                  start = str(start)
                  times.append( start+":00")
              elif time[i] == 'A' or time[i] == 'P':
                  end = time[time.index("-")+1:i]
                  end = (int(end) + 12) % 24
                  end = str(end)
          for min in range(1,60):
              if min < 10:
                  interval = start + ':0' + str(min)
                  times.append(interval)
              if min > 9:
                  interval = start + ':' + str(min)
                  times.append(interval)
          times.append(end+":00")

        #special case
        if time == period and index == 4:
            times = ['12:00', '12:01', '12:02', '12:03', '12:04', '12:05', '12:06', '12:07', '12:08', '12:09', '12:10', '12:11', '12:12', '12:13', '12:14', '12:15', '12:16', '12:17', '12:18', '12:19', '12:20', '12:21', '12:22', '12:23', '12:24', '12:25', '12:26', '12:27', '12:28', '12:29', '12:30', '12:31', '12:32', '12:33', '12:34', '12:35', '12:36', '12:37', '12:38', '12:39', '12:40', '12:41', '12:42', '12:43', '12:44', '12:45', '12:46', '12:47', '12:48', '12:49', '12:50', '12:51', '12:52', '12:53', '12:54', '12:55', '12:56', '12:57', '12:58', '12:59', '13:00']

    return times




#Gets hour in militarytime from iso8601
#In: (Str) iso8601 time
#Out: (Str) military time "HH:MM"
def getHour(iso):
    date = iso[0:10]
    time = iso[11:25]
    militarytime = (int(iso[11:13]))% 24
    currtime = str(militarytime)+":00"
    if len(currtime) != 5:
        currtime = '0'+currtime
    return currtime

#Reads all data in  'Pickups.csv' and stores it in a dictionary
def readPickup():
    df = pd.read_csv("Pickups.csv")
    info = defaultdict(list)
    for col, row in df.iterrows():
        for i in row:
            info[col].append(i)
    return info

#Reads all data in  'Recipients.csv' and stores it in a dictionary
def readRecipient():
    df = pd.read_csv("Recipients.csv")
    info = defaultdict(list)
    for col, row in df.iterrows():
        for i in row:
            info[col].append(i)
    return info

#The distance between a pickup and recipient
#In: (tuple,tuple)two tuples ((lat,long),(lat,long))
#Out: (Int) miles
def LatitudetoMiles(coords_1, coords_2):
    return vincenty(coords_1, coords_2).miles

#The distance between a pickup and recipient must be within 5 miles
#In: (tuple,tuple)two tuples ((lat,long),(lat,long))
#Out: (Int) miles
def Under5Miles(coords_1, coords_2):
    return vincenty(coords_1, coords_2).miles <= 5

#gets a list of categories without the restrictions
#In: ((6 bit integer))
#Out:List of categories
def category(num):
    category = []
    categories = {0:"Raw Meat", 1:"Dairy", 2:"Seafood", 3:"Hot Prepared", 4:"Cold Prepared", 5:"Frozen"}
    mask = 63
    numbit = str(bin(num & mask)[2:])
    while len(numbit) != 6:
        numbit = "0" + numbit
    for i,j in enumerate(numbit[::-1]):
        if j == '1':
            category+=[categories[i]]
    return category

#gets a list of categories with the restrictions
#In: ((6 bit integer),(6 bit integer))
#Out:List of categories with the restrictions
def categorywRestrictions(cat, restriction):
    category = []
    categories = {0:"Raw Meat", 1:"Dairy", 2:"Seafood", 3:"Hot Prepared", 4:"Cold Prepared", 5:"Frozen"}
    numbit = str(bin(cat & ~restriction)[2:])
    while len(numbit) != 6:
        numbit = "0" + numbit
    for i,j in enumerate(numbit[::-1]):
        if j == '1':
            category+=[categories[i]]
    return category

#Returns a list of time itervals
#In: (16 bit integer)
#Out: List of categories with the stated hours of operations.
def hoursofoperations(num):
    category = []
    categories = {0:"8-9AM", 1:"9-10AM", 2:"10-11AM", 3:"11-12PM", 4:"12-1PM", 5:"1-2PM", 6:"2-3PM",7:"3-4PM",8:"4-5PM",9:"5-6PM",10:"6-7PM",11:"7-8PM",12:"8-9PM",13:"9-10PM",14:"10-11PM",15:"11-12AM"}
    numbit = str(bin(num)[2:])
    while len(numbit) != 16:
        numbit = "0" + numbit
    for i,j in enumerate(numbit[::-1]):
        if j == '1':
            category+=[categories[i]]
    return category

#check if the time given is within one hour of the time interval
#In:(str(HH:MM:SS), list[str(HH:MM)])
#Out:bool
def OneHourGap(time,timespan):
    for times in timespan:
        times = times + "00"
        times = times.replace(":","")
        time = time.replace(":","")
        if (int(times) - int(time)) <= 10000:
            return True
    return False

#check if the time given is within one hour of the time interval
#In:(str(HH:MM), list[str(HH:MM)])
#Out:bool
def OneHourGap_(time,timespan):
    for times in timespan:
        times = times.replace(":","")
        time = time.replace(":","")
        if (int(times) - int(time)) <= 1000:
            return True
    return False

#In: (Str) iso8601 time
#Out: (Str) day of the week
def pickupDay(iso):
  dayofweek = ['Monday', 
              'Tuesday', 
              'Wednesday', 
              'Thursday',  
              'Friday', 
              'Saturday','Sunday']
  dt = iso[0:10]
  year, month, day = (int(x) for x in dt.split('-'))    
  answer = datetime.date(year, month, day).weekday()
  return dayofweek[answer]

#Given a dict or 2d list return a csv
#In: 2D-list
#Out: csv file
def createCSVFile(input):
    with open("Favorable_Recipients.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(input)

#Sorts a 2D-list by the 11th element
#In:2D-list
#Out: sorted 2D-list by distance
def sort2dArray(input):
    input = input[1:]
    input = sorted(input, key=lambda x: x[10])
    return input

#Adds a header to a csv file
#In:csv file
#Out: csv file with headers
def addHeader(csv):
    df = read_csv("Favorable_Recipients.csv")
    df.columns = ['Recipients Information=>','FirstName','LastName', 'Street','City','State','Postal','Country','Email','Phone','Distance(miles)','Categories',' ','PickUp Information =>','FirstName','LastName', 'Street','City','State','Postal','Country','Email','Phone', 'Day of Week']
    df.to_csv('Favorable_Recipients.csv',index=False)

#Remove duplicate line from csv files
#In:csv file
#Out: csv file with headers
def removeDupCSV(csv):
    with open('Favorable_Recipients.csv', 'r') as in_file, open('Clean_Favorable_Recipients.csv', 'w') as out_file:
        seen = set()
        for line in in_file:
            if line in seen:
                continue
            seen.add(line)
            out_file.write(line)


#==========================================#

def main():
    recipients = readRecipient()
    pickup = readPickup()
    output = list()
    for pickupIndex, pickupValue in pickup.items():

        for recipientsIndex, recipientsValue in recipients.items():
            if Under5Miles((pickupValue[9],pickupValue[10]),(recipientsValue[9],recipientsValue[10])):
                date = pickupDay(pickupValue[12])
                hour = getHour(pickupValue[12])
                catWrest= categorywRestrictions(pickupValue[11],recipientsValue[11])
                daysoftheweek = ['Sunday''Monday', 'Tuesday', 'Wednesday', 'Thursday',  'Friday','Saturday']
                for index, day in enumerate(daysoftheweek):
                    if date == day:
                        operation = hoursofoperations(recipientsValue[12+index])
                        for intervals in operation:
                            listoftimes = timeInterval(intervals)
                            if OneHourGap_(hour, listoftimes):

                                distance = LatitudetoMiles((pickupValue[9],pickupValue[10]),(recipientsValue[9],recipientsValue[10]))
                                output.append([' ',recipientsValue[0],recipientsValue[1],recipientsValue[2],recipientsValue[3],recipientsValue[4],recipientsValue[5],recipientsValue[6],recipientsValue[7], recipientsValue[8], distance, catWrest, ' ',' ', pickupValue[0],pickupValue[1],pickupValue[2],pickupValue[3],pickupValue[4],pickupValue[5], pickupValue[6], pickupValue[7], pickupValue[8], date])
    toCsv = sort2dArray(output)
    csv = createCSVFile(toCsv)
    header = addHeader(csv)
    removeDupCSV(header)









if __name__ == "__main__":
    main()
