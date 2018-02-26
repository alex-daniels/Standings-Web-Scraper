class Match:
	"""
	fxtr = fxtr
	date = date
	time = time
	home = home
	away = away
	"""
	def __init__(self, date):
		self.date = date
	def AddTime(self, time):
		self.time = time
	def AddHome(self, home):
		self.home = home
	def AddAway(self, away):
		self.away = away
	def AddHomeScore(self, homeScore):
		self.homeScore = homeScore
	def AddAwayScore(self, awayScore):
		self.awayScore = awayScore
	def AddFixture(self, fxtr):
		self.fixture = fxtr
	def IsOver(self, over):
		self.over = over
	def AddTV(self, tv):
		self.tv = tv
	def GetDate(self):
		return str(self.date)
	def GetTime(self):
		return str(self.time)
	def GetHome(self):
		return self.home
	def GetAway(self):
		return self.away
	def GetHomeScore(self):
		return self.homeScore
	def GetAwayScore(self):
		return self.awayScore
	def GetFixture(self):
		return self.fixture
	def GetIsOver(self):
		return self.over
	def GetTV(self):
		return self.tv
	def GetFormatString(self):
		return str(self.date) + "," + self.time + "," + self.home + "," + self.homeScore + "," + self.away + "," + self.awayScore + "," + self.fixture + "," + str(self.over)

	def FixDates(self):
		months = {'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4,
					'May' : 5, 'June' : 6, 'July' : 7, 'August' : 8, 
					'September' : 9, 'October' : 10, 'November' : 11, 'December' : 12}
		date = self.date.split()

		dateStr = str(months[date[1]]) + " " + date[2].replace(",", "")
		dateStr = dateStr.replace(" ", "")
		#handle #/# dates
		if(len(dateStr) == 2):
			dateFixed = "0" + dateStr[0] + "/0" + dateStr[1]
			self.date = dateFixed
		#handle #/## dates
		if(len(dateStr) == 3):
			dateFixed = "0" + dateStr[0] + "/" + dateStr[1] + dateStr[2]
			self.date = dateFixed
		if(len(dateStr) == 4):
			dateFixed = dateStr[0] + "/" + dateStr[2] + dateStr[3]
			self.date = dateFixed
		