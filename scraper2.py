import urllib.request
import datetime

from bs4 import BeautifulSoup
from ClubClass import Club
from PlayerClass import Player
from SchedClass import Match

def GetSoup(website):
	#feed it the url
	url = urllib.request.urlopen(website)
	stuff = url.read()
	# feed it the data
	soup = BeautifulSoup(stuff)
	return soup

def ScrapeClubNames(soup):
	clubs = []
	# find what we're looking for
	table = soup.find_all('table', {'class': 'standings_table'})
	fine_table = table[0].find_all('td', {'data-title': "Club"})

	for s in fine_table:
		string = s.get_text()
		clubs.append(Club(string))

	return clubs

def GetStandings(soup, clubs):
	table = soup.find_all('table', {'class': 'standings_table'})
	points_table = table[0].find_all('td', {'class': "points ordered"})
	wins_table = table[0].find_all('td', {'data-title': "Wins"})
	loss_table = table[0].find_all('td', {'data-title': "Losses"})
	draw_table = table[0].find_all('td', {'data-title': 'Ties'})

	for i in range(0, 10):
		clubs[i].AddPoints(points_table[i].get_text())
		clubs[i].AddWins(wins_table[i].get_text())
		clubs[i].AddLosses(loss_table[i].get_text())
		clubs[i].AddDraws(draw_table[i].get_text())
	return clubs

def FormatStandings(clubs, f):
	i = 1
	f.write("Pos | Team | Pts | W | L | T\n")
	f.write("---|---|---|---|---|---\n")

	for obj in clubs:
		f.write(str(i) + "|" + obj.GetName() + "|" + obj.GetPoints() + "|" 
				+ obj.GetWins() + "|" + obj.GetLosses() + "|" + obj.GetDraws())
		f.write("\n")
		i += 1
	f.write("\n")

def GetSchedule(soup):
	matches = []
	fxtr = []
	home = []
	away = []
	club1_table = []
	table3 = soup.find_all("div", {"class":"match_location_competition"})
	table2 = soup.find_all("div", {"class": "item-list"})
	table = soup.find_all("ul", {"class": "schedule_list list-reset competition_schedule"})
	#get dates
	date_table = soup.find_all("div", {"class": "match_date"})

	for date in date_table:
		matches.append(Match(date.get_text()))

	for i in range(0, len(matches)):
		matches[i].FixDates()

	time_table = table[0].find("span", {"class": "match_status upcoming"})
	
	
	club1_table = table[0].find_all("div", {"class": "home_club"})
		

	for i in range(0, len(club1_table)):

		home.append(club1_table[i].find("span", {"class": "club_name"}).get_text())


	club2_table = table[0].find_all("div", {"class": "vs_club"})
	for i in range(0, len(club2_table)):
		away.append(club2_table[i].find("span", {"class": "club_name"}).get_text())

	fxtr_table = soup.find_all("div", {"class": "match_location_competition"})

	for f in fxtr_table:
		temp = f.get_text().split(" / ")
		if(temp[0] == "MLS Regular Season"):
			temp = "MLS"
			fxtr.append(temp)
		elif (temp[0] == "U.S. Open Cup"):
			temp = "USOC"
			fxtr.append(temp)

	
	for i in range(0, len(matches)):
		matches[i].AddTime(time_table[i])
		if(home[i] != "Philadelphia Union"):
			matches[i].AddOpponent("@"+home[i])
		elif(away[i] != "Philadelphia Union"):
			matches[i].AddOpponent(away[i])
		matches[i].AddFixture(fxtr[i])
	
		
	return matches

def FormatSchedule(matches, f):
	f.write("Fixt | Opponent | Date | Time | TV")
	f.write("\n")
	f.write("---|---|---|---|---|")
	f.write("\n")
	for obj in matches:
		f.write(obj.GetFixture() + "|" + obj.GetOpponent() + "|" + obj.GetDate() + "|" + obj.GetTime() + "|" + obj.GetTime())
		f.write("\n")
	f.write("\n")

def GetGoals(soup):
	players = []
	goals = []
	table = soup.find_all("tbody")
	players_table = table[0].find_all("td", {"data-title": "Player"})
	goals_table = table[0].find_all("td", {"data-title": "G"})
	for i in range(0, 5):
		players.append(Player(players_table[i].get_text()))

	for i in range(0, 5):
		goals.append(goals_table[i].get_text())

	i = 0
	for obj in players:
		obj.AddGoals(goals[i])
		i+= 1

	return players

def FormatGoals(players, f):
	f.write("Player|Goals")
	f.write("\n")
	f.write("---|---|")
	f.write("\n")
	
	for i in range(0, 5):
		f.write(players[i].GetName() + "|" + players[i].GetGoals())
		f.write("\n")
	f.write("\n")

def GetAssists(soup):
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

def FormatAssists(players2, f):
	f.write("Player|Assists")
	f.write("\n")
	f.write("---|---|")
	f.write("\n")

	for i in range(0, 5):
		f.write(players2[i].GetName() + "|" + players2[i].GetAssists())
		f.write("\n")
	f.write("\n")

if __name__ == '__main__':
	f = open("sidebar.txt", "w+")
	date = datetime.date.today()
	day = date.day
	month = 4
	year = date.year
	week = 1
	f.write("Updated: " + str(month) + "-" + str(day) + "-" + str(year) + "\n")
	f.write("Results as of Week " + str(week + 1)+ "\n")
	#scrape standings
	print("Scraping and formatting standings")
	urlStandings = "http://www.mlssoccer.com/standings/mls/" + str(year)
	standings_soup = GetSoup(urlStandings)
	clubs = ScrapeClubNames(standings_soup)
	results = GetStandings(standings_soup, clubs)
	FormatStandings(results, f)
	#end standings scraping

	#scrape schedule
	"""
	print("Scraping and formatting schedule")
	urlSchedule = "http://www.mlssoccer.com/schedule?month=4&year=2016&club=186&club_options=Filters&op=Update&form_build_id=form-Rm25jLlXS2Nxn5es00LGfKG2B_F-KF4vS892KiM37yA&form_id=mp7_schedule_hub_search_filters_form"
	schedule_soup = GetSoup(urlSchedule)
	matches = GetSchedule(schedule_soup)
	FormatSchedule(matches, f)
	#end scrape schedule
	"""
	#scrape scoring and assists
	print("Scraping and formatting goals")
	urlScoring = "http://www.mlssoccer.com/stats/season?franchise=5513&year=" + str(year) + "&season_type=REG&group=goals&op=Search&form_build_id=form-1V5Bkz7uHUNu_-v3oWL07bySMu7tYh83Y8vT0R-ZHJU&form_id=mp7_stats_hub_build_filter_form"
	scoring_soup = GetSoup(urlScoring)
	players = GetGoals(scoring_soup)
	FormatGoals(players, f)
	print("Scraping and formatting assists")
	urlAssists = "http://www.mlssoccer.com/stats/season?franchise=5513&year=" + str(year) +"&season_type=REG&group=assists&op=Search&form_build_id=form-liI8MO6EVwbYHK6qWgbvfKigzpudrKWqS9NCa3QYgfI&form_id=mp7_stats_hub_build_filter_form"
	assists_soup = GetSoup(urlAssists)
	players2 = GetAssists(assists_soup)
	FormatAssists(players2, f)
	f.close()