# Imports
import random
import requests
import xml.etree.ElementTree as ET

from objects import *
from actions import *

PREFIX = "http://myanimelist.net/malappinfo.php?u="
SUFFIX = "&status=all&type=anime"

ANIMESTATUS = {
	0:"all",
	1:"currently watching",
	2:"completed",
	3:"on hold",
	4:"dropped",
	6:"plan to watch"
}

def printBreak():
	print("-----")

def getUser():
	username = input("Enter the name of the user to retrieve: ").lower()
	print("Contacting MAL...")
	data = initUser(username)
	if (data[0] is None) or (data[1] is None):
		print("No such user.")
	else:
		print("User " + data[0].userName + " loaded in.")
		printBreak()
		printUser(data[0])
	return data

def initUser(inUser):

	response = requests.get(PREFIX + inUser + SUFFIX)
	rootNode = ET.fromstring(response.text.encode("ascii", "ignore"))
	
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

def printUser(inUser):
	if inUser is None:
		print("No user stored. Use the \"new\" command to store a user.")
	else:
		inUser.printUser()

def search(inAnime):

	searchTerm = input("Please enter a search term: ").lower()
	printBreak()
	subAnime = {}
	added = False

	for item in inAnime.anime:
		added = False
		theNames = inAnime.anime[item].getAllNames()

		for anyName in theNames:
			if (added == False) and (searchTerm in anyName.lower()):
				subAnime[item] = inAnime.anime[item]
				added = True

	searchSize = len(subAnime)
	if searchSize > 0:
		print(str(searchSize) + " results found:")
		print()
		for item in subAnime:
			subAnime[item].printAnime()
			print()
	else:
		print("There were no anime found with that string fragment in them.")

def detail(inAnime):

	print("Anime that can be selected:")
	print(allAnimeString(inAnime))
	category = input("Please enter the anime to select: ").lower()
	printBreak()
	subAnime = {}
	if category == "all":
		subAnime = inAnime.anime
	else:
		subAnime = inAnime.getAnimeByCategory(category)
	searchSize = len(subAnime)
	if searchSize > 0:
		print("The category contains " + str(searchSize) + " anime:")
		inAnime.printList(subAnime)
	else:
		print("The selected category has no anime.")

def showList(inAnime):

	print("Categories for the list:")
	print("All - Plan To Watch - On Hold - Dropped - Currently Watching - Completed")
	category = input("Please enter a category for the list: ").lower()
	printBreak()
	if statusStringToNumber(category) >= 0:
		subAnime = {}
		if category == "all":
			subAnime = inAnime.anime
		else:
			subAnime = inAnime.getAnimeByCategory(category)
		listSize = len(subAnime)
		if listSize > 0:
			print("The category contains " + str(listSize) + " anime:")
			inAnime.printList(subAnime)
		else:
			print("The selected category has no anime.")
	else:
		print("No such category.")

def roulette(inAnime):

	print("Categories for the roulette:")
	print("All - Plan To Watch - On Hold - Dropped - Currently Watching - Completed")
	category = input("Please enter a category for the roulette: ").lower()
	printBreak()
	if statusStringToNumber(category) >= 0:
		subAnime = {}
		if category == "all":
			subAnime = inAnime.anime
		else:
			subAnime = inAnime.getAnimeByCategory(category)
		rouletteSize = len(subAnime)
		if rouletteSize > 0:
			rouletteChoices = list(subAnime.keys())
			rouletteKey = random.choice(rouletteChoices)
			print("Out of " + str(rouletteSize) + " anime, the roulette chose: ")
			subAnime[rouletteKey].printAnime()
		else:
			print("The selected category has no anime.")
	else:
		print("No such category.")

def statusNumberToString(n):
	for key in ANIMESTATUS:
		if key == n:
			return ANIMESTATUS[key]
	return ""

def statusStringToNumber(s):
	for key in ANIMESTATUS:
		if ANIMESTATUS[key] == s:
			return key
	return -1