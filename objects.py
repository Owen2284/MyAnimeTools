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

	ANIMESTATUS = {
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
		for key in self.ANIMESTATUS:
			if key == n:
				return self.ANIMESTATUS[key]
		return ""

	def statusStringToNumber(self, s):
		for key in self.ANIMESTATUS:
			if self.ANIMESTATUS[key] == s:
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
		print(" Title: " + self.name)
		print(" ID: " + self.aID)
		print(" Link: " + self.link)
		print(" Synonyms: " + self.seriesSynonymsStr)
		print("")
		print(" Type: " + self.seriesTypeStr)
		print(" Number of episodes: " + str(self.seriesEpisodes))
		print(" Status: " + self.seriesStatusStr)
		print(" Airdates: " + self.seriesStartDate + " to " + self.seriesEndDate)
		print("")


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
				if currentName == inName:
					return currentAnime
		return None

	def getAnimeByCategory(self, inCategory):
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
