import random
import datetime
import os

from actions import getUser, getCategory, printBreak, getFilter, writeOptions
from objects import Tournament
from formatting import userStatusNumberToString
from gantt import createGanttChart

# Command display
def printCommands(inUser):
	printBreak()
	print("Available commands:-")
	for tupl in COMMANDLIST:
		if ((inUser.isLoaded()) or (tupl[3] == False)) and (tupl[2] is not None):
			print(" " + tupl[0] + ((15 - len(tupl[0])) * " ") + " - " + tupl[1])
	printBreak()

# Command methods.
def newUser(user, anime, options):
	outData = getUser("retrieve", True)
	if (outData[0] is not None):
		user.merge(outData[0])
		anime.merge(outData[1])

def printUser(user, anime, options):
	user.printUser()

def clearUser(user, anime, options):
	user.clear()
	anime.clear()
	print("User data cleared.")

def search(user, anime, options):

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

def detail(user, anime, options):

	detailName = input("Please enter the anime to select: ").lower()
	printBreak()

	detailResult = anime.getAnimeByName(detailName)
	
	if detailResult is not None:
		detailResult.printAnimeDetailed()
	else:
		print("No matching anime. Consider using the \"filter\" function to see exact names.")

def showList(user, anime, options):

	if options["useFiltering"] == True:
		animeFilter = getFilter("filter")
		subAnime = anime.filterAnime(animeFilter)
	else:
		category = getCategory("list")
		subAnime = anime.getAnimeByCategory(category)

	if subAnime is not None:
		listSize = len(subAnime)
		if listSize > 0:
			print("The category contains " + str(listSize) + " anime:")
			anime.printList(subAnime)
		else:
			if options["useFiltering"] == True:
				print("The filter returned no anime.")
			else:
				print("The selected category has no anime.")
	else:
		if options["useFiltering"] == True:
			print("Filtering cancelled.")
		else:
			print("Invalid category.")

def roulette(user, anime, options):

	if options["useFiltering"] == True:
		animeFilter = getFilter("roulette")
		subAnime = anime.filterAnime(animeFilter)
	else:
		category = getCategory("roulette")
		subAnime = anime.getAnimeByCategory(category)
		
	if subAnime is not None:
		rouletteSize = len(subAnime)
		if rouletteSize > 0:
			rouletteChoices = list(subAnime.keys())
			rouletteKey = random.choice(rouletteChoices)
			print("Out of " + str(rouletteSize) + " anime, the roulette chose: ")
			subAnime[rouletteKey].printAnime()
		else:
			if options["useFiltering"] == True:
				print("The filter returned no anime.")
			else:
				print("The selected category has no anime.")
	else:
		if options["useFiltering"] == True:
			print("Filtering cancelled.")
		else:
			print("Invalid category.")

def tourney(user, anime, options):

	categoryString = "blank"

	if options["useFiltering"] == True:
		animeFilter = getFilter("tournament")
		categoryString = "-".join(userStatusNumberToString(x) for x in animeFilter["userStatuses"]).replace(" ", "-")
		subAnime = anime.filterAnime(animeFilter)
	else:
		category = getCategory("tournament")
		categoryString = category
		subAnime = anime.getAnimeByCategory(category)

	if subAnime is not None:
		numAnime = len(subAnime)
		if numAnime > 0:

			# Defines the numbers to use for the tournament.
			initGroupSize = 2
			groupsToMerge = 2

			# Runs the tournament.
			t = Tournament(subAnime, initGroupSize)
			print("Number of items in the tournament:- " + str(numAnime))
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

			# TODO: Name list function.

			# Writing to file.
			dt = datetime.datetime.now()
			filename = "lists/tournament-"+categoryString+"-"+str(dt.hour)+"-"+str(dt.minute)+".txt"
			os.makedirs(filename.split("/")[0], exist_ok=True)
			with open(filename, "w") as f:
				f.write("Results:\n")
				f.write(t.toString())
			print("List written to " + filename + ".")

		else:
			if options["useFiltering"] == True:
				print("The filter returned no anime.")
			else:
				print("The selected category has no anime.")
	else:
		if options["useFiltering"] == True:
			print("Filtering cancelled.")
		else:
			print("Invalid category.")

