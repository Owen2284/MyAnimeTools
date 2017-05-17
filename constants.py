from collections import OrderedDict

VERSION = "v0.7.0"

ANIMEUSERSTATUS = OrderedDict([
	("All",0),
	("Currently Watching",1),
	("Watching",1),
	("CW",1),
	("Completed",2),
	("On Hold",3),
	("On hold",3),
	("Hold",3),
	("OH",3),
	("Dropped",4),
	("Drop",4),
	("Plan to Watch",6),
	("PTW",6)
])

ANIMESERIESTYPE = OrderedDict([
	("All",0),
	("TV",1),
	("OVA",2),
	("Movie",3),
	("Special",4),
	("ONA",5),
	("Music",6)
])

ANIMESERIESSTATUS = OrderedDict([
	("All",0),
	("Airing",1),
	("Finished Airing",2),
	("Not Yet Aired",3),
])

DAYS = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th", "15th", "16th", "17th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th", "26th", "27th", "28th", "29th", "30th", "31st"]

MONTHSSHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]