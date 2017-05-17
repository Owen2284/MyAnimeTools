# Imports
import requests
import xml.etree.ElementTree as ET

from formatting import userStatusNumberToString, userStatusStringToNumber, seriesTypeNumberToString, seriesTypeStringToNumber
from objects import Anime, AnimeList, User
from constants import VERSION, ANIMEUSERSTATUS

def printIntro():
	printBreak()
	print("MAL App " + VERSION)

def printBreak():
	print("-----")

def getCommand():
	return input("Enter a command:- ").lower().split()

def getUser():
	username = input("Enter the name of the user to retrieve: ").lower()
	print("Contacting MAL...")
	data = initUser(username)
	if (data[0] is None) or (data[1] is None):
		print("No such user.")
	else:
		print("User " + data[0].userName + " loaded in.")
		printBreak()
		data[0].printUser()
	return data

def initUser(inUser):

	# Example: https://kuristina.herokuapp.com/anime/EmeraldSplash.xml
	#rootNode = constructXMLTree("mal", "http://myanimelist.net/malappinfo.php?u=" + inUser + "&status=all&type=anime")
	rootNode = constructXMLTree("kuristina", "https://kuristina.herokuapp.com/anime/" + inUser + ".xml")
	
	userObj = None
	animeObj = None
	n = 0

	if len(list(rootNode)) > 0:
		animedata = {}
		animeObj = AnimeList(animedata)
		for section in rootNode:
			# Initialising storage variables.
			minidict = {}
			newAnime = None
			# Check that the data hasn't errored.
			if section.tag != "error":
				# Check if the current tag is a myinfo tag.
				if section.tag != "myinfo":
					# Constructing dict of values for ease of access.
					for value in section:
						if value.text is not None:
							minidict[value.tag] = value.text
						else:
							minidict[value.tag] = "0"
					# Constructing the anime object.
					animeName = minidict["series_title"]
					newAnime = Anime(minidict["series_animedb_id"], animeName, minidict["series_synonyms"], int(minidict["series_type"]), 
						int(minidict["series_episodes"]), int(minidict["series_status"]), minidict["series_start"], 
						minidict["series_end"], minidict["series_image"], int(minidict["my_watched_episodes"]), 
						minidict["my_start_date"], minidict["my_finish_date"], int(minidict["my_score"]), int(minidict["my_status"]),
						int(minidict["my_rewatching"]), int(minidict["my_rewatching_ep"]), 
						int(minidict["my_last_updated"]), minidict["my_tags"])
					# Dupe name check
					if len(animedata) > 0:
						dupeCount = list(animedata.keys()).count(animeName)
						if dupeCount > 0:
							animeName += "(" + str(dupeCount) + ")"
					# Storing anime in dict.
					animeObj.anime[animeName] = newAnime
					n += 1
				else:
					# Constructing dict of user data.
					userdata = {}
					for value in section:
						userdata[value.tag] = value.text
					# CReating the user object.
					userObj = User(userdata["user_id"], userdata["user_name"], int(userdata["user_watching"]),
						int(userdata["user_completed"]), int(userdata["user_onhold"]), int(userdata["user_dropped"]), 
						int(userdata["user_plantowatch"]), float(userdata["user_days_spent_watching"]))
			else:
				return (None, None, 0)
		return (userObj, animeObj, n)
	else:
		return (None, None, 0)

def constructXMLTree(type, url):
	response = requests.get(url)
	rawResponse = response.text.encode("ascii", "ignore")
	rootNode = ET.fromstring(rawResponse)
	return rootNode

def getCategory(word):
	print("Categories for the " + word + ":")
	print("All - Plan To Watch - On Hold - Dropped - Currently Watching - Completed")
	category = input("Please enter a category for the " + word + ": ").lower()
	printBreak()
	if category in [x.lower() for x in ANIMEUSERSTATUS]:
		return category
	else:
		return None

