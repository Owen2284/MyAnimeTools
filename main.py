from actions import printIntro, printBreak, getCommand
from objects import User, AnimeList
from commands import COMMANDLIST, printCommands

# functions
def start():	

	command = [""]
	commandInfo = None
	quitTime = False

	user = User("", "", 0, 0, 0, 0, 0, 0.0)
	anime = AnimeList(None)
	options = {
		"useFiltering": True,
		"launchLoad": False
	}
	# TODO: Instaload EmeraldSplash function.
	if options["launchLoad"] == True:
		COMMANDLIST[0][2](user, anime, options)

	printIntro()

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