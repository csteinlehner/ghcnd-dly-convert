# 
# 
# Converts GHCN DLY Data from ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ to JSON file structured by Year/Month/Day
# Usage python convert_to_json.py stationname.dly
#
#

import csv
import sys
import json
if len(sys.argv) > 1:
    if sys.argv[1].find('.dly')==-1:
        print "Please specify a .dly station file"
        quit()
else:
    print "Please specify a .dly station file"
    quit()

csvfile = sys.argv[1]
days = {}
days["years"] = []


def addMeasurement(measureType, measurement):
        return [measureType.strip(), measurement[0:5].strip(), measurement[5:6].strip(), measurement[6:7].strip(), measurement[7:8].strip()]

def readRow(lineOfData):
    rowData = {}
    rowData["countryCode"] = lineOfData[0:2]
    rowData["stationID"] = lineOfData[0:11]
    rowData["year"] = lineOfData[11:15]
    rowData["month"] = lineOfData[15:17]
    year = rowData["year"]
    month = rowData["month"]
    days["stationID"] = rowData["stationID"]
    days["countryCode"] = rowData["countryCode"]

    yearStr = str(year);
    monthStr = str(month);
    currentYearPos = -1
    currentMonthPos = -1
    # Check if this year already in days, if not add it with empty month array
    if not any(d["year"] == yearStr for d in days['years']):
        days["years"].append({'year': yearStr, 'months':[]})
        currentYearPos = len(days["years"])-1
    # Check if this month already in currentYear, if not add it with empty days array  
    if not any(d['month'] == monthStr for d in days['years'][currentYearPos]['months']):
        days['years'][currentYearPos]['months'].append({'month': monthStr, 'days':[]})
        currentMonthPos = len(days['years'][currentYearPos]['months'])-1
    element = lineOfData[17:21]
    for x in range(0, 31):
        dayOM = x + 1
        offsetStart = (x*8)+21
        offsetEnd = offsetStart + 8
        dayDat = addMeasurement(element, lineOfData[offsetStart:offsetEnd])
        dayStr = str("%02d" % (dayOM,))
        # Check if this day already in currentMonth, if not add day and empty data 
        if not any(d['day'] == dayStr for d in days['years'][currentYearPos]['months'][currentMonthPos]['days']):
            days['years'][currentYearPos]['months'][currentMonthPos]['days'].append({'day': dayStr, 'data':[]})

        for d in days['years'][currentYearPos]['months'][currentMonthPos]['days']:
            if (d['day'] == dayStr ):
                d['data'].append({dayDat[0] : int(dayDat[1])})
       
        # dayPos = days['years'][currentYearPos]['months'][currentMonthPos]['days'].index(dayOM)
        # print days['years'][currentYearPos]['months'][currentMonthPos]['days']
        # days['years'][currentYearPos]['months'][currentMonthPos]['days'][dayStr]
        # days[yearStr][monthStr][day][dayDat[0]] = int(dayDat[1])
    return rowData




with open(csvfile) as fp:
    for cnt, line in enumerate(fp):
       readRow(line)

output = csvfile.split('.')[0]
with open(output+'.json', 'w') as f:
    json.dump(days, f, indent=2, sort_keys=True)
    # json.dump(days, f, sort_keys=True)
    print 'Json written to '+output+'.json'

