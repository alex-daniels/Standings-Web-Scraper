class Player:
	"""
	name = name
	goals = goals
	assists = assists
	"""
	def __init__(self, name):
		self.name = name
	def AddName(self, n):
		self.name = n
	def AddGoals(self, g):
		self.goals = g
	def AddAssists(self, a):
		self.assists = a
	def GetName(self):
		return self.name
	def GetGoals(self):
		return self.goals
	def GetAssists(self):
		return self.assists
	def GetFormatString(self):
		return self.name + "," + str(self.goals) + "," + str(self.assists)