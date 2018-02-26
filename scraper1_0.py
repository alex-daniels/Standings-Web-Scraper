"""
Basic parser for mls standings/schedule
6 September 2015

V 1.1a

"""
import sys
import urllib.request
import datetime

sys.path.append('/beautifulsoup4-4.1.0')

from bs4 import BeautifulSoup

# opens the url and parses it into beautifulsoup
def ParseStandingsData(website):
	# feed it the url
	url = urllib.request.urlopen(website)
	stuff = url.read()
	# feed it the data
	soup = BeautifulSoup(stuff)
	# find what we're looking for
	table = soup.find_all('table', {'class': 'views-table tablesorter standings-table'})
	# still not enough, dive deeper and pass it along
	return table[0].find_all('td', {'class': 'views-field'})

def ParseScheduleData(website):
	#feed it the url
	url = urllib.request.urlopen(website)
	stuff = url.read()
	soup = BeautifulSoup(stuff)
	table = soup.find_all('div', {'class': 'schedule-page'})
	return table

def ParseStatsData(website):
	#feed it a URL
	url = urllib.request.urlopen(website)
	stuff = url.read()
	soup = BeautifulSoup(stuff)
	table = soup.find_all('div', {'class' : 'stats-table'})
	return table

#gets current standings
def FormatStandings(data, f):
	# 15 elements for each teem, need to offset by that much
	offset = 15
	# open file for writing
	# ugly reddit formatting begin!
	f.write("Pos | Team | Pts | W | L | T\n")
	f.write("---|---|---|---|---|---\n")
	for i in range(0, 10):
		# need to remove extra \n's and whitespace that appear
		# otherwise table doesn't display right on reddit
		string = data[i * offset + 1].text
		string = string.replace("\n", "")
		#string = string.replace(" ", "")
		# output
		f.write(
			data[i * offset].text + " | " +
			string + " | " +
			data[i * offset + 2].text + " | " +
			data[i * offset + 5].text + " | " +
			data[i * offset + 6].text + " | " +
			data[i * offset + 7].text + " | \n")

	f.write("\n")

#formats schedule for reddit usage
def FormatSchedule(data, f):

	f.write("Fixt | Opponent | Date | Time | Score\n")
	f.write("---|---|---|---|---\n")
	
	dates = data[0].find_all('h3')
	#find dates
	dateNum = []
	for i in range(0, len(dates)):
		dateNum.append(FixDates(dates[i].text))

	#fix date issue so it shows up m/d, m/dd, or mm/dd
	#keep this in mind! This is the correct date list!!
	fixedDates = FormatDates(dateNum)

	#find game time
	#times is the correct time list!!
	games = data[0].find_all('table', {'class': "views-table cols-1 schedule-table" })
	times = []
	for i in range(0, len(games)):
		time = games[i].find('div', {'class' : 'field-game-date-start-time'})
		time = time.text.replace(" " ,"")
		time = time.replace("\n", "")
		time = time.replace("EDT", "")
		times.append(time)

	#find game type, MLS regular season or US Open Cup
	#fixtures is the correct fixture list!!
	gameType = data[0].find_all('span', {'class' : 'competetion'})
	fixtures = []
	for i in range(0, len(gameType)):
		fixtureString = gameType[i].text
		if(fixtureString == "MLS Regular Season"):
			fixtures.append("MLS")
		elif(fixtureString == "U.S. Open Cup"):
			fixtures.append("USOC")

	#get teams 
	#opponent is corrected list form!
	homeTeam = data[0].find_all('div', {'class' : 'field-home-team'})
	awayTeam = data[0].find_all('div', {'class' : 'field-away-team'})
	opponent = []
	for i in range(0, len(homeTeam)):
		if(homeTeam[i].text != "Philadelphia"):
			opponent.append("@" + homeTeam[i].text)
		else:
			opponent.append('-')
	placeholder = '-'
	for i in range(0, len(awayTeam)):
		if(awayTeam[i].text != "Philadelphia"):
			if(opponent[i] == placeholder):
				opponent[i] = awayTeam[i].text
	
	#results! finalScores will list all scores!
	finalScores = []
	scores = data[0].find_all('div', {'class' : 'field-score'})
	for i in range(0, len(scores)):
		score = scores[i].text.replace("\n", "")
		score = score.replace(" ", "")
		finalScores.append(score)

	if(len(finalScores) < len(fixtures)):
		for i in range(0, (len(fixtures) - len(finalScores))):
			finalScores.append("TBD")
		
	for i in range(0, len(fixtures)):
		date = ''.join(fixedDates[i])

		f.write(
			fixtures[i] + " | " +
			opponent[i] + " | " + 
			date + " | " + 
			times[i] + " | " + 
			finalScores[i] + " | \n"
			)

	f.write("\n")

