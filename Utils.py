import calendar
from datetime import datetime, timedelta
from holidays import Holidays
import math
import uuid
import time


def isHoliday(datetimeObj):
    dateStr = datetimeObj.strftime('%Y-%m-%d')
    holidays = Holidays
    if (dateStr in holidays):
        return True
    else:
        return False


def priceToATM(price):
	return int(round(price / 100))*100



dateFormat = "%Y-%m-%d"
timeFormat = "%H:%M:%S"
dateTimeFormat = "%Y-%m-%d %H:%M:%S"




def getTodayDateStr():
	return convertToDateStr(datetime.now())


def convertToDateStr(datetimeObj):
	return datetimeObj.strftime(dateFormat)


def getWeeklyExpiryDayDate(dateTimeObj = None):
    if dateTimeObj == None:
        dateTimeObj = datetime.now()
    daysToAdd = 0
    if dateTimeObj.weekday() == 4:
        daysToAdd = 6
    elif dateTimeObj.weekday() == 5:
        daysToAdd = 5
    elif dateTimeObj.weekday() == 6:
        daysToAdd = 4
    else:
        daysToAdd = 3 - dateTimeObj.weekday()
    # print(daysToAdd)
    datetimeExpiryDay = dateTimeObj + timedelta(days=daysToAdd)
    # print(datetimeExpiryDay)
    while isHoliday(datetimeExpiryDay) == True:
        datetimeExpiryDay = datetimeExpiryDay - timedelta(days=1)
    datetimeExpiryDay=datetimeExpiryDay.date()
    #datetimeExpiryDay = getTimeOfDay(0, 0, 0, datetimeExpiryDay)
    return datetimeExpiryDay
    

def getMonthlyExpiryDayDate(datetimeObj = None):
	if datetimeObj == None:
		datetimeObj = datetime.now()
	year = datetimeObj.year
	month = datetimeObj.month
	lastDay = calendar.monthrange(year, month)[1] # 2nd entry is the last day of the month
	datetimeExpiryDay = datetime(year, month, lastDay).date()
	while calendar.day_name[datetimeExpiryDay.weekday()] != 'Thursday':
		datetimeExpiryDay = datetimeExpiryDay - timedelta(days=1)
	while isHoliday(datetimeExpiryDay) == True:
		datetimeExpiryDay = datetimeExpiryDay - timedelta(days=1)

	#datetimeExpiryDay = getTimeOfDay(0, 0, 0, datetimeExpiryDay)
	return datetimeExpiryDay
  

def getMarketStartTime(dateTimeObj = None):
	return getTimeOfDay(9, 15, 0, dateTimeObj)

def getMarketEndTime(dateTimeObj = None):
	return getTimeOfDay(15, 30, 0, dateTimeObj)


def getTimeOfDay(hours, minutes, seconds, dateTimeObj = None):
	if dateTimeObj == None:
	  dateTimeObj = datetime.now()
	dateTimeObj = dateTimeObj.replace(hour=hours, minute=minutes, second=seconds, microsecond=0)
	return dateTimeObj


def getTimeOfToDay(hours, minutes, seconds):
	return getTimeOfDay(hours, minutes, seconds, datetime.now())  



def isHoliday(datetimeObj):
	dayOfWeek = calendar.day_name[datetimeObj.weekday()]
	if dayOfWeek == 'Saturday' or dayOfWeek == 'Sunday':
		return True
	dateStr = convertToDateStr(datetimeObj)
	holidays = Holidays #getHolidays()
	if (dateStr in holidays):
		return True
	else:
		return False

def prepareWeeklyOptionsSymbol(inputSymbol, strike, optionType, expDate):
	expiryDateTime = getWeeklyExpiryDayDate(expDate)
    #todayMarketStartTime = getMarketStartTime()
    #expiryDayMarketEndTime = getMarketEndTime(expiryDateTime)
	
	
	# Check if monthly and weekly expiry same
	expiryDateTimeMonthly = getMonthlyExpiryDayDate(expDate)
	weekAndMonthExpriySame = False
	if expiryDateTime == expiryDateTimeMonthly:
		weekAndMonthExpriySame = True
	 
	year2Digits = str(expiryDateTime.year)[2:]
	optionSymbol = None
	if weekAndMonthExpriySame == True:
		monthShort = calendar.month_name[expiryDateTime.month].upper()[0:3]
		optionSymbol = inputSymbol + str(year2Digits) + monthShort + str(strike) + optionType.upper()
	else:
		m = expiryDateTime.month
		d = expiryDateTime.day
		mStr = str(m)
		if m == 10:
	  		mStr = "O"
		elif m == 11:
	  		mStr = "N"
		elif m == 12:
			mStr = "D"
		dStr = ("0" + str(d)) if d < 10 else str(d)
		optionSymbol = inputSymbol + str(year2Digits) + mStr + dStr + str(strike) + optionType.upper()
	return optionSymbol
