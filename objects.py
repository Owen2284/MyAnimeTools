import random

class Anime:

	# Fields
	aID = ""
	name = ""
	link = ""

	seriesSynonymsStr = ""
	seriesSynonymsList = list()
	seriesTypeNum = -1
	seriesEpisodes = -1
	seriesStatusNum = -1
	seriesStatusStr = ""
	seriesStartDate = ""
	seriesEndDate = ""
	seriesImageURL = ""

	userID = ""
	userWatchedEps = -1
	userStartDate = ""
	userEndDate = ""
	userScore = -1
	userStatusNum = -1
	userStatusStr = ""
	userRewatching = -1
	userRewatchingEp = -1
	userLastUpdatedTimestamp = -1
	userTags = ""

	ANIMEUSERSTATUS = {
		0:"All",
		1:"Currently Watching",
		2:"Completed",
		3:"On Hold",
		4:"Dropped",
		6:"Plan To Watch"
	}


	# Constructor
	def __init__(self, inID, inName, inSynonymsStr, inSeriesTypeNum, inSeriesEpisodes,
		inSeriesStatusNum, inSeriesStartDate, inSeriesEndDate, inSeriesImageURL,
		inUserWatchedEps, inUserStartDate, inUserEndDate, inUserScore, inUserStatusNum,
		inUserRewatching, inUserRewatchingEp, inUserLastUpdatedTimestamp, inUserTagsStr):

		self.aID = inID
		self.name = inName
		self.link = "https://myanimelist.net/anime/" + self.aID

		self.seriesSynonymsStr = inSynonymsStr
		self.seriesSynonymsList = self.synonymsStringToList(inSynonymsStr)
		self.seriesTypeNum = inSeriesTypeNum
		self.seriesTypeStr = ""
		self.seriesEpisodes = inSeriesEpisodes
		self.seriesStatusNum = inSeriesStatusNum
		self.seriesStatusStr = self.statusNumberToString(inSeriesStatusNum)
		self.seriesStartDate = inSeriesStartDate
		self.seriesEndDate = inSeriesEndDate
		self.seriesImageURL = inSeriesImageURL

		self.userID = "0"
		self.userWatchedEps = inUserWatchedEps
		self.userStartDate = inUserStartDate
		self.userEndDate = inUserEndDate
		self.userScore = inUserScore
		self.userStatusNum = inUserStatusNum
		self.userStatusStr = self.statusNumberToString(inUserStatusNum)
		self.userRewatching = inUserRewatching
		self.userRewatchingEp = inUserRewatchingEp
		self.userLastUpdatedTimestamp = inUserLastUpdatedTimestamp
		self.userTags = inUserTagsStr

	# Methods used during construction.
	def statusNumberToString(self, n):
		for key in self.ANIMEUSERSTATUS:
			if key == n:
				return self.ANIMEUSERSTATUS[key]
		return ""

	def statusStringToNumber(self, s):
		for key in self.ANIMEUSERSTATUS:
			if self.ANIMEUSERSTATUS[key] == s:
				return key
		return -1

	def synonymsStringToList(self, synStr):
		possibleNames = list()
		for altName in synStr.split(";"):
			possibleNames.append(altName)
		return possibleNames


	# Normal methods
	def getAllNames(self):
		possibleNames = [self.name]
		for altName in self.seriesSynonymsList:
			possibleNames.append(altName)
		return possibleNames

	def printAnime(self):
		print(" Title: " + self.name)
		print(" Synonyms: " + self.seriesSynonymsStr)
		print(" Number of episodes: " + str(self.seriesEpisodes))

	def printAnimeShort(self):
		print(" " + self.name)

	def printAnimeDetailed(self):
		print("General info:")
		print(" Title: " + self.name)
		print(" ID: " + self.aID)
		print(" Link: " + self.link)
		print(" Synonyms: " + self.seriesSynonymsStr)
		print(" Type: " + self.seriesTypeStr)
		print(" Number of episodes: " + str(self.seriesEpisodes))
		print(" Status: " + self.seriesStatusStr)
		print(" Airdates: " + self.seriesStartDate + " to " + self.seriesEndDate)
		print("User info:")
		print(" User status: " + self.userStatusStr)
		print(" User score: " + str(self.userScore) + " \ 10")		
		print(" Number of episodes watched: " + str(self.userWatchedEps) + " \ " + str(self.seriesEpisodes))
		print(" Watch dates: From " + self.userStartDate + " to " + self.userEndDate)
		print(" Times Rewatched: " + str(self.userRewatching))
		print(" Rewatched to episode: " + str(self.userRewatchingEp))
		print(" User Tags: " + self.userTags)



