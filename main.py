import os
import os.path

from actions import printIntro, printBreak, getCommand, getUserAtLaunch, readOptions, writeOptions, createOptions
from objects import User, AnimeList
from commands import COMMANDLIST, printCommands
from constants import OPTIONSPATH

# functions
def start():

	printIntro()

	command = [""]
	commandInfo = None
	quitTime = False

	user = User("", "", 0, 0, 0, 0, 0, 0.0)
	anime = AnimeList(None)
	
	# Reading in options.
	if os.path.exists(OPTIONSPATH) == False:
		os.makedirs(OPTIONSPATH.split("/")[0], exist_ok=True)
		createOptions(OPTIONSPATH)
	options = readOptions(OPTIONSPATH)

	# Applying options.
	if options["defaultUserLoad"] != "":
		printBreak()
		print("Attemting to load in default user...")
		outData = getUserAtLaunch(options["defaultUserLoad"])
		if (outData[0] is not None):
			user.merge(outData[0])
			anime.merge(outData[1])
		else:
			options["defaultUserLoad"] = ""
			writeOptions(OPTIONSPATH, options)

	while quitTime != True:

		# List the available commands.
		printCommands(user)		

		# Acquire the user's next command.
		command = getCommand()
		if len(command) > 0:
			quitTime = (command[0] == "quit")

		printBreak()

		# Search through the command tuples for one that matches the data entered
		if (quitTime != True):
			commandInfo = None
			for tupl in COMMANDLIST:
				if (len(command) > 0) and (tupl[0] == command[0]):
					commandInfo = tupl

			# Execute the found command.
			if commandInfo != None:
				if (commandInfo[3] == False) or (user.isLoaded()):
					if commandInfo[2] != None:
						commandInfo[2](user, anime, options)
					else :
						print("Unimplemented.")
				else:
					print("Please store a user using the \"new\" command before using the " + commandInfo[0] + " command.")
			else:
				print("No such command.")

	print("Closing...")

# main program
start()