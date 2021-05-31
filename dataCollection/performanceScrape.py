from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
from bs4 import BeautifulSoup

def getClubName(club):
    clubParts = club.strip().split(' ')
    return clubParts[-1]
    
def fetchSeasonData():
    url = "https://www.premierleague.com/tables?team=FIRST"

    driver = webdriver.Chrome(executable_path='/Users/Owen/Desktop/chromedriver')
    wait = WebDriverWait(driver,40)
    driver.get(url)
    driver.implicitly_wait(6)
    cookie_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.btn-primary.cookies-notice-accept")))
    ActionChains(driver).move_to_element(cookie_button)
    driver.execute_script('arguments[0].click();', cookie_button)
    time.sleep(2)

    # close_button = wait.until(EC.element_to_be_clickable((By.ID, "advertClose")))
    # ActionChains(driver).move_to_element(close_button)
    # driver.execute_script('arguments[0].click();', close_button)

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.current[data-dropdown-current='gameweekNumbers']")))
    time.sleep(3)

    drop_down_click = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.current[data-dropdown-current='gameweekNumbers']")))
    drop_down_click.click()
    time.sleep(2)

    options = driver.find_elements_by_css_selector("ul[data-dropdown-list='gameweekNumbers'] li")
    seasonData = {}
    # iterate through 'matchweeks' and get table data for each week
    for i in range(1, len(options)):
        if (i != 1):
            drop_down_click.click()
        time.sleep(2)
        options[i].click()
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, features="lxml")
        table = soup.find('tbody', {"class", "tableBodyContainer"})
        rows = table.find_all('tr')
        for row in rows:
            clubData = row.find_all('td')
            if (len(clubData) > 2):
                clubName = getClubName(clubData[2].text) 
                if (clubName == '24'):
                    print("Potential data irregularity at matchweek {} for club {}".format(i, clubName))
                    break
                mdData = {
                    "matchesPlayed" : clubData[3].text,
                    "won" : clubData[4].text,
                    "draws" : clubData[5].text,
                    "lost" : clubData[6].text,
                    "GF" : clubData[7].text,
                    "GA" : clubData[8].text,
                    "GD" : clubData[9].text,
                    "points" : clubData[10].text
                }
                if clubName in seasonData:
                    seasonData[clubName].append(mdData)
                else:
                    seasonData[clubName] = [mdData]
            else:
                continue
    driver.quit()
    return seasonData
