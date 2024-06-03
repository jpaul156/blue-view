import csv
import os
from datetime import datetime
from math import sqrt
import geopy.distance
from matplotlib import pyplot as plt

print("Hello World!")

bikeData = []
febData = []

def find_csv_files(folder_path='.'):
    csv_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            csv_files.append(filename)
    return csv_files

def listNamer(file):
    months = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }
    year_name = file[0:4]
    month_name = months[file[4:6]]
    lol_name = year_name + " " + month_name
    return lol_name


def idCols(row):
    bikeType = "classic"
    hasLength = False
    for i, x in enumerate(row):
##        print(i,x)
        if x in ("start_lat","start station latitude"):
            startLat = i
        elif x in ("start_lng","start station longitude"):
            startLng = i
        elif x in ("end_lat","end station latitude"):
            endLat = i
        elif x in ("end_lng","end station longitude"):
            endLng = i
        elif x in ("start_station_name","start station name"):
            startName = i
        elif x in ("start_station_id","start station id"):
            startId = i
        elif x in ("end_station_name","end station name"):
            endName = i
        elif x in ("end_station_id","end station id"):
            endId = i
        elif x in ("member_casual","usertype"):
            userType = i
        elif x in ("started_at","starttime"):
            startTime = i
        elif x in ("ended_at","stoptime"):
            endTime = i
        elif x == "tripduration":
            hasLength = True
    colInfo = [startLat, startLng, endLat, endLng,
               startName, startId, endName, endId,
               userType, startTime, endTime, hasLength]
    return colInfo

def countBikes(monthList):
    classicBikes = 0
    electricBikes = 0
    for row in monthList:
        if row[1] == "classic_bike":
            classicBikes += 1
        elif row[1] == "electric_bike":
            electricBikes += 1
    print("Classic Bikes: ", classicBikes)
    print("Electric Bikes: ", electricBikes)
    bikeCount = [classicBikes,electricBikes]

    return bikeCount

def rideTime(startTime, endTime):
    rideLength = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S') -
                  datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')).total_seconds()
    rideLength = int(rideLength)

    return rideLength

class station:
    def __init__(self, stnName, stnId, stnLat, stnLng):
        self.stnName = stnName
        self.stnId = stnId
        self.stnLat = stnLat
        self.stnLng = stnLng
        self.counter = 0


files = find_csv_files()
files.sort()

stnList = []

monthlyRides = []
monthlyCRides = []
monthlyERides = []

monthlyLengths = []

for file in files:
    listName = listNamer(file)
    with open(file, "r") as data:
        csv_reader = csv.reader(data)
        monthData = list(csv_reader)
        print("")
        print(listNamer(file))
        print("Number of Rides:", len(monthData))
        monthlyRides.append(len(monthData))

##        for row in monthData[1:10]:
##            print(rideTime(row[2],row[3]))

##        bikeCount = countBikes(monthData)
##        monthlyCRides.append(bikeCount[0])
##        monthlyERides.append(bikeCount[1])

        try:
            colInfo = idCols(monthData[0])
        except:
            print("idCols error")
            continue

        totalLength = 0
        if colInfo[11] == False:
            for row in monthData[1:]:
                rideLength = rideTime(row[2],row[3])
                totalLength += rideLength
            monthlyLengths.append(totalLength)
        else:
            for row in monthData[1:]:
                totalLength += int(row[0])
            monthlyLengths.append(totalLength)

####        print(colInfo)
##        distList = [] # creating new list for trip distances
##        monthStnList = []
##        for row in monthData[1:4]:
##            try:
##                if "" in (row[colInfo[0]],
##                          row[colInfo[1]],
##                          row[colInfo[2]],
##                          row[colInfo[3]]):
##                    continue
##                foundStartStn = False
##                foundEndStn = False
##                if len(monthStnList) == 0:
####                    print(row[colInfo[4]])
####                    print(row[colInfo[5]])
####                    print(row[colInfo[0]])
####                    print(row[colInfo[1]])
##                    monthStnList.append(station(row[colInfo[4]],
##                                                row[colInfo[5]],
##                                                row[colInfo[0]],
##                                                row[colInfo[1]]))
##                    if row[colInfo[7]] != row[colInfo[5]]:
####                        print(row[colInfo[6]])
####                        print(row[colInfo[7]])
####                        print(row[colInfo[2]])
####                        print(row[colInfo[3]])
##                        monthStnList.append(station(row[colInfo[6]],
##                                                    row[colInfo[7]],
##                                                    row[colInfo[2]],
##                                                    row[colInfo[3]]))
##                print("monthStnList length: ", len(monthStnList))
##                for stn in monthStnList:
##                    print(stn.stnId, row[colInfo[5]], row[colInfo[7]])
##                    if stn.stnId in (row[colInfo[5]],row[colInfo[7]]):
##                        foundStartStn = True
##                        print("foundStartStn True")
##                        stn.counter += 1
##                        continue
##                    if foundStartStn == False:
##                        print("foundStartStn False")
##                        monthStnList.append(station(row[colInfo[4]],
##                                                    row[colInfo[5]],
##                                                    row[colInfo[0]],
##                                                    row[colInfo[1]]))
##                    if stn.stnId == row[colInfo[7]]:
##                        foundEndStn = True
##                        stn.counter += 1
##                        continue
##                    if foundEndStn == False:
##                        monthStnList.append(station(row[colInfo[6]],
##                                                    row[colInfo[7]],
##                                                    row[colInfo[2]],
##                                                    row[colInfo[3]]))
##
##                startCoords = (row[colInfo[0]], row[colInfo[1]])
##                endCoords = (row[colInfo[2]], row[colInfo[3]])
##                rideDist = geopy.distance.geodesic(startCoords, endCoords).km
####                print(rideDist)
##                if rideDist > 100 or rideDist == 0.0:
##                    continue
##                else:
####                    print(rideDist)
##                    distList.append(rideDist)
##            except:
##                print("data row error")
##                pass
##        print("Average trip length:")
##        print(sum(distList)/len(distList))
##        print(len(distList))
##
##        monthStnList.sort(key=lambda x: x.counter, reverse=True)
##        for stn in monthStnList[:5]:
##            print(stn.counter, stn.stnName)




