#class
class Club:
	"""
	gp = games played
	name = name
	pts = points
	w = wins
	l = loss
	d = draw
	"""
	def __init__(self, name):
		self.name = name
	def AddGamesPlayed(self, gp):
		self.games = gp
	def AddPoints(self, pts):
		self.points = pts
	def AddWins(self, w):
		self.wins = w
	def AddLosses(self, l):
		self.losses = l
	def AddDraws(self, d):
		self.draws = d
	def GetName(self):
		return self.name
	def GetGamesPlayed(self):
		return self.games
	def GetPoints(self):
		return self.points
	def GetWins(self):
		return self.wins
	def GetLosses(self):
		return self.losses
	def GetDraws(self):
		return self.draws
	def GetFormatString(self):
		return self.name + "," + self.points + "," + self.wins + "," + self.losses + "," + self.draws
#/class