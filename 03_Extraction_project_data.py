
"""
 WFI Ingolstadt School of Management
 Webscraping & Textual Analysis in Python
 Winter 2023/24
 
 03_Extraction_project_data
 
 1. Parsing HTML script (RegEx/BeautifulSoup)


"""

#Import BeautifulSoup + Requests

from bs4 import BeautifulSoup
import requests

#Import HTML document and assign it to a variable 

DUMMY= "'/HTML DOCUMENT EXPLORER PATH"

response = requests.get(DUMMY)

print(response.text)


#Run HTML document 

soup = BeautifulSoup(DUMMY)

print(soup)

print(soup.prettify()) ##Improve data visualisation (hierarchy)

-------------------------------------------------------------------------------

#Find all needed box class objects within the HTML

##Recipe Name

name = soup.find_all('h1', class_ = '?????') ####?????

##Preptime, difficulty, calories 

preptime = soup.find_all('span', class_ = 'recipe-preptime rds-recipe-meta_badge') 
difficulty = soup.find_all('span', class_ = 'recipe-difficulty rds-recipe-meta_badge') 
calories = soup.find_all('span', class_ = 'recipe-kcalories rds-recipe-meta_badge') 

OR 

soup.find_all('i', class_ = 'material-icons') ####?????

##Rating average, rating count 

rat_avg = soup.find_all('div', class_ = 'ds-rating-avg') 
rat_count = soup.find_all('div', class_ = 'ds-rating-count') 

##Recipe servings 

serv = soup.find_all('input', class_ = 'ds-input') 

##Quantity & Ingredients 

quant = soup.find_all('td', class_ = 'td-left') 
ingredient = soup.find_all('td', class_ = 'td-right') 

##Nutrition values 

nutrition = soup.find_all('div', class_ = 'ds-col-3') ####?????


##Optional Clean up data 

e.g.
soup.find_all('div', class_ = 'ds-col-3').text.strip()


#Create dataframe to storage final data

import pandas as pd
dftable = pd.DataFrame() 
recipe = []
time = []
level = []
calorie_counter = []
rating_stars = []
ratings_counter = []
servings = []
quantity = []
ingredients = []
nutrition_values = []

soup = BeautifulSoup(response.content)



dftable['name'] = recipe
dftable['preptime'] = time
dftable['difficulty'] = level
dftable['calorires] = calorie_counter
dftable['rat_avg'] = rating_stars
dftable['rat_count'] = ratings_counter
dftable['serv'] = servings
dftable['quant'] = quantity
dftable['ingredient'] = ingredients
dftable['nutrition'] = nutrition_values
dftable.head()
dftable.to_csv('/XXXXXXXXXXXXXXXXXX, index = False)


