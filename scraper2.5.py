import urllib.request
import datetime

from bs4 import BeautifulSoup
from ClubClass import Club
from PlayerClass import Player
from SchedClass import Match
from phillyunionscript import Bot

def SoupGetFromWebsiteAndReturn(website):
	#feed it the url
	url = urllib.request.urlopen(website)
	stuff = url.read()
	# feed it the data
	soup = BeautifulSoup(stuff, "html.parser")
	return soup

def ClubNameGrabAndReturn(soup):
	clubs = []
	# find what we're looking for
	table = soup.find_all('table', {'class': 'standings_table'})
	fine_table = table[0].find_all('td', {'data-title': "Club"})

	for s in fine_table:
		string = s.get_text()
		clubs.append(Club(string))

	return clubs

def StandingsGrabAndReturn(soup, clubs):
	table = soup.find_all('table', {'class': 'standings_table'})
	points_table = table[0].find_all('td', {'class': "points ordered"})
	wins_table = table[0].find_all('td', {'data-title': "Wins"})
	loss_table = table[0].find_all('td', {'data-title': "Losses"})
	draw_table = table[0].find_all('td', {'data-title': 'Ties'})
	games_played = table[0].find_all('td', {'data-title': 'Games Played'})

	for i in range(0, 10):
		clubs[i].AddPoints(points_table[i].get_text())
		clubs[i].AddWins(wins_table[i].get_text())
		clubs[i].AddLosses(loss_table[i].get_text())
		clubs[i].AddDraws(draw_table[i].get_text())
		clubs[i].AddGamesPlayed(games_played[i].get_text())
	return clubs

def StandingsFormatter(clubs, f):
	i = 1
	week = 0

	for club in clubs:
		if(club.GetName() == "Philadelphia Union"):
			week = club.GetGamesPlayed()

	f.write("Current Results as of Week " + str(week) + "\n\n")
	f.write("Pos | Team | Pts | W | L | T\n")
	f.write("---|---|---|---|---|---\n")

	for obj in clubs:
		f.write(str(i) + "|" + obj.GetName() + "|" + obj.GetPoints() + "|" 
				+ obj.GetWins() + "|" + obj.GetLosses() + "|" + obj.GetDraws())
		f.write("\n")
		i += 1
	f.write("\n")

def GetSchedule(soup):
	#matches
	fixtures = []
	matches = []
	dates = soup.find_all("div", {"class":"match_date"})
	table = soup.find_all("div", {"class":"match_click_area"})
	times = soup.find_all("span", {"class":"match_status"})
	tv = soup.find_all("span", {"class":"match_category"})

	tvlist = tv[0].get_text().split(", ")
	
	channel = FormatTV(tvlist)


	for item in table:
		f = item.find("div", {"class":"match_location_competition"}).get_text()
		fixtures.append(FormatFixture(f))

	#get all attributes for each match
	for i in range(0, len(table)):
		match = Match(dates[i].get_text())
		match.FixDates()
		match.AddHome(table[i].find("div",{"class":"home_club"}).find("span",{"class":"club_name"}).get_text())
		match.AddAway(table[i].find("div",{"class":"vs_club"}).find("span",{"class":"club_name"}).get_text())

		#check to see if game was played, add score if it has, add x if not
		if((table[i].find("div",{"class":"home_club"}).find("span",{"class":"match_score"}))is not None):
			match.AddHomeScore(table[i].find("div",{"class":"home_club"}).find("span",{"class":"match_score"}).get_text())
		else:
			match.AddHomeScore("-")
		#check to see if game was played, add score if it has, add x if not
		if((table[i].find("div",{"class":"vs_club"}).find("span",{"class":"match_score"})) is not None):
			match.AddAwayScore(table[i].find("div",{"class":"vs_club"}).find("span",{"class":"match_score"}).get_text())
		else:
			match.AddAwayScore("-")

		match.AddFixture(fixtures[i])

		if(times[i].get_text() == "FINAL"):
			match.IsOver(True)
			match.AddTime(times[i].get_text())
		else:
			time = times[i].get_text().replace(" ET", "")
			time = time.replace("PM", "")
			match.AddTime(time)
			match.IsOver(False)

		match.AddTV(channel)
		
		matches.append(match)

	return matches

