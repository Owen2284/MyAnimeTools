# imports
import random
import requests
import xml.etree.ElementTree as ET

# functions
def start():	

	command = [""]
	commandInfo = None

	user = None
	anime = None
	animeCount = 0

	printIntro()
	printCommands()
	command = getCommand()
	printBreak()

	while command[0] != "quit":

		commandInfo = None
		for tupl in COMMANDLIST:
			if tupl[0] == command[0]:
				commandInfo = tupl

		if commandInfo != None:
			if (commandInfo[2] == False) or (user != None):
				if commandInfo[0] == "user":
					printUser(user, animeCount)
				elif commandInfo[0] == "new":
					outData = getUser()
					if (outData[0] is not None):
						user = outData[0]
						anime = outData[1]
						animeCount = outData[2]
				elif commandInfo[0] == "search":
					search(anime)
				elif commandInfo[0] == "roulette":
					roulette(anime)
				elif commandInfo[0] == "list":
					showList(anime)
			else:
				print("Please store a user using the \"new\" command before using the " + commandInfo[0] + " function.")
		else:
			print("No such command.")

		printCommands()
		command = getCommand()
		printBreak()

	print("Closing...")

def getUser():
	username = input("Enter the name of the user to retrieve: ").lower()
	data = initUser(username)
	if (data[0] is None) or (data[1] is None):
		print("No such user.")
	else:
		printUser(data[0], data[2])
	return data

def getUserLoop():
	username = input("Enter the name of the user to retrieve: ").lower()
	data = initUser(username)
	while (data[0] is None) or (data[1] is None):
		print("No such user.")
		username = input("Enter the name of the user to retrieve: ").lower()
		data = initUser(username)
	printUser(data[0], data[2])
	return data

def initUser(inUser):

	response = requests.get(PREFIX + inUser + SUFFIX)
	rootNode = ET.fromstring(response.text.encode("ascii", "ignore"))
	
	userdata = {}
	animedata = {}
	n = 0

	if len(list(rootNode)) > 0:
		for section in rootNode:
			minidict = {}
			if section.tag != "error":
				if section.tag != "myinfo":
					for value in section:
						minidict[value.tag] = value.text
					animeName = minidict["series_title"]
					if len(animedata) > 0:
						dupeCount = list(animedata.keys()).count(animeName)
						if dupeCount > 0:
							animeName += "(" + str(dupeCount) + ")"
					animedata[animeName] = minidict
					n += 1
				else:
					for value in section:
						userdata[value.tag] = value.text
			else:
				return (None, None, 0)
		return (userdata, animedata, n)
	else:
		return (None, None, 0)

def printUser(inUser, inAnimeCount):
	if inUser is None:
		print("No user stored. Use the \"new\" command to store a user.")
	else:
		print("Username: " + inUser["user_name"] + "")
		print(str(inAnimeCount) + " anime found:")
		print("- Watching: " + inUser["user_watching"])
		print("- Completed: " + inUser["user_completed"])
		print("- On Hold: " + inUser["user_onhold"])
		print("- Dropped: " + inUser["user_dropped"])
		print("- Plan to Watch: " + inUser["user_plantowatch"])

def printIntro():
	printBreak()
	print("MAL App " + VERSION)

def printCommands():
	printBreak()
	for tupl in COMMANDLIST:
		print(tupl[0] + ((15 - len(tupl[0])) * " ") + " - " + tupl[1])
	printBreak()

def printBreak():
	print("-----")

def printAnime(inAnimeShow):
	print(" Title: " + inAnimeShow["series_title"])
	print(" Synonyms: " + inAnimeShow["series_synonyms"])
	print(" Number of episodes: " + inAnimeShow["series_episodes"])

def printAnimeShort(inAnimeShow):
	print(" " + inAnimeShow["series_title"])

def printList(inAnimu):
	for item in inAnimu:
		printAnimeShort(inAnimu[item])

def getCommand():
	return input("Enter a command:- ").lower().split()

def search(inAnime):

	searchTerm = input("Please enter a search term: ").lower()
	printBreak()
	subAnime = {}
	added = False

	for item in inAnime:
		added = False
		theNames = getAllNames(inAnime[item])

		for anyName in theNames:
			if (added == False) and (searchTerm in anyName.lower()):
				subAnime[item] = inAnime[item]
				added = True

	searchSize = len(subAnime)
	if searchSize > 0:
		print(str(searchSize) + " results found:")
		print()
		for item in subAnime:
			printAnime(subAnime[item])
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
		subAnime = inAnime
	else:
		subAnime = getAnimeByCategory(inAnime, category)
	searchSize = len(subAnime)
	if searchSize > 0:
		print("The category contains " + str(searchSize) + " anime:")
		printList(subAnime)
	else:
		print("The selected category has no anime.")

def allAnimeString(inAnime):
	ret = ""
	for item in inAnime:
		ret += item + ", "
	return ret[:len(ret) - 2]

def showList(inAnime):

	print("Categories for the list:")
	print("All - Plan To Watch - On Hold - Dropped - Currently Watching - Completed")
	category = input("Please enter a category for the list: ").lower()
	printBreak()
	if statusStringToNumber(category) >= 0:
		subAnime = {}
		if category == "all":
			subAnime = inAnime
		else:
			subAnime = getAnimeByCategory(inAnime, category)
		rouletteSize = len(subAnime)
		if rouletteSize > 0:
			print("The category contains " + str(rouletteSize) + " anime:")
			printList(subAnime)
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
			subAnime = inAnime
		else:
			subAnime = getAnimeByCategory(inAnime, category)
		rouletteSize = len(subAnime)
		if rouletteSize > 0:
			rouletteChoices = list(subAnime.keys())
			rouletteKey = random.choice(rouletteChoices)
			print("Out of " + str(rouletteSize) + " anime, the roulette chose: ")
			printAnime(subAnime[rouletteKey])
		else:
			print("The selected category has no anime.")
	else:
		print("No such category.")

def getAnimeByCategory(inInAnime, inCategory):
	newAnime = {}
	for key in inInAnime:
		currentAnime = inInAnime[key]
		if statusNumberToString(int(currentAnime["my_status"])) == inCategory:
			newAnime[key] = currentAnime
	return newAnime

def getAllNames(inAniShow):
	possibleNames = [inAniShow["series_title"]]
	if inAniShow["series_synonyms"] is not None:
		for altName in inAniShow["series_synonyms"].split(";"):
			possibleNames.append(altName)
	return possibleNames

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

# constants
COMMANDLIST = [
	("new", "Allows a new user to be stored.", False),
	#("clear", "Removes the currently stored user.", False),
	("user", "Shows details about a user.", False),
	("list", "Lists all anime in a category.", True),
	("search", "Displays all anime that match your search term.", True),
	#("display", "Displays in depth details about the selected anime.", True),
	("roulette", "Select a random anime.", True),
	#("tournament", "Mode allowing you to determine your favourite anime.", True),
	#("stats", "", True),
	#("options", "", False),
	("quit", "Closes the program.", False)
]
ANIMESTATUS = {
	0:"all",
	1:"currently watching",
	2:"completed",
	3:"on hold",
	4:"dropped",
	6:"plan to watch"
}
PREFIX = "http://myanimelist.net/malappinfo.php?u="
SUFFIX = "&status=all&type=anime"
VERSION = "v0.3"

# main program
start()
quit()