startMonth = 0
endMonth = 4

sum2015 = sum(monthlyRides[0+startMonth:0+endMonth])
sum2016 = sum(monthlyRides[12+startMonth:12+endMonth])
sum2017 = sum(monthlyRides[24+startMonth:24+endMonth])
sum2018 = sum(monthlyRides[36+startMonth:36+endMonth])
sum2019 = sum(monthlyRides[48+startMonth:48+endMonth])
sum2020 = sum(monthlyRides[60+startMonth:60+endMonth])
sum2021 = sum(monthlyRides[72+startMonth:72+endMonth])
sum2022 = sum(monthlyRides[84+startMonth:84+endMonth])
sum2023 = sum(monthlyRides[96+startMonth:96+endMonth])
sum2024 = sum(monthlyRides[108+startMonth:108+endMonth])


print("")
print("Jan-Apr   -   total   -   % change")
print("2015 Rides: ", sum2015)
print("2016 Rides: ", sum2016, "   ", round(((sum2016-sum2015)/sum2015)*100,2))
print("2017 Rides: ", sum2017, "   ", round(((sum2017-sum2016)/sum2016)*100,2))
print("2018 Rides: ", sum2018, "   ", round(((sum2018-sum2017)/sum2017)*100,2))
print("2019 Rides: ", sum2019, "   ", round(((sum2019-sum2018)/sum2018)*100,2))
print("2020 Rides: ", sum2020, "   ", round(((sum2020-sum2019)/sum2019)*100,2))
print("2021 Rides: ", sum2021, "   ", round(((sum2021-sum2020)/sum2020)*100,2))
print("2022 Rides: ", sum2022, "   ", round(((sum2022-sum2021)/sum2021)*100,2))
print("2023 Rides: ", sum2023, "   ", round(((sum2023-sum2022)/sum2022)*100,2))
print("2024 Rides: ", sum2024, "   ", round(((sum2024-sum2023)/sum2023)*100,2))

print("Monthly Totals:", len(monthlyRides))
print("Monthly Lengths:", len(monthlyLengths))

##for tripTotal, tripLength in monthlyRides, monthlyLengths:
##    print(tripLength/tripTotal)

for i in range(112):
    print(monthlyLengths[i]/monthlyRides[i])

plt.plot([1,2,3,4],monthlyRides[108:], label="2024")
plt.plot([1,2,3,4,5,6,7,8,9,10,11,12],monthlyRides[96:108], label="2023")
plt.plot([1,2,3,4,5,6,7,8,9,10,11,12],monthlyRides[84:96], label="2022")
plt.plot([1,2,3,4,5,6,7,8,9,10,11,12],monthlyRides[72:84], label="2021")
plt.plot([1,2,3,4,5,6,7,8,9,10,11,12],monthlyRides[60:72], label="2020")
plt.plot([1,2,3,4,5,6,7,8,9,10,11,12],monthlyRides[48:60], label="2019")
plt.plot([1,2,3,4,5,6,7,8,9,10,11,12],monthlyRides[36:48], label="2018")
plt.plot([1,2,3,4,5,6,7,8,9,10,11,12],monthlyRides[24:36], label="2017")
plt.plot([1,2,3,4,5,6,7,8,9,10,11,12],monthlyRides[12:24], label="2016")
plt.plot([1,2,3,4,5,6,7,8,9,10,11,12],monthlyRides[:12], label="2015")
plt.plot([1],[0])
plt.legend()
plt.show()


##plt.plot([1,2,3,4,5,6,7,8,9,10,11,12],monthlyRides[:12],
##         [1,2,3,4],monthlyRides[12:],
##         [1],[0])

##plt.plot([1,2,3,4,5,6,7,8,9,10,11,12],monthlyCRides[:12], label="2023 Classic")
##plt.plot([1,2,3,4],monthlyCRides[12:], label="2024 Classic")
##plt.plot([1,2,3,4,5,6,7,8,9,10,11,12],monthlyERides[:12], label="2023 Electric")
##plt.plot([1,2,3,4],monthlyERides[12:], label="2024 Electric")

##plt.show()



##with open("202402-bluebikes-tripdata.csv", "r") as data:
##    csv_reader = csv.reader(data)
##    monthData = list(csv_reader)
##
##startTime = 0
##endTime = 0
##
##print(len(monthData))




##for i, row in enumerate(monthData[0:3]):
##    if i == 0:
##        keys = row
##    elif i == 1:
##        values = row
##        for key, value in zip(keys, values):
##            if startTime == 0 and endTime == 0:
##                print("here")
##                startTimeDT = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
##                print(startTimeDT)
###                endTimeDT = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
###                timeDiff = endTimeDT - startTimeDT
###                print("#########")
###                print(timeDiff)
##            elif i==2:
##                startTime = value
##                print("at startTime")
##            elif i==3:
##                endTime = value
##            else:
##                print(key, value)