"""
def FormatSchedule(matches, f):
	f.write("Fixt | Opponent | Date | Time")
	f.write("\n")
	f.write("---|---|---|---|")
	f.write("\n")
	for obj in matches:
		if (obj.GetHome() == "Philadelphia Union"):
			opponent = obj.GetAway()
			score2 = obj.GetAwayScore()
			score1 = obj.GetHomeScore()
		else:
			opponent = "@" + obj.GetHome()
			score1 = obj.GetAwayScore()
			score2 = obj.GetHomeScore()

		f.write(obj.GetFixture() + "|" + opponent + "|" + obj.GetDate() + "|" + obj.GetTime())
		f.write("\n")
	f.write("\n")
"""

def FormatTV(tv):
	channels = {"The Comcast Network": "TCN",
		  "FS1": "FS1",
		  "6abc": "ABC",
		  "UniMás": "Uni",
		  "ESPN": "ESPN",
		  "CSN-PHL": "CSN"}
	channel = None
	for c in tv:
		if(c in channels):
			channel = channels[c]
		else:
			continue
	if(channel is None):
		channel = "n/a"

	return channel

def FormatFixture(fix):
	tempFix = fix.split(" / ")

	if(tempFix[0] == "MLS Regular Season"):
		fixture = "MLS"
	elif(tempFix[0] == "U.S. Open Cup"):
		fixture = "USOC"

	return fixture

def GoalsLeadersGrabAndReturn(soup):
	players = []
	goals = []
	table = soup.find_all("tbody")
	players_table = table[0].find_all("td", {"data-title": "Player"})
	goals_table = table[0].find_all("td", {"data-title": "G"})

	for i in range(0, 5):
		player = players_table[i].get_text()
		players.append(Player(player))

	for i in range(0, 5):
		goals.append(goals_table[i].get_text())

	i = 0
	for obj in players:
		obj.AddGoals(goals[i])
		i+= 1

	return players

"""
def GoalsFormatter(players, f):
	f.write("Player|Goals")
	f.write("\n")
	f.write("---|---|")
	f.write("\n")
	
	for i in range(0, 4):
		f.write(players[i].GetName() + "|" + players[i].GetGoals())
		f.write("\n")
	f.write("\n")
"""

def AssistsLeadersGrabAndReturn(soup):
	assists = []
	player = []
	table = soup.find_all("tbody")
	players_table2 = table[0].find_all("td", {"data-title": "Player"})
	for i in range(0, 5):
		player.append(Player(players_table2[i].get_text()))

	assists_table = table[0].find_all("td", {"data-title": "A"})
	for i in range(0, len(assists_table)):
		assists.append(assists_table[i].get_text())

	i = 0
	for obj in player:
		obj.AddAssists(assists[i])
		i+=1

	return player

"""
def AssistsFormatter(players2, f):
	f.write("Player|Assists")
	f.write("\n")
	f.write("---|---|")
	f.write("\n")

	for i in range(0, 4):
		if(players2[i].GetName() == "Fabio Alves"):
			players2[i].AddName("Fabinho")
		if(players2[i].GetAssists() != 0):
			f.write(players2[i].GetName() + "|" + players2[i].GetAssists())
			f.write("\n")

	f.write("\n")	
"""

def DateFixer(date):
	fixedDate = []
	day = date.day
	month = date.month
	year = date.year

	if(day < 10):
		day = "0" + str(day)
	if(month < 10):
		month = "0" + str(month)

	fixedDate.append(day)
	fixedDate.append(month)
	fixedDate.append(year)

	return fixedDate	

