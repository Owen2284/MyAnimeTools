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
		if data[2] == 0:
			print("Error: No such user.")
		elif data[2] == 1:
			print("Error: Connection issue arose.")
		else:
			print("Error: Unknown error.")
	else:
		print("User " + data[0].userName + " loaded in.")
		printBreak()
		data[0].printUser()
	return data

def initUser(inUser):

	# Example: https://kuristina.herokuapp.com/anime/EmeraldSplash.xml
	#rootNode = constructXMLTree("mal", "http://myanimelist.net/malappinfo.php?u=" + inUser + "&status=all&type=anime")
	rootNode = constructXMLTree("kuristina", "https://kuristina.herokuapp.com/anime/" + inUser + ".xml")
	if rootNode == None:
		return (None, None, 1)
	
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
	response = None
	try:
		response = requests.get(url)
	except requests.exceptions.ConnectionError:
		return None
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
	done = False
	view = True
	help = False
	filterCommand = None
	while done != True:

		# Display
		if view:
			print("Current filter status for the " + word + ":")
			print(" (U)ser statuses: " + ", ".join(userStatusNumberToString(x) for x in animeFilter["userStatuses"]))
			print(" (N)ame contains: \"" + animeFilter["name"] + "\"")
			print(" (S)core range: " + str(animeFilter["scoreMin"]) + " to " + str(animeFilter["scoreMax"]))
			print(" (A)ired in the year: " + animeFilter["airedIn"])
			print(" (T)ype of series: " + ", ".join(seriesTypeNumberToString(x) for x in animeFilter["seriesTypes"]))
			print("Operations:")
			print(" <bracketed letter> <values>  Sets the values of the field of the filter, multiple values must be comma-separated.")
			print(" \"view\"                   View this dialogue again.")
			print(" \"help\"                   Show examples of how to enter filter fields.")
			print(" \"done\"                   Confirm the filter's settings.")
			print(" \"cancel\"                 Return to the main command menu.")
			printBreak()
			view = False
		elif help:
			print("Example commands:")
			print(" \"U watching, dropped\"    Only show anime on your watching and dropped lists.")
			print(" \"N jo\"                   Only show anime whose name(s) contain the fragment \"jo\" (ignores case).")
			print(" \"S 8,10\"                 Only show anime you have rated with a score from 8 to 10 (inclusive).")
			print(" \"A 2017\"                 Only show anime that aired during 2017.")
			print(" \"T TV, OVA\"              Only show TV and OVA anime.")
			help = False

		# Input
		filterCommand = input("> ").strip()

		# Filter alteration
		if filterCommand.lower().startswith("done"):
			done = True
		elif filterCommand.lower().startswith("view"):
			view = True
			printBreak()
		elif filterCommand.lower().startswith("help"):
			help = True
		elif filterCommand.lower().startswith("cancel"):
			return None
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
				if (len(splitCommand[1]) == 4) and (splitCommand[1].isdigit()):
					animeFilter["airedIn"] = splitCommand[1]
					print("Air year to filter by set to: " + animeFilter["airedIn"])
				elif splitCommand[1] == "":
					animeFilter["airedIn"] = ""
					print("Air year filtering disabled.")
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

	return animeFilter

def getUserAtLaunch(username):
	data = initUser(username)
	if (data[0] is None) or (data[1] is None):
		print("Unable to load initial user.")
	else:
		print("User " + data[0].userName + " loaded in.")
		printBreak()
		data[0].printUser()
	return data

def readOptions(path):
	options = {}

	with open(path, "r") as f:
		for line in f:
			datas = line.strip().split(":")
			options[datas[0]] = datas[1]

	for key in options:
		if isinstance(options[key], str):
			if options[key].lower() == "on":
				options[key] = True
			elif options[key].lower() == "off":
				options[key] = False

	return options

def writeOptions(path, options):

	for key in options:
		if isinstance(options[key], bool):
			if options[key]:
				options[key] = "On"
			else:
				options[key] = "Off"

	with open(path, "w") as f:
		for key in options:
			newline = key + ":" + options[key] + "\n"
			f.write(newline)

def createOptions(path):
	writeOptions(path, {
		"useFiltering":"On",
		"defaultUserLoad":""
	})