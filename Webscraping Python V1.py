# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 15:37:16 2023

@author: craco
"""

#First, we need to access Chefkoch

#To do so, we initiate Selenium, to use it as an autoclicker (only needs to be ran 1 time)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

######

print('What ingredients do you have?')
ingredient= input() ### The goal here was to let the user type in its ingredients, so that the program can type it in later (line 49)

#We launch chrome as a different user
opts = Options()
opts.add_argument("user-agent=gene")

driver = webdriver.Chrome()
driver.maximize_window()
driver.set_page_load_timeout(600) # the maximum delay time to response is set as 600s, maybe we can reduce it.
 
#Then, we tell him to go to Chefkoch

driver.get("https://www.chefkoch.de/")
time.sleep(10)

####Attempts to close the cookie pop up

button =driver.find_elements(By.CLASS_NAME,'message-component message-button no-children focusable ds-btn ds-btn--primary sp_choice_type_11 first-focusable-el')
button.click() 


driver.find_element(By.NAME, 'Zustimmen').click()


#We ask him to find any input field
search=driver.find_element(By.XPATH,'//*[@id="search-bar"]')

#We type in the result of the ingredients input
search.send_keys('ingredients' + Keys.RETURN)
time.sleep(5)















import requests
link = "https://www.chefkoch.de/"

response = requests.get(link)
print(response)


#Implement the possibility to type in one or more ingredients, with a text saying "ingredients:"

print('What ingredients do you have?')
ingredient= input()