#do not need to use anymore. 
def Write(standings, schedule, goals, assists, f):
	#standings
	i = 1
	week = 0

	for club in clubs:
		if(club.GetName() == "Philadelphia Union"):
			week = club.GetGamesPlayed()

	f.write("Current Results as of Week " + str(week) + "\n\n")
	f.write("Pos | Team | Pts | W | L | T\n")
	f.write("---|---|---|---|---|---\n")

	for obj in clubs:
		f.write(str(i) + "|" + obj.GetName() + "|" + obj.GetPoints() + "|" 
				+ obj.GetWins() + "|" + obj.GetLosses() + "|" + obj.GetDraws())
		f.write("\n")
		i += 1
	f.write("\n")

	#schedule
	f.write("Fixt | Opponent | Date | Time")
	f.write("\n")
	f.write("---|---|---|---|")
	f.write("\n")
	for obj in matches:
		if (obj.GetHome() == "Philadelphia Union"):
			opponent = obj.GetAway()
			score2 = obj.GetAwayScore()
			score1 = obj.GetHomeScore()
		else:
			opponent = "@" + obj.GetHome()
			score1 = obj.GetAwayScore()
			score2 = obj.GetHomeScore()

		f.write(obj.GetFixture() + "|" + opponent + "|" + obj.GetDate() + "|" + obj.GetTime())
		f.write("\n")
	f.write("\n")
	
	#goals
	f.write("Player|Goals")
	f.write("\n")
	f.write("---|---|")
	f.write("\n")
	
	for i in range(0, 4):
		f.write(players[i].GetName() + "|" + players[i].GetGoals())
		f.write("\n")
	f.write("\n")

	#assists
	f.write("Player|Assists")
	f.write("\n")
	f.write("---|---|")
	f.write("\n")

	for i in range(0, 4):
		if(players2[i].GetName() == "Fabio Alves"):
			players2[i].AddName("Fabinho")
		if(players2[i].GetAssists() != 0):
			f.write(players2[i].GetName() + "|" + players2[i].GetAssists())
			f.write("\n")

	f.write("\n")	

def BotStart(standings, schedule, goals, assists, date):
	print("Initializing Bot...")
	bot = Bot()
	print("Logging in...")
	bot.LogIn()
	print("Saving old sidebar (in case of error)")
	bot.GetOldSidebar()
	print("Feeding Bot...")
	bot.AddDate(date)
	bot.AddStandings(standings)
	bot.AddSchedule(schedule)
	bot.AddGoals(goals)
	bot.AddAssists(assists)
	bot.AddData()
	print("Updating Sidebar...")
	bot.Update()

if __name__ == '__main__':
	date = datetime.date.today()
	year = date.year
	fixedDate = DateFixer(date)
	#f.write("Updated: " + str(fixedDate[1]) + "-" + str(fixedDate[0]) + "-" + str(fixedDate[2]) + "\n\n")
	
	#scrape standings
	print("Scraping and formatting standings")
	urlStandings = "http://www.mlssoccer.com/standings/mls/" + str(fixedDate[2])
	standings_soup = SoupGetFromWebsiteAndReturn(urlStandings)
	clubs = ClubNameGrabAndReturn(standings_soup)
	results = StandingsGrabAndReturn(standings_soup, clubs)
	#StandingsFormatter(results, f)
	#end standings scraping
	
	#scrape schedule
	print("Scraping and formatting schedule")
	urlSchedule = "http://www.mlssoccer.com/schedule?month="+str(fixedDate[1])+"&year="+str(year)+"&club=186&club_options=Filters&op=Update&form_build_id=form-Rm25jLlXS2Nxn5es00LGfKG2B_F-KF4vS892KiM37yA&form_id=mp7_schedule_hub_search_filters_form"
	schedule_soup = SoupGetFromWebsiteAndReturn(urlSchedule)
	matches = GetSchedule(schedule_soup)
	#FormatSchedule(matches, f)
	#end scrape schedule
	
	#sccape scoring and assists
	print("Scraping and formatting goals")
	urlScoring = "http://www.mlssoccer.com/stats/season?franchise=5513&year=" + str(fixedDate[2]) + "&season_type=REG&group=goals&op=Search&form_build_id=form-1V5Bkz7uHUNu_-v3oWL07bySMu7tYh83Y8vT0R-ZHJU&form_id=mp7_stats_hub_build_filter_form"
	scoring_soup = SoupGetFromWebsiteAndReturn(urlScoring)
	players = GoalsLeadersGrabAndReturn(scoring_soup)
	#GoalsFormatter(players, f)
	print("Scraping and formatting assists")
	urlAssists = "http://www.mlssoccer.com/stats/season?franchise=5513&year=" + str(fixedDate[2]) +"&season_type=REG&group=assists&op=Search&form_build_id=form-liI8MO6EVwbYHK6qWgbvfKigzpudrKWqS9NCa3QYgfI&form_id=mp7_stats_hub_build_filter_form"
	assists_soup = SoupGetFromWebsiteAndReturn(urlAssists)
	players2 = AssistsLeadersGrabAndReturn(assists_soup)
	#AssistsFormatter(players2, f)
	
	BotStart(results, matches, players, players2, fixedDate)

	#Write(results, matches, players, players2, f)
	#f.close()
	print("Done")