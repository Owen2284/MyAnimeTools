# Imports
import random
import requests
import xml.etree.ElementTree as ET

from objects import *
from actions import *

ANIMEUSERSTATUS = {
	0:"all",
	1:"currently watching",
	2:"completed",
	3:"on hold",
	4:"dropped",
	6:"plan to watch"
}

def printBreak():
	print("-----")

def newUser(user, anime):
	outData = getUser()
	if (outData[0] is not None):
		user.merge(outData[0])
		anime.merge(outData[1])

def getUser():
	username = input("Enter the name of the user to retrieve: ").lower()
	print("Contacting MAL...")
	data = initUser(username)
	if (data[0] is None) or (data[1] is None):
		print("No such user.")
	else:
		print("User " + data[0].userName + " loaded in.")
		printBreak()
		printUser(data[0], data[1])
	return data

def initUser(inUser):

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

def printUser(user, anime):
	user.printUser()

def clearUser(user, anime):
	user.clear()
	anime.clear()
	print("User data cleared.")

def search(user, anime):

	searchTerm = input("Please enter a search term: ").lower()
	printBreak()
	subAnime = {}
	added = False

	subAnime = anime.getAnimeByPartName(searchTerm)

	searchSize = len(subAnime)
	if searchSize > 0:
		print(str(searchSize) + " results found:")
		print()
		for item in subAnime:
			subAnime[item].printAnime()
			print()
	else:
		print("There were no anime found with that string fragment in them.")

def detail(user, anime):

	detailName = input("Please enter the anime to select: ").lower()
	printBreak()

	detailResult = anime.getAnimeByName(detailName)
	
	if detailResult is not None:
		detailResult.printAnimeDetailed()
	else:
		print("No matching anime. Consider using the \"list\" function to see exact names.")

def showList(user, anime):

	category = getCategory("list")
	if category is not None:
		subAnime = anime.getAnimeByCategory(category)
		listSize = len(subAnime)
		if listSize > 0:
			print("The category contains " + str(listSize) + " anime:")
			anime.printList(subAnime)
		else:
			print("The selected category has no anime.")

def roulette(user, anime):

	category = getCategory("roulette")
	if category is not None:
		subAnime = anime.getAnimeByCategory(category)
		rouletteSize = len(subAnime)
		if rouletteSize > 0:
			rouletteChoices = list(subAnime.keys())
			rouletteKey = random.choice(rouletteChoices)
			print("Out of " + str(rouletteSize) + " anime, the roulette chose: ")
			subAnime[rouletteKey].printAnime()
		else:
			print("The selected category has no anime.")

def tourney(user, anime):

	category = getCategory("sorter")
	if category is not None:
		subAnime = anime.getAnimeByCategory(category)
		numAnime = len(subAnime)
		if numAnime > 0:

			# Defines the numbers to use for the tournament.
			initGroupSize = 2
			groupsToMerge = 2

			# Runs the tournament.
			t = Tournament(subAnime, initGroupSize)
			print("Starting the sorter; type 1 to vote for the first anime, type 2 to vote for the second anime.")
			print("The sorting process may take a long time to complete, depending on the size of your list.")
			t.run(groupsToMerge)

			# TODO: Add optimisation stage.

			# Displays the tournament results.
			print("Sorting process complete, here are the results:")
			print(t.toString())

			# TODO: Writing to file

		else:
			print("The selected category has no anime.")

def quitter(user, anime):
	pass

def statusNumberToString(n):
	for key in ANIMEUSERSTATUS:
		if key == n:
			return ANIMEUSERSTATUS[key]
	return ""

def statusStringToNumber(s):
	for key in ANIMEUSERSTATUS:
		if ANIMEUSERSTATUS[key] == s:
			return key
	return -1

def getCategory(word):
	print("Categories for the " + word + ":")
	print("All - Plan To Watch - On Hold - Dropped - Currently Watching - Completed")
	category = input("Please enter a category for the " + word + ": ").lower()
	printBreak()
	if statusStringToNumber(category) >= 0:
		return category
	else:
		print("No such category.")
		return None

def filter(animeData, filterData):
	# TODO: Program this.
	pass

# Taken from http://stackoverflow.com/questions/15285534/isprime-function-for-python-language
def is_prime(n):
  if n == 2 or n == 3: return True
  if n < 2 or n%2 == 0: return False
  if n < 9: return True
  if n%3 == 0: return False
  r = int(n**0.5)
  f = 5
  while f <= r:
    if n%f == 0: return False
    if n%(f+2) == 0: return False
    f +=6
  return True   

actionNew = newUser
actionUser = printUser
actionClear = clearUser
actionList = showList
actionSearch = search
actionDisplay = detail
actionRoulette = roulette
actionTournament = tourney
actionQuit = quitter