def blankFilter():
	newDict = {
		"userStatuses" : [1,2,3,4,6],		# User's category for the anime.
		"name" : "",						# Series part name search
		"scoreMax" : 10,
		"scoreMin" : 0,						# Range of scores to include
		"airedIn": "",						# Shows airing in year specified. (Blank to ignore)
		"seriesTypes": [1,2,3,4,5,6]		# Series types, such as TV, OVA, etc.
	}
	return newDict

def getFilter(word):
	animeFilter = blankFilter()
	filterDone = False
	filterCommand = None
	while filterDone != True:

		# Display
		print("Current filter status for the " + word + ":")
		print(" (U)ser statuses: " + ", ".join(userStatusNumberToString(x) for x in animeFilter["userStatuses"]))
		print(" (N)ame contains: \"" + animeFilter["name"] + "\"")
		print(" (S)core range: " + str(animeFilter["scoreMin"]) + " to " + str(animeFilter["scoreMax"]))
		print(" (A)ired in the year: " + animeFilter["airedIn"])
		print(" (T)ype of series: " + ", ".join(seriesTypeNumberToString(x) for x in animeFilter["seriesTypes"]))
		print("Type the first letter of a filter field followed by the values to use for it to edit the filter separated by commas (e.g. \"U watching, plan to watch, dropped\", \"S 4,9\", \"T tv,ova\"), or enter \"done\" to confirm the filter.")
		printBreak()

		# Input
		filterCommand = input("> ").strip()

		# Filter alteration
		if filterCommand.startswith("done"):
			filterDone = True
		else:
			splitCommand = [filterCommand[0].lower(), filterCommand[2:]]
			if splitCommand[0] == "u":
				commandStatuses = [x.strip() for x in splitCommand[1].split(",")]
				newStatuses = []
				for sta in commandStatuses:
					staNum = userStatusStringToNumber(sta)
					if staNum >= 0:
						newStatuses.append(staNum)
				if len(newStatuses) > 0:
					animeFilter["userStatuses"] = newStatuses
					print("User statuses set to: " + ", ".join(userStatusNumberToString(x) for x in animeFilter["userStatuses"]))
				else:
					print("Invalid statuses entered for (U)ser status field.")
			elif splitCommand[0] == "n":
				animeFilter["name"] = splitCommand[1]
				print("Name fragment to search for set to: \"" + animeFilter["name"] + "\"")
			elif splitCommand[0] == "s":
				scoreRanges = [int(x) for x in splitCommand[1].split(",") if x.isdigit()]
				if (len(scoreRanges) == 2) and (scoreRanges[0] <= scoreRanges[1]) and (scoreRanges[0] >= 0) and (scoreRanges[1] <= 10):
					animeFilter["scoreMin"] = scoreRanges[0]
					animeFilter["scoreMax"] = scoreRanges[1]
					print("Score range set to: " + str(animeFilter["scoreMin"]) + " to " + str(animeFilter["scoreMax"]))
				else:
					print("Invalid range for (S)core range.")
			elif splitCommand[0] == "a":
				if (len(splitCommand[1]) == 4) and (splitCommand.isdigit()):
					animeFilter["airedIn"] = int(splitCommand[1])
					print("Air year to filter by set to: " + animeFilter["airedIn"])
				else:
					print("Invalid year entered for (A)ir year.")
			elif splitCommand[0] == "t":
				commandStatuses = [x.strip() for x in splitCommand[1].split(",")]
				newStatuses = []
				for sta in commandStatuses:
					staNum = seriesTypeStringToNumber(sta)
					if staNum >= 0:
						newStatuses.append(staNum)
				if len(newStatuses) > 0:
					animeFilter["seriesTypes"] = newStatuses
					print("Series types set to: " + ", ".join(seriesTypeNumberToString(x) for x in animeFilter["seriesTypes"]))
				else:
					print("Invalid series (T)ypes entered.")
			else:
				print("Invalid command.")
		printBreak()

	return animeFilter