#formats goals for reddit usage
def FormatGoalStats(data, f):
	f.write("Player | Goals |\n")
	f.write("---|---|\n")
	td = data[0].find_all('td')

	offset = 15
	goalLeader = []
	numGoals = []
	for i in range(0, 5):
		goalLeader.append(td[i * offset].text)
		numGoals.append(td[i * offset + 5].text)

	for i in range(0, len(goalLeader)):
		f.write(goalLeader[i] + " | " + numGoals[i] + " | \n")

	f.write("\n")
#formats goals for reddit usage
def FormatAssistsStats(data, f):
	f.write("Player | Assists |\n")
	f.write("---|---|\n")

	td = data[0].find_all('td')
	offset = 9
	assistsLeader = []
	numAssists = []
	for i in range(0, 5):
		assistsLeader.append(td[i * offset].text)
		numAssists.append(td[i * offset + 4].text)

	for i in range(0, len(assistsLeader)):
		f.write(assistsLeader[i] + " | " + numAssists[i] + " | \n")

	f.write("\n")


#replaces string month with int month i.e january == 1 etc.
def FixDates(date):
	months = {'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4,
				'May' : 5, 'June' : 6, 'July' : 7, 'August' : 8, 
				'September' : 9, 'October' : 10, 'November' : 11, 'December' : 12}
	date = date.split()

	dateStr = str(months[date[1]]) + " " + date[2].replace(",", "")
	dateStr = dateStr.replace(" ", "")
	return dateStr

#just fixes date formatting
def FormatDates(dates):
	formattedDates = []
	#just for formatting dates! fuck this
	for i in range(0, len(dates)):
		#g.write("---|---|")
		date = dates[i]
		string = []
		#handle #/# dates
		if(len(date) == 2):
			for j in range(0, len(date)):
				string.append(date[j])
				if(j == 0):
					string.append("/")
		#handle #/## dates
		elif(len(date) == 3):
			for j in range(0, len(date)):
				string.append(date[j])
				if(j == 0):
					string.append("/")
		#handle ##/## dates
		elif(len(date) == 4):
			for j in range(0, len(date)):
				string.append(date[j])
				if(j == 0):
					string.append("/")
		formattedDates.append(string)

	return formattedDates

if __name__ == '__main__':

	f = open("sidebar.txt", "w+")
	date = datetime.date.today()
	month = date.month
	#year = date.year
	urlStandings = "http://www.mlssoccer.com/standings/2015" #+ str(year)
	urlSchedule = "http://www.mlssoccer.com/schedule?month=" + str(month) + "&year=2015&club=10&competition_type=all&broadcast_type=all&op=Search&form_id=mls_schedule_form"
	urlScoring = "http://www.mlssoccer.com/stats/season?season_year=2015&season_type=REG&team=5513&group=GOALS&op=Search&form_id=mls_stats_individual_form"
	urlAssists = "http://www.mlssoccer.com/stats/season?season_year=2015&season_type=REG&team=5513&group=ASSISTS&op=Search&form_id=mls_stats_individual_form"
	table = ParseStandingsData(urlStandings)
	FormatStandings(table, f)
	table2 = ParseScheduleData(urlSchedule)
	FormatSchedule(table2, f)
	table3 = ParseStatsData(urlScoring)
	FormatGoalStats(table3, f)
	table4 = ParseStatsData(urlAssists)
	FormatAssistsStats(table4, f)

	f.close()