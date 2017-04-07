# Imports
from objects import *
from actions import *

# functions
def start():	

	command = [""]
	commandInfo = None
	quitTime = False

	user = User("", "", 0, 0, 0, 0, 0, 0.0)
	anime = AnimeList(None)

	printIntro()
	printCommands(user)
	command = getCommand()
	printBreak()

	while quitTime != True:

		# Search through the command tuples for one that matches the data entered
		commandInfo = None
		for tupl in COMMANDLIST:
			if (len(command) > 0) and (tupl[0] == command[0]):
				commandInfo = tupl

		# Execute the found command.
		if commandInfo != None:
			if (commandInfo[3] == False) or (user.isLoaded()):
				if commandInfo[2] != None:
					commandInfo[2](user, anime)
				else :
					print("Unimplemented.")
			else:
				print("Please store a user using the \"new\" command before using the " + commandInfo[0] + " command.")
		else:
			print("No such command.")

		# List the available commands.
		printCommands(user)

		# Acquire the user's next command.
		command = getCommand()
		if len(command) > 0:
			quitTime = (command[0] == "quit")

		printBreak()


	print("Closing...")

def printIntro():
	printBreak()
	print("MAL App " + VERSION)

def printCommands(inUser):
	printBreak()
	for tupl in COMMANDLIST:
		if ((inUser.isLoaded()) or (tupl[3] == False)) and (tupl[2] is not None):
			print(tupl[0] + ((15 - len(tupl[0])) * " ") + " - " + tupl[1])
	printBreak()

def getCommand():
	return input("Enter a command:- ").lower().split()

# constants
COMMANDLIST = [
	("new", "Get a user's MAL data to use with the program.", actionNew, False),
	#("cache", "Load in a locally cached user to use the program with.", actionCache, False),
	("clear", "Removes the currently stored user.", actionClear, True),
	("user", "Shows details about a user.", actionUser, True),
	("list", "Lists all anime in a category.", actionList, True),
	("search", "Displays all anime that match your search term.", actionSearch, True),
	("display", "Displays in depth details about the selected anime.", actionDisplay, True),
	("roulette", "Selects a random anime from your list.", actionRoulette, True),
	("sorter", "Orders anime based on your preferences to determine your favourite shows.", actionTournament, True),
	#("stats", "Generate various statistics about your anime watching habits.", None, True),
	#("gantt", "Create a Gantt chart showing when you've been watching anime.", None, True),
	#("options", "Toggle or change various setting of this app.", None, False),
	#("test", "dev", actionTest, True),
	("quit", "Closes the program.", actionQuit, False)
]
VERSION = "v0.6.1"

# main program
start()
quit()