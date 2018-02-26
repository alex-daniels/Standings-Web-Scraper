# coding=utf-8

import praw

class Bot:
	def __init__(self):
		self.sub = "PhillyUnion"
		self.user = "--smokeandmirrors--"
		self.pw = ""
		self.r = praw.Reddit("PC:phillyunionscript.py:v0.0.1 (by /u/--smokeandmirrors--)")
		self.settings = None
		self.sidebar = None

	def AddDate(self, date):
		self.date = date
	def AddStandings(self, standings):
		self.standings = standings
	def AddSchedule(self, schedule):
		self.schedule = schedule
	def AddGoals(self, goals):
		self.goals = goals
	def AddAssists(self, assists):
		self.assists = assists
	
	def LogIn(self):
		self.r.login(self.user, self.pw, disable_warning=True)
		self.settings = self.r.get_settings(self.sub)
		#self.sidebar = self.settings['description']

	def Update(self):
		self.r.update_settings(self.r.get_subreddit(self.sub), description=self.sidebar)

	def GetOldSidebar(self):
		self.sidebar = self.settings['description']
		self.oldSidebar = self.sidebar
		#print(self.sidebar)
		f = open("sidebar.txt", "w+")
		f.write(self.sidebar)
		f.close()

	def AddData(self):

		top = """
Welcome to **/r/PhillyUnion**, the Reddit home for all fans of the Philadelphia Union. Post all of your Union links here and have fun.

Follow us on Twitter: **[@rPhillyUnion](https://twitter.com/rPhillyUnion)**
**********\n\n
"""
		upcomingHeader = "##### [Upcoming Match](http://www.mlssoccer.com/schedule)\n\n"
		standingsHeader = "##### [Current Standings] (http://www.mlssoccer.com/standings)\n\n Updated: " + str(self.date[1]) + "-" + str(self.date[0]) + "-" + str(self.date[2]) +"\n\n" 
		scheduleHeader  = "##### [Upcoming Opponents](http://www.mlssoccer.com/schedule)\n\n"
		teamLeaders = "#####Team Leaders\n\n"
		goalsHeader = "###[Goals](http://www.mlssoccer.com/stats/season?franchise=5513&year=2016&season_type=REG&group=goals&op=Search&form_build_id=form-X3HoZKCggRxYf0eMRqfVCemoH1MBYIgRHdek-HP7dg0&form_id=mp7_stats_hub_build_filter_form)\n\n"
		assistsHeader = "###[Assists](http://www.mlssoccer.com/stats/season?franchise=5513&year=2016&season_type=REG&group=assists&op=Search&form_build_id=form-6nrEGCTYMfIYLZ4OJ_N1U5rTV_lUuiVt_nuV8Tt9A7A&form_id=mp7_stats_hub_build_filter_form)\n\n"

		#upcoming
		upcoming = upcomingHeader + """
Fixt | Opponent | Date-Time | TV
---|---|---|---|
		"""
		up = ""
		for u in self.schedule:
			if(u.GetIsOver() == True):
				continue
			elif(u.GetIsOver() == False):
				if(u.GetHome() == "Philadelphia Union"):
					opponent = u.GetAway()
				else:
					opponent = "@" + u.GetHome()
			
				up += u.GetFixture() + "|" + opponent + "|" + u.GetDate() + " - " + u.GetTime() + "|" + u.GetTV() + "\n"
				break

		upcoming += up + "\n\n"

		#standings
		i = 1
		week = 0

		for club in self.standings:
			if(club.GetName() == "Philadelphia Union"):
				week = club.GetGamesPlayed()

		#f.write("Current Results as of Week " + str(week) + "\n\n")
		#f.write("Pos | Team | Pts | W | L | T\n")
		#f.write("---|---|---|---|---|---\n")

		current = standingsHeader +  "Current Results as of Week " + str(week) + "\n\n"
		s = ""
		for obj in self.standings:
			s+= str(i) + "|" + obj.GetName() + "|" + obj.GetPoints() + "|" + obj.GetWins() + "|" + obj.GetLosses() + "|" + obj.GetDraws() + "\n"
			i+=1
			
		table = """
		Pos | Team | Pts | W | L | T
		---|---|---|---|--|--|
		""" 
		
		table += s
		current += table 

		#schedule
		schedule = scheduleHeader + """
		Fixt | Opponent | Date | Time
		---|---|---|---
		"""
		
		sched = ""
		for obj in self.schedule:
			if(obj.GetHome() == "Philadelphia Union"):
				opponent = obj.GetAway()
			else:
				opponent = "@" + obj.GetHome()

			sched += obj.GetFixture() + "|" + opponent + "|" + obj.GetDate() + "|" + obj.GetTime() + "\n"

		schedule += sched

		#goals
		leaders = teamLeaders + goalsHeader + """
		Players | Goals
		---|---
		"""

		g = ""

		for i in range(0, 4):
			g+= self.goals[i].GetName() + "|" + self.goals[i].GetGoals() + "\n"

		leaders += g

		#assists
		leaders += assistsHeader + """
		Players | Assists 
		---|---
		"""

		a = ""
		for i in range(0, 4):
			if(self.assists[i].GetName() == "Fabio Alves"):
				self.assists[i].AddName("Fabinho")

			a += self.assists[i].GetName() + "|" + self.assists[i].GetAssists() + "\n"

		leaders += a

		bottom = """
##### [Guides to The U](https://www.reddit.com/r/PhillyUnion/wiki/countdowntokickoff)

#####[AmA Archive](https://www.reddit.com/r/PhillyUnion/search?sort=new&restrict_sr=on&q=flair%3ACompleted%2BAMA)

##### Fantasy League
* [Classic League Standings](http://fantasy.mlssoccer.com/)  
* [Head 2 Head Standings](http://fantasy.mlssoccer.com/)  
* [Head 2 Head Fixtures](http://fantasy.mlssoccer.com/)  
* [Fantasy Talk Tuesday](https://www.reddit.com/r/PhillyUnion/search?q=flair%3AFTT&restrict_sr=on&sort=new&t=all)  
* [2016 Fantasy League Post](http://fantasy.mlssoccer.com/)  

##### Union Podcasts
* [The DoopCast](http://www.doopcast.com/)  
* [KYW Philly Soccer Show](http://www.phillysoccerpage.net/category/podcasts/)  
* [The 90th Minute](http://philadelphia.cbslocal.com/personality/the-90th-minute/)  
* [The All Three Points Podcast](https://itunes.apple.com/us/podcast/the-all-three-points-podcast/id804201431?mt=2)  


###

#####Union Blogs
- [The Goalkeeper](http://www.philly.com/philly/blogs/thegoalkeeper/)
- [Brotherly Game](http://www.brotherlygame.com/)
- [Philly Soccer Page](http://www.phillysoccerpage.net/)
- [Zolo Talk](https://zolotalk.wordpress.com/)
- [Philly Soccer News](http://www.phillysoccernews.com/)

##### Union Supporter Groups
* [Sons of Ben](http://www.sonsofben.com/)
* [Bearfight Brigade](http://thebearfightbrigade.com/) 
* Corner Creeps
* The IllegitimateS 



##### Related Subreddits
- /r/BSFC
-  /r/SonsofBen
-  /r/MLS
- /r/Philadelphia
- /r/Eagles 
- /r/Flyers 
- /r/Phillies
- /r/Sixers 
 
***

**Have content you would like to add to our sidebar? Message /u/MrChips217**
		"""

		self.sidebar = top + upcoming + current + schedule + leaders + bottom



