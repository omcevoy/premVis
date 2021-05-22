from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
from bs4 import BeautifulSoup

url = "https://www.premierleague.com/tables?team=FIRST"

driver = webdriver.Chrome(executable_path='/Users/Owen/Desktop/chromedriver')
wait = WebDriverWait(driver,40)

driver.get(url)
driver.implicitly_wait(6)
cookie_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.btn-primary.cookies-notice-accept")))
ActionChains(driver).move_to_element(cookie_button)
driver.execute_script('arguments[0].click();', cookie_button)
time.sleep(2)

close_button = wait.until(EC.element_to_be_clickable((By.ID, "advertClose")))
ActionChains(driver).move_to_element(close_button)
driver.execute_script('arguments[0].click();', close_button)

wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.current[data-dropdown-current='gameweekNumbers']")))
time.sleep(3)

drop_down_click = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.current[data-dropdown-current='gameweekNumbers']")))
drop_down_click.click()
time.sleep(1)

options = driver.find_elements_by_css_selector("ul[data-dropdown-list='gameweekNumbers'] li")
time.sleep(1)
options[1].click()
time.sleep(5)

soup = BeautifulSoup(driver.page_source, features="lxml")
table = soup.find('tbody', {"class", "tableBodyContainer"})
print(table)
driver.quit()