class AnimeList:

	anime = {}

	# Constructor
	def __init__(self, animeDict):
		self.anime = animeDict

	# Methods
	def printList(self):
		for key in self.anime:
			self.anime[key].printAnimeShort()

	def printList(self, subAnime):
		for key in subAnime:
			self.anime[key].printAnimeShort()

	def getAnimeByName(self, inName):
		for key in self.anime:
			currentAnime = self.anime[key]
			for currentName in currentAnime.getAllNames():
				if currentName.lower() == inName.lower():
					return currentAnime
		return None

	def getAnimeByPartName(self, inPart):
		returnAnime = {}
		for key in self.anime:
			added = False
			currentAnime = self.anime[key]
			for anyName in currentAnime.getAllNames():
				if (added == False) and (inPart in anyName.lower()):
					returnAnime[key] = currentAnime
					added = True
		return returnAnime

	def getAnimeByCategory(self, inCategory):
		if inCategory == "all":
			return list(self.anime)
		else:
			newAnime = {}
			for key in self.anime:
				currentAnime = self.anime[key]
				if currentAnime.userStatusStr.lower() == inCategory:
					newAnime[key] = currentAnime
			return newAnime

	def getAnimeCount():
		return len(anime)

	def isEmpty():
		return getAnimeCount() == 0;

	def merge(self, target):
		self.anime = target.anime

	def clear(self):
		self.anime = {}



class User:

	# Fields
	userID = ""
	userName = ""

	countWatching = 0
	countCompleted = 0
	countOnHold = 0
	countDropped = 0
	countPlanToWatch = 0
	countAll = 0

	daysSpentWatching = 0.0

	def __init__(self, inID, inName, inCountWatch, inCountComp, inCountOnHold, inCountDrop,
		inCountPlan, inDays):
		
		self.userID = inID
		self.userName = inName
		
		self.countWatching = inCountWatch
		self.countCompleted = inCountComp
		self.countOnHold = inCountOnHold
		self.countDropped = inCountDrop
		self.countPlanToWatch = inCountPlan
		self.countAll = inCountWatch + inCountComp + inCountOnHold + inCountOnHold + inCountPlan

		self.daysSpentWatching = inDays

	def merge(self, target):
		self.userID = target.userID
		self.userName = target.userName
		self.countWatching = target.countWatching
		self.countCompleted = target.countCompleted
		self.countOnHold = target.countOnHold
		self.countDropped = target.countDropped
		self.countPlanToWatch = target.countPlanToWatch
		self.countAll = target.countAll
		self.daysSpentWatching = target.daysSpentWatching

	def printUser(self):
		print("Username: " + self.userName + "")
		print(str(self.countAll) + " anime found:")
		print("- Watching: " + str(self.countWatching))
		print("- Completed: " + str(self.countCompleted))
		print("- On Hold: " + str(self.countOnHold))
		print("- Dropped: " + str(self.countDropped))
		print("- Plan to Watch: " + str(self.countPlanToWatch))

	def isLoaded(self):
		return (self.userName != "" and self.userID != "")

	def clear(self):
		self.userID = ""
		self.userName = ""
		self.countWatching = 0
		self.countCompleted = 0
		self.countOnHold = 0
		self.countDropped = 0
		self.countPlanToWatch = 0
		self.countAll = 0
		self.daysSpentWatching = 0.0



class TournamentRound:

	# Fields
	orderedAnime = None

	# Methods
	def __init__(self):
		self.orderedAnime = []

	def addStart(self, inAnime):
		self.orderedAnime.insert(0, inAnime)

	def addEnd(self, inAnime):
		self.orderedAnime.append(inAnime)

	def getAnimes(self):
		return list(self.orderedAnime)

	def getAnimesShuffled(self):
		return random.shuffle(list(self.orderedAnime))

	def numAnime(self):
		return len(self.orderedAnime)

	def numChoices(self):
		return len(self.orderedAnime)-1

	def toString(self):
		for j in range(0, len(orderedAnime)):
			animo = roundoAnimes[j]
			returnedString += " " + str(j+1) + ". " + animo.name + "\n"



