# Imports
from objects import *
from actions import *

# functions
def start():	

	command = [""]
	commandInfo = None

	user = None
	anime = None

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
			if (commandInfo[3] == False) or (user != None):
				if commandInfo[0] == "user":
					printUser(user)
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

def printIntro():
	printBreak()
	print("MAL App " + VERSION)

def printCommands():
	printBreak()
	for tupl in COMMANDLIST:
		print(tupl[0] + ((15 - len(tupl[0])) * " ") + " - " + tupl[1])
	printBreak()

def getCommand():
	return input("Enter a command:- ").lower().split()

# constants
COMMANDLIST = [
	("new", "Allows a new user to be stored.", None, False),
	#("clear", "Removes the currently stored user.", None, True),
	("user", "Shows details about a user.", None, False),
	("list", "Lists all anime in a category.", None, True),
	("search", "Displays all anime that match your search term.", None, True),
	#("display", "Displays in depth details about the selected anime.", None, True),
	("roulette", "Select a random anime.", None, True),
	#("tournament", "Mode allowing you to determine your favourite anime.", None, True),
	#("stats", "", None, True),
	#("options", "", None, False),
	("quit", "Closes the program.", None, False)
]
VERSION = "v0.4"

# main program
start()
quit()