def gantt(user, anime, options):

	if options["useFiltering"] == True:
		animeFilter = getFilter("Gantt chart")
		subAnime = anime.filterAnime(animeFilter)
	else:
		category = getCategory("Gantt chart")
		subAnime = anime.getAnimeByCategory(category)

	if subAnime is not None:
		listSize = len(subAnime)
		if listSize > 0:
			ganttData = []
			idNum = 0
			warn1 = False
			warn2 = False
			todayStr = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)

			# Loop to format all anime appropriately.
			for key in subAnime:
				addit = True
				currentAnime = subAnime[key]
				aniName, aniColour, aniStart, aniEnd = currentAnime.name, currentAnime.userStatusNum, currentAnime.userStartDateRaw, currentAnime.userEndDateRaw

				# Check end date to see if it's unknown.
				if currentAnime.userEndDateRaw == "0000-00-00":
					# Check if it's CW and fixable.
					if currentAnime.userStartDateRaw != "0000-00-00" and currentAnime.userStatusNum == 1:
						if warn1 == False:
							print("Currently Watching anime have their end date set to today.")
							warn1 = True
						aniEnd = todayStr
					# Otherwise discard it.
					else:
						if warn2 == False:
							print("Some anime have been excluded, as they had unknown start and end dates.")
							warn2 = True
						addit = False

				# Add the anime to the dataset.
				if addit:
					animeTuple = (idNum, aniName, aniColour, aniStart, aniEnd)
					ganttData.append(animeTuple)
					idNum +=1

			# Sorting the data by starting date.
			ganttData.sort(key=lambda x: x[3])
			#ganttData.sort(key=lambda x: x[4])

			# Run the Gantt chart creator.
			plt = createGanttChart(ganttData)
			print("Gantt chart creation complete, now displaying result...")
			plt.show(block=False)

			# Saving the Gantt chart as a .svg file.
			filename = "gantts/gantt-" + str(datetime.datetime.now().hour) + "-" + str(datetime.datetime.now().minute) + ".svg"
			os.makedirs(filename.split("/")[0], exist_ok=True)
			plt.savefig(filename)
			print("The gantt chart has been saved to \"" + filename + "\".")

		else:
			if options["useFiltering"] == True:
				print("The filter returned no anime.")
			else:
				print("The selected category has no anime.")
	else:
		if options["useFiltering"] == True:
			print("Filtering cancelled.")
		else:
			print("Invalid category.")

def optioniser(user, anime, options):
	print("Current options:")
	print(" (A)dvanced filters: " + ("On" if options["useFiltering"] == True else "Off"))
	print(" (D)efault user to load in: " + ("\"" + options["defaultUserLoad"] + "\"" if options["defaultUserLoad"] != "" else "None"))
	print("Enter the bracketed letter to toggle the corresponding option.")
	printBreak()

	optionToToggle = input("> ").strip().lower()
	if len(optionToToggle) == 1:
		if optionToToggle == "a":
			options["useFiltering"] = not options["useFiltering"]
			print("Advanced filters are now " + ("enabled." if options["useFiltering"] == True else "disabled."))
			writeOptions("data/options.txt", options)
		elif optionToToggle == "d":
			theuser = input("Enter the username to load in at launch, or enter nothing to disable the function: ")
			options["defaultUserLoad"] = theuser
			print("Default user to load in now set to " + ("\"" + options["defaultUserLoad"] + "\"." if options["defaultUserLoad"] != "" else "None."))
			writeOptions("data/options.txt", options)
		else:
			print("Invalid character entered.")
	else:
		print("Invalid input.")

def comparator(user, anime, options):
	outData = getUser("compare", True)
	if (outData[0] is not None):
		user2 = outData[0]
		anime2 = outData[1]
	# TODO: Compare stuff.


def statifier(user, anime, options):
	userstats = user.getStats()
	animestats = anime.getStats()
	print("Number of anime on list: " + userstats["total"])


def quitter(user, anime, options):
	pass

def tester(user, anime, options):
	pass

actionNew = newUser
actionUser = printUser
actionClear = clearUser
actionCompare = comparator
actionFilter = showList
actionDisplay = detail
actionRoulette = roulette
actionTournament = tourney
actionStats = statifier
actionGantt = gantt
actionOptions = optioniser
actionTest = tester
actionQuit = quitter

COMMANDLIST = [
	("new", "Get a user's MAL data to use with the program.", actionNew, False),
	#("cache", "Load in a locally cached user to use the program with.", None, False),
	("clear", "Removes the currently stored user.", actionClear, True),
	("user", "Shows details about a user.", actionUser, True),
	("compare", "Find out how similar or different you are from another user.", actionCompare, True),
	("filter", "Lists all anime that match your filter.", actionFilter, True),
	("display", "Displays in depth details about the selected anime.", actionDisplay, True),
	("roulette", "Selects a random anime from your list.", actionRoulette, True),
	("tournament", "Orders anime based on your preferences to determine your favourite shows.", actionTournament, True),
	("stats", "Generate various statistics about your anime watching habits.", actionStats, True),
	("gantt", "Create a Gantt chart showing when you've been watching anime.", actionGantt, True),
	("options", "Toggle or change various setting of this app.", actionOptions, False),
	#("test", "Developer command for testing code.", actionTest, True),
	("quit", "Closes the program.", actionQuit, False)
]