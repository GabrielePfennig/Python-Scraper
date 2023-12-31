#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 11:46:22 2023

@author: gabriele
"""

##----------------------------#Part 1 and 2--------------------------------------

from selenium import webdriver
import re
from bs4 import BeautifulSoup
import os


# importing the overview page 
import requests
link_cat = "https://www.chefkoch.de/rezepte/"

response = requests.get(link_cat)
#print(response)

# Save to a text file (encoding has to be set to utf-8)
with open('C:/Users/craco/Outputs Web Scraping/overview.html', 'w', encoding="utf-8") as file:
    file.write(response.text)
    
with open('C:/Users/craco/Outputs Web Scraping/overview.html', 'r', encoding='utf-8') as file:
    # Lese den Inhalt der HTML-Datei
    html_content = file.read()

# Verwende BeautifulSoup, um das HTML zu analysieren
soup = BeautifulSoup(html_content, 'html.parser')

# Alle Rezepte-Links mit der Klasse 'sg-pill' extrahieren
links_cat = soup.find_all('a', class_='sg-pill')

# Die gewünschten Rezepte-Links ausgeben
for link_cat in links_cat:
    href_cat = link_cat['href']
   
# Liste der href-Werte erstellen
href_cats = [link_cat['href'] for link_cat in links_cat]

href_catsends = []

for href_cat in href_cats:
    split_result = href_cat.split('t', 1)
    href_catend = 't' + split_result[1]
    href_catsends.append(href_catend)
    print (href_catsends)
#
base_caturl = "https://www.chefkoch.de/rs/s"
num_pages = 1  # Hier die gewünschte Anzahl eintragen  #########Leave #No. of recipe pages as a restrictor or use a loop instead#######

base_caturls = [f"{base_caturl}{page_number}" for page_number in range(num_pages)]

category_links = [f"{base_caturl}{href_catend}" for base_caturl in base_caturls for href_catend in href_catsends]

for url in category_links:
    response = requests.head(url)
    if response.status_code == 200 :
    
        print(f"URL {url} is available.")
        
    elif response.status_code == 301 :
        print(f"URL {url} is available.")
    
    else:
        print(f"URL {url} is not available. Status code: {response.status_code}")
    

     
# Ordner erstellen, um HTML-Dateien zu speichern
output_folder = "C:/Users/craco/Outputs Web Scraping/category_pages"
os.makedirs(output_folder, exist_ok=True)


for url in category_links:
    # Anfrage an die URL senden
    response = requests.get(url)

    # Sicherstellen, dass die Anfrage erfolgreich war (Statuscode 200)
    if response.status_code == 200:
        # HTML-Inhalt extrahieren
        html_content = response.text
        
        # HTML-Dateiname aus der URL ableiten
        filename = os.path.join(output_folder, f"{url.replace('https://www.chefkoch.de/rezepte/', '').replace('/', '_')}.html")

        # HTML-Datei speichern
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"HTML of {url} was successfully stored.")
    else:
        print(f"Error during the retrieval of {url}. Statuscode: {response.status_code}")


# Ordner, in dem die HTML-Dateien gespeichert sind
output_folder = "C:/Users/craco/Outputs Web Scraping/category_pages"
print("Data successfully exported")

# Liste der HTML-Dateien im Ordner abrufen
html_files = [f for f in os.listdir(output_folder) if f.endswith(".html")]
print("list obtained")

# Liste für die Rezeptlinks erstellen
recipe_links = []

# Durchlaufe alle HTML-Dateien
for filename in html_files:
    # Pfad zur HTML-Datei erstellen
    file_path = os.path.join(output_folder, filename)
    
    # HTML-Datei öffnen und den Inhalt lesen
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Beautiful Soup verwenden, um den HTML-Inhalt zu analysieren
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Alle Links mit der Klasse 'ds-recipe-card__link ds-teaser-link' extrahieren (Links zu den bestimmten Rezepten)
    links = soup.select('.ds-recipe-card__link.ds-teaser-link')
   
    # Rezeptlinks in der Liste hinzufügen
    for link in links:
        recipe_links.append(link['href'])

print(recipe_links)

        
 
    
##--------------------------#Part 3----------------------------------------------
import pandas as pd

# Lists for Recipe Data
recipe_names = []
preptimes = []
difficulties = []
calories_list = []
rating_avgs = []
rating_counts = []
servings_list = []
quantities = []
ingredients_list = []
nutrition_values_list = []

for recipe_link in recipe_links:
    # Anfrage an die Rezeptseite senden
    response_recipe = requests.get(recipe_link, timeout=120)
    
    soup = BeautifulSoup(response_recipe.content)
    
    # Sicherstellen, dass die Anfrage erfolgreich war (Statuscode 200)
    if response_recipe.status_code == 200:
        print(f"Request to {recipe_link} was successful.")
        
        # HTML-Inhalt extrahieren
        html_content_recipe = response_recipe.text
       
        # Beautiful Soup verwenden, um den HTML-Inhalt zu analysieren
        soup_recipe = BeautifulSoup(html_content_recipe, 'html.parser')
        
        # Recipe Name
        recipe_name = soup_recipe.find('h1')
        recipe_name_value = recipe_name.text.strip() if recipe_name else 'N/A'

        # Preptime
        preptime = soup_recipe.find('span', class_='recipe-preptime rds-recipe-meta__badge')
        preptime_value = re.sub(r'[^\x00-\x7F]+', '', preptime.text.strip()) if preptime else 'N/A'


        # Difficulty
        difficulty = soup_recipe.find('span', class_='recipe-difficulty rds-recipe-meta__badge')
        difficulty_value = re.sub(r'[^\x00-\x7F]+', '', difficulty.text.strip()) if difficulty else 'N/A'


        # Calories
        calories = soup_recipe.find('span', class_='recipe-kcalories rds-recipe-meta__badge')
        calories_value = re.search(r'\d+', calories.text.strip()).group() if calories else 'N/A'


        # Rating Average
        rating_avg = soup_recipe.find('div', class_='ds-rating-avg')
        rating_avg_value = rating_avg.text.strip() if rating_avg else 'N/A'

      
        # Rating Count
        rating_count = soup_recipe.find('div', class_='ds-rating-count')
        rating_count_value = re.search(r'(\d+)', rating_count.text.strip()).group() if rating_count else 'N/A'

        
        # Recipe Servings
        servings = soup_recipe.find('input', class_='ds-input')
        servings_value = servings['value'].strip() if servings else 'N/A'
        
        # Quantity
        quantity = soup_recipe.find('td', class_='td-left')
        quantity_value = quantity.text.strip() if quantity else 'N/A'
       
        # Ingredients
        ingredients = soup_recipe.find('td', class_='td-right')
        ingredients_value = ingredients.text.strip() if ingredients else 'N/A'
        
        # Nutrition Values
       
        nutrition_values = soup_recipe.find('div', class_='ds-col-3')
        nutrition_values_text = ''

        if nutrition_values:
            # Durchlaufe jedes Element in der Nährwert-Tabelle
            for item in nutrition_values.find_all('div', class_='ds-col-3'):
                # Extrahiere den Nährstofftyp (z.B., kcal, Kohlenhydr., Eiweiß, Fett)
                nutrient_type = item.find('h5').text.strip()
        
                # Extrahiere den Nährstoffwert
                nutrient_value = item.contents[-1].strip()
        
                # Füge den Nährstofftyp und -wert zum Text hinzu
                nutrition_values_text += f"{nutrient_type}: {nutrient_value}\n"

# Entferne nicht-druckbare Zeichen
nutrition_values_text = re.sub(r'[^\x00-\x7F]+', '', nutrition_values_text).strip()

# Falls keine Nährwertinformationen gefunden wurden, setze 'N/A'
nutrition_values_text = nutrition_values_text if nutrition_values_text else 'N/A'

        
        
        
# Append values to lists
recipe_names.append(recipe_name_value)
preptimes.append(preptime_value)
difficulties.append(difficulty_value)
calories_list.append(calories_value)
rating_avgs.append(rating_avg_value)
rating_counts.append(rating_count_value)
servings_list.append(servings_value)
quantities.append(quantity_value)
ingredients_list.append(ingredients_value)
nutrition_values_list.append(nutrition_values_text)
        
# Consolidate in dataframe and save as csv
all_recipes_df = pd.DataFrame({
    'Recipe Name': recipe_names,
    'Preptime': preptimes,
    'Difficulty': difficulties,
    'Calories': calories_list,
    'Rating Average': rating_avgs,
    'Rating Count': rating_counts,
    'Recipe Servings': servings_list,
    'Quantity': quantities,
    'Ingredients': ingredients_list,
    'Nutrition Values': nutrition_values_list
})

# Display the DataFrame (shows first lines)
all_recipes_df.head()

all_recipes_df.to_csv('C:/Users/craco/Outputs Web Scraping/Recipe_dataset.csv', index = False)

##It only works partly, see screenshot in the wiki

