import requests
from bs4 import BeautifulSoup
import unicodecsv as csv

url = "https://www.spotrac.com/epl/payroll/"

r = requests.get(url)

soup = BeautifulSoup(r.text, 'lxml')
rows = soup.find_all('tr')
rows = rows[1:]
for team in rows:
    cols = team.find_all('td')
    print(cols)

