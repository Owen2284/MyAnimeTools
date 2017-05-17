from constants import *

def userStatusNumberToString(n):
	for key in ANIMEUSERSTATUS:
		if ANIMEUSERSTATUS[key] == n:
			return key
	return ""

def userStatusStringToNumber(s):
	for key in ANIMEUSERSTATUS:
		if key.lower() == s.lower():
			return ANIMEUSERSTATUS[key]
	return -1

def seriesStatusNumberToString(n):
	for key in ANIMESERIESSTATUS:
		if ANIMESERIESSTATUS[key] == n:
			return key
	return ""

def seriesTypeNumberToString(n):
	for key in ANIMESERIESTYPE:
		if ANIMESERIESTYPE[key] == n:
			return key
	return ""

def seriesTypeStringToNumber(s):
	for key in ANIMESERIESTYPE:
		if key.lower() == s.lower():
			return ANIMESERIESTYPE[key]
	return -1

def formatDateNicely(dateStr):
	return DAYS[int(dateStr.split("-")[2])-1] + " " + MONTHSSHORT[int(dateStr.split("-")[1])-1] + " " + dateStr.split("-")[0]