class Tournament:

	# Fields
	rounds = []

	# Methods
	def __init__(self, inAnime, initRoundSize):
		internalList = list(inAnime.values())
		# Creates whole rounds.
		while (len(internalList) >= initRoundSize):
			# Creating round object.
			newRound = TournamentRound()
			# Adding the required number of anime to the round.
			for i in range(0, initRoundSize):
				newRound.addEnd(internalList.pop(random.randrange(len(internalList))))
			# Adding the round to the main list.
			self.rounds.append(newRound)
		# Creates partial rounds.
		if (len(internalList) > 0):
			# Creating round object.
			newRound = TournamentRound()
			# Adding the remaining anime to the round.
			for i in range(0, len(internalList)):
				newRound.addEnd(internalList.pop(random.randrange(len(internalList))))
			# Adding the round to the main list.
			self.rounds.append(newRound)

	def run(self, mergeNum):

		# TODO: Store edges to determine preference of non neighbour anime? Like planning in AI module.

		# Return if only one anime.
		if (len(self.rounds) == 1 and len(self.rounds[0].getAnimes()) <= 1):
			return
		# Initialising stage variables.
		stage = 1
		maxStages = self.getMaxStages(mergeNum)
		# Loop for all stages of the tournament
		while(stage <= maxStages):

			# Stage initialisation.
			print("Stage " + str(stage) + " of " + str(maxStages))
			completeRounds = []

			# Loops through the rounds.
			for roundu in self.rounds:
				newRoundu = TournamentRound()
				# Creates a queue for all of the anime in the current round.
				animeQueue = list(roundu.getAnimes())
				if (len(animeQueue) > 1):
					# Creates a list to store the two choices.
					currentQueue = [animeQueue.pop(), animeQueue.pop()]
					# Looping through the anime to sort.
					while (len(animeQueue) > 0 or len(currentQueue) == 2):
						# Gets the user input.
						print(" \"" + currentQueue[0].name + "\" or \"" + currentQueue[1].name + "\"?")
						choice = input(" > ")
						if (choice == "1" or choice == "2"):
							# Stores the not chosen anime in the new round.
							notChoice = int(choice) % 2
							newRoundu.addStart(currentQueue[notChoice])
							# Get the next anime.
							if (len(animeQueue) > 0):
								currentQueue[notChoice] = animeQueue.pop()
							else:
								currentQueue.remove(currentQueue[notChoice])
						# TODO: Allow undoing.
					# Put the final choice into the new round, and store the now completed round.
					newRoundu.addStart(currentQueue.pop())
				elif (len(animeQueue) == 1):
					newRoundu.addStart(animeQueue.pop())
				completeRounds.append(newRoundu)

			# Performing the merge.
			self.rounds = completeRounds
			if (len(self.rounds) > 1):
				self.rounds = self.merge(self.rounds, mergeNum)	

			# Moving to the next stage.
			stage += 1

	def merge(self, inRounds, numToMerge):
		mergedRounds = []
		internalRounds = list(inRounds)
		# Merging a full number of rounds.
		while (len(internalRounds) >= numToMerge):
			# Create round object.
			newRound = TournamentRound()
			# Gather all of the rounds and their lengths.
			roundsToMerge = []
			lengths = []
			for i in range(0, numToMerge):
				roundsToMerge.append(internalRounds.pop(random.randrange(len(internalRounds))).getAnimes())
				lengths.append(len(roundsToMerge[i]))
			# Determine the max length of the rounds.
			maxAnimes = max(lengths)
			# Adding the animes to the new round.
			# TODO: Change merging order around, so that it maches flow of decision bubbling in the main algorithm
			for i in range(0, maxAnimes):
				for j in range(0, len(roundsToMerge)):
					if (i < lengths[j]):
						newRound.addEnd(roundsToMerge[j][i])
			# Add the round to the merged rounds.
			mergedRounds.append(newRound)
		# Merging remaining rounds.
		if (len(internalRounds) > 0):
			# Create round object.
			newRound = TournamentRound()
			# Gather the reamining rounds and their lengths.
			roundsToMerge = []
			lengths = []
			for i in range(0, len(internalRounds)): 
				roundsToMerge.append(internalRounds[i].getAnimes())
				lengths.append(len(roundsToMerge[i]))
			# Determine the max length of the rounds.
			maxAnimes = max(lengths)
			# Adding the animes to the new round.
			for i in range(0, maxAnimes):
				for j in range(0, len(roundsToMerge)):
					if (i < lengths[j]):
						newRound.addEnd(roundsToMerge[j][i])
			# Add the round to the merged rounds.
			mergedRounds.append(newRound)
		# Return the list of merged rounds.
		return mergedRounds

	def getMaxStages(self, mergeNum):
		maxStages = 1
		runningTotal = len(self.rounds)
		while(runningTotal > 1):
			if (runningTotal % mergeNum == 0):
				runningTotal = runningTotal // 2
			else:
				runningTotal = (runningTotal // 2) + 1
			maxStages += 1
		return maxStages

	def toString(self):
		returnedString = ""
		if (len(self.rounds) == 1):
			roundoAnimes = self.rounds[0].getAnimes()
			for j in range(0, len(roundoAnimes)):
				animo = roundoAnimes[j]
				returnedString += " " + str(j+1) + ". " + animo.name + "\n"
		else:
			for i in range(0, len(self.rounds)):
				returnedString += "Round " + str(i+1) + ":\n"
				roundoAnimes = self.rounds[i].getAnimes()
				for j in range(0, len(roundoAnimes)):
					animo = roundoAnimes[j]
					returnedString += " " + str(j+1) + ". " + animo.name + "\n"
		return returnedString
