import random
import datetime

from actions import getUser, getCategory, printBreak
from objects import Tournament

# Command display
def printCommands(inUser):
	printBreak()
	print("Available commands:-")
	for tupl in COMMANDLIST:
		if ((inUser.isLoaded()) or (tupl[3] == False)) and (tupl[2] is not None):
			print(" " + tupl[0] + ((15 - len(tupl[0])) * " ") + " - " + tupl[1])
	printBreak()

# Command methods.
def newUser(user, anime):
	outData = getUser()
	if (outData[0] is not None):
		user.merge(outData[0])
		anime.merge(outData[1])

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

	category = getCategory("tournament")
	if category is not None:
		subAnime = anime.getAnimeByCategory(category)
		numAnime = len(subAnime)
		if numAnime > 0:

			# Defines the numbers to use for the tournament.
			initGroupSize = 2
			groupsToMerge = 2

			# Runs the tournament.
			t = Tournament(subAnime, initGroupSize)
			print("Starting the tournament sorter; type 1 to vote for the first anime, type 2 to vote for the second anime, or U to undo your last choice.")
			print("The sorting process may take a long time to complete, depending on the size of your list.")
			t.run(groupsToMerge)

			# Runs the optimiser.
			printBreak()
			print("Main tournament sorting stage complete, you can now run one or more optimisation stages.")
			print("Please enter how many optimisation stages you want to run. (Enter 0 or a non-number for no optimisation)")
			optimisations = input("> ")
			try:
				optimisations = int(optimisations)
				t.optimise(optimisations)
			except:
				pass

			# Displays the tournament results.
			printBreak()
			print("Tournament sorting process complete, here are the results:")
			print(t.toString())

			# Writing to file.
			dt = datetime.datetime.now()
			filename = "lists/tournament-"+category+"-"+str(dt.hour)+"-"+str(dt.minute)+".txt"
			f = open(filename, "w")
			f.write("Results:\n")
			f.write(t.toString())
			print("List written to " + filename + ".")

		else:
			print("The selected category has no anime.")

def quitter(user, anime):
	pass

def tester(user, anime):
	pass

actionNew = newUser
actionUser = printUser
actionClear = clearUser
actionList = showList
actionSearch = search
actionDisplay = detail
actionRoulette = roulette
actionTournament = tourney
actionTest = tester
actionQuit = quitter

COMMANDLIST = [
	("new", "Get a user's MAL data to use with the program.", actionNew, False),
	#("cache", "Load in a locally cached user to use the program with.", actionCache, False),
	("clear", "Removes the currently stored user.", actionClear, True),
	("user", "Shows details about a user.", actionUser, True),
	#("compare", "Find out how similar or different you are from another user.", actionCompare, True),
	("list", "Lists all anime in a category.", actionList, True),
	("search", "Displays all anime that match your search term.", actionSearch, True),
	("display", "Displays in depth details about the selected anime.", actionDisplay, True),
	("roulette", "Selects a random anime from your list.", actionRoulette, True),
	("tournament", "Orders anime based on your preferences to determine your favourite shows.", actionTournament, True),
	#("stats", "Generate various statistics about your anime watching habits.", None, True),
	#("gantt", "Create a Gantt chart showing when you've been watching anime.", None, True),
	#("options", "Toggle or change various setting of this app.", None, False),
	#("test", "Developer command for testing code.", actionTest, True),
	("quit", "Closes the program.", actionQuit, False)
]