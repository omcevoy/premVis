import requests
from bs4 import BeautifulSoup
import unicodecsv as csv

def intRetriever(data):
    startIndex = data.index('>')
    endIndex = data.index('</td')
    finalCut = data[startIndex + 1 : endIndex].replace(",", "").replace("£", "")
    return int(finalCut)

def stringRetriever(data):
    startIndex = data.index("<a")
    endIndex = data.index("</a")
    cutString = data[startIndex:endIndex]
    finalCut = cutString.index(">")
    return cutString[finalCut + 1:]

def getData(rows): 
    leagueStats = {}
    for team in rows:
        if (len(team) > 0):
            clubdata = team.find_all('td')
            club = stringRetriever(str(clubdata[1]))
            clubstats = {
                "players" : intRetriever(str(clubdata[2])),
                "forwards": intRetriever(str(clubdata[3])),
                "midfielders": intRetriever(str(clubdata[4])),
                "defenders" : intRetriever(str(clubdata[5])),
                "goalkeepers" : intRetriever(str(clubdata[6])),
                "transfers" : intRetriever(str(clubdata[7])),
                "total_wages" : intRetriever(str(clubdata[8]))
                }
            leagueStats[club] = clubstats
        else:
            continue
    return leagueStats

def getPay():
    url = "https://www.spotrac.com/epl/payroll/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    rows = soup.find_all('tr')[1:]
    leagueData = getData(rows)
    print(leagueData)